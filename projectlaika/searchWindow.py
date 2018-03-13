from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QMessageBox
from PyQt5.QtCore import Qt
from windows.message import Message
from internationalization import LANGUAGE
from DatabaseAccess import DbMethods

class SearchWindow(QMainWindow):
    def __init__(self, lang):
        QMainWindow.__init__(self)
        uic.loadUi("windows/SearchUser.ui", self)
        self.lang = lang
        self.reload_text()
        self.populate_table()
        self.back_button.clicked.connect(self.back_buthon_method)
        self.result_table.cellClicked.connect(self.turn_on_buttons)
        self.delete_button.clicked.connect(self.confirm_delete)
        self.edit_button.clicked.connect(self.edit_user)
        self.search_text.textEdited.connect(self.populate_table)

    def reload_text(self):
        """Change the language of the window according to the chosen previously"""
        self.language = LANGUAGE.get(self.lang)
        self.setWindowTitle(self.language["search"])
        self.back_button.setText(self.language["back"])
        self.edit_button.setText(self.language["change_pass"])
        self.delete_button.setText(self.language["delete"])
        self.search_text.setPlaceholderText(self.language["search"])
        self.result_table.setHorizontalHeaderItem(
            0, QTableWidgetItem(self.language["user_header"]))

    def populate_table(self, username = ""):
        """Populate the player's table with all the players registered at the moment"""
        db_acces = DbMethods()
        users = db_acces.select_users(username)

        self.result_table.setRowCount(len(users))

        for i in range(len(users)):
            user = users[i]
            item_user = QTableWidgetItem(user["username"])
            self.result_table.setItem(i, 0, item_user)

    def turn_on_buttons(self):
        """Enable the buttons 'Change Password' and 'Delete' when a user is selected"""
        self.edit_button.setEnabled(True)
        self.delete_button.setEnabled(True)

    def edit_user(self):
        """Open the edit player window"""
        from editWindow import EditPlayer
        self.edit = EditPlayer(self.lang, self.result_table.currentItem().text())
        self.edit.show()

    def confirm_delete(self):
        """Ask if the administrator is sure to delete a player"""
        self.language = LANGUAGE.get(self.lang)
        message = Message(self.language["del_user"], self.language["del_info"])
        delete_message = message.create_question_message(self.language["yes"])
        response = delete_message.exec()

        if response == QMessageBox.Yes:
            self.delete_user()
        elif response == QMessageBox.No:
            delete_message.close()

    def delete_user(self):
        """Delete a player from the database game"""
        db_acces = DbMethods()
        username = self.result_table.currentItem().text()
        response = db_acces.delete_user(username)

        if response == True:
            self.populate_table()
        else:
            message = Message(
                self.language["error"], self.language["inf_error"])
            warning_message = message.create_iw_message(
                self.language["ok"], "warning")
            warning_message.exec()

    def back_buthon_method(self):
        """Return to user's administrator window"""
        from adminWindow import AdminWindow
        self.admin = AdminWindow(self.lang)
        self.admin.show()
        self.close()
