import sys, os, shutil
from PyQt5.QtWidgets import QApplication, QWidget, QTreeView, QVBoxLayout, QPushButton, QInputDialog, QLineEdit, \
    QMessageBox, QFileSystemModel, QTabWidget, QMenu, QComboBox
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

        self.tv1 = QTreeView(self)
        self.tv2 = QTreeView(self)
        self.tv3 = QTreeView(self)
        self.model = QFileSystemModel()

        self.cbOperations = QComboBox(self)
        self.cbOperations.addItems(["파일 확장자별 정렬", "수정 날짜순 정렬"])
        self.btnFilterExt = QPushButton("확장자별 필터링")
        self.btnSearch = QPushButton("파일 검색")

        self.tabWidget = QTabWidget()
        self.tabWidget.setTabPosition(QTabWidget.West)
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tab4 = QWidget()

        self.setUi()
        self.setSlot()

    def open_item(self, index):
        if index.isValid() and index.column() == 0:
            item_path = self.model.filePath(index)
            if self.model.isDir(index):
                # 디렉토리일 경우 해당 디렉토리 열기
                self.tv1.setRootIndex(index)
                self.tv1.scrollTo(index, QTreeView.PositionAtCenter)
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

        for tv in [self.tv1, self.tv2, self.tv3]:
            tv.setModel(self.model)
            tv.setColumnWidth(0, 250)
            tv.setContextMenuPolicy(Qt.CustomContextMenu)
            tv.customContextMenuRequested.connect(self.openMenu)

        self.tab1_ui()
        self.tab2_ui()
        self.tab3_ui()

        self.tabWidget.addTab(self.tab1, "파일 탐색기")
        self.tabWidget.addTab(self.tab2, "파일 로그")
        self.tabWidget.addTab(self.tab3, "악성 코드 스캔 및 진단")

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.tabWidget)
        self.setLayout(self.layout)

    def openMenu(self, position):
        self.index = self.sender().indexAt(position)
        indexes = self.sender().selectedIndexes()
        if len(indexes) > 0:
            menu = QMenu()
            renameAction = menu.addAction("이름 바꾸기")
            deleteAction = menu.addAction("파일 삭제")
            propertiesAction = menu.addAction("파일 속성")
            action = menu.exec_(self.sender().viewport().mapToGlobal(position))

            if action == renameAction:
                self.ren()
            elif action == deleteAction:
                self.rm()
            elif action == propertiesAction:
                self.show_properties()

    def tab1_ui(self):
        layout = QVBoxLayout()
        layout.addWidget(self.cbOperations)
        layout.addWidget(self.btnFilterExt)
        layout.addWidget(self.btnSearch)
        layout.addWidget(self.tv1)
        self.tab1.setLayout(layout)

    def tab2_ui(self):
        layout = QVBoxLayout()
        layout.addWidget(self.tv2)
        self.tab2.setLayout(layout)

    def tab3_ui(self):
        layout = QVBoxLayout()
        layout.addWidget(self.tv3)
        self.tab3.setLayout(layout)

    def setSlot(self):
        self.tv1.clicked.connect(self.setIndex)
        self.tv2.clicked.connect(self.setIndex)
        self.tv3.clicked.connect(self.setIndex)
        self.btnFilterExt.clicked.connect(self.filter_by_ext)
        self.btnSearch.clicked.connect(self.search_file)
        self.tv1.doubleClicked.connect(self.open_item)
        self.tv2.doubleClicked.connect(self.open_item)
        self.tv3.doubleClicked.connect(self.open_item)
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
        search_file(self.model)

    def show_properties(self):
        if self.index:
            item_path = self.model.filePath(self.index)
            item_info = QFileInfo(item_path)
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("파일 속성")
            msg.setInformativeText(f"파일 경로: {item_info.filePath()}\n"
                                   f"크기: {item_info.size()} bytes\n"
                                   f"생성 시간: {item_info.created().toString()}\n"
                                   f"수정 시간: {item_info.lastModified().toString()}\n"
                                   f"접근 시간: {item_info.lastRead().toString()}")
            msg.setWindowTitle("파일 속성")
            msg.exec_()


if __name__ == "__main__":
    app = QApplication([])
    ex = Main()
    ex.show()
    sys.exit(app.exec_())