from PyQt5.QtWidgets import QTreeView, QFileSystemModel
from PyQt5.QtCore import Qt

class TreeView(QTreeView):
    def __init__(self):
        super().__init__()
        self.path = "C:"
        self.model = QFileSystemModel()
        self.set_model()
        self.set_column_width()

    def set_model(self):
        self.model.setRootPath(self.path)
        self.setModel(self.model)

    def set_column_width(self):
        self.setColumnWidth(0, 250)

    def get_selected_index(self):
        return self.selectedIndexes()[0]

    def get_file_name(self, index):
        return self.model.fileName(index)

    def get_file_path(self, index):
        return self.model.filePath(index)

    def get_parent_path(self, index):
        return self.model.filePath(self.model.parent(index))

    def is_dir(self, index):
        return self.model.isDir(index)

    def sort_by_ext(self):
        self.model.sort(2, Qt.AscendingOrder)

    def sort_by_date(self):
        self.model.sort(3, Qt.DescendingOrder)

    def filter_by_ext(self):
        pass
