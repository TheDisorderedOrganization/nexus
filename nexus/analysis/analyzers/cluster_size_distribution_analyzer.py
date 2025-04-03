from typing import List, Dict
from ...core.frame import Frame
from ...core.cluster import Cluster
from .base_analyzer import BaseAnalyzer
from ...config.settings import Settings
import numpy as np


class ClusterSizeDistributionAnalyzer(BaseAnalyzer):
    def __init__(self, settings: Settings) -> None:
        super().__init__(settings)
        self.size_distribution = {}
        self.std = {}

    def analyze(self, frame: Frame) -> None:
        clusters = frame.get_clusters()

        # get all connectivities
        connectivities = [c.get_connectivity() for c in clusters]
        connectivities = np.unique(connectivities)

        # get all sizes per connectivity
        for connectivity in connectivities:
            sizes = [c.get_size() for c in clusters if c.get_connectivity() == connectivity]
            sizes, ns = np.unique(sizes, return_counts=True)

            # calculate the size distribution
            self.size_distribution[connectivity] = (sizes, ns)

        self.update_frame_processed(frame)

    def update_frame_processed(self, frame: Frame) -> None:
        self.frame_processed.append(frame)

    def finalize(self) -> None:
        pass
            

    def get_result(self) -> Dict[str, float]:
        return {}

    def print_to_file(self) -> None:
        pass

    def __str__(self) -> str:
        return f"{self.__class__.__name__}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"