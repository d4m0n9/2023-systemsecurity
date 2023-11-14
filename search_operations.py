import os
from PyQt5.QtWidgets import QInputDialog, QLineEdit, QMessageBox

def search_file():
    text, res = QInputDialog.getText(None, "파일 검색", "검색할 파일 이름을 입력하세요.", QLineEdit.Normal)
    if res:
        for root, dirs, files in os.walk('/'):
            if text in files:
                QMessageBox.information(None,"파일 위치",os.path.join(root,text))
                return
        QMessageBox.warning(None,"오류","찾는 파일이 없습니다.")
