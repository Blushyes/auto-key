import json
import os
from dataclasses import dataclass, field
from typing import Optional

from context.logging import logger

SCRIPT_DIR: str = 'scripts'
METADATA_NAME: str = 'meta.json'
METADATA_EXAMPLE_PATH: str = os.path.join(SCRIPT_DIR, 'meta.example.json')

with open(METADATA_EXAMPLE_PATH, 'r', encoding='utf-8') as f:
    DEFAULT_METADATA: str = f.read()


@dataclass
class KeyScript:
    commands: list[int]
    contents: list[str]
    jump_list: list[int]  # 如果没有设置，则默认为-1


@dataclass
class ScriptInfo:
    path: str
    name: Optional[str] = field(default='未命名脚本')
    description: Optional[str] = field(default='无描述')
    version: Optional[str] = field(default='0.0.1')
    author: Optional[str] = field(default='未知的作者')


class ScriptLoader:
    """
    脚本加载器
    """

    def loads(self, path: str) -> KeyScript:
        """
        加载按键脚本

        Args:
            path: 脚本的路径

        Returns: 解析好的脚本对象
        """
        ...


def pick_scripts() -> list[ScriptInfo]:
    """
    获取所有的脚本

    Returns:
        所有脚本的信息
    """

    def load_metadata(path: str) -> dict:
        metadata_path = os.path.join(path, METADATA_NAME)
        if not os.path.exists(metadata_path):
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
            metadata['path'] = path
            return metadata

    logger.debug('获取所有脚本')
    scripts = os.listdir(SCRIPT_DIR)
    scripts = [script for script in scripts if os.path.isdir(os.path.join(SCRIPT_DIR, script))]
    logger.debug(f'获取到的脚本为：{scripts}')
    scripts = [os.path.join(SCRIPT_DIR, script) for script in scripts]
    scripts = [load_metadata(script) for script in scripts]
    scripts = [ScriptInfo(**script) for script in scripts]
    for script in scripts:
        logger.debug(script)
    return scripts
