class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Point({self.x}, {self.y})"
    
    def draw_point(self):
        print(f"Drawing point at ({self.x}, {self.y})")

# ^^ you are given this code ^^

class Line:
    def __init__(self, start: Point, end: Point):
        self.start = start
        self.end = end

    def __repr__(self):
        return f"Line({self.start}, {self.end})"
    
    def draw_line(self):
        print(f"Drawing line from ({self.start.x}, {self.start.y}) to ({self.end.x}, {self.end.y})")

class Rectangle(list):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.append(Line(Point(x, y), Point(x + width, y)))               # Top edge
        self.append(Line(Point(x + width, y), Point(x + width, y + height))) # Right edge
        self.append(Line(Point(x + width, y + height), Point(x, y + height))) # Bottom edge
        self.append(Line(Point(x, y + height), Point(x, y)))               # Left edge

class LineToPointAdapter(list):
    count = 0

    def __init__(self, line):
        super().__init__()
        self.line = line
        LineToPointAdapter.count += 1
        print(f"{LineToPointAdapter.count}: Generating points for line")

        left = min(self.line.start.x, self.line.end.x)
        right = max(self.line.start.x, self.line.end.x)
        top = min(self.line.start.y, self.line.end.y)
        bottom = max(self.line.start.y, self.line.end.y)

        if right - left == 0:  # vertical line
            for y in range(top, bottom + 1):
                self.append(Point(left, y))
        elif bottom - top == 0:  # horizontal line
            for x in range(left, right + 1):
                self.append(Point(x, top))

def draw(rcs):
    for rc in rcs:
        for line in rc:
            adapter = LineToPointAdapter(line)
            for p in adapter:
                p.draw_point()


if __name__ == "__main__":
    rs = [
        Rectangle(1, 1, 10, 10),
        Rectangle(20, 20, 100, 100)
    ]
    draw(rs)    