from abc import ABC, abstractmethod
from typing import List, Dict

from ...core.frame import Frame   
from ...config.settings import Settings

class BaseAnalyzer(ABC):
    def __init__(self, settings: Settings) -> None:
        self.frame_processed: List[Frame] = []
        self._settings: Settings = settings

    @abstractmethod
    def analyze(self, frame: Frame) -> None:
        pass

    @abstractmethod
    def update_frame_processed(self, frame: Frame) -> None:
        pass

    @abstractmethod
    def finalize(self) -> None:
        pass

    @abstractmethod
    def get_result(self) -> Dict[str, float]:
        pass

    @abstractmethod
    def print_to_file(self) -> None:
        pass

    def __str__(self) -> str:
        return f"{self.__class__.__name__}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"