import sys, os, shutil
from PyQt5.QtWidgets import QApplication, QWidget, QTreeView, QVBoxLayout, QPushButton, QInputDialog, QLineEdit, \
    QMessageBox, QFileSystemModel, QMenu, QComboBox
from PyQt5.QtCore import Qt, QFileInfo
from file_operations import open_item, rename_item, delete_item
from sort_operations import sort_by_ext, sort_by_date
from filter_operations import filter_by_ext
from search_operations import search_file


class Main(QWidget):
    def __init__(self):
        super().__init__()
        self.path = "C:"
        self.index = None

        self.tv = QTreeView(self)
        self.model = QFileSystemModel()

        self.cbOperations = QComboBox(self)
        self.cbOperations.addItems(["파일 확장자별 정렬", "수정 날짜순 정렬"])
        self.btnFilterExt = QPushButton("확장자별 필터링")
        self.btnSearch = QPushButton("파일 검색")

        self.setUi()
        self.setSlot()

    def open_item(self, index):
        if index.isValid() and index.column() == 0:
            item_path = self.model.filePath(index)
            if self.model.isDir(index):
                # 디렉토리일 경우 해당 디렉토리 열기
                self.tv.setRootIndex(index)
                self.tv.scrollTo(index, QTreeView.PositionAtCenter)
            else:
                # 파일일 경우 파일 열기
                try:
                    os.startfile(item_path)
                except Exception as e:
                    QMessageBox.warning(self, "오류", "파일을 열 수 없습니다.")

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

    def openMenu(self, position):
        self.index = self.sender().indexAt(position)
        indexes = self.sender().selectedIndexes()
        if len(indexes) > 0:
            menu = QMenu()
            renameAction = menu.addAction("이름 바꾸기")
            deleteAction = menu.addAction("파일/폴더 삭제")
            propertiesAction = menu.addAction("파일/폴더 속성")
            fileLogAction = menu.addAction("파일 로그")
            scanVirusAction = menu.addAction("악성 코드 스캔 및 진단")
            action = menu.exec_(self.sender().viewport().mapToGlobal(position))

            if action == renameAction:
                self.ren()
            elif action == deleteAction:
                self.rm()

    def setSlot(self):
        self.tv.clicked.connect(self.setIndex)
        self.btnFilterExt.clicked.connect(self.filter_by_ext)
        self.btnSearch.clicked.connect(self.search_file)
        self.tv.doubleClicked.connect(self.open_item)
        self.cbOperations.currentIndexChanged.connect(self.execute_operation)

    def execute_operation(self):
        operation = self.cbOperations.currentText()
        if operation == "파일 확장자별 정렬":
            self.sort_by_ext()
        elif operation == "수정 날짜순 정렬":
            self.sort_by_date()

    def setIndex(self, index):
        self.index = index

    def ren(self):
        os.chdir(self.model.filePath(self.model.parent(self.index)))
        fname = self.model.fileName(self.index)
        text, res = QInputDialog.getText(self, "이름 바꾸기", "바꿀 이름을 입력하세요.", QLineEdit.Normal, fname)

        if res:
            while True:
                self.ok = True
                for i in os.listdir(os.getcwd()):
                    if i == text:
                        text, res = QInputDialog.getText(self, "중복 오류", "바꿀 이름을 입력하세요", QLineEdit.Normal, text)
                        if not res:
                            return
                        self.ok = False
                if self.ok:
                    break
            os.rename(fname, text)

    def rm(self):
        os.chdir(self.model.filePath(self.model.parent(self.index)))
        fname = self.model.fileName(self.index)
        reply = QMessageBox.question(self, '삭제 확인',
                                     f"'{fname}'를 삭제하시겠습니까?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            try:
                if not self.model.isDir(self.index):
                    delete_item(fname)
                    print(fname + ' 파일 삭제')
                else:
                    shutil.rmtree(fname)
                    print(fname + ' 폴더 삭제')
            except Exception as e:
                print("Error:", e)

    def sort_by_ext(self):
        sort_by_ext(self.model)

    def sort_by_date(self):
        sort_by_date(self.model)

    def filter_by_ext(self):
        filter_by_ext(self.model)

    def search_file(self):
        text, res = QInputDialog.getText(self, "파일 검색", "검색할 파일 이름을 입력하세요.", QLineEdit.Normal)
        if res:
            root_index = self.tv.rootIndex()
            self.search_in_directory(root_index, text)

    def search_in_directory(self, index, text):
        for i in range(self.model.rowCount(index)):
            child_index = self.model.index(i, 0, index)
            if self.model.fileName(child_index).lower().startswith(text.lower()):
                self.tv.scrollTo(child_index, QTreeView.PositionAtCenter)
                self.tv.setCurrentIndex(child_index)
                return
            if self.model.hasChildren(child_index):
                self.search_in_directory(child_index, text)

            self.search_in_directory(child_index, text)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Backspace:
            current_index = self.tv.rootIndex()
            parent_index = self.model.parent(current_index)
            if parent_index.isValid():
                self.tv.setRootIndex(parent_index)
                self.tv.scrollTo(parent_index, QTreeView.PositionAtCenter)
                return
        super().keyPressEvent(event)


if __name__ == "__main__":
    app = QApplication([])
    ex = Main()
    ex.show()
    sys.exit(app.exec_())



