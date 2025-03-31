from typing import List, Dict
from ...core.frame import Frame
from ...core.cluster import Cluster
from .base_analyzer import BaseAnalyzer


class ClusterSizeDistributionAnalyzer(BaseAnalyzer):
    def __init__(self, frame_processed: List[Frame], verbose: bool = True) -> None:
        super().__init__(frame_processed, verbose)
        self.size_distribution = {}
        self.std = {}

    def analyze(self, frame: Frame) -> None:
        pass

    def update_frame_processed(self, frame: Frame) -> None:
        self.frame_processed.append(frame)

    def finalize(self) -> None:
        pass

    def get_result(self) -> Dict[str, float]:
        return {}

    def __str__(self) -> str:
        return f"{self.__class__.__name__}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"