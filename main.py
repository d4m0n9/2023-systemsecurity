import sys
from PyQt5.QtWidgets import QApplication
from main_widget import MainWidget
from delete_file import delete_item
from rename_file import rename_item
from open_file import open_item
from sort import sort_by_ext, sort_by_date
from filter_by_ext import filter_by_ext
from search_file import search_files

def setUi(self):
        self.setGeometry(300, 300, 700, 350)
        self.setWindowTitle("파일 탐색기")
        self.model.setRootPath(self.path)

        self.tv.setModel(self.model)
        self.tv.setColumnWidth(0, 250)
        self.tv.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tv.customContextMenuRequested.connect(self.openMenu)

        layout = QVBoxLayout()
        layout.addWidget(self.cbOperations)
        layout.addWidget(self.btnFilterExt)
        layout.addWidget(self.btnSearch)
        layout.addWidget(self.tv)
        self.setLayout(layout)

def setSlot(self):
        self.tv.clicked.connect(self.setIndex)
        self.btnFilterExt.clicked.connect(self.filter_by_ext)
        self.btnSearch.clicked.connect(self.search_file)
        self.tv.doubleClicked.connect(self.open_item)

        self.cbOperations.currentIndexChanged.connect(self.execute_operation)

def main():
    app = QApplication([])
    ex = MainWidget()
    ex.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
