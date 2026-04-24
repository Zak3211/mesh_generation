import math

class node:
    """Defines a point in R^2"""

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_coordinates(self):
        return (self.x, self.y)

    def get_integer_coordinates(self):
        """Returns the coordinates as integers"""
        return (int(self.x), int(self.y))
    
    def __sub__(self, other_node):
        """Overrides the - operator, returns the vector other_node - self_node"""
        x = other_node.x - self.x 
        y = other_node.y - self.y 
        return vector(x, y)
    
    def __add__(self, vector):
        """Returns a new node translate by the vector"""
        return node(self.x + vector.x, self.y + vector.y)
    

class vector:
    """Defines a 2D vector"""

    def __init__(self, x, y):
        self.x = x 
        self.y = y 

    def rotate_counterclockwise(self, theta):

        s_theta = math.sin(theta) # sin(theta)
        c_theta = math.cos(theta) # cos(theta)

        new_x = self.x*c_theta - self.y*s_theta
        new_y = self.x*s_theta + self.y*c_theta

        self.x, self.y = x, y
    
    def get_magnitutude(self):
        return math.sqrt(self.x * self.x + self.y * self.y)

class edge:
    
    def __init__(self, n1 : node, n2 : node):
        self.n1 = n1
        self.n2 = n2
    
    def get_coordinates(self):
        return self.n1.get_coordinates(), self.n2.get_coordinates()

    def get_length(self):
        """Returns the length of the edge"""
        return (self.n2 - self.n1).get_magnitutude()
    
    def get_candidate_node(self):
        """Gets the candidate node forming an equilateral triangle for this edge"""

        edge_vector = self.n2 - self.n1
        edge_vector.rotate_counterclockwise(theta=math.pi/3)
        candidate_node = self.n1 + edge_vector
        return candidate_node

    def __lt__(self, other_edge):
        """Defines the < operator between two edges"""
        return self.get_length() < other_edge.get_length()
