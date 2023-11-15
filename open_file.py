import os
from PyQt5.QtWidgets import QMessageBox 

def open_item(model, index):
    if index.isValid() and index.column() == 0:
        item_path = model.filePath(index)
        if model.isDir(index):
            # 디렉토리일 경우 해당 디렉토리 열기
            model.tv1.setRootIndex(index)
            model.tv1.scrollTo(index, QTreeView.PositionAtCenter)
        else:
            # 파일일 경우 파일 열기
            try:
                os.startfile(item_path)
            except Exception as e:
                QMessageBox.warning(model, "오류", "파일을 열 수 없습니다.")
