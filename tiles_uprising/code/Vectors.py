class Vector2D:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):

        if type(other) == Vector2D:
            return Vector2D(self.x + other.x, self.y + other.y)

        elif type(other) == tuple:
            return Vector2D(self.x + other[0], self.y + other[1])

        elif type(other) == int or type(other) == float:
            return Vector2D(self.x + other, self.y + other)

    def __mul__(self, other):

        if type(other) == Vector2D:
            return Vector2D(self.x * other.x, self.y * other.y)

        elif type(other) == tuple:
            return Vector2D(self.x * other[0], self.y * other[1])

        elif type(other) == int or type(other) == float:
            return Vector2D(self.x * other, self.y * other)

    def __le__(self, other):

        if type(other) == Vector2D:
            return self.x < other.x and self.y < other.y

        if type(other) == tuple:
            return self.x < other[0] and self.y < other[1]

        if type(other) == int or type(other) == float:
            return self.x < other and self.y < other

    def __call__(self):
        return self.x, self.y

    def __str__(self):
        return f"{self.x}, {self.y}"

