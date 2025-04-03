from typing import List, Dict
from ...core.frame import Frame
from ...core.cluster import Cluster
from .base_analyzer import BaseAnalyzer
from ...config.settings import Settings
from ...utils.aesthetics import remove_duplicate_lines

import numpy as np
import os


class AverageClusterSizeAnalyzer(BaseAnalyzer):
    def __init__(self, settings: Settings) -> None:
        super().__init__(settings)
        self.average_sizes: Dict[str, List[float]] = {}
        self.std: Dict[str, float] = {}
        self.concentrations: Dict[str, List[float]] = {}

    def analyze(self, frame: Frame) -> None:
        clusters = frame.get_clusters()
        concentrations = frame.get_concentration()

        # get all connectivities
        connectivities = [c.get_connectivity() for c in clusters]
        connectivities = np.unique(connectivities)

        # get all sizes per connectivity
        for connectivity in connectivities:
            sizes = [c.get_size() for c in clusters if c.get_connectivity() == connectivity and not c.is_percolating]
            if sizes:
                sizes, ns = np.unique(sizes, return_counts=True)

                # calculate average cluster size
                average_size = 0.0
                for s, n in zip(sizes, ns):
                    average_size += (s**2 * n) / np.sum(sizes * ns)

                if connectivity not in self.average_sizes:
                    self.average_sizes[connectivity] = []
                self.average_sizes[connectivity].append(average_size)

                if connectivity not in self.concentrations:
                    self.concentrations[connectivity] = []
                self.concentrations[connectivity].append(concentrations[connectivity])

            else:
                if connectivity not in self.average_sizes:
                    self.average_sizes[connectivity] = []
                self.average_sizes[connectivity].append(0.0)

                if connectivity not in self.concentrations:
                    self.concentrations[connectivity] = []
                self.concentrations[connectivity].append(concentrations[connectivity])

        self.update_frame_processed(frame)

    def update_frame_processed(self, frame: Frame) -> None:
        self.frame_processed.append(frame)

    def finalize(self) -> Dict[str, float]:
        for connectivity, sizes in self.average_sizes.items():
            if len(sizes) == 1:
                self.std[connectivity] = 0.0
            else:
                self.std[connectivity] = np.std(sizes, ddof=1)
            self.average_sizes[connectivity] = np.mean(sizes)
            # replace eventual nan with 0.0
            self.std[connectivity] = np.nan_to_num(self.std[connectivity])

        for connectivity, concentrations in self.concentrations.items():
            self.concentrations[connectivity] = np.mean(concentrations)

        return {"concentrations": self.concentrations, "average_cluster_size": self.average_sizes, "std": self.std}

    def get_result(self) -> Dict[str, float]:
        return {"concentrations": self.concentrations, "average_cluster_size": self.average_sizes, "std": self.std}

    def print_to_file(self) -> None:
        self._write_header()
        self._write_data()
        

    def get_std(self) -> Dict[str, float]:
        return self.std

    def _write_header(self) -> None:
        """
        Initializes the output file with a header.

        Parameters:
        -----------
            overwrite (bool): Whether to overwrite the existing file.
            path_to_directory (str): The directory where the output file will be saved.
            number_of_frames (int): The number of frames used in averaging.
        """
        path = os.path.join(self._settings.export_directory, "average_cluster_size.dat")
        number_of_frames = len(self.frame_processed)
        overwrite = self._settings.analysis.overwrite
        if not overwrite and os.path.exists(path):
            with open(path, 'a', encoding='utf-8') as output:
                output.write(f"# Average cluster size \u279c {number_of_frames} frames averaged.\n")
                output.write("# Concentration \u279c Average cluster size +/- Error # Connectivity\n")
            output.close()
        else:
            with open(path, 'w', encoding='utf-8') as output:
                output.write(f"# Average cluster size \u279c {number_of_frames} frames averaged.\n")
                output.write("# Concentration \u279c Average cluster size +/- Error # Connectivity\n")
            output.close()

    def _write_data(self) -> None:
        output = self.finalize()
        path = os.path.join(self._settings.export_directory, "average_cluster_size.dat")
        with open(path, "a") as f:
            for connectivity in self.average_sizes:
                concentration = output["concentrations"][connectivity]
                average_size = output["average_cluster_size"][connectivity]
                std = output["std"][connectivity]
                f.write(f"{concentration:10.6f} \u279c {average_size:10.6f} +/- {std:<10.5f} # {connectivity}\n")
        remove_duplicate_lines(path)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"