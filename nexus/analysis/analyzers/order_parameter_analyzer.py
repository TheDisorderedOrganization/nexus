from typing import List
from ...core.frame import Frame
from .base_analyzer import BaseAnalyzer


class OrderParameterAnalyzer(BaseAnalyzer):
    def __init__(self, frame_processed: List[Frame], verbose: bool = True) -> None:
        super().__init__(frame_processed, verbose)

    def analyze(self) -> None:
        pass

    def update_frame_processed(self, frame: Frame) -> None:
        self.frame_processed.append(frame)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"
