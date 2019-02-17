from PyQt5.QtWidgets import QTabWidget, QTabBar
from PyQt5.QtCore import Qt, QIODevice
from editor.editor import Editor


class TabWidget(QTabWidget):

    open_files = []

    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.setMovable(True)
        # self.tabwidget.setTabBarAutoHide(True) # Dikkat!
        self.setTabsClosable(True)
        self.setElideMode(Qt.ElideRight)
        # self.tabwidget.setDocumentMode(True) # Dikkat
        self.setStyleSheet("QTabBar::tab { width: 150px; }")
        self.tabBar().tabCloseRequested.connect(self.removeFileTab)


    def removeFileTab(self, index):
        self.open_files.remove(self.widget(index).file_path)
        self.removeTab(index)

    def addFileTab(self, file_path=None, file_mode=QIODevice.ReadOnly):
        if file_path in self.open_files:
            return

        if file_path:
            index = self.addTab(Editor(self, file_path, file_mode), file_path.split("/")[-1])

        else:
            index = self.addTab(Editor(self, file_path, file_mode), self.tr("untitled"))

        self.open_files.append(file_path)
        self.setCurrentIndex(index)