import os
import shutil
from PyQt5.QtWidgets import QInputDialog, QLineEdit, QMessageBox

def open_item(model, index):
    selected_index = index
    if selected_index:
        item_name = model.fileName(selected_index)
        item_path = model.filePath(selected_index)
        try:
            os.startfile(item_path)
        except Exception as e:
            QMessageBox.warning(None, "오류", "파일을 열 수 없습니다")
    
def rename_file(model, index):
    os.chdir(model.filePath(model.parent(index)))
    fname = model.fileName(index)
    text, res = QInputDialog.getText(None, "이름 바꾸기", "바꿀 이름을 입력하세요.", QLineEdit.Normal, fname)

    if res:
        while True:
            ok = True
            for i in os.listdir(os.getcwd()):
                if i == text:
                    text, res = QInputDialog.getText(None, "중복 오류", "바꿀 이름을 입력하세요", QLineEdit.Normal, text)
                    if not res:
                        return
                    ok = False
                if ok:
                    break
        os.rename(fname, text)

def remove_file(model, index):
    os.chdir(model.filePath(model.parent(index)))
    fname = model.fileName(index)
    try:
        if not model.isDir(index):
            os.unlink(fname)
        else:
            shutil.rmtree(fname)
    except Exception as e:
        print("Error:", e)
