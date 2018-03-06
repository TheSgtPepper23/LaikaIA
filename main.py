import sys
from PyQt5.QtWidgets import QApplication
from logInWindow import LogIn

if __name__ == '__main__':
    app = QApplication(sys.argv)
    logIn = LogIn("en")
    logIn.show()
    sys.exit(app.exec_())
