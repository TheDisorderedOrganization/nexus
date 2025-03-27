from typing import List

# Internal imports
from .node import Node
from .frame import Frame
from ..config.settings import Settings

class Cluster:
    def __init__(self, nodes: List[Node], connectivity: str, root_id: int, frame: Frame, size: int, settings: Settings) -> None:
        self.nodes: List[Node] = nodes
        self.connectivity: str = connectivity
        self.root_id: int = root_id
        self.frame: Frame = frame
        self.size: int = size
        self.settings: Settings = settings

        self.center_of_mass: list = []
        self.indices: list = []
        self.unwrapped_positions: list = []
        self.percolation_probability: str = ''
        self.gyration_radius: float = 0.0
        self.order_parameter: list = [0.0] * 3
        self.total_nodes: int = 0
        self.concentration: float = 0.0
        self.is_percolating: bool = False
        
    def add_node(self, node: Node) -> None:
        self.nodes.append(node)

    def get_nodes(self) -> List[Node]:
        return self.nodes

    def set_indices_and_positions(self, positions_dict) -> None:
        for node_id, position in positions_dict.items():
            self.indices.append(node_id)
            self.unwrapped_positions.append([position[0], position[1], position[2]])
        self.unwrapped_positions = np.array(self.unwrapped_positions)

    def calculate_center_of_mass(self) -> None:
        self.center_of_mass = np.mean(self.unwrapped_positions, axis=0)
        
    def write_coordinates(self, path_to_directory) -> None:
        # implement writers first
        pass

    def calculate_gyration_radius(self) -> None:
        self.gyration_radius = 0
        for i in range(self.unwrapped_positions.shape[0]):
            squared_rij = np.linalg.norm(self.unwrapped_positions[i, :] - self.unwrapped_positions[:, :], axis=1)** 2
            self.gyration_radius += np.sum(squared_rij)
            
        # Normalize the sum by 0.5 s²
        self.gyration_radius = np.sqrt((0.5 / (self.size**2)) * self.gyration_radius) 

    def calculate_percolation_probability(self) -> None:
        percolate_x = False
        percolate_y = False
        percolate_z = False

        lattice = self.frame.lattice.get_lattice()

        for i in range(self.unwrapped_positions.shape[0]):
            dx = np.abs(self.unwrapped_positions[i, 0] - self.unwrapped_positions[:, 0])
            dy = np.abs(self.unwrapped_positions[i, 1] - self.unwrapped_positions[:, 1])
            dz = np.abs(self.unwrapped_positions[i, 2] - self.unwrapped_positions[:, 2])
            
            dx = np.max(dx)
            dy = np.max(dy)
            dz = np.max(dz)
            
            if dx > lattice[0, 0]:
                percolate_x = True
            if dy > lattice[1, 1]:
                percolate_y = True
            if dz > lattice[2, 2]:
                percolate_z = True
        
        if percolate_x:
            self.percolation_probability += 'x'
        if percolate_y:
            self.percolation_probability += 'y'
        if percolate_z:
            self.percolation_probability += 'z'
        
        self.is_percolating = 'x' in self.percolation_probability or 'y' in self.percolation_probability or 'z' in self.percolation_probability

    def calculate_order_parameter(self) -> None:
        if len(self.percolation_probability) == 0:
            return
        elif len(self.percolation_probability) == 1:
            self.order_parameter[0] = self.size / self.total_nodes
            self.order_parameter[1] = 0.0
            self.order_parameter[2] = 0.0
        elif len(self.percolation_probability) == 2:
            self.order_parameter[0] = self.size / self.total_nodes
            self.order_parameter[1] = self.size / self.total_nodes
            self.order_parameter[2] = 0.0
        elif len(self.percolation_probability) == 3:
            self.order_parameter[0] = self.size / self.total_nodes
            self.order_parameter[1] = self.size / self.total_nodes
            self.order_parameter[2] = self.size / self.total_nodes

    def calculate_concentration(self) -> None:
        self.concentration = self.size / self.total_nodes

    def calculate_unwrapped_positions(self, criteria, chain, quiet=False) -> None:
        stack = [self.nodes[0].parent]

        dict_positions = {stack[0].id: self.nodes[0].position}

        lattice = self.frame.lattice.get_lattice()

        if criteria == 'bond' and len(chain) ==3:
           # ok
           pass
        elif criteria == 'distance' and len(chain) ==2:
            pass
        else:
            raise ValueError("Invalid criteria or chain length")

        if criteria == 'bond':
            node_1 = chain[0]
            bridge = chain[1]
            node_2 = chain[2]
            progress_bar = tqdm(stack, desc="Unwrapping clusters ...", disable=quiet, leave=False, unit="node")
            while progress_bar:
                current_node = stack.pop()
                if current_node.symbol == node_1:
                    for fn in current_node.get_neighbors():
                        if fn.symbol == bridge:
                            for sn in fn.get_neighbors():
                                if (
                                    sn.symbol == node_2 
                                    and sn.id not in dict_positions
                                    and sn.cluster_id == self.root_id
                                ):
                                    # Compute relative position from the current atom to its second_neighbour
                                    relative_position = self.unwrap_position(
                                        sn.position - current_node.position, box_size
                                    )

                                    # Accumulate relative position to get unwrapped position
                                    dict_positions[sn.id] = (
                                        dict_positions[current_node.id] + relative_position
                                    )

                                    # Add second_neighbour to the stack
                                    stack.append(sn)
        elif criteria == 'distance':
            node_1 = chain[0]
            node_2 = chain[1]
            progress_bar = tqdm(stack, desc="Unwrapping clusters ...", disable=quiet, leave=False, unit="node")
            while progress_bar:
                current_node = stack.pop()
                if current_node.symbol == node_1:
                    for fn in current_node.get_neighbors():
                        if (
                            fn.symbol == node_2
                            and fn.id not in dict_positions
                            and fn.cluster_id == self.root_id
                        ):
                            # Compute relative position from the current atom to its first neighbour
                            relative_position = self.unwrap_position(
                                fn.position - current_node.position, box_size
                            )
                            
                            # Accumulate relative position to get unwrapped position
                            dict_positions[fn.id] = (
                                dict_positions[current_node.id] + relative_position
                            )
                            
                            # Add first neighbour to the stack
                            stack.append(fn)
        
        self.set_indices_and_positions(dict_positions)

    def unwrap_position(self, vector):
        """
        Unwraps position considering periodic boundary conditions.
        """
        unwrapped_position = []

        lattice = self.frame.lattice.get_lattice()
        
        for i in range(3):
            delta = vector[i] - round(vector[i] / lattice[i, i]) * lattice[i, i]
            unwrapped_position.append(delta)
        return tuple(unwrapped_position)