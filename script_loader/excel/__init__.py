import json
from pathlib import Path

import pandas as pd
from pandas import DataFrame, Series

from executor import CommandExecutorWrapper
from executor.external import CommandType
from executor.interfaces import CommandExecutorFactory
from executor.simple import SimpleCommandExecutorFactory
from script_loader.interfaces import ScriptLoader

# 脚本文件名
SCRIPT_NAME = "index"

# 定义Excel文件类型
class ExcelFileType:
    XLSX = "xlsx"
    CSV = "csv"

# 获取DataFrame中指定列的值，如果列不存在则返回None
def _get_col(df: DataFrame, col_index: int) -> list | None:
    _, col_len = df.shape
    if col_len - 1 < col_index:
        return None

    col: Series = df.iloc[:, col_index]
    col = col.fillna(-1)
    return col.to_list()

# 实现ScriptLoader接口的ExcelLoader类
class ExcelLoader(ScriptLoader):
    # TODO 后续再优化
    # 从Excel文件中加载脚本
    def loads(self, path: Path | str) -> list[CommandExecutorWrapper]:
        if isinstance(path, str):
            path = Path(path)

        # 查找所有包含SCRIPT_NAME的文件
        scripts = [file for file in path.iterdir() if SCRIPT_NAME in file.name]

        if len(scripts) == 0:
            raise Exception("没有脚本文件")

        first_script = scripts[0]
        first_script_type = first_script.suffix.lower()[1:]
        script_path = path / f"{SCRIPT_NAME}.{first_script_type}"

        # 读取Excel文件
        def read_excel():
            match first_script_type:
                case ExcelFileType.XLSX:
                    return pd.read_excel(script_path)
                case ExcelFileType.CSV:
                    return pd.read_csv(script_path)
                case _:
                    raise Exception("不支持的脚本类型")

        df: DataFrame = read_excel()
        commands: list = _get_col(df, 0)
        contents: list = _get_col(df, 1)
        jump_list: list = _get_col(df, 2)
        offset_x_list: list = _get_col(df, 3)
        offset_y_list: list = _get_col(df, 4)

        if jump_list is None:
            jump_list = [None] * len(commands)
        if offset_x_list is None:
            offset_x_list = [0] * len(commands)
        if offset_y_list is None:
            offset_y_list = [0] * len(commands)

        executor_factory: CommandExecutorFactory = SimpleCommandExecutorFactory()

        # 根据命令类型和参数组装CommandExecutorWrapper
        def assemble_wrapper(
            command_code: int, arg: str, jump_to: int, offset_x: int, offset_y: int
        ) -> CommandExecutorWrapper:
            # NOTE 如果为单击、双击、右击、拖拽，需要将参数转换为json（因为需要设置offset）
            if (
                command_code == CommandType.SINGLE_CLICK.value
                or command_code == CommandType.DOUBLE_CLICK.value
                or command_code == CommandType.RIGHT_CLICK.value
                or command_code == CommandType.DRAG.value
            ):
                return CommandExecutorWrapper(
                    executor_factory.create(CommandType(command_code)),
                    json.dumps(
                        {"img_name": arg, "offset_x": offset_x, "offset_y": offset_y}
                    ),
                    jump_to,
                )

            return CommandExecutorWrapper(
                executor_factory.create(CommandType(command_code)), arg, jump_to
            )

        # 组装所有命令
        return [
            assemble_wrapper(command, content, jump, offset_x, offset_y)
            for command, content, jump, offset_x, offset_y in zip(
                commands, contents, jump_list, offset_x_list, offset_y_list
            )
        ]
