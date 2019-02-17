from PyQt5.QtWidgets import (QTreeWidget, QInputDialog, QAbstractItemView, QFileSystemModel, QTreeView,
                             QMenu, QAction, QMessageBox)
from PyQt5.QtGui import QIcon, QCursor
from PyQt5.QtCore import Qt, QDir, QFile
import os
import posixpath



class ProjectTree(QTreeView):

    hide_file_and_folder = [".git", ".workspace"]
    project_path = None

    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.setModel(QFileSystemModel())
        self.model().setReadOnly(False)
        self.setDragEnabled(True)
        self.viewport().setAcceptDrops(True)
        self.setDragDropMode(QAbstractItemView.InternalMove)
        self.setDefaultDropAction(Qt.MoveAction)
        self.setDropIndicatorShown(True)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.contextMenu)
        self.setAnimated(True)
        self.setHeaderHidden(True)

        # context menu actions

        self.renameAction = QAction(self.tr("Rename"))
        self.renameAction.setShortcut("F2")
        self.renameAction.setShortcutVisibleInContextMenu(True)
        self.addAction(self.renameAction)

        self.deleteAction = QAction(self.tr("Delete"), self)
        self.deleteAction.setShortcut("Delete")
        self.deleteAction.setShortcutVisibleInContextMenu(True)
        self.addAction(self.deleteAction)

        self.openTerminalAction = QAction(self.tr("Open in Terminal"))

        self.renameAction.triggered.connect(self.rename)
        self.deleteAction.triggered.connect(self.remove)
        self.openTerminalAction.triggered.connect(self.openTerminal)
        self.doubleClicked.connect(self.openFile)
        self.model().fileRenamed.connect(self.renameControl)


    def openFile(self, model):

        if not self.model().isDir(model):
            self.parent.tabwidget.addFileTab(self.model().filePath(model))

    def contextMenu(self):
        menu = QMenu(self)
        menu.addMenu(self.parent.newFileActionMenu)
        menu.addSeparator()
        menu.addAction(self.renameAction)
        menu.addAction(self.deleteAction)
        menu.addSeparator()
        menu.addAction(self.openTerminalAction)

        cursor = QCursor()
        return menu.exec(cursor.pos())


    def rename(self):
        file_name = self.model().fileName(self.currentIndex())
        new_file_name, ok = QInputDialog.getText(self, self.tr("Rename"), self.tr(f"Rename file \"{file_name}\" and its usages to:"),
                                   text=file_name)

        if ok:
            file = QFile(self.model().filePath(self.currentIndex()))
            rename_ok = file.rename(new_file_name)
            if rename_ok:
                self.model().fileRenamed.emit(posixpath.dirname(self.model().filePath(self.currentIndex())),
                                              self.model().fileName(self.currentIndex()), new_file_name)

            else:
                QMessageBox.warning(self, self.tr("Warning"), self.tr("Cannot rename"))


    def remove(self):
        msg = QMessageBox.question(self, self.tr("Delete"), self.tr("Delete file \"{}\"").format(self.currentIndex().data()))
        if msg == QMessageBox.Yes:
            self.model().remove(self.currentIndex())


    def renameControl(self, path, oldName, newName):
        old_file = posixpath.join(path, oldName)
        new_file = posixpath.join(path, newName)
        if old_file in self.parent.tabwidget.open_files:
            index = self.parent.tabwidget.open_files.index(old_file)
            self.parent.tabwidget.open_files[index] = new_file
            self.parent.tabwidget.widget(index).file_path = new_file
            self.parent.tabwidget.setTabText(index, newName)


    def openTerminal(self):
        if not self.model().isDir(self.currentIndex()):
            dir = posixpath.dirname(self.model().filePath(self.currentIndex()))

        else:
            dir = self.model().filePath(self.currentIndex())

        print(dir)


    def edit(self, index, trigger, event):
        if trigger == QAbstractItemView.DoubleClicked:
            return False

        return QTreeView.edit(self, index, trigger, event)

    def setProject(self, folder):
        self.project_path = folder
        # model.setNameFilters(["__pycache__/", ".git/"])
        # model.setNameFilterDisables(False)
        self.model().setRootPath(self.project_path)
        self.setRootIndex(self.model().index(self.project_path))

        self.setColumnHidden(1, True)
        self.setColumnHidden(2, True)
        self.setColumnHidden(3, True)

        # folder_item = QTreeWidgetItem()
        # folder_item.setText(0, folder.split("/")[-1])
        # folder_item.setIcon(0, QIcon(":/img/folder.svg"))
        # file_item = QTreeWidgetItem()
        # file_item.setText(0, "file.py")
        # file_item.setIcon(0, QIcon(":/img/text-python.svg"))
        # folder_item.addChild(file_item)
        # self.addTopLevelItem(folder_item)

    def project(self): return self.project_path