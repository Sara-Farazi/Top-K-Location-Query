__author__="Sara Farazi"

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Coordinates:
    def __init__(self, upper_right, upper_left, lower_right, lower_left):
        self.upper_right = upper_right
        self.upper_left = upper_left
        self.lower_right = lower_right
        self.lower_left = lower_left


class Cell:
    def __init__(self, id, coordinates):
        self.id = id
        self.coordinates = coordinates



    def is_in_cell(self, point):
        if point.y > self.lower_left.y and point.y < self.upper_left.y:
            if point.x > self.upper_left.x and point.x < self.upper_right.x:
                return True

        return False




