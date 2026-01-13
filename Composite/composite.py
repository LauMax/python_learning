class GraphicObject:
    def __init__(self, color=None):
        self.color = color
        self.children = []
        self._name = "Group" 

    @property
    def name(self):
        return self._name
    
    def _print(self, items, depth):
        items.append('*' * depth)
        if self.color:
            items.append(f"{self.color} ")
        items.append(f"{self.name}\n")
        for child in self.children:
            child._print(items, depth + 1)


    def __str__(self):
        items = []
        self._print(items, 0)
        return ''.join(items)
    
class Circle(GraphicObject):
    def __init__(self, color):
        super().__init__(color)
        self._name = "Circle"
    
    @property
    def name(self):
        return self._name
    
class Square(GraphicObject):
    def __init__(self, color):
        super().__init__(color)
        self._name = "Square"
    
    @property
    def name(self):
        return self._name
    

if __name__ == "__main__":
    drawing = GraphicObject()
    drawing._name = "My Drawing"
    drawing.children.append(Square("Red"))
    drawing.children.append(Circle("Yellow"))

    group = GraphicObject()
    group._name = "Group 1"
    group.children.append(Circle("Blue"))
    group.children.append(Square("Blue"))

    drawing.children.append(group)

    print(drawing)
