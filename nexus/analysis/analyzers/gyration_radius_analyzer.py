from typing import List, Dict
from ...core.frame import Frame
from .base_analyzer import BaseAnalyzer
from ...config.settings import Settings
import numpy as np

class GyrationRadiusAnalyzer(BaseAnalyzer):
    def __init__(self, settings: Settings) -> None:
        super().__init__(settings)
        self.gyration_radii = {}
        self.std = {}

    def analyze(self, frame: Frame) -> None:
        clusters = frame.get_clusters()
        self.concentrations.append(frame.get_concentration())
        
        # get all connectivities
        connectivities = [c.get_connectivity() for c in clusters]
        connectivities = np.unique(connectivities)

        # get all gyration radii per connectivity
        for connectivity in connectivities:
            gyration_radii = [c.get_gyration_radius() for c in clusters if c.get_connectivity() == connectivity and not c.is_percolating]
            sizes = [c.get_size() for c in clusters if c.get_connectivity() == connectivity and not c.is_percolating]
            
            if gyration_radii:
                unique_sizes, ns = np.unique(sizes, return_counts=True)
                distribution = {}
                for size, gyration_radius, n in zip(sizes, gyration_radii, ns):
                    if size not in distribution:
                        distribution[size] = []
                    distribution[size].append(gyration_radius)

                self.gyration_radii[connectivity] = distribution

    def finalize(self) -> None:
        pass

    def get_result(self) -> Dict[str, float]:
        return {}

    def update_frame_processed(self, frame: Frame) -> None:
        self.frame_processed.append(frame)

    def print_to_file(self) -> None:
        pass

    def __str__(self) -> str:
        return f"{self.__class__.__name__}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"