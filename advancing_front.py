from mesh import mesh

class advancing_front:

    def __init__(self, boundary):

        self.mesh = mesh()
        self.node_set = boundary.get_node_set()


    