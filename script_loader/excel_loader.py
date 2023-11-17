import os

import pandas as pd
from pandas import DataFrame, Series

from script_loader.main import ScriptLoader, KeyScript

SCRIPT_NAME = 'index'


class ExcelFileType:
    XLSX = 'xlsx'
    CSV = 'csv'


def _get_col(df: DataFrame, col_index: int) -> list:
    col: Series = df.iloc[:, col_index]
    col = col.fillna(-1)
    return col.to_list()


class ExcelLoader(ScriptLoader):

    def loads(self, path: str) -> list[KeyScript]:
        files = os.listdir(path)
        scripts = [file for file in files if SCRIPT_NAME in file]
        if len(scripts) == 0:
            raise Exception('没有脚本文件')
        first_script: str = scripts[0]
        first_script_type: str = first_script.split('.')[-1]
        script_name: str = SCRIPT_NAME + '.' + first_script_type
        script_path: str = os.path.join(path, script_name)

        def read_excel():
            match first_script_type:
                case ExcelFileType.XLSX:
                    return pd.read_excel(script_path)
                case ExcelFileType.CSV:
                    return pd.read_csv(script_path)
                case _:
                    raise Exception('不支持的脚本类型')

        df: DataFrame = read_excel()
        commands: list = _get_col(df, 0)
        contents: list = _get_col(df, 1)
        jump_list: list = _get_col(df, 2)

        return [KeyScript(command, content, jump) for command, content, jump in zip(commands, contents, jump_list)]
