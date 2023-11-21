# 파일 탐색기 관련 기능 (파일 열기, 이름 변경, 삭제, 확장자/날짜별 정렬, 확장자별 필터링, 파일 검색)
import os
import shutil
import datetime
import win32api
import win32con
import stat
from PyQt5.QtWidgets import QInputDialog, QLineEdit, QMessageBox, QTreeView, QVBoxLayout, QDialog, QLabel
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices


# 선택된 파일/폴더 열기
def Open(main, index):
    if index.isValid() and index.column() == 0:
        item_path = main.model.filePath(index)
        if main.model.isDir(index):
            main.tv.setRootIndex(index)
            main.tv.scrollTo(index, QTreeView.PositionAtCenter)
        else:
            try:
                os.startfile(item_path)
            except Exception as e:
                QMessageBox.warning(main, "오류", "파일을 열 수 없습니다.")

# 선택된 파일/폴더 이름 변경
def Rename(main):
    os.chdir(main.model.filePath(main.model.parent(main.index)))
    fname = main.model.fileName(main.index)
    text, res = QInputDialog.getText(main, "이름 바꾸기", "바꿀 이름을 입력하세요.", QLineEdit.Normal, fname)

    if res:
        while True:
            main.ok = True
            for i in os.listdir(os.getcwd()):
                if i == text:
                    text, res = QInputDialog.getText(main, "중복 오류", "바꿀 이름을 입력하세요", QLineEdit.Normal, text)
                    if not res:
                        return
                    main.ok = False
                if main.ok:
                    break
        os.rename(fname, text)

# 선택된 파일/폴더 삭제
def Remove(main):
    os.chdir(main.model.filePath(main.model.parent(main.index)))
    fname = main.model.fileName(main.index)
    reply = QMessageBox.question(main, '삭제 확인',f"'{fname}'를 삭제하시겠습니까?",
                                 QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
    try:
        if not main.model.isDir(main.index):
            os.unlink(fname)
            print(fname + ' 파일 삭제')
        else:
            shutil.rmtree(fname)
            print(fname + ' 폴더 삭제')
    except Exception as e:
        print("Error:", e)


# 특정 디렉토리 내에서 파일을 검색하는 기능 수행
def SearchInDirectory(main, index, text, results):
    for i in range(main.model.rowCount(index)):
        child_index = main.model.index(i, 0, index)
        if text in main.model.fileName(child_index).lower():
            results.append(main.model.filePath(child_index)) 
        if main.model.hasChildren(child_index):
            SearchInDirectory(main, child_index, text, results)

# 사용자가 입력한 파일 이름 또는 확장자 검색
def Search(main, text):
        root_index = main.tv.rootIndex()
        results = []
        SearchInDirectory(main, root_index, text, results) 

        # 검색 결과를 별도의 Dialog에 표시
        dialog = QDialog(main)
        dialog.setWindowTitle("검색 결과")
        layout = QVBoxLayout()
        if results:
            for file_path in results:
                label = QLabel(file_path)
                layout.addWidget(label)
        else:
            label = QLabel("검색 결과가 없습니다.")
            layout.addWidget(label)
        dialog.setLayout(layout)
        dialog.show()

# 키 이벤트 처리
def GoBack(main):
    current_index = main.tv.rootIndex()
    parent_index = main.model.parent(current_index)
    if parent_index.isValid():
        main.tv.setRootIndex(parent_index)
        main.tv.scrollTo(parent_index, QTreeView.PositionAtCenter)
    else:
        main.tv.setRootIndex(main.model.index(""))
def OpenItem(main):
    if main.index.isValid():
        if main.model.isDir(main.index):
            main.tv.setRootIndex(main.index)
            main.tv.scrollTo(main.index, QTreeView.PositionAtCenter)
        else:
            item_path = main.model.filePath(main.index)
            url = QUrl.fromLocalFile(item_path)
            QDesktopServices.openUrl(url)

#타임스탬프를 날짜 형식으로 변환하는 함수
def format_date(timestamp):
    return datetime.datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")

#파일 경로에서 파일 이름을 추출하는 함수
def get_file_name(file_path):
    return os.path.basename(file_path)

#파일 이름에서 확장자를 추출하는 함수
def get_file_extension(file_name):
    return os.path.splitext(file_name)[1]

#파일 경로에서 디렉토리 경로를 추출하는 함수
def get_directory(file_path):
    return os.path.dirname(file_path)

#파일 정보를 가져오는 함수
def get_file_info(file_path):
    try:
        file_stat = os.stat(file_path)
        file_info = {
            'size': file_stat.st_size,
            'ctime': file_stat.st_ctime,
            'mtime': file_stat.st_mtime,
            'atime': file_stat.st_atime,
            'disk_usage': get_disk_usage(file_path)
        }
        return file_info
    except OSError:
        return None

# 디스크 사용량을 가져오는 함수
def get_disk_usage(path):
    try:
        usage = shutil.disk_usage(os.path.dirname(path))
        total = usage.total
        formatted_usage = format_byte_size(total)
        return formatted_usage
    except FileNotFoundError:
        return "0"
    
# 바이트 크기를 포맷팅하는 함수
def format_byte_size(size):
    # 단위별 바이트 크기
    units = ["바이트", "KB", "MB", "GB", "TB"]

    # 1024로 나누어가면서 단위를 변경
    for unit in units:
        if size < 1024:
            return f"{size:.0f}{unit}"
        size /= 1024

    return f"{size:.0f}{units[-1]}"

#파일 속성을 가져오는 함수
def get_file_attributes(file_path):
    try:
        file_attributes = win32api.GetFileAttributes(file_path)
        return file_attributes
    except OSError:
        return 0

#파일 속성을 표시하는 함수
def ShowProperties(self):
    if self.index is not None:
        file_path = self.model.filePath(self.index)
        file_attributes = get_file_attributes(file_path)
        properties_dialog = self.PropertiesDialog(file_path, file_attributes) 
        properties_dialog.accepted.connect(lambda: self.apply_properties(file_path, properties_dialog.file_attributes))
        properties_dialog.exec_()

# #파일 속성을 적용하는 함수
# def apply_properties(file_path, file_attributes):
#     try:
#         if file_attributes & stat.FILE_ATTRIBUTE_READONLY:
#             win32api.SetFileAttributes(file_path, win32con.FILE_ATTRIBUTE_NORMAL)
#         else:
#             win32api.SetFileAttributes(file_path, win32con.FILE_ATTRIBUTE_READONLY)
#         return True, "속성이 성공적으로 적용되었습니다."
#     except OSError as e:
#         return False, f"속성 적용 중 오류가 발생했습니다: {str(e)}"
