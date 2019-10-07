import sys
import re
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5 import uic
from internationalization import LANGUAGE
from logic import Hash
from windows.message import Message
from databaseAccess import DbMethods


class LogIn(QMainWindow):
    def __init__(self, lang):
        QMainWindow.__init__(self)
        uic.loadUi("windows/LogIn.ui", self)
        battle_image = QPixmap("resources/battle.png")
        self.lang_state = True
        self.lang = lang
        self.reload_text()
        self.image.setPixmap(battle_image)
        self.flag_icon = QPixmap("resources/bandera_usa.png")
        self.flag_button.setIcon(QIcon(self.flag_icon))

        self.log_in_button.clicked.connect(self.log_in_success)
        self.flag_button.clicked.connect(self.choose_language)

        self.name_tf.setText("Revo")
        self.pass_tf.setText("12345678")

    def log_in_success(self):
        """Determines if a player or administrator can enter to the game or
        player's administrator respectively"""
        self.language = LANGUAGE.get(self.lang)
        self.username = self.name_tf.text()
        self.password = Hash.encrypt(self.pass_tf.text())

        database = DbMethods()

        response = database.user_log_in(self.username, self.password)

        if response == 2:
            from adminWindow import AdminWindow
            self.admin = AdminWindow(self.lang)
            self.admin.show()
            self.close()
        elif response == 1:
            from menuWindow import Menu
            self.menu = Menu(self.lang, self.username)
            self.menu.show()
            self.close()
        elif response == 0:
            message = Message(
                self.language["wrong_pass"], self.language["wrong_pass_text"])
            information_mess = message.create_iw_message(
                self.language["ok"], "information")
            information_mess.exec()
        elif response == -1:
            message = Message(self.language["user_no"],
                              self.language["fail_user"])
            information_mess = message.create_iw_message(
                self.language["ok"], "information")
            information_mess.exec()
        elif response == None:
            print("ERrrp")

    def reload_text(self):
        """Change the language of the window according to the chosen
        previously"""
        self.language = LANGUAGE.get(self.lang)
        self.username_label.setText(self.language["username"])
        self.name_tf.setPlaceholderText(
            self.language["username_placeholder_input"])
        self.password_label.setText(self.language["password"])
        self.pass_tf.setPlaceholderText(
            self.language["password_placeholder_input"])
        self.log_in_button.setText(self.language["log_in"])
        self.setWindowTitle(self.language["log_in"])

    def choose_language(self):
        """Determines what language is selected for the rest of the game"""
        self.lang_state = not self.lang_state
        if self.lang_state == True:
            self.lang = "en"
            self.reload_text()
            self.flag_icon = QPixmap("resources/bandera_usa.png")
        else:
            self.lang = "es"
            self.reload_text()
            self.flag_icon = QPixmap("resources/bandera_mexico.png")

        self.flag_button.setIcon(QIcon(self.flag_icon))
