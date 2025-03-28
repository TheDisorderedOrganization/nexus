from typing import List
from scipy.spatial import cKDTree
import numpy as np
import os
from tqdm import tqdm

# Internal imports
from ..core.node import Node
from ..core.cluster import Cluster
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
        for cutoff in cutoffs:
            if cutoff.distance > max_cutoff:
                max_cutoff = cutoff.distance

        # Calculate the graph 
        if self._settings.apply_pbc:
            kdtree = cKDTree(positions, boxsize=lattice)
        else:
            kdtree = cKDTree(positions)

        progress_bar_kwargs = {
            "disable": not self._settings.verbose,
            "leave": False,
            "ncols": os.get_terminal_size().columns,
            "colour": "green"
        }
        progress_bar = tqdm(range(len(positions)), desc="Fetching nearest neighbors ...", **progress_bar_kwargs)

        # Loop over the node positions
        for i in progress_bar:
            # Query the neighboring nodes within the cutoff distance
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
                self._nodes[i].add_neighbor(self._nodes[j])
            
            # Filter the neighbors
            self.filter_neighbors(idx=i, distances=distances) # TODO: find an implementation

            # Calculate the coordination number
            self.calculate_coordination(idx=i) # TODO: find an implementation
            

    def filter_neighbors(self, idx: int, distances: List[float]) -> None:
        new_list_neighbors = []
        new_list_distances  = []
        
        node = self._nodes[idx]

        for k, neighbor in enumerate(node.neighbors):
            rcut = self._settings.clustering.get_cutoff(node.symbol, neighbor.symbol)
            
            if isinstance(distances, float):
                # if 'distances' is a float, it means that the neighbor of this node is itself.
                current_distance = distances
            else:
                current_distance = distances[k]
            
            if current_distance > rcut: # neighbor is too far 
                continue # go next neighbor
            elif current_distance == 0: # neighbor is this node.
                continue # go next neighbor
            else:
                new_list_neighbors.append(neighbor) # keep the neighbor
                new_list_distances.append(current_distance)

        node.neighbors = new_list_neighbors
        node.distances = new_list_distances

    def calculate_coordination(self, idx: int) -> None:
        node = self._nodes[idx]
        
        mode = self._settings.clustering.coordination_mode

        # "all_types", "same_type", "different_type", "<node_type>"
        if mode == 'all_types':
            node.set_coordination(len(node.neighbors))
        elif mode == 'same_type':
            node.set_coordination(len([n for n in node.neighbors if n.symbol == node.symbol]))
        elif mode == 'different_type':
            node.set_coordination(len([n for n in node.neighbors if n.symbol != node.symbol]))
        else:
            node.set_coordination(len([n for n in node.neighbors if n.symbol == mode]))

    def find(self, node: Node) -> Node:
        if node.parent != node:
            node.parent = self.find(node.parent)
        return node.parent

    def union(self, node_1: Node, node_2: Node) -> None:
        root_1 = self.find(node_1)
        root_2 = self.find(node_2)
        
        if root_1 != root_2:
            root_2.parent = root_1

    def find_clusters(self) -> None:
        # Select the networking nodes based on clustering settings
        # 1 - check node types
        networking_nodes = [node for node in self._nodes if node.symbol in self._settings.clustering.node_types]

        # 2 - create rules for clustering
        # rules are a list of strings that will be used to filter the nodes using their class attributes.
        rules = []

        # 3 - check coordination
        if self._settings.clustering.with_coordination_number:
            networking_nodes = [node for node in networking_nodes if node.coordination >= self._settings.clustering.coordination_range[0] and node.coordination <= self._settings.clustering.coordination_range[1]]
            rules.append()

            if self._settings.clustering.with_alternating:
                rules

            
        