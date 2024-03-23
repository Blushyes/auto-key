import json

config: dict | None = None


class Config:
    INTERACTION = 'interaction'


def initialize_config() -> None:
    """
    初始化配置，不需要懒加载的时候，在程序运行前使用
    """
    global config
    if config is None:
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)


def get_config() -> dict:
    """
    获取配置Json，支持懒加载
    """
    if config is None:
        initialize_config()
    return config
