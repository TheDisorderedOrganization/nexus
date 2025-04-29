# Import necessary modules
from nexus import SettingsBuilder, main
import nexus.config.settings as c
import nexus.io.parser.parser as p
from natsort import natsorted

# Lattice config
config_lattice = c.LatticeSettings(
    apply_custom_lattice=False,
)

# Analysis config
config_analysis = c.AnalysisSettings(
    with_all=True,
)

rootdir = "/media/jperradin/Expansion/STORE_julien/LAMMPS/sio2/glass/shik+wolf/decompression/8064at-hdnnp/unload_35GPa/B-part/positions_xyz"
parser = p.Parser(file_location=rootdir, format="xyz")
files = parser.get_files()
infos = parser.get_infos()
files = natsorted(files)

for i, file in enumerate(files):
    path = file
    project_name = infos["project_name"][i]
    config_general = c.GeneralSettings(
        project_name=project_name,
        export_directory="./tests",
        file_location=path,
        range_of_frames=(0, -1),
        apply_pbc=True,
        verbose=True,
        save_logs=True,
        save_performance=True,
    )

    config_clustering = c.ClusteringSettings(
        criteria="bond",
        node_types=["Si", "O"],
        node_masses=[28.0855, 15.9994],
        connectivity=["Si", "O", "Si"],
        cutoffs=[
            c.Cutoff(type1="Si", type2="Si", distance=3.50),
            c.Cutoff(type1="Si", type2="O", distance=2.30),
            c.Cutoff(type1="O", type2="O", distance=3.05),
        ],
        with_coordination_number=True,
        coordination_mode="O",
        coordination_range=[4, 6],
        with_alternating=True,
        with_number_of_shared=False,
        shared_mode="O",
        shared_threshold=2,
        with_printed_unwrapped_clusters=False,
        print_mode="connectivity",
    )

    # Build Settings object
    settings = (
        SettingsBuilder()
        .with_general(config_general)  # General settings \
        .with_lattice(config_lattice)  # Lattice settings \
        .with_clustering(config_clustering)  # Clustering settings \
        .with_analysis(config_analysis)  # Analysis settings \
        .build()  # Don't forget to build the settings object
    )

    main(settings)

    config_clustering.with_number_of_shared = True
    config_clustering.coordination_range = [6, 6]
    config_analysis.overwrite = False

    settings = (
        SettingsBuilder()
        .with_general(config_general)  # General settings \
        .with_lattice(config_lattice)  # Lattice settings \
        .with_clustering(config_clustering)  # Clustering settings \
        .with_analysis(config_analysis)  # Analysis settings \
        .build()  # Don't forget to build the settings object
    )

    # Run the main function to process the trajectory
    main(settings)
