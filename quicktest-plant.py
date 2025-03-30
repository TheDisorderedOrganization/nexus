# Import necessary modules
from nexus import SettingsBuilder, main
import nexus.config.settings as c
import numpy as np

# Lattice settings
config_lattice = c.LatticeSettings(
    apply_custom_lattice=False,                      # If False, read lattice from trajectory file
)

# Clustering settings
config_clustering = c.ClusteringSettings(
    criteria="distance",
    node_types=["1"],
    connectivity=["1", "1"],
    cutoffs=[c.Cutoff(type1="1", type2="1", distance=1.0)], # cutoff distance in reduced units
)

# Analysis settings
config_analysis = c.AnalysisSettings(
    with_all=True,
)

# Path to the trajectory file
path = 'examples/inputs/plant/20200606.xyz'

# Settings builder
settings = (SettingsBuilder() \
    .with_project_name('test')          # Name of the project \
    .with_export_directory('export')    # Directory to export results \
    .with_file_location(path)           # Path to the trajectory file \
    .with_number_of_nodes(9519)        # Number of nodes in the trajectory \
    .with_range_of_frames(0, 0)        # Range of frames to process (0 to -1 = all frames) \
    .with_apply_pbc(False)              # Whether to apply periodic boundary conditions (True = apply) \
    .with_verbose(True)                 # Whether to print settings, progress bars and other information (True = print) \
    .with_lattice(config_lattice)       # Lattice settings \
    .with_clustering(config_clustering) # Clustering settings \
    .with_analysis(config_analysis)     # Analysis settings \
    .build()                            # Don't forget to build the settings object
)

# Run the main function to process the trajectory
main(settings) 
