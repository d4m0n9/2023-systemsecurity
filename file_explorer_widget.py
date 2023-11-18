from PyQt5.QtWidgets import QWidget, QTreeView, QVBoxLayout, QHBoxLayout, QFileSystemModel, QMenu, QLineEdit
from PyQt5.QtCore import Qt
import file_explorer_functions


class Main(QWidget):
    # 초기화
    def __init__(self):
        super().__init__()
        self.path = ""
        self.index = None

        self.tv = QTreeView(self)
        self.model = QFileSystemModel()
        self.searchEdit = QLineEdit(self)
        self.searchEdit.setPlaceholderText("검색")
        self.searchEdit.setFixedWidth(200)
        
        self.setUi()
        self.setSlot()

    # 인터페이스 설정
    def setUi(self):
        self.setGeometry(300, 300, 700, 350)
        self.setWindowTitle("파일 탐색기")
        self.model.setRootPath(self.path)
        self.tv.setSortingEnabled(True)
        self.tv.setModel(self.model)
        self.tv.setColumnWidth(0, 250)
        self.tv.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tv.customContextMenuRequested.connect(self.openMenu)
        #self.tv.setSelectionMode(QAbstractItemView.ExtendedSelection)  # 다중 선택 가능

        searchLayout = QHBoxLayout()
        searchLayout.addStretch(1)
        searchLayout.addWidget(self.searchEdit)

        layout = QVBoxLayout()
        layout.addLayout(searchLayout)
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
            fileLogAction = menu.addAction("로그")
            scanVirusAction = menu.addAction("악성 코드 스캔 및 진단")
            propertiesAction = menu.addAction("속성")
            action = menu.exec_(self.sender().viewport().mapToGlobal(position))

            if action == openAction:
                self.Open(self.index)
            elif action == renameAction:
                self.Rename()
            elif action == deleteAction:
                self.Remove()
            elif action == propertiesAction:  # 파일 속성 확인 액션 처리
                self.ShowFileProperties()

    # Esc 키 누르면 뒤로가기, 파일/폴더 선택 후 Enter 키 누를 시 열기 동작 실행
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            file_explorer_functions.GoBack(self)
        elif event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            file_explorer_functions.OpenItem(self)
        super().keyPressEvent(event)
        
    # 액션 이벤트 연결
    def setSlot(self):
        self.tv.clicked.connect(self.SetIndex)
        self.tv.doubleClicked.connect(self.Open)
        self.searchEdit.returnPressed.connect(self.Search)


    # 선택된 파일의 인덱스 저장
    def SetIndex(self, index):
        self.index = index

    # 파일/폴더 열기 동작 실행
    def Open(self, index):
        file_explorer_functions.Open(self, index)

    # 이름 바꾸기 동작 실행
    def Rename(self):
        file_explorer_functions.Rename(self)

    # 파일/폴더 삭제 동작 실행
    def Remove(self):
        file_explorer_functions.Remove(self)

    # 확장자별 필터링 동작 실행
    def FilterByExt(self):
        file_explorer_functions.FilterByExt(self)

    # 파일/폴더 검색 동작 실행
    def Search(self):
        text = self.searchEdit.text()
        file_explorer_functions.Search(self, text)

    # 파일 속성 표시
    def ShowFileProperties(self):
        file_explorer_functions.ShowFileProperties(self)
        