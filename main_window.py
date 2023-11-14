from PyQt5.QtWidgets import QWidget, QVBoxLayout
from tree_view import TreeView
from button import Button
from input_dialog import InputDialog
from message_box import MessageBox

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.path = "C:"
        self.index = None

        self.tv = TreeView()
        self.btnRen = Button("이름 바꾸기")
        self.btnDel = Button("파일 삭제")
        self.btnOpen = Button("파일/폴더 열기")
        self.btnSortExt = Button("파일 확장자별 정렬")
        self.btnSortDate = Button("수정 날짜순 정렬")
        self.btnFilterExt = Button("확장자별 필터링")
        self.btnSearch = Button("파일 검색")
        self.layout = QVBoxLayout()
        self.setUi()
        self.setSlot()

    def open_item(self):
        selected_index = self.tv.get_selected_index()
        if selected_index:
            item_name = self.tv.get_file_name(selected_index)
            item_path = self.tv.get_file_path(selected_index)
            try:
                os.startfile(item_path)
            except Exception as e:
                MessageBox().show_warning("오류", "파일을 열 수 없습니다")

    def setUi(self):
        self.setGeometry(300, 300, 700, 350)
        self.setWindowTitle("파일 탐색기")

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
        self.btnRen.clicked.connect(self.ren)
        self.btnDel.clicked.connect(self.rm)
        self.btnOpen.clicked.connect(self.open_item)
        self.btnSortExt.clicked.connect(self.tv.sort_by_ext)
        self.btnSortDate.clicked.connect(self.tv.sort_by_date)
        self.btnFilterExt.clicked.connect(self.tv.filter_by_ext)
        self.btnSearch.clicked.connect(self.search_file)

    def ren(self):
        selected_index = self.tv.get_selected_index()
        if selected_index:
            parent_path = self.tv.get_parent_path(selected_index)
            fname = self.tv.get_file_name(selected_index)
            text, res = InputDialog().get_text("이름 바꾸기", "바꿀 이름을 입력하세요.", fname)

            if res:
                while True:
                    self.ok = True
                    for i in os.listdir(parent_path):
                        if i == text:
                            text, res = InputDialog().get_text("중복 오류", "바꿀 이름을 입력하세요.", text)
                            if not res:
                                return
                            self.ok = False
                    if self.ok:
                        break
                os.rename(os.path.join(parent_path, fname), os.path.join(parent_path, text))

    def rm(self):
        selected_index = self.tv.get_selected_index()
        if selected_index:
            parent_path = self.tv.get_parent_path(selected_index)
            fname = self.tv.get_file_name(selected_index)
            try:
                if not self.tv.is_dir(selected_index):
                    os.unlink(os.path.join(parent_path, fname))
                    print(fname + ' 파일 삭제')
                else:
                    shutil.rmtree(os.path.join(parent_path, fname))
                    print(fname + ' 폴더 삭제')
            except Exception as e:
                print("Error:", e)

    def search_file(self):
        text, res = InputDialog().get_text("파일 검색", "검색할 파일 이름을 입력하세요.")
        if res:
            for root, dirs, files in os.walk('/'):
                if text in files:
                    MessageBox().show_information("파일 위치", os.path.join(root, text))
                    return

            MessageBox().show_warning("오류", "찾는 파일이 없습니다.")
        
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
