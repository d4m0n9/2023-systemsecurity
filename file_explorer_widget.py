from PyQt5.QtWidgets import QWidget, QTreeView, QVBoxLayout, QHBoxLayout, QFileSystemModel, QMenu, QLineEdit
from PyQt5.QtWidgets import QDialog, QLabel, QVBoxLayout, QWidget, QPushButton, QCheckBox, QMessageBox, QFrame
from PyQt5.QtCore import Qt, pyqtSignal
import file_explorer_functions, stat
import malicious_diagnostics

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

        self.propertiesChanged = pyqtSignal(str, int)  # 속성 변경 시그널

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
            elif action == propertiesAction:
                self.ShowProperties()
            elif action == scanVirusAction:
                self.ScanVirus()

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

    # 속성 표시 동작 실행
    def ShowProperties(self):
        if self.index is not None:
            file_path = self.model.filePath(self.index)
            file_attributes = file_explorer_functions.get_file_attributes(file_path)
            properties_dialog = PropertiesDialog(file_path, file_attributes)
            properties_dialog.propertiesChanged.connect(self.apply_properties)
            properties_dialog.exec_()

    # 속성 적용
    def apply_properties(self, file_path, file_attributes):
        success, message = file_explorer_functions.apply_properties(file_path, file_attributes)
        if success:
            QMessageBox.information(self, "적용 완료", message)
        else:
            QMessageBox.warning(self, "오류", message)

class PropertiesDialog(QDialog):
    propertiesChanged = pyqtSignal(str, int)  # 속성 변경 시그널 정의

    def __init__(self, file_path, file_attributes, parent=None):
        super().__init__(parent)
        self.setWindowTitle("파일 속성")
        self.file_path = file_path
        self.file_attributes = file_attributes

        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"파일 경로: {self.file_path}"))

        info_layout = QVBoxLayout()
        info_layout.addWidget(QLabel(f"파일명: {file_explorer_functions.get_file_name(self.file_path)}"))
        info_layout.addWidget(QLabel(f"형식: {file_explorer_functions.get_file_extension(file_explorer_functions.get_file_name(self.file_path))}"))
        info_layout.addWidget(QLabel(f"위치: {file_explorer_functions.get_directory(self.file_path)}"))
        info_layout.addWidget(QFrame(frameShape=QFrame.HLine, frameShadow=QFrame.Sunken))

        file_info = file_explorer_functions.get_file_info(self.file_path)
        if file_info is not None:
            info_layout.addWidget(QLabel(f"크기: {file_info['size']} 바이트"))
            info_layout.addWidget(QLabel(f"만든 날짜: {file_explorer_functions.format_date(file_info['ctime'])}"))
            info_layout.addWidget(QLabel(f"수정한 날짜: {file_explorer_functions.format_date(file_info['mtime'])}"))
            info_layout.addWidget(QLabel(f"액세스한 날짜: {file_explorer_functions.format_date(file_info['atime'])}"))
            info_layout.addWidget(QFrame(frameShape=QFrame.HLine, frameShadow=QFrame.Sunken))
            if 'disk_usage' in file_info:
                info_layout.addWidget(QLabel(f"디스크 할당 크기: {file_info['disk_usage']} 바이트"))
            else:
                info_layout.addWidget(QLabel("디스크 할당 크기 정보를 가져올 수 없습니다."))
        else:
            info_layout.addWidget(QLabel("파일 정보를 가져올 수 없습니다."))

        info_layout.addWidget(QFrame(frameShape=QFrame.HLine, frameShadow=QFrame.Sunken))

        checkbox_layout = QHBoxLayout()
        self.readonly_checkbox = QCheckBox("읽기 전용")
        self.hidden_checkbox = QCheckBox("숨김")
        checkbox_layout.addWidget(self.readonly_checkbox)
        checkbox_layout.addWidget(self.hidden_checkbox)
        info_layout.addLayout(checkbox_layout)

        button_layout = QHBoxLayout()
        confirm_button = QPushButton("확인")
        confirm_button.clicked.connect(self.confirm_button_clicked)
        button_layout.addWidget(confirm_button)
        cancel_button = QPushButton("취소")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)
        apply_button = QPushButton("적용(A)")
        apply_button.clicked.connect(self.apply_button_clicked)
        button_layout.addWidget(apply_button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(info_layout)
        main_layout.addLayout(button_layout)

        layout.addLayout(main_layout)
        self.setLayout(layout)

        self.setModal(True)
        self.setWindowModality(Qt.ApplicationModal)

        self.readonly_checkbox.setChecked(bool(self.file_attributes & stat.S_IREAD))
        self.hidden_checkbox.setChecked(bool(self.file_attributes & stat.FILE_ATTRIBUTE_HIDDEN))

        self.previous_readonly_state = self.readonly_checkbox.isChecked()
        self.previous_hidden_state = self.hidden_checkbox.isChecked()

    def confirm_button_clicked(self):
        self.accept()

    def apply_button_clicked(self):
        file_attributes = self.file_attributes

        if self.readonly_checkbox.isChecked() != self.previous_readonly_state:
            if self.readonly_checkbox.isChecked():
                file_attributes |= stat.S_IREAD
            else:
                file_attributes &= ~stat.S_IREAD

        if self.hidden_checkbox.isChecked() != self.previous_hidden_state:
            if self.hidden_checkbox.isChecked():
                file_attributes |= stat.FILE_ATTRIBUTE_HIDDEN
            else:
                file_attributes &= ~stat.FILE_ATTRIBUTE_HIDDEN

        self.propertiesChanged.emit(self.file_path, file_attributes)  # 시그널 발생

    def reject(self):
        self.close()

    def closeEvent(self, event):
        self.close()

    def ScanVirus(self):
        api_key = 'd00e049b5870f0f4b82b1ce1f5a3879e87575961e03122b934f982dc46e66c19'
        file_path = self.model.filePath(self.index)
        report = malicious_diagnostics.virus_scan(api_key, file_path)

        # 검색 결과를 별도의 Dialog에 표시
        dialog = QDialog(self)
        dialog.setWindowTitle("바이러스 스캔 결과")
        layout = QVBoxLayout()
        label = QLabel()
        if report:
            label.setText(
                f"Scan results:\n  - Total scans: {report['total']}\n  - Positive scans: {report['positives']}\n  - Scan results: {report['scans']}")
        else:
            label.setText("스캔 결과가 없습니다.")
        layout.addWidget(label)
        dialog.setLayout(layout)
        dialog.exec_()