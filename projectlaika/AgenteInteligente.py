from logic import Coordinate, Ship
import random

class Agente:
    def __init__(self, name, turn):
        self.name = name
        self.turn = turn
        self.ships = []
        self.occupied = []
        self.board = IA_Board()
        self.upright = False

    def setShips():
        print("Se encarga de colocar los barcos utilizando todos los métodos que se encuentran abajo")

    def random_cell(self):
        pos_x = random.randint(0, 9)
        pos_y = random.randint(0, 9)
        if pos_x == pos_y:
            self.upright = not self.upright
        return Coordinate(pos_x, pos_y)

    def boundaries(self, row, col, width, height = 1):
        """Checks that the selected cells do not leave the boundaries of the board."""
        if self.upright == True:
            if row + width <= 10 and col + height <= 10:
                return True
            else:
                return False
        elif self.upright == False:
            if col + width <= 10 and row + height <= 10:
                return True
            else:
                return False

    def avalaible_cells(self, cells):
        """Verify that the selected cells are not occupied."""
        response = True
        for cell in cells:
            if cell in self.occupied:
                response =  False

        return response
            

    def place_ship(self, cells):
        for cell in cells:
            self.occupied.append(cell)
        ship = Ship(cells)
        ships.append(ship)
    
    def place_52(self, row, col):
        """Print the 5x2 ship on the board based on the upright variable."""
        coordinates = []
        if self.boundaries (row, col, 5, 2):
            if self.upright == False:
                for x in range(5):
                    for y in range(2):
                        coordinates.append(Coordinate(row + y, col + x))
            else:
                for x in range(2):
                    for y in range(5):
                        coordinates.append(Coordinate(row + y, col + x))

            if self.avalaible_cells(coordinates) == True:
                self.place_ship(coordinates)

    def place_41(self, row, col):
        """Print the 4x1 ship on the board based on the upright variable."""
        coordinates = []
        if self.boundaries(row, col, 4):
            if self.upright == False:
                for i in range(4):
                    coordinates.append(Coordinate(row, col + i))
            else:
                for i in range(4):
                    coordinates.append(Coordinate(row + i, col))

            if self.avalaible_cells(coordinates) == True:
                self.place_ship(coordinates)

    def place_31(self, row, col):
        """Print the 3x1 ship on the board based on the upright variable."""
        coordinates = []
        if self.boundaries(row, col, 3):
            if self.upright == False:
                for i in range(3):
                    coordinates.append(Coordinate(row, col + i))
            else:
                for i in range(3):
                    coordinates.append(Coordinate(row + i, col))
            if self.avalaible_cells(coordinates) == True:
                self.place_ship(coordinates)

    def place_33(self, row, col):
        """Print the 3x3 ship on the board."""
        coordinates = []
        if self.boundaries(row, col, 3, 3):
            for x in range(3):
                for y in range(3):
                    coordinates.append(Coordinate(row + y, col + x))
            if self.avalaible_cells(coordinates) == True:
                self.add_ships(coordinates)

    def place_11(self, row, col):
        """Print the 1x1 ship on the board."""
        coordinates = []
        coordinates.append(Coordinate(row, col))
        if self.avalaible_cells(coordinates) == True:
            self.add_ships(coordinates)
        