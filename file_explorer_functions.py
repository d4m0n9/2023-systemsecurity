# 파일 탐색기 관련 기능 (파일 열기, 이름 변경, 삭제, 확장자/날짜별 정렬, 확장자별 필터링, 파일 검색)
import os
import shutil
from PyQt5.QtWidgets import QInputDialog, QLineEdit, QMessageBox, QTreeView, QVBoxLayout, QDialog, QLabel
from PyQt5.QtCore import Qt, QStorageInfo, QUrl
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import QFileInfo

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
def OpenItem(main):
    if main.index.isValid():
        if main.model.isDir(main.index):
            main.tv.setRootIndex(main.index)
            main.tv.scrollTo(main.index, QTreeView.PositionAtCenter)
        else:
            item_path = main.model.filePath(main.index)
            url = QUrl.fromLocalFile(item_path)
            QDesktopServices.openUrl(url)

# 파일 속성 표시
def ShowFileProperties(main):
    if main.index is not None:
        file_info = QFileInfo(main.model.filePath(main.index))
        file_path = file_info.filePath()  # 파일의 경로 얻음
        attributes = {
        "파일 경로(위치)": file_path,
        "만든 날짜": file_info.created().toString(Qt.DefaultLocaleLongDate),
        "수정한 날짜": file_info.lastModified().toString(Qt.DefaultLocaleLongDate),
        "엑세스한 날짜": file_info.lastRead().toString(Qt.DefaultLocaleLongDate),
        "크기": file_info.size(),
        "디스크 할당 크기": GetDiskAllocationSize(file_path)  # 파일의 디스크 할당 크기 얻음
        }
        
        dialog = QDialog(main)
        dialog.setWindowTitle("속성")
        layout = QVBoxLayout()
        for key, value in attributes.items():
            label = QLabel(key + ": " + str(value))
            layout.addWidget(label)
        dialog.setLayout(layout)
        dialog.show()
        
# 디스크 할당 크기 얻기       
def GetDiskAllocationSize(file_path):
    storage_info = QStorageInfo(file_path)
    allocation_size = storage_info.bytesTotal()
    return allocation_size