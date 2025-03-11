# Import the package
import nexus

# Load trajectory data
# /!\ Only extended XYZ files are supported
#     No need to provide the lattice vectors, the code will automatically detect them
#     with the keyword 'Lattice' in the XYZ file.
#     The code will crash if the file is not an extended XYZ file
trajectory = "./inputs/SiO2-27216at-pos67B.xyz"

# Initialize settings
settings = nexus.settings.Settings(extension="SiOz")
settings.quiet.set_value(True)

# Set project name, this will be used to name the output directory in the export directory
settings.project_name.set_value("silica-sequential_processing")

# Set extension
settings.extension.set_value("SiOz")

# Set export directory
settings.export_directory.set_value(f"./export/")

# Set path to XYZ file
settings.path_to_xyz_file.set_value(trajectory)

# Set number of atoms
# /!\ This value must be the same as the number of atoms in the XYZ file.
#     If the number of atoms is not provided, or the value provided is wrong, the code will crash.
settings.number_of_atoms.set_value(27216)

# Set range of frames (optional)
# settings.range_of_frames.set_value([2, 5]) # Only frames 2 to 5 will be processed

# Set header of the XYZ file
#   (ie, number of atoms in the first line, lattice properties in the second line)
settings.header.set_value(2)
settings.range_of_frames.set_value([0, 1])

nSi = int(27216 / 3)
nO = int(nSi * 2)

# Set structure
# /!\ This value must be the same as the number of atoms in the XYZ file.
#     If the number of atoms is not provided, or the value provided is wrong, the code will crash.
settings.structure.set_value(
    [
        {"element": "Si", "number": nSi},
        {"element": "O", "number": nO},
    ]
)

# Set temperature in Kelvin (optional but recommended for the recap. of the results)
settings.temperature.set_value(300)

# Set pressure in GPa (optional but recommended for the recap. of the results)
settings.pressure.set_value(10.0)

# Set to print cluster positions (optional, default is False, if set to True, the user will be prompted to confirm the action)
# uncomment the following to remove the warning
settings.print_clusters_positions.disable_warnings = True
settings.print_clusters_positions.set_value(True)

# Set to not overwrite results to compare with the previous results (optional, default is True)
settings.overwrite_results.set_value(True)

# Set cluster analysis criteria (bond or distance)
settings.cluster_settings.set_cluster_parameter("criteria", "bond")
# Set cluster connectivities to look for
settings.cluster_settings.set_cluster_parameter("connectivity", ["Si", "O", "Si"])
# Set polyhedra to look for
settings.cluster_settings.set_cluster_parameter("polyhedra", [[4, 4], [5, 5], [6, 6]])
settings.cluster_settings.set_cluster_parameter("find_extra_clusters", True)


# Run the main function with the provided settings
print("Processing the trajectory with 'bond' criteria ...")
nexus.main(settings)

# Print the path to the results
print("\n\n\t\tAll trajectories have been processed successfully.")
print(f"\n\t\tResults are saved here \u279c {settings._output_directory}\n\n")
