from geometry_components.edge import edge
from geometry_components.node import node
from mesh import mesh
from advancing_front import advancing_front

def construct_boundary(coords_list):

    node_list = []
    for x, y in coords_list:
        node_list.append(node(x, y))
    
    edge_list = []
    for i in range(len(node_list)):
        node1 = node_list[i-1]
        node2 = node_list[i]

        edge_list.append(edge(node1, node2))
    
    return edge_list
def main():

    # 1. Setup the boundary
    boundary_edges = construct_boundary([
        (0.804, 0.473),
        (0.624, 0.765),
        (0.279, 0.784),
        (0.117, 0.596),
        (0.192, 0.242),
        (0.447, 0.213),
        (0.699, 0.229)
        ]
    )

    #boundary_edges = mesh.generate_square_boundary()

    #boundary_edges = mesh.generate_square_boundary()

    # 2. Initialize the Advancing Front
    front = advancing_front(boundary_edges, tolerance=0.5, iterations=1000)

    front.expand_mesh()
    
    # 4. Plot the result
    #front.mesh.plot(title=f"Mesh after closure")

if __name__ == "__main__":
    main()