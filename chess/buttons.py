class Buttons:
    def __init__(self, color, x, y, width, height, text, type, amount):
        self.color = color  # tuple - button's color
        self.x = x  # int / float - button's top left corner x
        self.y = y  # int / float - button's top left corner y
        self.width = width  # int / float - button's width
        self.height = height  # int / float - button's height
        self.text = text  # str - text displayed
        self.type = type  # time / game mode / settings
        self.amount = amount  # int / float - button's amount of time, specific to button of type time

    def Hover(self, x1, y1):  # if (x1, x2) in the parameters of self
        if self.x < x1 < self.x + self.width and \
                self.y < y1 < self.y + self.height:

            return True  # (x1, x2) is in self
        return False  # (x1, x2) is not in self


