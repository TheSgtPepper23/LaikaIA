from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow
from internationalization import LANGUAGE


class AdminWindow(QMainWindow):
	def __init__(self, lang):
		QMainWindow.__init__(self)
		uic.loadUi("windows/Administration.ui", self)
		self.lang = lang
		self.reload_text()
		leia_icon = QPixmap("resources/leia.png")
		self.leia_image.setPixmap(leia_icon)
		self.back_button.clicked.connect(self.go_to_back)
		self.add_button.clicked.connect(self.go_to_add_users)
		self.search_button.clicked.connect(self.go_to_search_user)

	def reload_text(self):
		"""Change the language of the window according to the chosen previously"""
		self.language = LANGUAGE.get(self.lang)
		self.setWindowTitle(self.language["admin"])
		self.back_button.setText(self.language["log_out"])
		self.add_button.setText(self.language["add_users"])
		self.search_button.setText(self.language["search_users"])

	def go_to_add_users(self):
		"""Go to add users window"""
		from addWindow import AddWindow
		self.add = AddWindow(self.lang)
		self.add.show()
		self.close()

	def go_to_back(self):
		"""Return to log in window"""
		from logInWindow import LogIn
		self.login = LogIn(self.lang)
		self.login.show()
		self.close()

	def go_to_search_user(self):
		"""Go to search user window"""
		from searchWindow import SearchWindow
		self.search = SearchWindow(self.lang)
		self.search.show()
		self.close()
