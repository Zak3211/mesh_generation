from utils import edge, get_node_distance
from collections import defaultdict

class boundary:
    
    def __init__(self, edges : list[edge]):
        self.edges = edges
        self.node_set = self.get_node_set() # Set containing all active node coordinates

        # (int(x), int(y)) -> set((x,y)), all nodes within an integer quadrant
        self.int_coords_to_node = defaultdict(set)

        # (x, y) -> unique node
        self.coordinates_to_node = {} 

        for node in self.node_set:
            int_coordinates = node.get_integer_coordinates()
            self.int_coords_to_node[int_coordinates].add(coordinates)
            coordinates = node.get_coordinates()
            self.coordinates_to_node[coordinates] = node

    def get_node_set(self):
        """Returns a set of all nodes in the boundary."""
        node_set = set()
        for edge in self.edges:
            node_set.update(edge.get_coordinates())
        return node_set

    def find_nearby_nodes(self, node):
        """Returns a set of neighbor candidates"""
        int_x, int_y = node.get_integer_coordinates()
        neighbor_candidates = set()
        for x in range(int_x-1, int_x + 2):
            for y in range(int_y-1, int_y+2):
                curr_neighbors = self.int_coords_to_node[(x,y)]
                neighbor_candidates.update(curr_neighbors)
        return neighbor_candidates
    
    def expand_edge(self):
        pass