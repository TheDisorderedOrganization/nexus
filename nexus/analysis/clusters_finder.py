# from typing import List
from scipy.spatial import cKDTree
import numpy as np
import os
from tqdm import tqdm


# Internal imports
from ..core.frame import Frame
from ..config.settings import Settings


class ClusterFinder:
    def __init__(self, frame: Frame, settings: Settings) -> None:
        self.frame = frame
        self._lattice = self.frame.lattice
        self._nodes = self.frame.nodes
        self._settings = settings
        
    def find_neighbors(self) -> None:
        
        # Get the lattice information 
        lattice = self._lattice
        lxx, lyy, lzz = lattice[0, 0], lattice[1, 1], lattice[2, 2]
        lattice = np.array([lxx, lyy, lzz])

        # Get the wrapped positions of all nodes
        positions = self.frame.get_wrapped_positions()

        # Get the cutoffs of the system
        cutoffs = self._settings.clustering.cutoffs

        # Get the maximum value of the cutoffs of the system
        max_cutoff = 0.0
        for k, v in cutoffs.items():
            if v > max_cutoff:
                max_cutoff = v

        # Calculate the graph 
        if self._settings.lattice.apply_pbc:
            kdtree = cKDTree(positions, boxsize=lattice)
        else:
            kdtree = cKDTree(positions)

        progress_bar_kwargs = {
            "disable": not self._settings.verbose,
            "leave": True,
            "ncols": os.get_terminal_size().columns,
            "colour": "green"
        }
        progress_bar = tqdm(range(len(positions)), desc="Fetching nearest neighbours ...", **progress_bar_kwargs)

        # Loop over the node positions
        for i in progress_bar:
            # Query the neighbouring nodes within the cutoff distance
            index = kdtree.query_ball_point(positions[i], max_cutoff)

            # Calculate the distance with k nearest neighbors
            distances, indices = kdtree.query(positions[i], k=len(index))

            # Check if result is a list or a int
            if isinstance(indices, int):
                # indices is an int, turn indices into a list of a single int
                indices = [indices]

            # Check if result is a list or a int
            if isinstance(distances, float):
                # distances is a float, turn distances into a list of a single float
                distances = [distances]

            # Add the distances and indices to the node
            self._nodes[i].distances = distances
            self._nodes[i].indices = indices

            # Add the nearest neighbors to the node
            for j in indices:
                self._nodes[i].add_neighbour(self._nodes[j])
            
            # Filter the neighbors
            # self._nodes[i].filter_neighbours(distances) # TODO: find an implementation

            # Calculate the coordination number
            # self._nodes[i].calculate_coordination() # TODO: find an implementation
            
