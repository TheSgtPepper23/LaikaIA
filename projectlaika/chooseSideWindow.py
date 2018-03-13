import sys
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5 import uic
from internationalization import LANGUAGE
from storyWindow import Story

class ChooseSide(QMainWindow):
    def __init__(self, language, username):
        QMainWindow.__init__(self)
        uic.loadUi("windows/ChooseSide.ui", self)
        self.side = ""
        self.lang = language
        self.username = username
        self.reload_text()

        self.empire_button.setIcon(QIcon("resources/empire.jpg"))
        self.empire_button.setIconSize(QSize(340, 400))
        self.empire_button.clicked.connect(self.select_empire)

        self.rebellion_button.setIcon(QIcon("resources/rebellion.jpg"))
        self.rebellion_button.setIconSize(QSize(340, 400))
        self.rebellion_button.clicked.connect(self.select_rebellion)

        self.play_button.clicked.connect(self.go_to_story)

    def reload_text(self):
        """Change the language of the window according to the chosen previously"""
        self.language = LANGUAGE.get(self.lang)
        self.choose_label.setText(self.language["choose"])
        self.play_button.setText(self.language["play"])
        self.setWindowTitle(self.language["choose"])

    def go_to_story(self):
        """Go to story window and send a signal to other player to continue"""
        self.story_window = Story(self.lang, self.side, self.username)
        self.story_window.show()
        self.close()

    def select_empire(self):
        """Change the color of the empire button when it's selected"""
        self.side = "empire"
        self.empire_button.setIcon(QIcon("resources/empire_selected.jpg"))
        self.rebellion_button.setIcon(QIcon("resources/rebellion.jpg"))
        self.play_button.setEnabled(True)

    def select_rebellion(self):
        """Change the color of the rebellion button when it's selected"""
        self.side = "rebellion"
        self.rebellion_button.setIcon(QIcon("resources/rebellion_selected.jpg"))
        self.empire_button.setIcon(QIcon("resources/empire.jpg"))
        self.play_button.setEnabled(True)
