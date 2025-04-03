# Import necessary modules
from nexus import SettingsBuilder, main
import nexus.config.settings as c
import nexus.io.parser.parser as p
import numpy as np

# Lattice settings
config_lattice = c.LatticeSettings(
    apply_custom_lattice=False,                      # If False, read lattice from trajectory file
)

# Clustering settings
config_clustering = c.ClusteringSettings(
    criteria="distance",
    node_types=["1"],
    node_masses=[1.0],
    connectivity=["1", "1"],
    cutoffs=[c.Cutoff(type1="1", type2="1", distance=1.1)], # cutoff distance in reduced units
    # with_printed_unwrapped_clusters=True,
    # print_mode="all", # "all", "connectivity", "individual", "none"
)

# Analysis settings
config_analysis = c.AnalysisSettings(
    with_all=False,
    with_average_cluster_size=True,
    with_spanning_cluster_size=True,
    with_largest_cluster_size=True,
    with_order_parameter=True,
)

# Path to the trajectory file
rootdir = './examples/inputs/ordinary_percolation'
parser = p.Parser(file_location=rootdir, format='xyz')
files = parser.get_files()
infos = parser.get_infos()

for i, file in enumerate(files):
    path = file
    project_name = infos['project_name'][i]
    # Settings builder
    settings = (SettingsBuilder() \
        .with_project_name(project_name)            # Name of the project \
        .with_export_directory('examples/exports')  # Directory to export results \
        .with_file_location(path)                   # Path to the trajectory file \
        .with_range_of_frames(0, 0)                 # Range of frames to process (0 to -1 = all frames) \
        .with_apply_pbc(True)                       # Whether to apply periodic boundary conditions (True = apply) \
        .with_verbose(True)                         # Whether to print settings, progress bars and other information (True = print) \
        .with_lattice(config_lattice)               # Lattice settings \
        .with_clustering(config_clustering)         # Clustering settings \
        .with_analysis(config_analysis)             # Analysis settings \
        .build()                                    # Don't forget to build the settings object
    )

    if file == './examples/inputs/ordinary_percolation/percolation_sites_0.300.xyz':
        main(settings)

    if file == './examples/inputs/ordinary_percolation/percolation_sites_0.025.xyz':
        main(settings)

    # Run the main function to process the trajectory
    # main(settings)