import sys
import os
import shutil
from PyQt5.QtWidgets import QWidget, QApplication, QTreeView, QVBoxLayout, QPushButton, QInputDialog, QLineEdit, QMessageBox, QFileSystemModel
from PyQt5.QtCore import Qt

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
        self.layout = QVBoxLayout()
        self.setUi()
        self.setSlot()

    def open_item(self):
        selected_index = self.index
        if selected_index:
            item_name = self.model.fileName(selected_index)
            item_path = self.model.filePath(selected_index)
            try:
                os.startfile(item_path)
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
        self.setLayout(self.layout)

    def setSlot(self):
        self.tv.clicked.connect(self.setIndex)
        self.btnRen.clicked.connect(self.ren)
        self.btnDel.clicked.connect(self.rm)
        self.btnOpen.clicked.connect(self.open_item)
        self.btnSortExt.clicked.connect(self.sort_by_ext)
        self.btnSortDate.clicked.connect(self.sort_by_date)
        self.btnFilterExt.clicked.connect(self.filter_by_ext)


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
                os.unlink(fname)  # Corrected typo here
                print(fname + ' 파일 삭제')
            else:
                shutil.rmtree(fname)
                print(fname + ' 폴더 삭제')
        except Exception as e:
            print("Error:", e)
    
    #파일 확장자별 정렬
    def sort_by_ext(self):
        self.model.sort(2, Qt.AscendingOrder)
    
    #파일 날짜순 정렬
    def sort_by_date(self):
        self.model.sort(3, Qt.DescendingOrder)
    
    #파일 확장자별 필터링
    def filter_by_ext(self):
        text, res = QInputDialog.getText(self, "확장자별 필터링", "필터링할 확장자를 입력하세요. (예:.txt)", QLineEdit.Normal)
        if res:
            ext_filter_list=["*" + text]
            self.model.setNameFilters(ext_filter_list)
            
if __name__ == "__main__":
    app = QApplication([])
    ex = Main()
    ex.show()
    sys.exit(app.exec_())
