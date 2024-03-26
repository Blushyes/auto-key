from abc import ABC, abstractmethod
from pathlib import Path

from executor import ScriptStep


class ScriptLoader(ABC):
    """
    脚本加载器
    """

    @abstractmethod
    def loads(self, path: Path | str) -> list[ScriptStep]:
        """
        加载按键脚本

        Args:
            path: 脚本的路径

        Returns: 解析好的脚本链表对象头节点
        """
        ...
