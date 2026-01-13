from enum import Enum
from math import *

class CoordinateSystem(Enum):
    CARTESIAN = 1
    POLAR = 2

class Point:
    def __init__(self, a, b, system=CoordinateSystem.CARTESIAN):
        if system == CoordinateSystem.CARTESIAN:
            self.x = a
            self.y = b
        elif system == CoordinateSystem.POLAR:
            self.x = a * cos(b)
            self.y = a * sin(b)
        else:
            raise ValueError("Unknown coordinate system")
        
    @staticmethod
    def from_cartesian(x, y):
        return Point(x, y, CoordinateSystem.CARTESIAN)
    
    @staticmethod
    def from_polar(rho, theta):
        return Point(rho, theta, CoordinateSystem.POLAR)