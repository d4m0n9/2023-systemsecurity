from PyQt5.QtWidgets import QWidget, QTreeView, QVBoxLayout, QPushButton, QFileSystemModel, QMenu, QComboBox, QTreeWidgetItem, QAbstractItemView, QDialog, QLabel, QApplication
from PyQt5.QtCore import Qt, QUrl, QModelIndex
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import QFileInfo, QStorageInfo
import file_explorer_functions
import sys

class PropertyDialog(QDialog):
    def __init__(self, properties, parent=None):
        super().__init__(parent)
        
        self.setWindowTitle("파일 속성")
        
        layout = QVBoxLayout()
        
        for key, value in properties.items():
            label = QLabel(f"{key}: {value}")
            layout.addWidget(label)
        
        self.setLayout(layout)

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
        self.tv.setSelectionMode(QAbstractItemView.ExtendedSelection)  # 다중 선택 가능

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
            propertiesAction = menu.addAction("속성")  # 파일 속성 확인 액션 추가
            action = menu.exec_(self.sender().viewport().mapToGlobal(position))

            if action == openAction:
                self.Open(self.index)
            elif action == renameAction:
                self.Rename()
            elif action == deleteAction:
                self.Remove()
            elif action == propertiesAction:  # 파일 속성 확인 액션 처리
                self.showFileProperties()

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
        file_explorer_functions.Open(self, index)

    # 이름 바꾸기 동작 실행
    def Rename(self):
        file_explorer_functions.Rename(self)

    # 파일/폴더 삭제 동작 실행
    def Remove(self):
        file_explorer_functions.Remove(self)

    # 확장자별 정렬 동작 실행
    def SortByExt(self):
        file_explorer_functions.SortByExt(self)

    # 수정 날짜순 정렬 동작 실행
    def SortByDate(self):
        file_explorer_functions.SortByDate(self)

    # 확장자별 필터링 동작 실행
    def FilterByExt(self):
        file_explorer_functions.FilterByExt(self)

    # 파일/폴더 검색 동작 실행
    def SearchFile(self):
        file_explorer_functions.SearchFile(self)

    # Esc 키 누르면 뒤로가기, 파일/폴더 선택 후 Enter 키 누를 시 열기 동작 실행
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            current_index = self.tv.rootIndex()
            parent_index = self.model.parent(current_index)
            if parent_index.isValid():
                self.tv.setRootIndex(parent_index)
                self.tv.scrollTo(parent_index, QTreeView.PositionAtCenter)
                return
        elif event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            if self.index.isValid():
                if self.model.isDir(self.index):
                    self.tv.setRootIndex(self.index)
                    self.tv.scrollTo(self.index, QTreeView.PositionAtCenter)
                else:
                    item_path = self.model.filePath(self.index)
                    url = QUrl.fromLocalFile(item_path)
                    QDesktopServices.openUrl(url)
        super().keyPressEvent(event)

    # 파일 속성 표시
    def showFileProperties(self):
        """
        선택된 파일의 속성을 표시합니다.
        """
        if self.index is not None:
            file_info = QFileInfo(self.model.filePath(self.index))
            attributes = {
                "파일 경로(위치)": file_info.filePath(),
                "만든 날짜": file_info.created().toString(Qt.DefaultLocaleLongDate),
                "수정한 날짜": file_info.lastModified().toString(Qt.DefaultLocaleLongDate),
                "엑세스한 날짜": file_info.lastRead().toString(Qt.DefaultLocaleLongDate),
                "크기": file_info.size(),
                "디스크 할당 크기": self.getDiskAllocationSize(file_info.filePath())
            }

            app = QApplication.instance()
            dialog = PropertyDialog(attributes, parent=self)
            dialog.exec_()
            app.processEvents()

    # 디스크 할당 크기 얻기
    def getDiskAllocationSize(self, file_path):
        """
        파일의 디스크 할당 크기를 얻어옵니다.
        """
        storage_info = QStorageInfo(file_path)
        allocation_size = storage_info.bytesTotal()
        return allocation_size