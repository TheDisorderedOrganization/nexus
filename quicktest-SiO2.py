# Import necessary modules
from nexus import SettingsBuilder, main
import nexus.config.settings as c

# Path to the trajectory file
path = 'examples/inputs/SiO2-27216at-pos67B.xyz'

# General settings
config_general = c.GeneralSettings(
    project_name="SiO2",                    # Project name
    export_directory="examples/exports",    # Export directory
    file_location=path,                     # File location
    range_of_frames=(0, 10),                # Range of frames
    apply_pbc=True,                         # Apply periodic boundary conditions
    verbose=True,                           # Verbose mode (if True, print title, progress bars, etc.)
    save_logs=True,                         # Save logs    (save logs to export_directory/logs.txt)
    save_performance=True                   # Save performance (save performance data to export_directory/performance...json)
)

# Lattice settings
config_lattice = c.LatticeSettings(
    apply_custom_lattice=False,                       # If False, read lattice from trajectory file
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
    
    with_number_of_shared=False, # if with_coordination_number is True, calculate number of shared
    shared_mode="O", # "all_types" or "same_type" or "different_type" or "<node_type>"
    shared_threshold=2, # Minimum of shared neighbors

    with_printed_unwrapped_clusters=False,
    print_mode="connectivity" # "all", "connectivity", "individual", "none"
)

# Analysis settings
config_analysis = c.AnalysisSettings(
    with_all=True,
)

# Build Settings object
settings = (SettingsBuilder() \
    .with_general(config_general)               # General settings \
    .with_lattice(config_lattice)               # Lattice settings \
    .with_clustering(config_clustering)         # Clustering settings \
    .with_analysis(config_analysis)             # Analysis settings \
    .build()                                    # Don't forget to build the settings object
)
 
# Run the main function to process the trajectory
main(settings) 

# Reconfigure and rerun
config_clustering.with_number_of_shared = True
config_clustering.coordination_range = [6, 6] # Looking for SiO6=SiO6
config_analysis.overwrite = False # Do not erase previous results

settings = (SettingsBuilder() \
    .with_general(config_general)               # General settings \
    .with_lattice(config_lattice)               # Lattice settings \
    .with_clustering(config_clustering)         # Clustering settings \
    .with_analysis(config_analysis)             # Analysis settings \
    .build()                                    # Don't forget to build the settings object
)
 
# Run the main function to process the trajectory
main(settings) 
