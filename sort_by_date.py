from PyQt5.QtCore import Qt

def sort_by_date(model):
    model.sort(1, Qt.AscendingOrder)
