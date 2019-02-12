from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem, QAbstractItemView
from PyQt5.QtCore import Qt


class ProjectTree(QTreeWidget):

    hide_file_and_folder = [".git", ".workspace"]

    def __init__(self, parent=None):
        super().__init__()
        self.headerItem().setText(0, self.tr("Project"))
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDragDropMode(QAbstractItemView.DragDrop)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.setAnimated(True)
        self.setHeaderHidden(True)


