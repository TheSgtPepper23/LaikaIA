import sys
from PyQt5 import uic
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
from internationalization import LANGUAGE
from logic import Ship, Coordinate
from attackWindow import Attack
from windows.message import Message
from winWindow import Win
from looseWindow import Loose
from agenteInteligente import Agente

class Game(QMainWindow):
    def __init__(self, language, side, ships, username, enemyShips):
        QMainWindow.__init__(self)
        uic.loadUi("windows/Game.ui", self)
        self.username = username
        self.lang = language
        self.side = side
        self.ships = ships
        self.enemyShips = enemyShips
        self.enemySons = []
        self.reload_text()
        self.determine_icon_side()
        self.populate_board()
        self.agente = Agente()
        self.agente.ships = enemyShips
        self.attack = Attack(self.lang, self.username, self.enemyShips)
        for ship in self.ships:
            for coordinate, _ in ship.positions.items():
                self.player_table.item(coordinate.pos_x, coordinate.pos_y).setBackground(Qt.blue)
        self.attack_button.setEnabled(True);
        self.attack_button.clicked.connect(self.show_rival_table)
        self.player_table.cellClicked.connect(self.player_table.clearSelection)

    def populate_board(self):
        """Populate all the cells with Coordinate objects"""
        for row in range(10):
            for col in range(10):
                coord = Coordinate(row, col)
                self.player_table.setItem(row, col, coord)

    def hit_coordinate(self):
        """Receive a signal from the server and hit a coordinate of the player_table"""
        if not self.enemySons:
            self.enemySons = self.agente.hitPlayer()
        coordHit = self.enemySons.pop(0)
        self.player_table.item(coordHit.pos_x, coordHit.pos_y).setBackground(Qt.red)
        self.attack_button.setEnabled(True)
        for ship in self.ships:
            if ship.check_position(coordHit) == True:
                ship.hit(coordHit)

    def check_fleet(self):
        """Check that there are still surviving ships"""
        if len(self.ships) > 0:
            response = False
            for ship in self.ships:
                if ship.afloat == True:
                    response = True
            return response

    def reload_text(self):
        """Change the language of the window according to the chosen previously"""
        self.language = LANGUAGE.get(self.lang)
        self.setWindowTitle(self.language["game"])

    def determine_icon_side(self):
        """Determine the icon to show from the selected previously"""
        if self.side == "empire":
            side = QPixmap("resources/empire_icon.png")
        else:
            side = QPixmap("resources/rebellion_icon.png")
        self.side_image.setPixmap(side)

    def show_rival_table(self):
        """Show the rival's table and their shots so far or determine the game winner"""
        if self.check_fleet() == False:
            self.lose_window = Loose(self.lang)
            self.lose_window.show()
        else:
            self.hit_coordinate()
            self.attack.show()
