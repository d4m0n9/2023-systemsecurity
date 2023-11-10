from PyQt5.QtWidgets import QWidget, QTreeView, QVBoxLayout, QPushButton
from PyQt5.QtCore import Qt
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
        self.btnRen = QPushButton("이름 바꾸기")
        self.btnDel = QPushButton("파일 삭제")
        self.btnOpen = QPushButton("파일/폴더 열기")
        self.btnSortExt = QPushButton("파일 확장자별 정렬")
        self.btnSortDate = QPushButton("수정 날짜순 정렬")
        self.btnFilterExt = QPushButton("확장자별 필터링")
        self.btnSearch = QPushButton("파일 검색")
        self.layout = QVBoxLayout()
        self.setUi()
        self.setSlot()

    def open_item(self):
        selected_index = self.index
        if selected_index:
            item_name = self.model.fileName(selected_index)
            item_path = self.model.filePath(selected_index)
            try:
                open_item(item_path)
            except Exception as e:
                QMessageBox.warning(self, "오류", "파일을 열 수 없습니다")

    def setUi(self):
        self.setGeometry(300, 300, 700, 350)
        self.setWindowTitle("파일 탐색기")
        self.model.setRootPath(self.path)
        self.tv.setModel(self.model)
        self.tv.setColumnWidth(0, 250)

        self.layout.addWidget(self.tv)
        self.layout.addWidget(self.btnDel)
        self.layout.addWidget(self.btnRen)
        self.layout.addWidget(self.btnOpen)
        self.layout.addWidget(self.btnSortExt)
        self.layout.addWidget(self.btnSortDate)
        self.layout.addWidget(self.btnFilterExt)
        self.layout.addWidget(self.btnSearch)
        self.setLayout(self.layout)

    def setSlot(self):
        self.tv.clicked.connect(self.setIndex)
        self.btnRen.clicked.connect(self.ren)
        self.btnDel.clicked.connect(self.rm)
        self.btnOpen.clicked.connect(self.open_item)
        self.btnSortExt.clicked.connect(self.sort_by_ext)
        self.btnSortDate.clicked.connect(self.sort_by_date)
        self.btnFilterExt.clicked.connect(self.filter_by_ext)
        self.btnSearch.clicked.connect(self.search_file)

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

if __name__ == "__main__":
    app = QApplication([])
    ex = Main()
    ex.show()
    sys.exit(app.exec_())
