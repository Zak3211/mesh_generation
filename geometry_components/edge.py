from geometry_components.node import node
from geometry_components.vector import vector
import math
import random

class edge:
    def __init__(self, n1 : node, n2 : node, stochasticity = 0):
        self.n1 = n1
        self.n2 = n2

        self.stochasticity = stochasticity
    
    def get_coordinates(self):
        return self.n1.get_coordinates(), self.n2.get_coordinates()

    def get_nodes(self):
        return self.n1, self.n2
    
    def get_length(self):
        """Returns the length of the edge"""
        return (self.n2 - self.n1).get_magnitude()
    
    def get_midpoint(self):
        x = (self.n1.x + self.n2.x) / 2
        y = (self.n1.y + self.n2.y) / 2
        return node(x, y)
    
    def get_candidate_node(self):
        """Gets the candidate node forming an equilateral triangle for this edge"""

        v = self.n2 - self.n1

        # Midpoint of the vector
        midpoint = self.get_midpoint()

        # Normal perpendicular vecotr
        perp = vector(-v.y, v.x)
        perp.normalize()

        # Height of equilateral triangle
        h = math.sqrt(3) / 2 * v.get_magnitude()

        return midpoint + h*perp

    def get_integer_buckets(self):
        """Gets the integer buckets of the bounding box of the edge"""
        
        # Gets the bounding box of the edge
        min_x = min(self.n1.x, self.n2.x)
        max_x = max(self.n1.x, self.n2.x)
        min_y = min(self.n1.y, self.n2.y)
        max_y = max(self.n1.y, self.n2.y)

        # Declaring loop boundaries
        start_x = math.floor(min_x)
        end_x = math.floor(max_x)
        start_y = math.floor(min_y)
        end_y = math.floor(max_y)
        
        # Populating the buckets
        buckets = []
        for x in range(start_x, end_x + 1):
            for y in range(start_y, end_y + 1):
                buckets.append((x, y))
                
        return buckets
    
    def __lt__(self, other_edge):
        """Defines the < operator between two edges"""
        return random.uniform(1, 1 + self.stochasticity)*self.get_length() < other_edge.get_length()

    def __eq__(self, other_edge):
        """Overrides the == operator, orientation invarariant"""
        if not isinstance(other_edge, edge):
            return False
        return  (self.n1 == other_edge.n1 and self.n2 == other_edge.n2) or \
                (self.n1 == other_edge.n2 and self.n2 == other_edge.n1)

    def __hash__(self):
        """Makes the edge object hashable"""
        return hash(frozenset([self.n1, self.n2]))

    def __str__(self):
        return f"{self.n1.get_coordinates()} -> {self.n2.get_coordinates()}"

    def __repr__(self):
        return f"{self.n1.get_coordinates()} -> {self.n2.get_coordinates()}"
    
    """AI Generated Code Below"""

    def intersects(self, other_edge):
        # Setup points as vectors
        p = vector(self.n1.x, self.n1.y)
        q = vector(other_edge.n1.x, other_edge.n1.y)
        
        # Direction vectors for the edges
        r = self.n2 - self.n1
        s = other_edge.n2 - other_edge.n1

        # The denominator of the intersection formula
        r_cross_s = r.cross(s)
        
        # If r_cross_s is zero, the lines are parallel or collinear
        if abs(r_cross_s) < 1e-10:
            return False

        # Vector between the start points
        q_minus_p = q - p

        # Solve for t and u:
        # t: how far along edge1 the intersection is
        # u: how far along edge2 the intersection is
        t = q_minus_p.cross(s) / r_cross_s
        u = q_minus_p.cross(r) / r_cross_s

        # CRITICAL FOR MESHING:
        # We use a small epsilon (0.01) instead of 0 and 1.
        # This prevents the algorithm from thinking that edges 
        # touching at a shared vertex are "intersecting."
        if 0.01 < t < 0.99 and 0.01 < u < 0.99:
            return True

        return False
