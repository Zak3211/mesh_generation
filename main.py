from mesh import mesh
from advancing_front import advancing_front

def main():

    # 1. Setup the boundary
    boundary_edges = mesh.generate_square_boundary()

    # 2. Initialize the Advancing Front
    front = advancing_front(boundary_edges)

    # 3. Expansion Loop
    # For a square of 10x10, we might need ~100-150 triangles to fill it
    # depending on your candidate node logic.
    max_iterations = 290
    for i in range(max_iterations):
        if not front.edge_heap:
            print("Front closed successfully!")
            break
        try:
            front.expand_mesh()
        except Exception as e:
            print(f"Stopping expansion: {e}")
            break

    # 4. Plot the result
    front.mesh.plot(title=f"Mesh after {i+1} iterations")

if __name__ == "__main__":
    main()