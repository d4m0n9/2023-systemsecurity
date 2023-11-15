import os
import shutil 
from PyQt5.QtWidgets import QMessageBox

def delete_item(model, index):
    os.chdir(model.filePath(model.parent(index)))
    fname = model.fileName(index)
    reply = QMessageBox.question(model, '삭제 확인',
                                 f"'{fname}'를 삭제하시겠습니까?",
                                 QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

    if reply == QMessageBox.Yes:
        try:
            if not model.isDir(index):
                os.remove(fname)
                print(fname + ' 파일 삭제')
            else:
                shutil.rmtree(fname)
                print(fname + ' 폴더 삭제')
        except Exception as e:
            print("Error:", e)
