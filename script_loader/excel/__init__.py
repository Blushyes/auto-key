import json
from pathlib import Path

import pandas as pd
from pandas import DataFrame, Series, isna

from executor import ScriptStep
from executor.external import CommandType
from executor.interfaces import CommandExecutorFactory
from executor.simple import SimpleCommandExecutorFactory
from script_loader.interfaces import ScriptLoader

# 脚本文件名
SCRIPT_NAME = "index"


class ExcelFileType:
    XLSX = "xlsx"
    CSV = "csv"


def _get_col(df: DataFrame, col_index: int) -> list | None:
    """
    Returns:
        若列不存在则返回None，否则返回列的值列表
    """
    _, col_len = df.shape
    if col_len - 1 < col_index:
        return None

    col: Series = df.iloc[:, col_index]
    return col.to_list()


class ExcelLoader(ScriptLoader):
    """
    Excel加载器，用于加载xlsx和csv类型的脚本
    """

    # TODO 后续再优化
    def loads(self, path: Path | str) -> list[ScriptStep]:
        if isinstance(path, str):
            path = Path(path)

        # 搜索脚本目录下面的脚本文件
        scripts = [file for file in path.iterdir() if SCRIPT_NAME in file.name]

        if len(scripts) == 0:
            raise Exception("没有脚本文件")

        first_script = scripts[0]
        first_script_type = first_script.suffix.lower()[1:]
        script_path = path / f"{SCRIPT_NAME}.{first_script_type}"

        def read_excel():
            match first_script_type:
                case ExcelFileType.XLSX:
                    return pd.read_excel(script_path)
                case ExcelFileType.CSV:
                    return pd.read_csv(script_path)
                case _:
                    raise Exception("不支持的脚本类型")

        # TODO 表格优化为配置化（方便给表格添加列）
        df: DataFrame = read_excel()
        commands: list = _get_col(df, 0)
        contents: list = _get_col(df, 1)
        jump_list: list = _get_col(df, 2)
        offset_x_list: list = _get_col(df, 3)
        offset_y_list: list = _get_col(df, 4)

        # 给可选列赋默认值
        if jump_list is None:
            jump_list = [None] * len(commands)
        else:
            jump_list = [None if isna(jump_to) else jump_to for jump_to in jump_list]

        if offset_x_list is None:
            offset_x_list = [0] * len(commands)
        else:
            offset_x_list = [
                0 if isna(offset_x) else offset_x for offset_x in offset_x_list
            ]

        if offset_y_list is None:
            offset_y_list = [0] * len(commands)
        else:
            offset_y_list = [
                0 if isna(offset_y) else offset_y for offset_y in offset_y_list
            ]

        executor_factory: CommandExecutorFactory = SimpleCommandExecutorFactory()

        def assemble_wrapper(
            command_code: int, arg: str, jump_to: int, offset_x: int, offset_y: int
        ) -> ScriptStep:
            # NOTE 如果为单击、双击、右击、拖拽，需要将参数转换为json（因为需要设置offset）
            if (
                command_code == CommandType.SINGLE_CLICK.value
                or command_code == CommandType.DOUBLE_CLICK.value
                or command_code == CommandType.RIGHT_CLICK.value
                or command_code == CommandType.DRAG.value
            ):
                return ScriptStep(
                    executor_factory.create(CommandType(command_code)),
                    json.dumps(
                        {"arg": arg, "offset_x": offset_x, "offset_y": offset_y}
                    ),
                    jump_to,
                )

            if (
                command_code == CommandType.MOVE.value
                or command_code == CommandType.SCROLL.value
            ):
                x, y = map(int, arg.split(","))
                return ScriptStep(
                    executor_factory.create(CommandType(command_code)),
                    json.dumps({'x': x, 'y': y, 'duration': 0.2}),
                    jump_to,
                )

            return ScriptStep(
                executor_factory.create(CommandType(command_code)), arg, jump_to
            )

        return [
            assemble_wrapper(command, content, jump, offset_x, offset_y)
            for command, content, jump, offset_x, offset_y in zip(
                commands, contents, jump_list, offset_x_list, offset_y_list
            )
        ]
