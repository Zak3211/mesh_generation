from collections import defaultdict
from mesh import mesh
from utils import edge
import heapq

class advancing_front:
    """Advancing front data structure containing the boundary and the generated mesh"""

    def __init__(self, edges : list[edge]):
        
        self.mesh = mesh()

        self.edge_heap = edges
        heapq.heapify(self.edge_heap)

        self.node_set = self.get_node_set() # Active nodes on the front
        self.int_coords_to_node = defaultdict(set) # Int coordinates to set of nodes
        self.coordinates_to_node = {} # Coordinates to unique node

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

    def find_nearest_node(self, node, tolerance = 0.5):
        """Returns the nearest node within distance tolerance, or node if none exist"""
        
        int_x, int_y = node.get_integer_coordinates()
        curr_neighbors = self.int_coords_to_node[(int_x,int_y)]
        
        minimum_distance = tolerance
        curr_node = node

        for neighbor in curr_neighbors:
            distance = (node - neighbor).get_magnitutude()

            if distance < minimum_distance:
                minimum_distance = distance
                curr_node = neighbor
    
        return curr_node

    def expand_edge(self, edge):
        """Expands the front inwards at the given edge""" 

        candidate_node = edge.get_candidate_node()
        node = self.find_nearest_node(candidate_node)
        self._add_node(node)

        # Extracts the nodes
        node1 = edge.n1
        node2 = edge.n2

        # Creates the two new edges
        new_edge1 = edge(node1, node)
        new_edge2 = edge(node, node2)

        # Adds the new edges to the heap
        heapq.heappush(self.edge_heap, new_edge1)
        heapq.heappush(self.edge_heap, new_edge2)
    
    def _add_node(self, node):
        """Adds a new node to the data strucutre"""

        node_coordinates = node.get_coordinates()
        node_int_coordinates = node.get_integer_coordinates()

        self.node_set.delete(node_coordinates)
        self.int_coords_to_node[node_int_coordinates].add(node)
        self.coordinates_to_node = node_coordinates

    def _delete_node(self, node):
        """Deletes a node from the data structure"""

        node_coordinates = node.get_coordinates()
        node_int_coordinates = node.get_integer_coordinates()

        self.node_set.delete(node_coordinates)
        self.int_coords_to_node[node_int_coordinates].delete(node)
        del self.coordinates_to_node[node_coordinates]
        