import math

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
        self.x, self.y = new_x, new_y
    
    def normalize(self):
        magnitude = self.get_magnitude()
        if magnitude == 0:
            return False
        self.x /= magnitude
        self.y /= magnitude
        return True

    def cross(self, other):
        """2D Cross Product (perp-dot product)"""
        return self.x * other.y - self.y * other.x
    
    def get_magnitude(self):
        return math.sqrt(self.x * self.x + self.y * self.y)

    def get_perpindicular(self):
        return vector(-self.y, self.x)
    
    def __str__(self):
        return f"Vector: {(self.x, self.y)}"
    
    def __sub__(self, other):
        return vector(self.x - other.x, self.y - other.y)

    def __rmul__(self, scalar):
        return vector(scalar*self.x, scalar*self.y)
    