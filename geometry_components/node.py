from geometry_components.vector import vector

class node:
    """Defines a point in R^2"""

    def __init__(self, x, y, precision = 10):
        
        # Number of decimal places to round to
        self.precision = precision

        # Node coordinates
        self.x = round(x, self.precision)
        self.y = round(y, self.precision)

    def get_coordinates(self):
        return (self.x, self.y)

    def get_integer_coordinates(self):
        """Returns the coordinates as integers"""
        return (int(self.x), int(self.y))
    
    def __sub__(self, other_node):
        """Overrides the - operator, returns the vector other_node - self_node"""
        x = self.x - other_node.x 
        y = self.y - other_node.y
        return vector(x, y)
    
    def __add__(self, vector):
        """Returns a new node translate by the vector"""
        return node(self.x + vector.x, self.y + vector.y)

    def __eq__(self, other_node):
        """Overrides the == operator"""
        return self.x == other_node.x and self.y == other_node.y

    def __hash__(self):
        """Makes the node hashable"""
        return hash((self.x, self.y))

    def __str__(self):
        return f"{(self.x, self.y)}"