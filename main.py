from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QMenu, QMenuBar, QAction, QActionGroup, QTabWidget,
                             QSplitter, QGridLayout, QHBoxLayout, QVBoxLayout, QTreeWidget, QTreeWidgetItem,
                             QTreeWidgetItemIterator, QStatusBar, QDockWidget)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.Qsci import *
import sys


class EditorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(1280, 720)

        self.setMenuBar(QMenuBar())
        self.menuBar().addMenu(QMenu("asdad", self))
        self.setCentralWidget(QWidget())
        self.setStatusBar(QStatusBar())
        self.centralWidget().setLayout(QHBoxLayout())
        self.centralWidget().layout().setSpacing(0)
        self.centralWidget().layout().setContentsMargins(0, 0, 0, 0)


        self.splitter = QSplitter(self.centralWidget())
        self.centralWidget().layout().addWidget(self.splitter)

        self.treeWidget = QTreeWidget(self.splitter)
        self.treeWidget.hide()
        self.splitter.addWidget(self.treeWidget)

        self.tabwidget = QTabWidget()
        self.edit = QsciScintilla(self.splitter)
        self.tabwidget.addTab(self.edit, "sex")
        self.splitter.addWidget(self.tabwidget)






app = QApplication(sys.argv)
window = EditorWindow()
window.show()
sys.exit(app.exec_())