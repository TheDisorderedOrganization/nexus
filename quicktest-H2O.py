# Import necessary modules
from nexus import SettingsBuilder, main
import nexus.config.settings as c

# Path to the trajectory file
path = './examples/inputs/waterM2825-5kbar.xyz'

# General settings
config_general = c.GeneralSettings(
    project_name="H2O",                    # Project name
    export_directory="examples/exports",    # Export directory
    file_location=path,                     # File location
    range_of_frames=(0, -1),                # Range of frames
    apply_pbc=True,                         # Apply periodic boundary conditions
    verbose=True,                           # Verbose mode (if True, print title, progress bars, etc.)
    save_logs=True,                         # Save logs    (save logs to export_directory/logs.txt)
    save_performance=False                   # Save performance (save performance data to export_directory/performance...json)
)

# Lattice settings
config_lattice = c.LatticeSettings(
    apply_custom_lattice=False,                       # If False, read lattice from trajectory file
)

# Clustering settings
config_clustering = c.ClusteringSettings(
    # your configuration goes here
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

