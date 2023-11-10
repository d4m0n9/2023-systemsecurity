from PyQt5.QtCore import Qt

def sort_by_ext(model):
    model.sort(2, Qt.AscendingOrder)

def sort_by_date(model):
    model.sort(3, Qt.DescendingOrder)
