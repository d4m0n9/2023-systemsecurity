import sys
from PyQt5.QtWidgets import QApplication
from explorer import Main

if __name__ == "__main__":
    app = QApplication([])
    ex = Main()
    ex.show()
    sys.exit(app.exec_())