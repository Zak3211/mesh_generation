import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from geometry_components.node import node
from geometry_components.edge import edge
import math 

class mesh:
    def __init__(self, edge_list):
        self.edge_set = set()
        for edge in edge_list:
            self.edge_set.add(edge)
    
    @staticmethod
    def generate_square_boundary(side_length=10, points_per_side=11):
        """
        Generates a CCW list of edges with multiple segments per side.
        
        Note that this method is AI generated (Gemini)
        """

        nodes = []
        
        # h is the step size (e.g., 10 / 10 = 1.0)
        h = side_length / points_per_side
        
        # 1. Bottom: x goes 0 to L-h, y=0
        for i in range(points_per_side):
            nodes.append(node(i * h, 0))
            
        # 2. Right: x=L, y goes 0 to L-h
        for i in range(points_per_side):
            nodes.append(node(side_length, i * h))
            
        # 3. Top: x goes L down to h, y=L
        for i in range(points_per_side):
            nodes.append(node(side_length - (i * h), side_length))
            
        # 4. Left: x=0, y goes L down to h
        for i in range(points_per_side):
            nodes.append(node(0, side_length - (i * h)))

        edges = []
        for i in range(len(nodes)):
            n_curr = nodes[i]
            n_next = nodes[(i + 1) % len(nodes)]
            edges.append(edge(n_curr, n_next))
        
        return edges

    @staticmethod
    def generate_circle_boundary(radius=5, segments=30):
        """
        Generates a CCW approximation of a circle.
        Ensure segments is high (30-50) for smoothness.
        """
        nodes = []
        
        for i in range(segments):
            # We need to explicitly avoid range(segments + 1)
            # to ensure the last segment connects back to the first node,
            # rather than placing two nodes at the exact same coordinate.
            theta = (2.0 * math.pi * i) / segments
            # Vector winding logic: Cos/Sin is standard CCW
            x = radius * math.cos(theta)
            y = radius * math.sin(theta)
            # Assuming you center the circle at (0,0)
            nodes.append(node(x, y))

        edges = []
        for i in range(len(nodes)):
            n_curr = nodes[i]
            n_next = nodes[(i + 1) % len(nodes)]
            edges.append(edge(n_curr, n_next))
        
        return edges
    @staticmethod
    def generate_triangle_boundary(side_length=10, points_per_side=10):
        """
        Generates a simple CCW equilateral triangle.
        """
        nodes = []
        
        # Vertex A: (0, 0)
        # Vertex B: (L, 0)
        # Vertex C: (L/2, L * sqrt(3)/2)
        h_step = side_length / points_per_side
        tri_height = side_length * math.sqrt(3) / 2.0
        
        # 1. Bottom: (0,0) -> (L,0)
        for i in range(points_per_side):
            nodes.append(node(i * h_step, 0))
            
        # 2. Right Diagonal: (L,0) -> (L/2, Height)
        for i in range(points_per_side):
            t = i / points_per_side # Interpolation factor 0 -> 1
            x = side_length * (1 - t) + (side_length / 2) * t
            y = tri_height * t
            nodes.append(node(x, y))
            
        # 3. Left Diagonal: (L/2, Height) -> (0,0)
        for i in range(points_per_side):
            t = i / points_per_side
            x = (side_length / 2) * (1 - t)
            y = tri_height * (1 - t)
            nodes.append(node(x, y))

        edges = []
        for i in range(len(nodes)):
            n_curr = nodes[i]
            n_next = nodes[(i + 1) % len(nodes)]
            edges.append(edge(n_curr, n_next))
        
        return edges
    
    @staticmethod
    def generate_lshape_boundary(side_length=10, points_per_side=10):
        """
        Generates a simple CCW L-shape polygon.
        Testing the 90° concave corner.
        """
        nodes = []
        # Using 1/2 of side_length for the cut-out
        mid = side_length / 2.0
        
        # Loop setup: Outer loop (0->10), Inner notch (5,5)
        # Must be consistently CCW.
        for x in range(0, int(mid)): nodes.append(node(x, 0)) # Bottom-Left
        for x in range(int(mid), side_length): nodes.append(node(x, 0)) # Bottom-Right
        for y in range(0, int(mid)): nodes.append(node(side_length, y)) # Right-Bottom
        
        # THE INNER CORNER:
        for x in range(side_length, int(mid), -1): nodes.append(node(x, mid))
        for y in range(int(mid), side_length): nodes.append(node(mid, y))
        
        # THE OUTER WALLS:
        for x in range(int(mid), 0, -1): nodes.append(node(x, side_length))
        for y in range(side_length, 0, -1): nodes.append(node(0, y))

        edges = []
        for i in range(len(nodes)):
            n_curr = nodes[i]
            n_next = nodes[(i + 1) % len(nodes)]
            edges.append(edge(n_curr, n_next))
        
        return edges
    def plot(self, title="Mesh Visualization"):
        """
        Plots the current edges in the mesh.
        
        This method is AI generated (Gemini)
        """
        fig, ax = plt.subplots(figsize=(8, 8))
        
        # Prepare the line segments for fast plotting
        lines = []
        for e in self.edge_set:
            (x1, y1), (x2, y2) = e.get_coordinates()
            lines.append([(x1, y1), (x2, y2)])

        lc = LineCollection(lines, colors='blue', linewidths=1)
        ax.add_collection(lc)
        
        ax.autoscale()
        ax.set_aspect('equal')
        plt.title(title)
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.show()
