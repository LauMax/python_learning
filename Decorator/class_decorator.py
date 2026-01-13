from abc import ABC

class shape(ABC):
    def __str__(self):
        return ''
    
class Circle(shape):
    def __init__(self, radius):
        super().__init__()
        self.radius = radius

    def resize(self, factor):
        self.radius *= factor
    def __str__(self):
        return f'Circle with radius {self.radius}'
    
class Square(shape):
    def __init__(self, side):
        super().__init__()
        self.side = side

    def resize(self, factor):
        self.side *= factor
    def __str__(self):
        return f'Square with side {self.side}'
    
class ColoredShape(shape):
    def __init__(self, shape: shape, color: str):
        super().__init__()
        self.shape = shape
        self.color = color

    def __str__(self):
        return f'{self.shape} has the color {self.color}'
    

class TransparentShape(shape):
    def __init__(self, shape: shape, transparency: float):
        super().__init__()
        self.shape = shape
        self.transparency = transparency

    def __str__(self):
        return f'{self.shape} has {self.transparency * 100}% transparency'
    
if __name__ == "__main__":
    circle = Circle(5)
    print(circle)

    red_circle = ColoredShape(circle, "red")
    red_half_transparent_circle = TransparentShape(red_circle, 0.5)
    print(red_half_transparent_circle)

    square = Square(4)
    blue_square = ColoredShape(square, "blue")
    print(blue_square)