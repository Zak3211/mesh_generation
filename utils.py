import math

def get_distance(n1, n2):
    """Calculates the euclidean distance between two nodes"""

    delta_x = n1.x - n2.x
    delta_x *= delta_x

    delta_y = n1.y - n2.y
    delta_y *= delta_y

    return math.sqrt(delta_x + delta_y)

class node:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_coordinates(self):
        return (self.x, self.y)

    def get_integer_coordinates(self):
        """Returns the coordinates as integers"""
        return (int(self.x), int(self.y))
    
class edge:
    def __init__(self, n1 : node, n2 : node):
        self.n1 = n1
        self.n2 = n2
    
    def get_coordinates(self):
        return self.n1.get_coordinates(), self.n2.get_coordinates()

    def get_maginatude(self):
        """Returns the length of the edge"""
        return get_distance(self.n1, self.n2)
