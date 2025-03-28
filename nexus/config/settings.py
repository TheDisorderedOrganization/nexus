import os
from dataclasses import dataclass, field
import numpy as np
from typing import Tuple, Optional, List, Dict

from nexus.core import cluster


@dataclass
class Cutoff:
    """
    Cutoff that contains all the cutoffs.
    
    Attributes:
    """
    type1: str
    type2: str
    distance: float

    def __str__(self) -> str:
        return f"{self.type1}-{self.type2} : distance={self.distance}"

    def get_distance(self) -> float:
        return self.distance


@dataclass
class ClusteringSettings:
    """
    Clustering settings that contains all the clustering settings. 
    
    Attributes:
    """
    criteria: str = "distance" # "distance" or "bond"
    node_types: List[str] = field(default_factory=lambda: ["A", "B"]) # List of node types
    node_masses: List[float] = field(default_factory=lambda: [1.0, 1.0]) # List of node masses in reduced units
    connectivity: List[str] = field(default_factory=lambda: ["A", "B", "A"]) # List of connectivity
    cutoffs: List[Cutoff] = field(default_factory=lambda: [Cutoff(type1="A", type2="B", distance=1.0)]) # Cutoffs for distance and bond criteria

    # Coordination number ie number of nearest neighbors
    # - all_types: all types of nodes are considered A-AB, B-AB
    # - same_type: only nodes of the same type are considered A-A, B-B
    # - different_type: only nodes of the different types are considered A-B, B-A
    
    with_coordination_number: bool = False # Whether to calculate the coordination number

    coordination_mode: str = "all_types" # "all_types", "same_type", "different_type", "<node_type>"
    
    coordination_range: List[int] = field(default_factory=lambda: [1, 4]) # Minimum and maximum coordination numbers to consider

    with_alternating: bool = False # Whether to calculate the alternating clusters ie A4-B5, B2-A3

    def get_cutoff(self, type1: str, type2: str) -> float:
        for cutoff in self.cutoffs:
            if cutoff.type1 == type1 and cutoff.type2 == type2:
                return cutoff.distance
            elif cutoff.type1 == type2 and cutoff.type2 == type1:
                return cutoff.distance
        return None

    def __str__(self) -> str:
        lines = []
        for key, value in self.__dict__.items():
            if value is not None:
                if not self.with_coordination_number and key == "with_coordination_number":
                    continue
                elif not self.with_coordination_number and key == "coordination_mode":
                    continue
                elif not self.with_coordination_number and key == "coordination_range":
                    continue
                elif not self.with_alternating and key == "with_alternating":
                    continue

                lines.append(f"\t\t|- {key}: {value}")
        output = '''
        Clustering Settings:
        -----------------
{}
        '''.format('\n'.join(lines))
        return output

