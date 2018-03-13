import sys
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5 import uic
from internationalization import LANGUAGE

class Loose(QMainWindow):
    def __init__(self, lang):
        QMainWindow.__init__(self)
        uic.loadUi("windows/Looser.ui", self)
        self.lang = lang
        self.reload_text()
        self.loser = QPixmap("resources/loser.png")
        self.lose_button.clicked.connect(self.end_game)
        self.lose_image.setPixmap(self.loser)

    def reload_text(self):
        """Change the language of the window according to the chosen previously"""
        self.language=LANGUAGE.get(self.lang)
        self.setWindowTitle(self.language["lose_title"])
        self.lose_label.setText(self.language["lose_text"])
        self.lose_button.setText(self.language["return_to_menu"])

    def end_game(self):
        self.close()