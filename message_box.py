from PyQt5.QtWidgets import QMessageBox

class MessageBox(QMessageBox):
    def __init__(self, parent=None):
        super().__init__(parent)

    def show_warning(self, title, message):
        self.warning(self, title, message)

    def show_information(self, title, message):
        self.information(self, title, message)
