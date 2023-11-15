import os
from PyQt5.QtWidgets import QInputDialog, QLineEdit

def rename_item(model, index):
    os.chdir(model.filePath(model.parent(index)))
    fname = model.fileName(index) 
    text, res = QInputDialog.getText(model, "이름 바꾸기", "바꿀 이름을 입력하세요.", QLineEdit.Normal, fname)

    if res:
        while True:
            ok = True
            for i in os.listdir(os.getcwd()):
                if i == text:
                    text, res = QInputDialog.getText(model, "중복 오류", "바꿀 이름을 입력하세요", QLineEdit.Normal, text)
                    if not res:
                        return
                    ok = False
            if ok:
                break
        os.rename(fname, text)
