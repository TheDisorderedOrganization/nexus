import numpy as np
from dataclasses import dataclass
from typing import List, Dict, Optional

from .node import Node
from ..utils.geometry import wrap_positions
from ..core.cluster import Cluster

@dataclass(slots=True)
class Frame:
    """ 
    Reprensation of a frame of a trajectory

    Attributes:
    -----------
    frame_id : int
        Id of the frame
    nodes : List[Node]
        List of nodes in the frame
    lattice : np.ndarray
        Lattice of the frame
    clusters : Optional[List[Cluster]]
        List of clusters in the frame
    _data : Dict[str, np.ndarray]
        Internal data structure for node data (symbol, position)
    """
    frame_id: int
    nodes: List[Node]
    lattice: np.ndarray
    _data: Dict[str, np.ndarray]
    clusters: Optional[List[Cluster]] = None

    def __post_init__(self):
        """ Initialisation after object creation """
        if not isinstance(self.nodes, list):
            raise TypeError("nodes must be a list of Nodes")
        if self.lattice is not None and not isinstance(self.lattice, np.ndarray):
            raise TypeError("lattice must be a numpy array")
        
    def initialize_nodes(self) -> None:
        """ Initialize the list of nodes in the frame """
        id = 0
        symbols = self._data['symbol']
        positions = self._data['position']
        
        if len(symbols) != len(positions):
            raise ValueError("symbols and positions must have the same length")
        
        for symbol, position in zip(symbols, positions):
            self.nodes.append(Node(node_id=id, symbol=symbol, position=position))
            id += 1
        
    def set_lattice(self, lattice: np.ndarray) -> None:
        """ Set the lattice of the frame """
        if lattice.shape != (3, 3):
            raise ValueError("lattice must be a 3x3 numpy array")

        try:
            np.linalg.inv(lattice)
        except np.linalg.LinAlgError:
            raise ValueError("lattice must be a non-singular matrix")

        self.lattice = lattice

    def get_lattice(self) -> Optional[np.ndarray]:
        """ Get the lattice of the frame """
        return self.lattice

    def get_unique_elements(self) -> List[str]:
        """ Get the unique elements in the frame """
        return np.unique([node.symbol for node in self.nodes])

    def get_node_by_id(self, node_id: int) -> Optional[Node]:
        """ Get an node by its id """
        for node in self.nodes:
            if node.node_id == node_id:
                return node
        return None

    def get_positions(self) -> np.ndarray:
        """ Get the positions of all nodes in the frame """
        return np.array([node.position for node in self.nodes])

    def get_positions_by_element(self) -> Dict[str, np.ndarray]:
        """ Get the positions of all nodes in the frame grouped by element """
        return {node.symbol: np.array([node.position for node in self.nodes if node.symbol == node.symbol]) for node in self.nodes}

    def get_wrapped_positions(self) -> np.ndarray:
        """ Get the wrapped positions of all nodes in the frame """
        return wrap_positions(self.get_positions(), self.lattice)

    def get_wrapped_positions_by_element(self) -> Dict[str, np.ndarray]:
        """ Get the wrapped positions of all nodes in the frame grouped by element """
        return {node.symbol: wrap_positions(np.array([node.position for node in self.nodes if node.symbol == node.symbol]), self.lattice) for node in self.nodes}

    def get_clusters(self) -> List[Cluster]:
        """ Get the clusters of the frame """
        return self.clusters

    def add_cluster(self, cluster: Cluster) -> None:
        """ Add a cluster to the frame """
        if self.clusters is None:
            self.clusters = []
        self.clusters.append(cluster)

    def __len__(self) -> int:
        """ Get the number of nodes in the frame """
        return len(self.nodes)

    def __str__(self) -> str:
        return f"Frame {self.frame_id} (num_nodes={len(self.nodes)}, num_clusters={len(self.clusters)})"

    def __repr__(self) -> str:
        return f"Frame {self.frame_id} (num_nodes={len(self.nodes)})\n(first node: {(self.nodes[0].symbol, self.nodes[0].position) if len(self.nodes) > 0 else ''}\n(lattice=\n{self.lattice})\n"