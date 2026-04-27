from collections import defaultdict
from mesh import mesh
from geometry_components.edge import edge
import heapq

def orient(a, b, c):
    return (b.x - a.x)*(c.y - a.y) - (b.y - a.y)*(c.x - a.x)

class advancing_front:
    """Advancing front data structure containing the boundary and the generated mesh"""

    def __init__(self, edges : list[edge]):
        
        self.mesh = mesh(edges)

        self.edge_heap = edges
        heapq.heapify(self.edge_heap)

        # Tracking the active edges in the front
        self.active_edges = set(edges)

        # Creating a hashset of active noes
        self.node_set = set()
        for edge in edges:
            self.node_set.update(edge.get_nodes())
        
        # Int coordinates to set of nodes, used for proximity lookup
        self.int_coords_to_nodes = defaultdict(set)
        for node in self.node_set:
            int_coordinates = node.get_integer_coordinates()
            self.int_coords_to_nodes[int_coordinates].add(node)

    def find_nearest_node(self, node, tolerance=0.2):

        int_x, int_y = node.get_integer_coordinates()
        curr_node = node
        minimum_distance = tolerance

        # Gets all neighbors in the 3x3 grid
        neighbors = set()
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                new_neighbors = self.int_coords_to_nodes[(int_x + dx, int_y + dy)]
                neighbors.update(new_neighbors)
        
        # Finds the closest neighbor within the tolerance
        for neighbor in neighbors:
            distance = (node - neighbor).get_magnitude()
            if distance < minimum_distance:
                minimum_distance = distance
                curr_node = neighbor
        
        return curr_node

    def brute_force_intersection_check(self, curr_edge):
        for other_edge in self.mesh.edge_set:
            if curr_edge.intersects(other_edge):
                return True
        return False
    
    def expand_mesh(self):
        """Expands the front inwards at the given edge""" 

        for _ in range(1000):
            if not self.edge_heap:
                print("Mesh Closure Achieved")
                return
        
            # Fetch the shortest edge
            curr_edge = heapq.heappop(self.edge_heap)

            # Checks if the current edge is active
            if curr_edge not in self.active_edges:
                continue
            self.active_edges.remove(curr_edge)

            # Fetch the node to expand to
            candidate_node = curr_edge.get_candidate_node()
            node = self.find_nearest_node(candidate_node)

            # Extracts the nodes
            node1 = curr_edge.n1
            node2 = curr_edge.n2
            
            # Checks orientation of triangle
            if orient(node1, node2, node) <= 0:
                print("Invalid Triangle Reached")
                continue

            # We have generated a flat triangle
            if node == node1 or node == node2:
                print("Flat Triangle Generated")
                continue
        
            # Creates the two new edges
            new_edge1 = edge(node1, node)
            new_edge2 = edge(node, node2)

            if self.brute_force_intersection_check(new_edge1):
                continue
            if self.brute_force_intersection_check(new_edge2):
                continue
        
            for e in [new_edge1, new_edge2]:
                
                # Triangle closure
                if e in self.active_edges:
                    self.active_edges.remove(e)
                    continue
                
                self.active_edges.add(e)
                heapq.heappush(self.edge_heap, e)
                self.mesh.edge_set.add(e)

            if node == candidate_node:
                self._add_node(node)

        print(f"Upper iteration limit achieved, edge_heap size: {len(self.edge_heap)}")


    def _add_node(self, node):
        """Adds a new node to the data strucutre"""
        self.node_set.add(node)
        node_int_coordinates = node.get_integer_coordinates()
        self.int_coords_to_nodes[node_int_coordinates].add(node)    

    def _delete_node(self, node):
        """Deletes a node from the data structure"""
        self.node_set.remove(node)
        node_int_coordinates = node.get_integer_coordinates()
        self.int_coords_to_nodes[node_int_coordinates].remove(node)
        