@dataclass
class AnalysisSettings:
    """ 
    Analysis settings that contains all the analyzer settings. 
    
    Attributes:
    """
    with_all: bool = False # Whether to calculate all the properties
    with_average_cluster_size: bool = False # Whether to calculate the average cluster size
    with_largest_cluster_size: bool = False # Whether to calculate the largest cluster size
    with_spanning_cluster_size: bool = False # Whether to calculate the spanning cluster size
    with_gyration_radius: bool = False # Whether to calculate the gyration radius
    with_correlation_length: bool = False # Whether to calculate the correlation length
    with_percolation_probability: bool = False # Whether to calculate the percolation probability
    with_order_parameter: bool = False # Whether to calculate the order parameter
    with_cluster_size_distribution: bool = False # Whether to calculate the cluster size distribution
    with_printed_unwrapped_clusters: bool = False # Whether to print the unwrapped clusters
    _disable_warnings: bool = False # Whether to disable warnings

    def get_analyzers(self) -> List[str]:
        analyzers = []
        if self.with_average_cluster_size:
            analyzers.append("AverageClusterSizeAnalyzer")
        if self.with_largest_cluster_size:
            analyzers.append("LargestClusterSizeAnalyzer")
        if self.with_spanning_cluster_size:
            analyzers.append("SpanningClusterSizeAnalyzer")
        if self.with_gyration_radius:
            analyzers.append("GyrationRadiusAnalyzer")
        if self.with_correlation_length:
            analyzers.append("CorrelationLengthAnalyzer")
        if self.with_percolation_probability:
            analyzers.append("PercolationProbabilityAnalyzer")
        if self.with_order_parameter:
            analyzers.append("OrderParameterAnalyzer")
        if self.with_cluster_size_distribution:
            analyzers.append("ClusterSizeDistributionAnalyzer")
        if self.with_all:
            analyzers.append("AverageClusterSizeAnalyzer")
            analyzers.append("LargestClusterSizeAnalyzer")
            analyzers.append("SpanningClusterSizeAnalyzer")
            analyzers.append("GyrationRadiusAnalyzer")
            analyzers.append("CorrelationLengthAnalyzer")
            analyzers.append("PercolationProbabilityAnalyzer")
            analyzers.append("OrderParameterAnalyzer")
            analyzers.append("ClusterSizeDistributionAnalyzer")
        return analyzers

    def __str__(self) -> str:
        lines = []
        for key, value in self.__dict__.items():
            if value is not None:
                if not self.with_all and key == "with_all":
                    continue
                elif not self.with_average_cluster_size and key == "with_average_cluster_size":
                    continue
                elif not self.with_largest_cluster_size and key == "with_largest_cluster_size":
                    continue
                elif not self.with_spanning_cluster_size and key == "with_spanning_cluster_size":
                    continue
                elif not self.with_gyration_radius and key == "with_gyration_radius":
                    continue
                elif not self.with_correlation_length and key == "with_correlation_length":
                    continue
                elif not self.with_percolation_probability and key == "with_percolation_probability":
                    continue
                elif not self.with_order_parameter and key == "with_order_parameter":
                    continue
                elif not self.with_cluster_size_distribution and key == "with_cluster_size_distribution":
                    continue
                elif key == "_with_printed_unwrapped_clusters":
                    continue
                elif key == "_disable_warnings":
                    continue
                lines.append(f"\t\t|- {key}: {value}")
        output = '''
        Analysis Settings:
        -----------------
{}
        '''.format('\n'.join(lines))
        return output

@dataclass
class LatticeSettings:
    """ 
    Lattice settings. 
    
    TODO implement lattice fetcher from file
         implement the handling of lattice settings in the system

    Attributes:
        lattice_in_trajectory_file (bool): Whether the lattice is present in the trajectory file.
        lattice (np.ndarray): The lattice matrix.
        get_lattice_from_file (bool): Whether to get the lattice from a file.
        lattice_file_location (str): Location of the lattice file.
        apply_lattice_to_all_frames (bool): Whether to apply the lattice to all frames.
        apply_pbc (bool): Whether to apply periodic boundary conditions.
    """
    apply_custom_lattice: bool = False
    custom_lattice: np.ndarray = field(default_factory=lambda: np.array([[0., 0., 0.], [0., 0., 0.], [0., 0., 0.]]))
    get_lattice_from_file: bool = False
    lattice_file_location: str = "./"
    apply_lattice_to_all_frames: bool = True

    def __str__(self) -> str:
        if not self.apply_custom_lattice:
            return ""
        lines = []
        for key, value in self.__dict__.items():
            if value is not None:
                if key == "custom_lattice":
                    line1 = f"\t\t|- {key}:"
                    lx = np.array2string(value[0], separator=', ', formatter={'float_kind': lambda x: f'{x}'})
                    ly = np.array2string(value[1], separator=', ', formatter={'float_kind': lambda x: f'{x}'})
                    lz = np.array2string(value[2], separator=', ', formatter={'float_kind': lambda x: f'{x}'})
                    lines.append(f"{line1}\n\t\t\tlx = {lx}\n\t\t\tly = {ly}\n\t\t\tlz = {lz}")
                else:
                    lines.append(f"\t\t|- {key}: {value}")
        output = '''

        Lattice Settings:
        -----------------
{}
        '''.format('\n'.join(lines))
        return output

