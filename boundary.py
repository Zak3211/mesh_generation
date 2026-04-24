from utils import edge
from collections import defaultdict

class boundary:
    
    def __init__(self, edges : list[edge]):
        self.edges = edges

        self.node_set = self.get_node_set() # Set containing all active node coordinates

        self.int_x_to_node = defaultdict(set) # int -> set((x,y)), all nodes with int(x) = key
        self.int_y_to_node = defaultdict(set) # int -> set((x,y)), all nodes with int(y) = key
        self.coordinates_to_node = {} # (x, y) -> unique node
        self.populate_parameter_dictionaries()

    def populate_parameter_dictionaries(self):
        """Populates self.int_x_to_node and self.int_y_to_node, and self.coordinates_to_node"""
        for node in self.node_set:
            int_x, int_y = node.get_integer_coordinates()
            coordinates = node.get_coordinates()
            self.coordinates_to_node[coordinates] = node
            self.int_x_to_node[int_x].add(coordinates)
            self.int_y_to_node[int_y].add(coordinates)

    def get_node_set(self):
        """Returns a set of all nodes in the boundary."""
        node_set = set()
        for edge in self.edges:
            node_set.update(edge.get_coordinates())
        return node_set

    def find_nearby_nodes(self, ):
        """Returns a list of all nearby nodes"""

    
    def expand_edge(self):
        pass