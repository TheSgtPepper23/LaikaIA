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

class Game(QMainWindow):
    def __init__(self, language, side, ships, username):
        QMainWindow.__init__(self)
        uic.loadUi("windows/Game.ui", self)
        self.username = username
        self.lang = language
        self.side = side
        self.ships = ships
        self.reload_text()
        self.determine_icon_side()
        self.populate_board()
        for ship in self.ships:
            for coordinate, _ in ship.positions.items():
                self.player_table.item(coordinate.pos_x, coordinate.pos_y).setBackground(Qt.blue)

        if self.side == "rebellion":
            self.attack_button.setEnabled(True)

        self.attack_button.clicked.connect(self.show_rival_table)

    def populate_board(self):
        """Populate all the cells with Coordinate objects"""
        for row in range(10):
            for col in range(10):
                coord = Coordinate(row, col)
                self.player_table.setItem(row, col, coord)

    def hit_coordinate(self, hit_info):
        """Receive a signal from the server and hit a coordinate of the player_table"""
        self.player_table.clearSelection()
        self.attack_button.setEnabled(True)
        hit_info = json.loads(hit_info)
        x, y = hit_info["coordinate"]
        coordinate = Coordinate(x, y)
        self.player_table.item(coordinate.pos_x, coordinate.pos_y).setBackground(Qt.red)
        for ship in self.ships:
            if ship.check_position(coordinate) == True:
                ship.hit(coordinate)

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
            self.client.set_winner(json.dumps(self.username))
            self.close()
        else:
            self.attack_button.setEnabled(False)
            self.attack = Attack(self.lang, self.username, self.server, self.ip_address)
            self.attack.show()

    def message_winner(self):
        """Shows the winner message"""
        self.win_window.show()
        self.close()
