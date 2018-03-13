from PyQt5.QtWidgets import QMessageBox

class Message():
    def __init__(self, title, text):
        self.title = title
        self.text = text

    def create_iw_message(self, button_text, message_type):
        """Create a warning or information message and returns it"""
        message_box = QMessageBox()
        if message_type == "warning":
            message_box.setIcon(QMessageBox.Warning)
        else:
            message_box.setIcon(QMessageBox.Information)
        message_box.setText(self.title)
        message_box.setInformativeText(self.text)
        message_box.setStandardButtons(QMessageBox.Ok)
        button_ok = message_box.button(QMessageBox.Ok)
        button_ok.setText(button_text)
        return message_box

    def create_question_message(self, button_text):
        """Create a information message and returns it"""
        message_box = QMessageBox()
        message_box.setIcon(QMessageBox.Question)
        message_box.setText(self.title)
        message_box.setInformativeText(self.text)
        message_box.setStandardButtons(QMessageBox.No|QMessageBox.Yes)
        button_yes = message_box.button(QMessageBox.Yes)
        button_yes.setText(button_text)
        button_no = message_box.button(QMessageBox.No)
        return message_box

    def create_last_message(self):
        """Create the last message of the game, and return it"""
        message_box = QMessageBox()
        message_box.setIcon(QMessageBox.Information)
        message_box.setText(self.title)
        message_box.setInformativeText(self.text)
        message_box.setStandardButtons(QMessageBox.Ok)
        button_ok = message_box.button(QMessageBox.Ok)
        return message_box

