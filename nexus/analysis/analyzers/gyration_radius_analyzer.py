from typing import List, Dict
from ...core.frame import Frame
from .base_analyzer import BaseAnalyzer
from ...config.settings import Settings
from ...utils.aesthetics import remove_duplicate_lines
import numpy as np
import os
from datetime import datetime

class GyrationRadiusAnalyzer(BaseAnalyzer):
    def __init__(self, settings: Settings) -> None:
        super().__init__(settings)
        self.gyration_radii = {}
        self.std = {}
        self.concentrations = {}

    def analyze(self, frame: Frame) -> None:
        clusters = frame.get_clusters()
        concentrations = frame.get_concentration()
        
        # get all connectivities
        connectivities = [c.get_connectivity() for c in clusters]
        connectivities = np.unique(connectivities)

        # get all gyration radii per connectivity
        for connectivity in connectivities:
            gyration_radii = [c.gyration_radius for c in clusters if c.get_connectivity() == connectivity and not c.is_percolating]
            sizes = [c.get_size() for c in clusters if c.get_connectivity() == connectivity and not c.is_percolating]
            if gyration_radii:
                unique_sizes, ns = np.unique(sizes, return_counts=True)
                distribution = {}
                std = {}
                for size, gyration_radius in zip(sizes, gyration_radii):
                    if size not in distribution:
                        distribution[size] = []
                        std[size] = []
                    distribution[size].append(gyration_radius)
                    std[size].append(gyration_radius)
                self.concentrations[connectivity] = concentrations[connectivity]
                self.gyration_radii[connectivity] = distribution
                self.std[connectivity] = std

        self.update_frame_processed(frame)

    def finalize(self) -> None:
        for connectivity, gyration_radii in self.gyration_radii.items():
            for size, gyration_radii in gyration_radii.items():
                gyration_radii = np.array(gyration_radii)
                self.gyration_radii[connectivity][size] = np.mean(gyration_radii)
                self.std[connectivity][size] = 0.0 # No standard deviation since sizes are counted

        return {"concentrations": self.concentrations, "gyration_radii": self.gyration_radii, "std": self.std}
                

    def get_result(self) -> Dict[str, float]:
        return {"concentrations": self.concentrations, "gyration_radii": self.gyration_radii, "std": self.std}

    def update_frame_processed(self, frame: Frame) -> None:
        self.frame_processed.append(frame)

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
        for connectivity in self.gyration_radii:
            path = os.path.join(self._settings.export_directory, f"gyration_radius_distribution-{connectivity}.dat")
            number_of_frames = len(self.frame_processed)
            overwrite = self._settings.analysis.overwrite
            if not overwrite and os.path.exists(path):
                with open(path, 'a', encoding='utf-8') as output:
                    output.write(f"# Gyration Radius Results\n")
                    output.write(f"# Date: {datetime.now()}\n")
                    output.write(f"# Frames averaged: {number_of_frames}\n")
                    output.write("# Connectivity_type,Concentration,Cluster_size,Gyration_radius,Standard_deviation_ddof=1\n")
                output.close()
            else:
                with open(path, 'w', encoding='utf-8') as output:
                    output.write(f"# Gyration Radius Results\n")
                    output.write(f"# Date: {datetime.now()}\n")
                    output.write(f"# Frames averaged: {number_of_frames}\n")
                    output.write("# Connectivity_type,Concentration,Cluster_size,Gyration_radius,Standard_deviation_ddof=1\n")
                output.close()

    def _write_data(self) -> None:
        output = self.finalize()
        # sort gyration radii by descending size
        for connectivity in output["gyration_radii"]:
            path = os.path.join(self._settings.export_directory, f"gyration_radius_distribution-{connectivity}.dat")
            with open(path, "a") as f:
                for size, gyration_radius in sorted(output["gyration_radii"][connectivity].items(), key=lambda x: x[0], reverse=True):
                    std = output["std"][connectivity][size]
                    f.write(f"{connectivity},{output['concentrations'][connectivity]},{size},{gyration_radius},{std}\n")
            remove_duplicate_lines(path)


    def __str__(self) -> str:
        return f"{self.__class__.__name__}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"