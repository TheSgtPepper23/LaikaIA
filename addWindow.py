import os
import hashlib
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from internationalization import LANGUAGE
from logic import Hash
from windows.message import Message
from databaseAccess import DbMethods

class AddWindow(QMainWindow):
    def __init__(self, lang):
        QMainWindow.__init__(self)
        uic.loadUi("windows/AddUser.ui", self)
        self.lang = lang
        self.reload_text()
        self.back_button.clicked.connect(self.go_to_back)
        self.add_button.clicked.connect(self.add_user)

    def reload_text(self):
        """Change the language of the window according to the chosen previously"""
        self.language = LANGUAGE.get(self.lang)
        self.setWindowTitle(self.language["add_user"])
        self.user_name_label.setText(self.language["username"])
        self.pass_label.setText(self.language["password"])
        self.confirm_pass_label.setText(self.language["confirm_pass"])
        self.add_button.setText(self.language["add_user"])
        self.back_button.setText(self.language["back"])

    def add_user(self):
        """Add a new user to the game"""
        if len(self.user_name_text.text()) < 4:
            message = Message(self.language["inv_username"], self.language["user_not_long"])
            warning_message = message.create_iw_message(self.language["ok"], "warning")
            warning_message.exec()
        elif len(self.password_text.text()) < 8:
            message = Message(self.language["inv_pass"], self.language["pass_not_long"])
            warning_message = message.create_iw_message(self.language["ok"], "warning")
            warning_message.exec()
        else:
            if self.password_text.text() == self.confirm_pass_text.text():
                data_acces = DbMethods()
                response = data_acces.add_player(self.user_name_text.text(), Hash.encrypt(self.password_text.text()))

                if response == True:
                    message = Message(self.language["registered"], self.language["welcome"])
                    information_message = message.create_iw_message(self.language["ok"], "information")
                    information_message.exec()
                elif response == False:
                    message = Message(self.language["other_name"], self.language["existing_user"])
                    warning_message = message.create_iw_message(self.language["ok"], "warning")
                    warning_message.exec()
                self.user_name_text.clear()
                self.password_text.clear()
                self.confirm_pass_text.clear()
            else:
                message = Message(self.language["pass_problem"], self.language["pass_dont_match"])
                warning_message = message.create_iw_message(self.language["ok"], "warning")
                warning_message.exec()

    def go_to_back(self):
        """Return to administration window"""
        from adminWindow import AdminWindow
        self.admin = AdminWindow(self.lang)
        self.admin.show()
        self.close()
