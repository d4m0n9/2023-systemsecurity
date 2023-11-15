from PyQt5.QtCore import Qt

def sort_by_date(model):
    model.sort(1, Qt.AscendingOrder) 
 
def sort_by_ext(model):
    model.sort(0, Qt.AscendingOrder)
 
