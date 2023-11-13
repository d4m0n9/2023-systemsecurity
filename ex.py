import sys
import os
import shutil
from PyQt5.QtWidgets import (QWidget, QApplication, QTreeView, QVBoxLayout, QPushButton, 
                             QInputDialog, QLineEdit, QMessageBox, QFileSystemModel, QTabWidget)
from PyQt5.QtCore import Qt

class Main(QWidget):
    def __init__(self):
        super().__init__()
        self.path = "C:"
        self.index = None

        self.tv1 = QTreeView(self)
        self.tv2 = QTreeView(self)
        self.tv3 = QTreeView(self)
        self.model = QFileSystemModel()

        self.btnRen = QPushButton("이름 바꾸기")
        self.btnDel = QPushButton("파일 삭제")
        self.btnOpen = QPushButton("파일/폴더 열기")
        self.btnSortExt = QPushButton("파일 확장자별 정렬")
        self.btnSortDate = QPushButton("수정 날짜순 정렬")
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

    def setUi(self):
        self.setGeometry(300, 300, 700, 350)
        self.setWindowTitle("파일 탐색기")
        self.model.setRootPath(self.path)

        for tv in [self.tv1, self.tv2, self.tv3]:
            tv.setModel(self.model)
            tv.setColumnWidth(0, 250)

        self.tab1_ui()
        self.tab2_ui()
        self.tab3_ui()

        self.tabWidget.addTab(self.tab1, "파일 탐색기")
        self.tabWidget.addTab(self.tab2, "파일 로그")
        self.tabWidget.addTab(self.tab3, "악성 코드 스캔 및 진단")

        self.layout = QVBoxLayout(self)  # 메인 레이아웃 생성
        self.layout.addWidget(self.tabWidget)  # 메인 레이아웃에 탭 위젯 추가
        self.setLayout(self.layout)  # 메인 레이아웃 설정


    def tab1_ui(self):
        layout = QVBoxLayout()
        layout.addWidget(self.tv1)
        layout.addWidget(self.btnDel)
        layout.addWidget(self.btnRen)
        self.tab1.setLayout(layout)

    def tab2_ui(self):
        layout = QVBoxLayout()
        layout.addWidget(self.tv2)
        layout.addWidget(self.btnOpen)
        layout.addWidget(self.btnSortExt)
        self.tab2.setLayout(layout)

    def tab3_ui(self):
        layout = QVBoxLayout()
        layout.addWidget(self.tv3)
        layout.addWidget(self.btnSortDate)
        layout.addWidget(self.btnFilterExt)
        self.tab3.setLayout(layout)

    def setSlot(self):
        self.tv1.clicked.connect(self.setIndex)
        self.tv2.clicked.connect(self.setIndex)
        self.tv3.clicked.connect(self.setIndex)
        self.btnRen.clicked.connect(self.ren)
        self.btnDel.clicked.connect(self.rm)
        self.btnOpen.clicked.connect(self.open_item)
        self.btnSortExt.clicked.connect(self.sort_by_ext)
        self.btnSortDate.clicked.connect(self.sort_by_date)
        self.btnFilterExt.clicked.connect(self.filter_by_ext)
        self.btnSearch.clicked.connect(self.search_file)

    def setIndex(self, index):
        self.index = index

    def open_item(self):
        selected_index = self.index
        if selected_index:
            item_name = self.model.fileName(selected_index)
            item_path = self.model.filePath(selected_index)
            try:
                os.startfile(item_path)
            except Exception as e:
                QMessageBox.warning(self, "오류", "파일을 열 수 없습니다")

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
                os.unlink(fname)
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

    # 파일 검색 기능
    def search_file(self):
        text, res = QInputDialog.getText(self, "파일 검색", "검색할 파일 이름을 입력하세요.", QLineEdit.Normal)
        if res:
            for root, dirs, files in os.walk('/'):
                if text in files:
                    QMessageBox.information(self,"파일 위치",os.path.join(root,text))
                    return
            QMessageBox.warning(self,"오류","찾는 파일이 없습니다.")

if __name__ == "__main__":
    app = QApplication([])
    ex = Main()
    ex.show()
    sys.exit(app.exec_())