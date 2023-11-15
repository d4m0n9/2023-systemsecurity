import sys
from PyQt5.QtWidgets import QApplication
from main_widget import MainWidget
from delete_file import delete_item
from rename_file import rename_item
from open_file import open_item
from sort import sort_by_ext, sort_by_date
from filter_by_ext import ExtensionFilter
from search_file import search_files

def main():
    app = QApplication([])
    ex = MainWidget()
    ex.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
