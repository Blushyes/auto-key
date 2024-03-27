import json
from dataclasses import dataclass
from pathlib import Path

import pandas as pd
from pandas import DataFrame, Series, isna

from executor import ScriptStep
from executor.external import CommandType
from executor.interfaces import CommandExecutorFactory
from executor.simple import SimpleCommandExecutorFactory
from script_loader.interfaces import ScriptLoader

# 脚本文件名
SCRIPT_NAME = 'index'
COLUMNS_CONFIG = 'columns.json'


class ExcelFileType:
    XLSX = "xlsx"
    CSV = "csv"


@dataclass
class ExcelColMeta:
    name: str
    description: str
    optional: bool
    default_value: str | int | float | None


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

    def __init__(self):
        self._executor_factory: CommandExecutorFactory = SimpleCommandExecutorFactory()

    def _assemble_script_step(
        self,
        command_code: int,
        content: str,
        jump_to: int,
        offset_x: int,
        offset_y: int,
    ) -> ScriptStep:
        # NOTE 如果为单击、双击、右击、拖拽，需要将参数转换为json（因为需要设置offset）
        if (
            command_code == CommandType.SINGLE_CLICK.value
            or command_code == CommandType.DOUBLE_CLICK.value
            or command_code == CommandType.RIGHT_CLICK.value
            or command_code == CommandType.DRAG.value
        ):
            return ScriptStep(
                self._executor_factory.create(CommandType(command_code)),
                json.dumps(
                    {"arg": content, "offset_x": offset_x, "offset_y": offset_y}
                ),
                jump_to,
            )

        if (
            command_code == CommandType.MOVE.value
            or command_code == CommandType.SCROLL.value
        ):
            x, y = map(int, content.split(","))
            return ScriptStep(
                self._executor_factory.create(CommandType(command_code)),
                json.dumps({'x': x, 'y': y, 'duration': 0.2}),
                jump_to,
            )

        return ScriptStep(
            self._executor_factory.create(CommandType(command_code)), content, jump_to
        )

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

        # 读取表格
        df: DataFrame = read_excel()
        with open(Path(__file__).parent / COLUMNS_CONFIG, 'r', encoding='utf-8') as f:
            col_metas = json.load(f)
            col_metas = [ExcelColMeta(**meta) for meta in col_metas]

        # 读取列数据并且处理默认值
        cols = []
        for i, meta in enumerate(col_metas):
            col = _get_col(df, i)
            if col is None:
                if meta.optional:
                    col = [meta.default_value] * df.shape[1]
                else:
                    raise Exception(f"第{i + 1}列不存在")
            else:
                col = [meta.default_value if isna(it) else it for it in col]
            cols.append(col)

        script = []
        for i in range(len(cols[0])):
            # TODO 暂时先这样
            # 根据name进行传参，所以name必须跟assemble_script_step函数的参数名一一对应
            script.append(
                self._assemble_script_step(
                    **{col_metas[j].name: cols[j][i] for j in range(len(cols))}
                )
            )

        return script
