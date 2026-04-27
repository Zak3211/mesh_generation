class mesh:
    def __init__(self, edge_list):
        self.edge_set = set()
        for edge in edge_list:
            self.edge_set.add(edge)
