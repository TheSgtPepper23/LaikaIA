from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
from internationalization import LANGUAGE
from DatabaseAccess import DbMethods

class Leaderboards(QMainWindow):
    def __init__(self, lang):
        QMainWindow.__init__(self)
        uic.loadUi("windows/Leaderboards.ui", self)
        self.lang = lang
        self.reload_text()
        self.back_button.clicked.connect(self.close)
        self.populate_table()

    def reload_text(self):
        """Change the language of the window according to the chosen previously"""
        self.language = LANGUAGE.get(self.lang)
        self.setWindowTitle(self.language["leaderboards"])
        self.leader_label.setText(self.language["leaderboards"])
        self.back_button.setText(self.language["back"])
        self.leader_table.setHorizontalHeaderItem(0, QTableWidgetItem(self.language["player"]))
        self.leader_table.setHorizontalHeaderItem(1, QTableWidgetItem(self.language["score"]))

    def populate_table(self):
        """Populate the player's table with the best players ordered by their score"""
        self.leader_table.setRowCount(10)
        db_access = DbMethods()
        scores_list = db_access.select_best_players()
        for i in range(len(scores_list)):
            username, score = scores_list[i]
            item_user = QTableWidgetItem(username)
            item_score = QTableWidgetItem(str(score))
            self.leader_table.setItem(i, 0, item_user)
            self.leader_table.setItem(i, 1, item_score)
