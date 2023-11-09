import os

import pandas as pd
from pandas import DataFrame, Series

from script_loader.main import ScriptLoader, KeyScript

EXCEL_FILE_NAME = 'index.xlsx'


def _get_col(df: DataFrame, col_index: int) -> list:
    col: Series = df.iloc[:, col_index]
    col = col.fillna(-1)
    return col.to_list()


class ExcelLoader(ScriptLoader):

    def loads(self, path: str) -> KeyScript:
        df: DataFrame = pd.read_excel(os.path.join(path, EXCEL_FILE_NAME))
        commands: list = _get_col(df, 0)
        contents: list = _get_col(df, 1)
        jump_list: list = _get_col(df, 2)
        return KeyScript(commands, contents, jump_list)
