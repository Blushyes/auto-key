import json
import pathlib

from context.logging import logger
from script_loader.external import ScriptInfo

SCRIPT_DIR = pathlib.Path('scripts')
METADATA_NAME = 'meta.json'
METADATA_EXAMPLE_PATH = SCRIPT_DIR / 'meta.example.json'

with open(METADATA_EXAMPLE_PATH, 'r', encoding='utf-8') as f:
    DEFAULT_METADATA: str = f.read()


def pick_scripts() -> list[ScriptInfo]:
    """
    获取所有的脚本

    Returns:
        所有脚本的信息
    """

    def load_metadata(script_path: pathlib.Path) -> dict:
        metadata_path = script_path / METADATA_NAME
        if not metadata_path.exists():
            logger.warning('脚本不存在meta.json文件')
            with open(metadata_path, 'w', encoding='utf-8') as f:
                f.write(DEFAULT_METADATA)
            logger.info('自动创建meta.json文件完毕')

        with open(metadata_path, 'r', encoding='utf-8') as f:
            file_content = f.read()
            metadata = {}
            # 如果文件内容为空，则使用默认值
            if file_content is None or file_content == '':
                logger.warning('文件内容为空')
            # 如果文件内容为 DEFAULT_METADATA 说明是程序创建的，所以不予加载
            elif file_content != DEFAULT_METADATA:
                metadata = json.loads(file_content)
            metadata['path'] = str(script_path)
            return metadata

    logger.debug('获取所有脚本')
    scripts = [script for script in SCRIPT_DIR.iterdir() if script.is_dir()]
    logger.debug(f'获取到的脚本为：{scripts}')
    scripts = [load_metadata(script) for script in scripts]
    scripts = [ScriptInfo(**script) for script in scripts]
    for script in scripts:
        logger.debug(script)
    return scripts
