import sys
from PyQt5.QtWidgets import QApplication
from main_window import MainWindow

if __name__ == "__main__":
    app = QApplication([])
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
