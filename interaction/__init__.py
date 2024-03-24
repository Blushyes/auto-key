from abc import ABC, abstractmethod


class InteractionLayer(ABC):
    @abstractmethod
    def start(self) -> None: ...
