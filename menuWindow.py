import sys
import vlc
import json
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QPixmap
from PyQt5 import uic
from internationalization import LANGUAGE

class Menu(QMainWindow):
    def __init__(self, lang, username):
        QMainWindow.__init__(self)
        uic.loadUi("windows/Menu.ui", self)
        self.lang = lang
        self.reload_text()
        self.username = username

        death_star_image = QPixmap("resources/death_star.png")
        self.image.setPixmap(death_star_image)

        self.cantina_song = vlc.MediaPlayer("resources/cantina.mp3")
        self.cantina_song.play()

        self.play_button.clicked.connect(self.go_to_play)
        self.leaderboards_button.clicked.connect(self.open_leaderboards)
        self.exit_button.clicked.connect(self.close_game)

    def showEvent(self, event):
        """Play the game song when the window appears
        This is an override method"""
        self.cantina_song.play()

    def closeEvent(self, event):
        """Stop the game song when the window close
        This is an override method"""
        self.cantina_song.stop()

    def go_to_play(self):
        """Go to create lobby window"""
        from chooseSideWindow import ChooseSide
        self.choose = ChooseSide(self.lang, self.username)
        self.choose.show()
        self.close()

    def open_leaderboards(self):
        """Show the leaderboards window"""
        from leaderboardsWindow import Leaderboards
        self.leader = Leaderboards(self.lang)
        self.leader.show()

    def reload_text(self):
        """Change the language of the window according to the chosen previously"""
        self.language = LANGUAGE.get(self.lang)
        self.leaderboards_button.setText(self.language["leaderboards"])
        self.exit_button.setText(self.language["exit"])
        self.setWindowTitle(self.language["menu"])
        self.play_button.setText(self.language["play"])

    def close_game(self):
        """Close the game window"""
        self.close()
