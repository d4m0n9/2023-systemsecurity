import file_explorer_functions
import os
import ctypes
from PyQt5.QtWidgets import QWidget, QTreeView, QVBoxLayout, QHBoxLayout, QFileSystemModel, QMenu, QLineEdit, QScrollArea, \
                            QDialog, QLabel, QPushButton, QMessageBox, QFrame, QTextEdit, QDialogButtonBox
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from malicious_diagnostics import scan_file, get_scan_report
from file_log import log_file_access

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
        font = QFont("맑은 고딕", 8) 
        self.searchEdit.setFont(font)
        
        self.propertiesChanged = pyqtSignal(str, int)  # 속성 변경 시그널
        self.setUi()
        self.setSlot()

    # 인터페이스 설정
    def setUi(self):
        self.setGeometry(300, 150, 700, 500)
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
        
        self.fileLogTextEdit = QTextEdit(self)
        self.fileLogTextEdit.setReadOnly(True)
        self.fileLogTextEdit.setFixedHeight(150)
        font = QFont("맑은 고딕", 9) 
        self.fileLogTextEdit.setFont(font)
        layout.addWidget(self.fileLogTextEdit)
        
        self.setLayout(layout)
        
        self.updateFileLog()

    # 우클릭 메뉴
    def openMenu(self, position):
        self.index = self.sender().indexAt(position)
        indexes = self.sender().selectedIndexes()
        if len(indexes) > 0:
            menu = QMenu()
            font = QFont("맑은 고딕", 9)
            menu.setFont(font) 
            openAction = menu.addAction("열기")
            renameAction = menu.addAction("이름 바꾸기")
            deleteAction = menu.addAction("삭제")
            propertiesAction = menu.addAction("속성")
            fileInfo = self.model.fileInfo(self.index)
            if not fileInfo.isDir():  # 파일일 때만
                scanVirusAction = menu.addAction("악성코드 스캔")
            action = menu.exec_(self.sender().viewport().mapToGlobal(position))

            if action == openAction:
                self.Open(self.index)
            elif action == renameAction:
                self.Rename()
            elif action == deleteAction:
                self.Remove()
            elif action == propertiesAction:
                self.ShowProperties()
            elif 'scanVirusAction' in locals() and action == scanVirusAction:
                self.ScanVirus()


    # Backspace 키 누르면 뒤로가기
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Backspace:
            file_explorer_functions.GoBack(self)
        super().keyPressEvent(event)

    # 액션 이벤트 연결
    def setSlot(self):
        self.tv.clicked.connect(self.SetIndex) # 선택된 아이템에 대한 정보 처리
        self.tv.doubleClicked.connect(self.updateFileLog) # 아이템 더블 클릭 시 파일 로그 업데이트
        self.tv.doubleClicked.connect(self.Open) # 아이템 더블 클릭 시 열기 기능 실행
        self.searchEdit.returnPressed.connect(self.Search) # 엔터 키 누를 시 검색 기능 실행

    # 선택된 파일/폴더의 인덱스 저장
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
    
    # 파일 로그 업데이트
    def updateFileLog(self):
        index = self.tv.currentIndex()
        self.path = self.model.filePath(index)  # 선택된 디렉토리 경로 가져오기
        if self.path:
            file_log = log_file_access(self.path)
            self.fileLogTextEdit.setPlainText(file_log)
        
    # 사용자로부터 API 키를 입력 받는 메서드
    def get_api_key(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("API Key Input")

        layout = QVBoxLayout(dialog)

        label = QLabel("Enter your VirusTotal API key:")
        font = QFont("맑은 고딕", 9)
        label.setFont(font)
        layout.addWidget(label)

        lineEdit = QLineEdit()
        lineEdit.setFont(font)
        layout.addWidget(lineEdit)

        helpLabel = QLabel("일반 사용자 : 30초마다 스캔 가능\n비즈니스 사용자 : 무제한 스캔 가능")  # 도움말 레이블
        helpLabel.setFont(QFont("맑은 고딕", 7))
        helpLabel.setStyleSheet("color: gray;")
        layout.addWidget(helpLabel)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        for button in buttonBox.buttons():
            button.setFont(font)

        buttonBox.accepted.connect(dialog.accept)
        buttonBox.rejected.connect(dialog.reject)
        layout.addWidget(buttonBox)

        if dialog.exec_() == QDialog.Accepted:
            return lineEdit.text()
        else:
            return None
        
    # 악성 코드 스캔 및 진단 기능을 사용해서 새 창을 띄워줌
    def ScanVirus(self):
        if self.index is not None:
            self.api_key = self.get_api_key()  # 악성코드 스캔을 실행할 때 API 키를 입력받음
            if self.api_key is not None:  # API 키가 있을 때만 스캔 수행
                file_path = self.model.filePath(self.index)


                # 1단계: 스캔할 파일 업로드
                upload_result = scan_file(self.api_key, file_path)

                # 2단계: 검색이 완료될 때까지 대기(VirusTotal 정책에 따라 다름)
                # 3단계: 스캔 보고서 검색
                resource = upload_result['resource']
                report = get_scan_report(self.api_key, resource)

                # 4단계: 스캔 결과 인쇄
                result_message = f" Scan results:\n\n" \
                                f"  - Total scans: {report['total']}\n" \
                                f"  - Positive scans: {report['positives']}\n" \
                                f"  - Scan results:"
                for scanner, result in report['scans'].items():
                    result_message += f"\n    - {scanner}: {result}"
        
                # 스캔 결과 인쇄 창
                result_dialog = QDialog()
                result_dialog.setGeometry(340, 200, 620, 400)
                result_dialog.setWindowTitle("악성코드 스캔 결과")

                scroll = QScrollArea(result_dialog)
                label = QLabel(result_message)
                label.setWordWrap(True)
                font = QFont("맑은 고딕", 9)
                label.setFont(font)
                scroll.setWidget(label)
                scroll.setWidgetResizable(True)

                layout = QVBoxLayout(result_dialog)
                layout.addWidget(scroll)
                result_dialog.setLayout(layout)

                result_dialog.exec_()

def get_disk_usage(file_path):
    sectorsPerCluster = ctypes.c_ulonglong(0)
    bytesPerSector = ctypes.c_ulonglong(0)
    rootPathName = ctypes.c_wchar_p(file_path[:3])  # 드라이브 경로 (예: 'C:\\')

    ctypes.windll.kernel32.GetDiskFreeSpaceW(rootPathName, ctypes.byref(sectorsPerCluster), ctypes.byref(bytesPerSector), None, None)

    clusterSize = sectorsPerCluster.value * bytesPerSector.value  # 클러스터 크기 (바이트)
    fileSize = os.path.getsize(file_path)  # 파일 크기 (바이트)

    return ((fileSize // clusterSize) + 1) * clusterSize  # 디스크 할당 크기 (바이트)
    
# 파일 속성을 표시
class PropertiesDialog(QDialog):
    # 파일 속성이 변경될 때 발생하는 시그널
    propertiesChanged = pyqtSignal(str, int) 

    def __init__(self, file_path, file_attributes, parent=None):
        super().__init__(parent)
        # 창 제목 설정
        self.setWindowTitle("파일 속성")
        self.file_path = file_path
        self.file_attributes = file_attributes

        layout = QVBoxLayout()
        font = QFont("맑은 고딕", 9)
        
        # 파일 경로 표시
        path_label = QLabel(f"파일 경로: {self.file_path}")
        path_label.setFont(font)  
        layout.addWidget(path_label)
        
        # 정보 레이아웃
        info_layout = QVBoxLayout()
        # 파일명, 형식, 위치 표시
        file_name_label = QLabel(f"파일명: {file_explorer_functions.get_file_name(self.file_path)}")
        file_name_label.setFont(font)  
        info_layout.addWidget(file_name_label)
        
        file_type_label = QLabel(f"형식: {file_explorer_functions.get_file_extension(file_explorer_functions.get_file_name(self.file_path))}")
        file_type_label.setFont(font)  
        info_layout.addWidget(file_type_label)
        
        file_location_label = QLabel(f"위치: {file_explorer_functions.get_directory(self.file_path)}")
        file_location_label.setFont(font) 
        info_layout.addWidget(file_location_label)
        
        info_layout.addWidget(QFrame(frameShape=QFrame.HLine, frameShadow=QFrame.Sunken))

        # 파일 정보 표시
        file_info = file_explorer_functions.get_file_info(self.file_path)
        if file_info is not None:
            file_size_label = QLabel(f"크기: {file_info['size']} byte")
            file_size_label.setFont(font)
            info_layout.addWidget(file_size_label)

            # 디스크 사용량 표시
            disk_usage_label = QLabel(f"디스크 할당 크기: {get_disk_usage(self.file_path)} byte")
            disk_usage_label.setFont(font)  
            info_layout.addWidget(disk_usage_label)
            info_layout.addWidget(QFrame(frameShape=QFrame.HLine, frameShadow=QFrame.Sunken))
            
            file_ctime_label = QLabel(f"만든 날짜: {file_explorer_functions.format_date(file_info['ctime'])}")
            file_ctime_label.setFont(font)  
            info_layout.addWidget(file_ctime_label)
            
            file_mtime_label = QLabel(f"수정한 날짜: {file_explorer_functions.format_date(file_info['mtime'])}")
            file_mtime_label.setFont(font)  
            info_layout.addWidget(file_mtime_label)
            
            file_atime_label = QLabel(f"액세스한 날짜: {file_explorer_functions.format_date(file_info['atime'])}")
            file_atime_label.setFont(font)  
            info_layout.addWidget(file_atime_label)
    
        else:
            file_info_error_label = QLabel("파일 정보를 가져올 수 없습니다.")
            file_info_error_label.setFont(font)
            info_layout.addWidget(file_info_error_label)

        info_layout.addWidget(QFrame(frameShape=QFrame.HLine, frameShadow=QFrame.Sunken))

        # 버튼 레이아웃
        button_layout = QHBoxLayout()
        confirm_button = QPushButton("확인")
        confirm_button.setFont(font)
        confirm_button.clicked.connect(self.confirm_button_clicked)
        button_layout.addWidget(confirm_button)

        # 메인 레이아웃
        main_layout = QVBoxLayout()
        main_layout.addLayout(info_layout)
        main_layout.addLayout(button_layout)

        layout.addLayout(main_layout)
        self.setLayout(layout)

        self.setModal(True)
        self.setWindowModality(Qt.ApplicationModal)

    # 확인 버튼 클릭 시 호출되는 함수
    def confirm_button_clicked(self):
        self.accept()