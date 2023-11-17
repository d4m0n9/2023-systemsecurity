import os
import shutil
from PyQt5.QtWidgets import QInputDialog, QLineEdit, QMessageBox, QTreeView
from PyQt5.QtCore import Qt
# 파일 탐색기 관련 기능 (파일 열기, 이름 변경, 삭제, 확장자/날짜별 정렬, 확장자별 필터링, 파일 검색)

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

# 파일 확장자별 정렬
def SortByExt(main):
    main.model.sort(2, Qt.AscendingOrder)

# 파일 수정 날짜순 정렬
def SortByDate(main):
    main.model.sort(3, Qt.DescendingOrder)

# 사용자가 입력한 특정 확장자를 가진 파일 필터링하여 표시
def FilterByExt(main):
    text, res = QInputDialog.getText(main, "확장자별 필터링", "필터링할 확장자를 입력하세요. (예:.txt)", QLineEdit.Normal)
    if res:
        ext_filter_list=["*" + text]
        main.model.setNameFilters(ext_filter_list)

# 사용자가 입력한 파일 이름 검색
def SearchFile(main):
    text, res = QInputDialog.getText(main, "파일 검색", "검색할 파일 이름을 입력하세요.", QLineEdit.Normal)
    if res:
        root_index = main.tv.rootIndex()
        SearchInDirectory(main, root_index, text)

# 특정 디렉토리 내에서 파일을 검색하는 기능 수행
def SearchInDirectory(main, index, text):
    for i in range(main.model.rowCount(index)):
        child_index = main.model.index(i, 0, index)
        if main.model.fileName(child_index).lower().startswith(text.lower()):
            main.tv.scrollTo(child_index, QTreeView.PositionAtCenter)
            main.tv.setCurrentIndex(child_index)
            return
        if main.model.hasChildren(child_index):
            SearchInDirectory(main, child_index, text)