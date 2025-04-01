# Import necessary modules
from nexus import SettingsBuilder, main
import nexus.config.settings as c
import numpy as np

# Lattice settings
config_lattice = c.LatticeSettings(
    apply_custom_lattice=True,                      # If False, read lattice from trajectory file
    custom_lattice=np.array([[66.2574, 0.0, 0.0],     # Put a custom lattice here or None
                             [0.0, 66.2574, 0.0],     # lattice values MUST be float.
                             [0.0, 0.0, 66.2574]]), 
    apply_lattice_to_all_frames=False,               # Apply the same lattice to all frames
    get_lattice_from_file=False,                    # Get lattice from file (will read from lattice.dat if True)
    lattice_file_location="./",                     # Location of the lattice file
)

# Clustering settings
config_clustering = c.ClusteringSettings(
    criteria="bond",
    node_types=["Si", "O"],
    node_masses=[28.0855, 15.9994],
    connectivity=["Si", "O", "Si"],
    cutoffs=[c.Cutoff(type1="Si", type2="Si", distance=3.50), # cutoff distance in reduced units
             c.Cutoff(type1="Si", type2="O", distance=2.30),
             c.Cutoff(type1="O", type2="O", distance=3.05)],
    with_coordination_number=True,
    coordination_mode="O", # "all_types" or "same_type" or "different_type" or "<node_type>"
    coordination_range=[4, 6],

    with_alternating=True, # if with_coordination_number is True, calculate alternating coordination number ie 4-5, 5-6 ...
    
    with_number_of_shared=True, # if with_coordination_number is True, calculate number of shared
    shared_mode="O", # "all_types" or "same_type" or "different_type" or "<node_type>"
    shared_threshold=2, # Minimum of shared neighbors
)

# Analysis settings
config_analysis = c.AnalysisSettings(
    with_all=True,
    with_printed_unwrapped_clusters=True,
)

# Path to the trajectory file
path = 'examples/inputs/SiO2-27216at-pos67B.xyz'

# Settings builder
settings = (SettingsBuilder() \
    .with_project_name('test')          # Name of the project \
    .with_export_directory('export')    # Directory to export results \
    .with_file_location(path)           # Path to the trajectory file \
    .with_number_of_nodes(27216)        # Number of nodes in the trajectory \
    .with_range_of_frames(4, 7)        # Range of frames to process (0 to -1 = all frames) \
    .with_apply_pbc(True)              # Whether to apply periodic boundary conditions (True = apply) \
    .with_verbose(True)                 # Whether to print settings, progress bars and other information (True = print) \
    
    .with_lattice(config_lattice)       # Lattice settings \
    .with_clustering(config_clustering) # Clustering settings \
    .with_analysis(config_analysis)     # Analysis settings \
    .build()                            # Don't forget to build the settings object
)

# Run the main function to process the trajectory
main(settings) 
