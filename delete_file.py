def open_item(self, index):
    if index.isValid() and index.column() == 0:
        item_path = self.model.filePath(index)
        if self.model.isDir(index):
            self.tv1.setRootIndex(index)
            self.tv1.scrollTo(index, QTreeView.PositionAtCenter)
        else:
            try:
                os.startfile(item_path)
            except Exception as e:
                QMessageBox.warning(self, "오류", "파일을 열 수 없습니다.")
