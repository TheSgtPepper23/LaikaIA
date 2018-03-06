import sys
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5 import uic
from internationalization import LANGUAGE
from menuWindow import Menu

class Win(QMainWindow):
    def __init__(self, lang):
        QMainWindow.__init__(self)
        uic.loadUi("windows/Winner.ui", self)
        self.lang = lang
        self.reload_text()
        self.winner = QPixmap("resources/winner.png")
        self.win_image.setPixmap(self.winner)
        self.win_button.clicked.connect(self.end_game)
        self.show()

    def reload_text(self):
        """Change the language of the window according to the chosen previously"""
        self.language=LANGUAGE.get(self.lang)
        self.setWindowTitle(self.language["win_title"])
        self.win_label.setText(self.language["win_text"])
        self.win_button.setText(self.language["return_to_menu"])

    def end_game(self):
        self.close()