@dataclass
class Settings:
    """ Settings for the Reve package and it is constructed using the SettingsBuilder. """
    project_name: str = "default"
    export_directory: str = "export"
    file_location: str = "./"
    number_of_nodes: int = 0
    range_of_frames: Tuple[int, int] = (0, -1)
    apply_pbc: bool = True
    verbose: bool = False
    lattice: LatticeSettings = field(default_factory=LatticeSettings)
    clustering: ClusteringSettings = field(default_factory=ClusteringSettings)
    analysis: AnalysisSettings = field(default_factory=AnalysisSettings)

    @property
    def output_directory(self) -> str:
        return os.path.join(self.export_directory, self.project_name)

    def set_range_of_frames(self, start: int, end: Optional[int] = None):
        if end is None:
            end = -1
        if start < 0:
            raise ValueError("Start frame cannot be negative")
        if end != -1 and start > end:
            raise ValueError("Start frame cannot be greater than end frame")
        self.range_of_frames = (start, end)

    def __str__(self) -> str:
        lines = []
        for key, value in self.__dict__.items():
            if value is not None:
                if key == 'lattice' and not self.lattice.apply_custom_lattice:
                    continue
                elif key == 'lattice' and self.lattice.apply_custom_lattice:
                    lines.append(f"\t{str(self.lattice)}")
                elif key == 'analysis':
                    lines.append(f"\t{str(self.analysis)}")
                elif key == 'clustering':
                    lines.append(f"\t{str(self.clustering)}")
                else:
                    lines.append(f"\t|- {key}: {value}")
        output = '''
        Global Settings:
        ----------------
{}
        '''.format('\n'.join(lines))
        return output

class SettingsBuilder:
    def __init__(self):
        self._settings = Settings()  # Start with default settings

    def with_project_name(self, name: str):
        self._settings.project_name = name
        return self

    def with_export_directory(self, directory: str):
        self._settings.export_directory = directory
        return self

    def with_file_location(self, location: str):
        self._settings.file_location = location
        return self

    def with_number_of_nodes(self, num_nodes: int):
        self._settings.number_of_nodes = num_nodes
        return self

    def with_range_of_frames(self, start: int, end: Optional[int] = None):
        self._settings.set_range_of_frames(start, end)
        return self
    
    def with_apply_pbc(self, apply_pbc: bool):
        self._settings.apply_pbc = apply_pbc
        return self

    def with_lattice(self, lattice: LatticeSettings):
        self._settings.lattice = lattice
        return self

    def with_verbose(self, verbose: bool):
        self._settings.verbose = verbose
        return self

    def with_analysis(self, analysis: AnalysisSettings):
        if analysis.with_printed_unwrapped_clusters and not analysis._disable_warnings:
            print("Warning: with_printed_unwrapped_clusters is enabled. This may be disk usage consuming.")

        self._settings.analysis = analysis
        return self

    def with_clustering(self, clustering: ClusteringSettings):
        if clustering.criteria not in ['bond', 'distance']:
            raise ValueError(f"Invalid criteria: {clustering.criteria}")

        if clustering.connectivity is None:
            raise ValueError(f"Invalid connectivity: {clustering.connectivity}")

        if clustering.criteria == 'bond' and len(clustering.connectivity) != 3:
            raise ValueError(f"Invalid connectivity, connectivity must be a list of 3 elements, got {len(clustering.connectivity)}")

        if clustering.criteria == 'distance' and len(clustering.connectivity) != 2:
            raise ValueError(f"Invalid connectivity, connectivity must be a list of 2 elements, got {len(clustering.connectivity)}")

        if clustering.with_coordination_number:
            modes = ["all_types", "same_type", "different_type"]
            if clustering.coordination_mode not in modes and clustering.coordination_mode not in clustering.node_types:
                raise ValueError(f"Invalid coordination mode: {clustering.coordination_mode}")
            if len(clustering.coordination_range) != 2:
                raise ValueError(f"Invalid coordination range: {clustering.coordination_range}")
            if clustering.coordination_range[0] < 1:
                raise ValueError(f"Invalid coordination range: {clustering.coordination_range}")
            if clustering.coordination_range[0] > clustering.coordination_range[1]:
                raise ValueError(f"Invalid coordination range: {clustering.coordination_range}")
            
        self._settings.clustering = clustering
        return self

    def build(self) -> Settings:
        return self._settings

__all__ = [
    Settings,
    SettingsBuilder,
    AnalysisSettings,
    ClusteringSettings,
    LatticeSettings,
    Cutoff,
]