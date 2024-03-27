from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


@dataclass
class ScriptInfo:
    path: str | Path
    name: Optional[str] = field(default='未命名脚本')
    description: Optional[str] = field(default='无描述')
    version: Optional[str] = field(default='0.0.1')
    author: Optional[str] = field(default='未知的作者')
