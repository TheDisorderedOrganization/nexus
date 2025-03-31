from typing import List, Dict
from .base_analyzer import BaseAnalyzer
from ...core.frame import Frame
import numpy as np


class LargestClusterSizeAnalyzer(BaseAnalyzer):
    def __init__(self, frame_processed: List[Frame], verbose: bool = True) -> None:
        super().__init__(frame_processed, verbose)
        self.largest_cluster_size = {}
        self.std = {}

    def analyze(self, frame: Frame) -> None:
        clusters = frame.get_clusters()
        
        # get all connectivities
        connectivities = [c.get_connectivity() for c in clusters]
        connectivities = np.unique(connectivities)

        # get all sizes per connectivity
        for connectivity in connectivities:
            sizes = [c.get_size() for c in clusters if c.get_connectivity() == connectivity]
            max_size = np.max(sizes)

            if connectivity not in self.largest_cluster_size:
                self.largest_cluster_size[connectivity] = []
            self.largest_cluster_size[connectivity].append(max_size)

        self.update_frame_processed(frame)

    def finalize(self) -> None:
        for connectivity, sizes in self.largest_cluster_size.items():
            self.largest_cluster_size[connectivity] = np.mean(sizes)
            self.std[connectivity] = np.std(sizes, ddof=1)

    def get_result(self) -> Dict[str, float]:
        return {"largest_cluster_size": self.largest_cluster_size, "std": self.std}

    def update_frame_processed(self, frame: Frame) -> None:
        self.frame_processed.append(frame)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"