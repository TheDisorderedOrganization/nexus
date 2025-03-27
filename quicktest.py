
# Import necessary modules
from nexus import SettingsBuilder, main
import nexus.config.settings as c
import numpy as np

# Lattice settings
config_lattice = c.LatticeSettings(
    apply_custom_lattice=False,                      # If False, read lattice from trajectory file
    custom_lattice=np.array([[66.2574, 0.0, 0.0],     # Put a custom lattice here or None
                             [0.0, 66.2574, 0.0],     # lattice values MUST be float.
                             [0.0, 0.0, 66.2574]]), 
    apply_lattice_to_all_frames=True,               # Apply the same lattice to all frames
    get_lattice_from_file=False,                    # Get lattice from file (will read from lattice.dat if True)
    lattice_file_location="./",                     # Location of the lattice file
)

# Path to the trajectory file
path = 'examples/inputs/SiO2-27216at-pos67B.xyz'

# Settings builder
settings = (SettingsBuilder() \
    .with_project_name('test')         # Name of the project \
    .with_export_directory('export')   # Directory to export results \
    .with_file_location(path)          # Path to the trajectory file \
    .with_number_of_nodes(27216)       # Number of nodes in the trajectory \
    .with_range_of_frames(0, -1)       # Range of frames to process (0 to -1 = all frames) \
    .with_verbose(True)               # Whether to print settings, progress bars and other information (True = print) \
    .with_lattice(config_lattice)      # Lattice settings \

    .build()                           # Don't forget to build the settings object
)

# Run the main function to process the trajectory
main(settings) 
