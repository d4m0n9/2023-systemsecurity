import sys
from PyQt5.QtWidgets import QApplication
from main_widget import Main
from delete_file import delete_item
from rename_file import rename_item
from open_file import open_item
from sort_by_ext import sort_by_ext
from sort_by_date import sort_by_date
from filter_by_ext import filter_by_ext
from search_file import search_file

def main():
    app = QApplication([])
    ex = Main()
    ex.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
