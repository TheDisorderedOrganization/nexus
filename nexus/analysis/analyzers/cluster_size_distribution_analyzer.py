from typing import List, Dict
from ...core.frame import Frame
from .base_analyzer import BaseAnalyzer
from ...config.settings import Settings
from ...utils.aesthetics import remove_duplicate_lines
import numpy as np
import os
from datetime import datetime

class ClusterSizeDistributionAnalyzer(BaseAnalyzer):
    def __init__(self, settings: Settings) -> None:
        super().__init__(settings)
        self.size_distribution = {}
        self.std = {}
        self.concentrations = {}

    def analyze(self, frame: Frame) -> None:
        clusters = frame.get_clusters()
        concentrations = frame.get_concentration()

        # get all connectivities
        connectivities = [c.get_connectivity() for c in clusters]
        connectivities = np.unique(connectivities)

        # get all sizes per connectivity
        for connectivity in connectivities:
            sizes = [c.get_size() for c in clusters if c.get_connectivity() == connectivity and not c.is_percolating]
            sizes, ns = np.unique(sizes, return_counts=True)
            if sizes.any():
                for s in sizes:
                    if connectivity not in self.size_distribution:
                        self.size_distribution[connectivity] = {}
                        self.std[connectivity] = {}
                        self.concentrations[connectivity] = concentrations[connectivity]
                    if s not in self.size_distribution[connectivity]:
                        self.size_distribution[connectivity][s] = []
                        self.std[connectivity][s] = []
                    self.size_distribution[connectivity][s].append(ns[sizes==s])
                    self.std[connectivity][s].append(ns[sizes==s])

        self.update_frame_processed(frame)

    def update_frame_processed(self, frame: Frame) -> None:
        self.frame_processed.append(frame)

    def finalize(self) -> None:
        for connectivity, sizes in self.size_distribution.items():
            for size, ns in sizes.items():
                self.size_distribution[connectivity][size] = np.sum(ns)
                if len(ns) == 1:
                    self.std[connectivity][size] = 0.0
                else:
                    self.std[connectivity][size] = np.std(ns, ddof=1)

        return {"concentrations": self.concentrations, "size_distribution": self.size_distribution, "std": self.std}

    def get_result(self) -> Dict[str, float]:
        return {"concentrations": self.concentrations, "size_distribution": self.size_distribution, "std": self.std}

    def print_to_file(self) -> None:
        self._write_header()
        self._write_data()

    def _write_header(self) -> None:
        """
        Initializes the output file with a header.

        Parameters:
        -----------
            overwrite (bool): Whether to overwrite the existing file.
            path_to_directory (str): The directory where the output file will be saved.
            number_of_frames (int): The number of frames used in averaging.
        """
        for connectivity in self.size_distribution:
            path = os.path.join(self._settings.export_directory, f"cluster_size_distribution-{connectivity}.dat")
            number_of_frames = len(self.frame_processed)
            overwrite = self._settings.analysis.overwrite
            if not overwrite and os.path.exists(path):
                with open(path, 'a', encoding='utf-8') as output:
                    output.write(f"# Cluster Size Distribution \u279c {number_of_frames} frames averaged.\n")
                    output.write(f"# Date: {datetime.now()}\n")
                    output.write(f"# Frames averaged: {number_of_frames}\n")
                    output.write("# Connectivity_type,Concentration,Cluster_size,N_clusters,Standard_deviation_ddof=1\n")
                output.close()
            else:
                with open(path, 'w', encoding='utf-8') as output:
                    output.write(f"# Cluster Size Distribution \u279c {number_of_frames} frames averaged.\n")
                    output.write(f"# Date: {datetime.now()}\n")
                    output.write(f"# Frames averaged: {number_of_frames}\n")
                    output.write("# Connectivity_type,Concentration,Cluster_size,N_clusters,Standard_deviation_ddof=1\n")
                output.close()

    def _write_data(self) -> None:
        output = self.finalize()
        # sort cluster sizes by descending size
        for connectivity in output["size_distribution"]:
            path = os.path.join(self._settings.export_directory, f"cluster_size_distribution-{connectivity}.dat")
            with open(path, "a") as f:
                for size, ns in sorted(output["size_distribution"][connectivity].items(), key=lambda x: x[0], reverse=True):
                    std = output["std"][connectivity][size]
                    f.write(f"{connectivity},{output['concentrations'][connectivity]},{size},{ns},{std}\n")
            remove_duplicate_lines(path)
        

    def __str__(self) -> str:
        return f"{self.__class__.__name__}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"