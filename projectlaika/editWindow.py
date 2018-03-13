import json
import xmlrpc.client
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
from windows.message import Message
from internationalization import LANGUAGE
from logic import Hash
from databaseAccess import DbMethods

class EditPlayer(QMainWindow):
    def __init__(self, lang, username):
        QMainWindow.__init__(self)
        uic.loadUi("windows/EditPlayer.ui", self)
        self.lang = lang
        self.username = username
        self.reload_text()
        self.player_name_label.setText(self.username)
        self.save_button.clicked.connect(self.save_info)
        self.cancel_button.clicked.connect(self.close)

    def reload_text(self):
        """Change the language of the window according to the chosen previously"""
        self.language = LANGUAGE.get(self.lang)
        self.setWindowTitle(self.language["change_pass"])
        self.username_label.setText(self.language["username"])
        self.password_label.setText(self.language["password"])
        self.password_text.setPlaceholderText(self.language["new_pass"])
        self.save_button.setText(self.language["save"])
        self.cancel_button.setText(self.language["cancel"])

    def save_info(self):
        """Save the new password of the selected Player"""
        if len(self.password_text.text()) < 8:
            message = Message(self.language["inv_pass"], self.language["pass_not_long"])
            warning_message = message.create_iw_message(self.language["ok"], "warning")
            warning_message.exec()
        else:
            data_acces = DbMethods()
            response = data_acces.change_user_information(self.username,
            Hash.encrypt(self.password_text.text()))

            if response == True:
                message = Message(
                    self.language["success"], self.language["act_info"])
                information_message = message.create_iw_message(
                    self.language["ok"], "information")
                information_message.exec()
            else:
                message = Message(self.language["error"], self.language["inf_error"])
                warning_message = message.create_iw_message(self.language["ok"], "warning")
                warning_message.exec()
            self.close()
