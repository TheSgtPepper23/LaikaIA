import sys
from PyQt5 import uic
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
from internationalization import LANGUAGE
from logic import Ship, Coordinate, CardinalDirections
from attackWindow import Attack
from windows.message import Message
from winWindow import Win
from looseWindow import Loose
from agenteInteligente import Agente
import vlc
from menuWindow import Menu


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
        self.clicked = []
        self.reload_text()
        self.determine_icon_side()
        self.populate_board()
        self.agente = Agente()
        self.agente.ships = enemyShips
        self.attack = Attack(self.lang, self.username, self.enemyShips)
        for ship in self.ships:
            for coordinate, _ in ship.positions.items():
                self.player_table.item(
                    coordinate.pos_x, coordinate.pos_y).setBackground(Qt.blue)

        self.player_table.cellClicked.connect(self.player_table.clearSelection)
        self.attack_table.cellClicked.connect(self.attack_opponent)
        # self.attack_button.clicked.connect(self.attack_opponent)

    def populate_board(self):
        """Populate all the cells with Coordinate objects"""
        for row in range(10):
            for col in range(10):
                coord = Coordinate(row, col)
                coord_attack = Coordinate(row, col)
                self.player_table.setItem(row, col, coord)
                self.attack_table.setItem(row, col, coord_attack)

    '''def enable_attack(self):
        """Enable the attack button for Attack"""
        self.attack_button.setEnabled(True)'''

    def hit_coordinate(self):

        if not self.enemySons:
            self.enemySons = self.agente.hitPlayer()
        coordHit = self.enemySons.pop(0)
        self.agente.hitted.append(coordHit)
        self.player_table.item(
            coordHit.pos_x, coordHit.pos_y).setBackground(Qt.gray)
        # self.attack_button.setEnabled(True)
        for ship in self.ships:
            if ship.check_position(coordHit) == True:
                self.player_table.item(
                    coordHit.pos_x, coordHit.pos_y).setBackground(Qt.darkBlue)
                ship.hit(coordHit)
                self.enemySons = self.agente.hitPlayer(coordHit)

        if self.check_fleet() == False:
            self.lose_window = Loose(self.lang)
            self.menu = Menu(self.lang, self.username)
            self.menu.show()
            self.lose_window.show()
            self.close()

    def check_enemy_fleet(self):
        """Check the enemy survivor ships"""
        if len(self.enemyShips) > 0:
            response = False
            for ship in self.enemyShips:
                if ship.afloat == True:
                    response = True
            return response

    def attack_opponent(self):
        """Send the coordinate to Server to hit the other player"""
        coordHit = self.attack_table.item(
            self.attack_table.currentRow(), self.attack_table.currentColumn())
        if coordHit in self.clicked:
            self.attack_table.clearSelection()
            error_sound = vlc.MediaPlayer("resources/error.mp3")
            error_sound.play()
        else:
            self.attack_table.item(self.attack_table.currentRow(
            ), self.attack_table.currentColumn()).setBackground(Qt.gray)
            self.clicked.append(coordHit)
            shoot_sound = vlc.MediaPlayer("resources/shoot.mp3")
            shoot_sound.play()
            for ship in self.enemyShips:
                if ship.check_position(coordHit) == True:
                    ship.hit(coordHit)
                    self.attack_table.item(self.attack_table.currentRow(
                    ), self.attack_table.currentColumn()).setBackground(Qt.darkRed)
            if self.check_enemy_fleet() == False:
                self.menu = Menu(self.lang, self.username)
                self.menu.show()
                self.win_window = Win(self.lang)
                self.win_window.show()
                self.close()
            self.hit_coordinate()
        self.attack_table.clearSelection()

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
        self.language = LANGUAGE.get(self.lang)
        # self.attack_button.setText(self.language["attack"])

    def determine_icon_side(self):
        """Determine the icon to show from the selected previously"""
        if self.side == "empire":
            side = QPixmap("resources/empire_icon.png")
        else:
            side = QPixmap("resources/rebellion_icon.png")
        self.side_image.setPixmap(side)
