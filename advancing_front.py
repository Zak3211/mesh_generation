from collections import defaultdict
from mesh import mesh
from geometry_components.edge import edge
import heapq
from collections import deque
import matplotlib.pyplot as plt

class edge_storage:
    def __init__(self, edges = None):
        self.q = deque()
        if edges is not None:
            for edge in edges:
                self.add_edge(edge)

    def add_edge(self, edge):
        #heapq.heappush(self.q, edge)
        self.q.append(edge)

    def get_edge(self):
        #return heapq.heappop(self.q)
        return self.q.popleft()
    
    def __bool__(self):
        return len(self.q) != 0

    def __len__(self):
        return len(self.q)

class advancing_front:
    """Advancing front data structure containing the boundary and the generated mesh"""

    def __init__(self, edges : list[edge], tolerance = 0.2, iterations = 1000, is_animated=False):
        
        # Global object variables
        self.mesh = mesh(edges, is_animated)
        self.tolerance = tolerance
        self.iterations = iterations
        self.edge_heap = edge_storage(edges=edges)

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

        # Int coordinates to set of edges
        self.int_coords_to_edges = defaultdict(set)
        for curr_edge in edges:
            int_coordinates_list = curr_edge.get_integer_buckets()
            for x, y in int_coordinates_list:
                self.int_coords_to_edges[x, y].add(curr_edge)

        self.expanded_edges = set()

    def find_nearest_node(self, curr_edge, node):
        """Returns the nearest neighbor such that (node->neighbor) does not exist in the mesh"""
        int_x, int_y = node.get_integer_coordinates()
        curr_node = node
        minimum_distance = float('inf')

        # Gets all neighbors in the 3x3 grid
        neighbors = set()
        for dx in [-2, -1, 0, 1, 2]:
            for dy in [-2, -1, 0, 1, 2]:
                new_neighbors = self.int_coords_to_nodes[(int_x + dx, int_y + dy)]
                neighbors.update(new_neighbors)
        
        # Finds the closest neighbor within the tolerance
        for neighbor in neighbors:
            
            # Checking if this neighbor forms a valid pairing
            if not self.check_new_edge_validity(curr_edge, neighbor):
                continue

            distance = (node - neighbor).get_magnitude()
            if distance < minimum_distance:
                minimum_distance = distance
                curr_node = neighbor
        
        return curr_node

    def bucketted_intersection_check(self, curr_edge):
        if curr_edge in self.mesh.edge_set:
           return False
        for x, y in curr_edge.get_integer_buckets():
            for other_edge in self.int_coords_to_edges[x, y]:
                if curr_edge.intersects(other_edge):
                    return True
        return False
    
    def check_triangle_quality(self, node1, node2, node3):
        """Ensures generated triangles are of adequate quality"""
        def orient(a, b, c):
            """Helper function to check the orientation of a triangle"""
            return (b.x - a.x)*(c.y - a.y) - (b.y - a.y)*(c.x - a.x)
        if orient(node1, node2, node3) <= 0:
            return False
        if node1 == node3 or node3 == node2:
            return False
        return True

    def check_new_edge_validity(self, curr_edge, candidate_node):
        node1 = curr_edge.n1
        node2 = curr_edge.n2

        # Creates the two new candidate edges
        new_edge1 = edge(node1, candidate_node)
        new_edge2 = edge(candidate_node, node2)

        # Checking triangle quality
        if not self.check_triangle_quality(node1, node2, candidate_node):
            return False
        
        # Checking for intersections
        if self.bucketted_intersection_check(new_edge1):
            return False
        if self.bucketted_intersection_check(new_edge2):
            return False

        return True
    
    def expand_mesh_with_node(self, curr_edge, candidate_node):
        """Expands curr_edge using candidate_node, returns True if succesful and False otherwise"""
        
        if not self.check_new_edge_validity(curr_edge, candidate_node):
            return False
        
        # Extracting the nodes
        node1 = curr_edge.n1
        node2 = curr_edge.n2

        # Creates the two new candidate edges
        new_edge1 = edge(node1, candidate_node)
        new_edge2 = edge(candidate_node, node2)

        # Addings the edges
        self._add_edge(new_edge1)
        self._add_edge(new_edge2)

        # Adding the node
        self._add_node(candidate_node)

        return True


    def expand_mesh(self):
        """Expands the front inwards at the given edge""" 

        for _ in range(self.iterations):
            if not self.edge_heap:
                print("Mesh Closure Achieved")
                return
        
            # Fetch the shortest edge and checks if we've visited it
            curr_edge = self.edge_heap.get_edge()
            if curr_edge in self.expanded_edges:
                continue
            self.expanded_edges.add(curr_edge)

            # Checks if the current edge is active
            if curr_edge not in self.active_edges:
                continue
            self.active_edges.remove(curr_edge)

            # Fetch the node to expand to
            candidate_node = curr_edge.get_candidate_node()
            nearest_neighbor = self.find_nearest_node(curr_edge, candidate_node)
            
            # Latch onto neighbor if within tolerance
            if (candidate_node - nearest_neighbor).get_magnitude() < self.tolerance:
                self.expand_mesh_with_node(curr_edge, nearest_neighbor)
                continue
            
            # Try the current node
            if not self.expand_mesh_with_node(curr_edge, candidate_node):

                # Latch onto neighbor if current node fails
                if not self.expand_mesh_with_node(curr_edge, nearest_neighbor):
                    print(f"Both Node and Neighbor failed, {curr_edge}, {candidate_node}, {nearest_neighbor}")

        print(f"Upper iteration limit achieved, edge_heap size: {len(self.edge_heap)}")
        
        plt.ioff()
        plt.show()

    def _add_edge(self, new_edge):
        
        if new_edge in self.active_edges:
            return self.active_edges.remove(new_edge)
        if new_edge in self.mesh.edge_set:
            print("here")
            return 
        
        self.active_edges.add(new_edge)
        self.edge_heap.add_edge(new_edge)
        self.mesh.add_edge(new_edge)

        integer_coordinates = new_edge.get_integer_buckets()
        for x, y in integer_coordinates:
            self.int_coords_to_edges[x, y].add(new_edge)

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
        