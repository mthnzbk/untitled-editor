from PyQt5.QtWidgets import (QInputDialog, QAbstractItemView, QFileSystemModel, QTreeView,
                             QMenu, QAction, QMessageBox, qApp)
from PyQt5.QtGui import QCursor, QKeyEvent
from PyQt5.QtCore import Qt, QFile
import posixpath
from .settings import Settings



class ProjectTree(QTreeView):

    hide_file_and_folder = [".git", "__pycache__", ".project.json"]
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
        self.expanded.connect(self.expandControl)
        self.collapsed.connect(self.collapseControl)
        self.clicked.connect(self.renameState)


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
            file = QFile.rename(self.model().filePath(self.currentIndex()),
                                posixpath.join(posixpath.dirname(self.model().filePath(self.currentIndex())), new_file_name))


            if file:
                self.model().fileRenamed.emit(posixpath.dirname(self.model().filePath(self.currentIndex())),
                                              self.model().fileName(self.currentIndex()), new_file_name)

            else:
                QMessageBox.warning(self, self.tr("Warning"), self.tr("Cannot rename"))


    def remove(self):
        selected = self.selectedIndexes()
        if len(selected) > 1:
            msg = QMessageBox.question(self, self.tr("Delete"),
                                       self.tr("Delete {} files").format(len(selected)))

        else:
            msg = QMessageBox.question(self, self.tr("Delete"), self.tr("Delete file \"{}\"").format(self.currentIndex().data()))

        if msg == QMessageBox.Yes:
            for index in selected:
                self.model().remove(index)


    def renameControl(self, path, oldName, newName):
        old_file = posixpath.join(path, oldName)
        new_file = posixpath.join(path, newName)
        if old_file in self.parent.tabwidget.open_files:
            index = self.parent.tabwidget.open_files.index(old_file)
            self.parent.tabwidget.open_files[index] = new_file
            self.parent.tabwidget.widget(index).file_path = new_file
            self.parent.tabwidget.setTabText(index, newName)

    def renameState(self):
        if len(self.selectedIndexes()) > 1:
            self.renameAction.setDisabled(True)

        else:
            self.renameAction.setDisabled(False)


    def keyPressEvent(self, event):
        self.renameState()
        super().keyPressEvent(event)

    def openTerminal(self):
        if not self.model().isDir(self.currentIndex()):
            dir = posixpath.dirname(self.model().filePath(self.currentIndex()))

        else:
            dir = self.model().filePath(self.currentIndex())



    # Çift tıklama ile rename özelliği pasif edildi.
    def edit(self, index, trigger, event):
        if trigger == QAbstractItemView.DoubleClicked:
            return False

        if isinstance(event, QKeyEvent):

            if event.key() == Qt.Key_F2:
                return False

        return QTreeView.edit(self, index, trigger, event)

    def expandControl(self, index):
        expand = self.model().filePath(index)
        s = Settings()
        project_settings = Settings(posixpath.join(s["open_project"], ".project.json"))
        if project_settings["open_project_folder"]:
            project_settings["open_project_folder"].append(expand)
            project_settings["open_project_folder"] = list(set(project_settings["open_project_folder"]))
            project_settings.write()

        else:
            project_settings["open_project_folder"] = [expand]


    def collapseControl(self, index):
        collapse = self.model().filePath(index)
        s = Settings()
        project_settings = Settings(posixpath.join(s["open_project"], ".project.json"))
        if project_settings["open_project_folder"]:
            project_settings["open_project_folder"].remove(collapse)
            project_settings.write()


    def setProject(self, folder):
        self.project_path = folder
        self.model().setRootPath(self.project_path)
        self.setRootIndex(self.model().index(self.project_path))

        self.setColumnHidden(1, True)
        self.setColumnHidden(2, True)
        self.setColumnHidden(3, True)

        for tab in list(range(self.parent.tabwidget.count())):
            qApp.processEvents()
            self.parent.tabwidget.removeTab(0)

        s = Settings()
        s["open_project"] = folder
        project_settings = Settings(posixpath.join(s["open_project"], ".project.json"))

        if project_settings["open_project_folder"]:
            for path in project_settings["open_project_folder"]:
                index = self.model().index(path)
                self.expand(index)

        if project_settings["open_tabs"]:
            for tab in project_settings["open_tabs"]:
                self.parent.tabwidget.addFileTab(tab)

            self.parent.tabwidget.setCurrentIndex(project_settings["open_tab"])

    def project(self): return self.project_path