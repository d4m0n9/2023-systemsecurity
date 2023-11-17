from PyQt5.QtWidgets import QWidget, QTreeView, QVBoxLayout, QPushButton, QFileSystemModel, QMenu, QComboBox
from PyQt5.QtCore import Qt
import actions

class Main(QWidget):
    # 초기화
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

    # 인터페이스 설정
    def setUi(self):
        self.setGeometry(300, 300, 700, 350)
        self.setWindowTitle("파일 탐색기")
        self.model.setRootPath(self.path)
        #self.tv.setSortingEnabled(True)  -> 화살표로 정렬 가능
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

    # 우클릭 메뉴 
    def openMenu(self, position):
        self.index = self.sender().indexAt(position)
        indexes = self.sender().selectedIndexes()
        if len(indexes) > 0:
            menu = QMenu()
            openAction = menu.addAction("열기")
            renameAction = menu.addAction("이름 바꾸기")
            deleteAction = menu.addAction("삭제")
            fileLogAction = menu.addAction("파일 로그")
            scanVirusAction = menu.addAction("악성 코드 스캔 및 진단")
            action = menu.exec_(self.sender().viewport().mapToGlobal(position))

            if action == openAction:
                self.Open(self.index)
            elif action == renameAction:
                self.Rename()
            elif action == deleteAction:
                self.Remove()

    # 버튼 / 콤보박스 동작 연결
    def setSlot(self):
        self.tv.clicked.connect(self.SetIndex)
        self.btnFilterExt.clicked.connect(self.FilterByExt)
        self.btnSearch.clicked.connect(self.SearchFile)
        self.tv.doubleClicked.connect(self.Open)
        self.cbOperations.currentIndexChanged.connect(self.Sort)

    # 콤보 박스에서 선택된 정렬 실행
    def Sort(self):
        sort = self.cbOperations.currentText()
        if sort == "파일 확장자별 정렬":
            self.SortByExt()
        elif sort == "수정 날짜순 정렬":
            self.SortByDate()

    # 선택된 파일의 인덱스 저장
    def SetIndex(self, index):
        self.index = index

    # 파일/폴더 열기 동작 실행
    def Open(self, index):
        actions.Open(self, index)

    # 이름 바꾸기 동작 실행
    def Rename(self):
        actions.Rename(self)

    # 파일/폴더 삭제 동작 실행
    def Remove(self):
        actions.Remove(self)

    # 확장자별 정렬 동작 실행
    def SortByExt(self):
        actions.SortByExt(self)

    # 수정 날짜순 정렬 동작 실행
    def SortByDate(self):
        actions.SortByDate(self)

    # 확장자별 필터링 동작 실행
    def FilterByExt(self):
        actions.FilterByExt(self)

    # 파일 검색 동작 실행
    def SearchFile(self):
        actions.SearchFile(self)

    # Backspace 키 누르면 뒤로가기 동작 실행
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Backspace:
            current_index = self.tv.rootIndex()
            parent_index = self.model.parent(current_index)
            if parent_index.isValid():
                self.tv.setRootIndex(parent_index)
                self.tv.scrollTo(parent_index, QTreeView.PositionAtCenter)
                return
        super().keyPressEvent(event)