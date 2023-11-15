from PyQt5.QtCore import Qt
 
def sort_by_ext(model):
    model.sort(0, Qt.AscendingOrder)
