import sys
from PyQt5 import uic
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
from internationalization import LANGUAGE
from logic import Coordinate
import vlc


class Attack(QMainWindow):
    def __init__(self, language, username, enemyShips):
        QMainWindow.__init__(self)
        uic.loadUi("windows/Attack.ui", self)
        self.username = username
        self.lang = language
        self.enemyShips = enemyShips
        self.clicked = []
        self.reload_text()
        self.populate_board()
        self.attack_table.cellClicked.connect(self.enable_attack)
        self.attack_button.clicked.connect(self.attack_opponent)

    def reload_text(self):
        """Change the language of the window according to the chosen previously"""
        self.language = LANGUAGE.get(self.lang)
        self.attack_button.setText(self.language["attack"])

    def populate_board(self):
        """Populate all the cells with Coordinate objects"""
        for row in range(10):
            for col in range(10):
                coord = Coordinate(row, col)
                self.attack_table.setItem(row, col, coord)

    def enable_attack(self):
        """Enable the attack button for Attack"""
        self.attack_button.setEnabled(True)

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
        coordHit = self.attack_table.item(self.attack_table.currentRow(), self.attack_table.currentColumn())
        if coordHit in self.clicked:
            self.attack_table.clearSelection()
            error_sound = vlc.MediaPlayer("resources/error.mp3")
            error_sound.play()
        else:
            self.attack_table.item(self.attack_table.currentRow(), self.attack_table.currentColumn()).setBackground(Qt.black)
            self.clicked.append(coordHit)
            for ship in self.enemyShips:
                if ship.check_position(coordHit) == True:
                    ship.hit(coordHit)
                    if self.check_enemy_fleet == False:
                        print("Ganó Laglo")
            self.hide()
