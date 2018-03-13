import sys
from PyQt5 import uic
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
from internationalization import LANGUAGE
from logic import Coordinate


class Attack(QMainWindow):
    def __init__(self, language, username):
        QMainWindow.__init__(self)
        uic.loadUi("windows/Attack.ui", self)
        self.username = username
        self.lang = language
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

    def attack_opponent(self):
        """Send the coordinate to Server to hit the other player"""
        item = self.attack_table.itemAt(self.attack_table.currentRow(), self.attack_table.currentColumn())
        item.setBackground(Qt.blue)
        self.hide()
