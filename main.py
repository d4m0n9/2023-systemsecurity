import sys
from PyQt5.QtWidgets import QApplication
from main_widget import Main

def main():
    app = QApplication([])
    ex = Main()
    ex.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
