from typing import List, Dict
from ...core.frame import Frame
from ...core.cluster import Cluster
from .base_analyzer import BaseAnalyzer

import numpy as np


class AverageClusterSizeAnalyzer(BaseAnalyzer):
    def __init__(self, frame_processed: List[Frame], verbose: bool = True) -> None:
        super().__init__(frame_processed, verbose)
        self.average_sizes: Dict[str, List[float]] = {}
        self.std: Dict[str, float] = {}

    def analyze(self, frame: Frame) -> None:
        clusters = frame.get_clusters()

        # get all connectivities
        connectivities = [c.get_connectivity() for c in clusters]
        connectivities = np.unique(connectivities)

        # get all sizes per connectivity
        for connectivity in connectivities:
            sizes = [c.get_size() for c in clusters if c.get_connectivity() == connectivity]
            sizes, ns = np.unique(sizes, return_counts=True)

            # calculate average cluster size
            average_size = 0.0
            for s, n in zip(sizes, ns):
                average_size += (s**2 * n) / np.sum(sizes * ns)

            if connectivity not in self.average_sizes:
                self.average_sizes[connectivity] = []
            self.average_sizes[connectivity].append(average_size)

        self.update_frame_processed(frame)

    def update_frame_processed(self, frame: Frame) -> None:
        self.frame_processed.append(frame)

    def finalize(self) -> None:
        for connectivity, sizes in self.average_sizes.items():
            self.average_sizes[connectivity] = np.mean(sizes)
            self.std[connectivity] = np.std(sizes, ddof=1)
            
    def get_result(self) -> Dict[str, float]:
        return {"average_cluster_size": self.average_sizes, "std": self.std}

    def get_std(self) -> Dict[str, float]:
        return self.std

    def __str__(self) -> str:
        return f"{self.__class__.__name__}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"