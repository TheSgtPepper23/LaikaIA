from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow
from logic import Coordinate, Ship
from internationalization import LANGUAGE
import vlc
import time

class SetShips(QMainWindow):

    def __init__(self, lang, side, username):
        QMainWindow.__init__(self)
        uic.loadUi("windows/SetShips.ui", self)
        self.username = username
        self.lang = lang
        self.side = side
        self.upright = False
        self.ships = []
        self.enemyShips = []
        self.reload_text()
        self.populate_board()
        self.ready_button.setEnabled(False)
        self.error_sound = vlc.MediaPlayer("resources/error.mp3")

        self.rotate_button.clicked.connect(self.rotate)
        self.clear_button.clicked.connect(self.clear_board)
        self.board.cellClicked.connect(self.select_cells)
        self.ready_button.clicked.connect(self.go_to_play)

    def reload_text(self):
        """Change the language of the window according to the chosen previously"""
        self.language = LANGUAGE.get(self.lang)
        self.setWindowTitle(self.language["set_ships"])
        self.shipsGroup.setTitle(self.language["ships"])
        self.rotate_button.setText(self.language["rotate"])
        self.clear_button.setText(self.language["clear_button"])
        self.ready_button.setText(self.language["ready"])

    def populate_board(self):
        """Populate all the cells with Coordinate objects"""
        for row in range(10):
            for col in range(10):
                coord = Coordinate(row, col)
                self.board.setItem(row, col, coord)

    def rotate(self):
        """Changes the value of the boolean variable 'upright'"""
        self.language = LANGUAGE.get(self.lang)
        self.upright = not self.upright
        if self.upright == True:
            self.rotation.setText(self.language["upright"])
        else:
            self.rotation.setText(self.language["horizontal"])

    def clear_board(self):
        """Enable all cells and mark them as available."""
        self.ships.clear()
        for row in range(10):
            for col in range(10):
                item = self.board.item(row, col)
                item.free = True
                item.setBackground(Qt.white)
        self.ship_52.setAutoExclusive(True)
        self.ship_52.setEnabled(True)
        self.ship_33.setEnabled(True)
        self.ship_33.setAutoExclusive(True)
        self.ship_41.setEnabled(True)
        self.ship_41.setAutoExclusive(True)
        self.ship_31.setEnabled(True)
        self.ship_31.setAutoExclusive(True)
        self.ship_11.setEnabled(True)
        self.ship_11.setAutoExclusive(True)
        self.board.clearSelection()

    def deselect_sizes(self):
        """Mark al the ship buttons as unchecked."""
        self.ship_52.setChecked(False)
        self.ship_41.setChecked(False)
        self.ship_33.setChecked(False)
        self.ship_11.setChecked(False)
        self.ship_31.setChecked(False)

    def add_ships(self, coordinates):
        """add the ship selected to the list of ships"""
        self.ship = Ship(coordinates)
        self.ships.append(self.ship)

    def ships_ready(self):
        """enable the Ready button when the five ships is positionated"""
        if len(self.ships) == 5:
            self.ready_button.setEnabled(True)

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
        for cell in cells:
            if cell.free != True:
                return False
        return True

    def place_52(self, row, col):
        """Print the 5x2 ship on the board based on the upright variable."""
        if self.boundaries (row, col, 5, 2):
            if self.upright == False:
                for x in range(5):
                    for y in range(2):
                        self.board.setCurrentCell(row + y, col + x)
            else:
                for x in range(2):
                    for y in range(5):
                        self.board.setCurrentCell(row + y, col + x)

            if self.avalaible_cells(self.board.selectedItems()) == True:
                self.ship_52.setAutoExclusive(False)
                self.ship_52.setEnabled(False)
                self.deselect_sizes()
                self.add_ships(self.board.selectedItems())
                place_sound = vlc.MediaPlayer("resources/place.mp3")
                place_sound.play()
            else:
                self.board.clearSelection()
                error_sound = vlc.MediaPlayer("resources/error.mp3")
                error_sound.play()
        else:
            error_sound = vlc.MediaPlayer("resources/error.mp3")
            error_sound.play()

    def place_41(self, row, col):
        """Print the 4x1 ship on the board based on the upright variable."""
        if self.boundaries(row, col, 4):
            if self.upright == False:
                for i in range(4):
                    self.board.setCurrentCell(row, col + i)
            else:
                for i in range(4):
                    self.board.setCurrentCell(row + i, col)
            if self.avalaible_cells(self.board.selectedItems()) == True:
                self.ship_41.setAutoExclusive(False)
                self.ship_41.setEnabled(False)
                self.deselect_sizes()
                self.add_ships(self.board.selectedItems())
                place_sound = vlc.MediaPlayer("resources/place.mp3")
                place_sound.play()
            else:
                self.board.clearSelection()
                error_sound = vlc.MediaPlayer("resources/error.mp3")
                error_sound.play()
        else:
            error_sound = vlc.MediaPlayer("resources/error.mp3")
            error_sound.play()

    def place_31(self, row, col):
        """Print the 3x1 ship on the board based on the upright variable."""
        if self.boundaries(row, col, 3):
            if self.upright == False:
                for i in range(3):
                    self.board.setCurrentCell(row, col + i)
            else:
                for i in range(3):
                    self.board.setCurrentCell(row + i, col)
            if self.avalaible_cells(self.board.selectedItems()) == True:
                self.ship_31.setAutoExclusive(False)
                self.ship_31.setEnabled(False)
                self.deselect_sizes()
                self.add_ships(self.board.selectedItems())
                place_sound = vlc.MediaPlayer("resources/place.mp3")
                place_sound.play()
            else:
                self.board.clearSelection()
                error_sound = vlc.MediaPlayer("resources/error.mp3")
                error_sound.play()
        else:
            error_sound = vlc.MediaPlayer("resources/error.mp3")
            error_sound.play()

    def place_33(self, row, col):
        """Print the 3x3 ship on the board."""
        if self.boundaries(row, col, 3, 3):
            for x in range(3):
                for y in range(3):
                    self.board.setCurrentCell(row + y, col + x)
            if self.avalaible_cells(self.board.selectedItems()) == True:
                self.ship_33.setAutoExclusive(False)
                self.ship_33.setEnabled(False)
                self.deselect_sizes()
                self.add_ships(self.board.selectedItems())
                place_sound = vlc.MediaPlayer("resources/place.mp3")
                place_sound.play()
            else:
                self.board.clearSelection()
                error_sound = vlc.MediaPlayer("resources/error.mp3")
                error_sound.play()
        else:
            error_sound = vlc.MediaPlayer("resources/error.mp3")
            error_sound.play()

    def place_11(self, row, col):
        """Print the 1x1 ship on the board."""
        self.board.setCurrentCell(row, col)
        if self.avalaible_cells(self.board.selectedItems()) == True:
            self.ship_11.setAutoExclusive(False)
            self.ship_11.setEnabled(False)
            self.deselect_sizes()
            self.add_ships(self.board.selectedItems())
            place_sound = vlc.MediaPlayer("resources/place.mp3")
            place_sound.play()
        else:
            self.board.clearSelection()
            error_sound = vlc.MediaPlayer("resources/error.mp3")
            error_sound.play()

    def select_cells(self, row, col):
        """It's called when a cell is clicked on the board."""
        self.board.clearSelection()
        if self.ship_52.isChecked():
            self.place_52(row, col)
        elif self.ship_41.isChecked():
            self.place_41(row, col)
        elif self.ship_31.isChecked():
            self.place_31(row, col)
        elif self.ship_33.isChecked():
            self.place_33(row, col)
        elif self.ship_11.isChecked():
            self.place_11(row, col)
        else:
            return

        items = self.board.selectedItems()
        self.ships_ready()
        for item in items:
            item.free = False
            item.setBackground(Qt.red)

    def go_to_play(self):
        """send a signal to the other player to pass to the next window"""
        from gameWindow import Game
        from agenteInteligente import Agente
        enemy = Agente()
        self.enemyShips = enemy.setShips()
        self.game_window = Game(self.lang, self.side, self.ships, self.username, self.enemyShips)
        self.game_window.show()
        self.close()
