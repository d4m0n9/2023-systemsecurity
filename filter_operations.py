from PyQt5.QtWidgets import QInputDialog, QLineEdit

def filter_by_ext(model):
    text, res = QInputDialog.getText(None, "확장자별 필터링", "필터링할 확장자를 입력하세요. (예:.txt)", QLineEdit.Normal)
    if res:
        ext_filter_list = ["*" + text] 
        model.setNameFilters(ext_filter_list)
