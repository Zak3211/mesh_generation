import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from utils import node, edge

class mesh:
    def __init__(self, edge_list):
        self.edge_set = set()
        for edge in edge_list:
            self.edge_set.add(edge)

    @staticmethod
    def generate_square_boundary(side_length=10, points_per_side=10):
        """
        Generates a CCW list of edges with multiple segments per side.
        
        Note that this method is AI generated (Gemini)
        """

        nodes = []
        
        # 1. Bottom side: (0,0) to (L,0)
        for i in range(points_per_side):
            nodes.append(node(i, 0))
            
        # 2. Right side: (L,0) to (L,L)
        for i in range(points_per_side):
            nodes.append(node(side_length, i))
            
        # 3. Top side: (L,L) to (0,L)
        for i in range(side_length, 0, -1):
            nodes.append(node(i, side_length))
            
        # 4. Left side: (0,L) to (0,0)
        for i in range(side_length, 0, -1):
            nodes.append(node(0, i))

        # Create edges by connecting each node to the next
        edges = []
        for i in range(len(nodes)):
            n_curr = nodes[i]
            n_next = nodes[(i + 1) % len(nodes)] # Wrap around to close the square
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
