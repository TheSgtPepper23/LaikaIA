import sys
import time
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout
from PyQt5.QtCore import QUrl, QFileInfo, Qt
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5 import uic
from internationalization import LANGUAGE

class Story(QMainWindow):
    def __init__(self, language, side, username):
        QMainWindow.__init__(self)
        uic.loadUi("windows/Story.ui", self)
        self.lang = language
        self.username = username
        self.side = side
        self.reload_text()

        #Declarando el reproductor y ajustándolo en la ventana
        self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        video_widget = QVideoWidget()
        wid = QWidget(self)
        self.setCentralWidget(wid)
        layout = QVBoxLayout()
        layout.addWidget(video_widget)
        wid.setLayout(layout)

        #Asignando la salida de video y el archivo a reproducir
        self.media_player.setVideoOutput(video_widget)
        self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(QFileInfo(self.video).absoluteFilePath())))

        self.show()

    def showEvent(self, event):
        """Play the story video when the window appears
        This is an override method"""
        self.media_player.play()

    def hideEvent(self, event):
        """Stop the story video when the window close
        This is an override method"""
        self.media_player.stop()

    def keyPressEvent(self, event):
        """Go to set ships window when the player press the space key
        This is an override method"""
        if event.key() == Qt.Key_Space:
            from setShipsWindow import SetShips
            self.ship = SetShips(self.lang, self.side, self.username)
            self.ship.show()
            self.close()

    def reload_text(self):
        """Change the language of the window according to the chosen previously"""
        self.language = LANGUAGE.get(self.lang)
        self.setWindowTitle(self.language["story"])
        self.video = self.language["video"]
