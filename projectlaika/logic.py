from PyQt5.QtWidgets import QTableWidgetItem, QTableWidget
import hashlib

class Coordinate(QTableWidgetItem):
    """Create a coordinate object with x and y positions.
    By default all the coordinates are available"""
    def __init__(self, pos_x, pos_y):
        QTableWidgetItem.__init__(self)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.free = True

    def __str__(self):
        return str(self.pos_x) + ", " + str(self.pos_y) + ", " + str(self.free)

    def __eq__(self, other):
        return self.pos_x == other.pos_x and self.pos_y == other.pos_y

    def __hash__(self):
        return hash((self.pos_x, self.pos_y))

class Ship:
    """Initialize the ship and specify the coordinates where it is located.
    In the positions, 1 means that the position is OK and 0 that it has been hit."""
    def __init__(self, coordinates):
        self.positions = {}
        self.afloat = True
        for coordinate in coordinates:
            self.positions[coordinate] = 1

    def check_position(self, coordinate):
        """"Check if the ship is in the coordinate entered as a parameter"""
        response = False
        for ship_coor in self.positions:
            if coordinate == ship_coor:
                response = True
        return response

    def hit(self, coordinate):
        """Mark the position of the indicated coordinate as inactive and understand 
        that there are still active positions, otherwise call a method that changes 
        the state of the ship"""
        self.positions[coordinate] = 0
        for _, state in self.positions.items():
            if state == 1:
                return
        self.destroy()

    def destroy(self):
        """Change the state of the ship from floating to sunken"""
        self.afloat = False

class Hash():
    def encrypt(text):
        return hashlib.sha256(text.encode()).hexdigest()
            