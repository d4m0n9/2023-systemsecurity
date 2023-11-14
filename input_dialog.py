from PyQt5.QtWidgets import QInputDialog, QLineEdit

class InputDialog(QInputDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

    def get_text(self, title, label, text=QLineEdit.Normal):
        return self.getText(self, title, label, text)
