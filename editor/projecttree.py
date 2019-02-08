from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem


class ProjectTree(QTreeWidget):
    def __init__(self, parent=None):
        super().__init__()
