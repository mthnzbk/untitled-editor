from PyQt5.QtWidgets import (QApplication, qApp, QWidget, QMenu, QMenuBar, QAction, QTabWidget,
                             QSplitter, QGridLayout, QHBoxLayout, QVBoxLayout, QTreeWidget, QTreeWidgetItem,
                             QInputDialog, QPushButton, QFileDialog)
from PyQt5.QtGui import QIcon, QFont, QColor, QGuiApplication, QDesktopServices
from PyQt5.QtCore import Qt, QIODevice, QCoreApplication, QUrl, QProcess
from PyQt5.Qsci import *
from editor.editor import Editor
from editor.projecttree import ProjectTree
from editor.settings import settings, Settings
from editor.mainwindow import EditorWindow
import rs
import sys


class Window(EditorWindow):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon("logo.png"))

        if not self.tabwidget.count():
            self.saveFileAction.setDisabled(True)
            self.saveAsAction.setDisabled(True)
            self.saveAllAction.setDisabled(True)
            self.closeFileAction.setDisabled(True)
            self.undoAction.setDisabled(True)
            self.redoAction.setDisabled(True)
            self.copyAction.setDisabled(True)
            self.cutAction.setDisabled(True)
            self.pasteAction.setDisabled(True)
            self.findAction.setDisabled(True)
            self.findNextAction.setDisabled(True)
            self.findPreviousAction.setDisabled(True)
            self.replaceAction.setDisabled(True)
            self.replaceNextAction.setDisabled(True)
            self.runAction.setDisabled(True)
            self.runWithAction.setDisabled(True)



        # self.newFileAction.triggered.connect(self.newFile) #TODO menu oldu
        self.openFileAction.triggered.connect(self.openFile)
        self.openProjectAction.triggered.connect(self.openProject)
        self.saveFileAction.triggered.connect(self.saveFile)
        self.saveAsAction.triggered.connect(self.saveAsFile)
        self.closeFileAction.triggered.connect(self.closeFile)
        self.closeAllFilesAction.triggered.connect(self.closeAllFiles)

        self.newWindowAction.triggered.connect(self.newWindow)
        self.closeWindowAction.triggered.connect(self.close)
        self.exitAction.triggered.connect(qApp.quit)

        self.undoAction.triggered.connect(self.undo)
        self.redoAction.triggered.connect(self.redo)
        self.copyAction.triggered.connect(self.copy)
        self.cutAction.triggered.connect(self.cut)
        self.pasteAction.triggered.connect(self.paste)


        self.runAction.triggered.connect(self.runScript)
        self.runWithAction.triggered.connect(self.runWithScript)


        self.documentationAction.triggered.connect(self.documentation)
        self.tabwidget.currentChanged.connect(self.tabChangeCommit)
        self.init()




    def init(self):
        s = Settings()

        if s["open_project"]:
            self.projectTree.setProject(s["open_project"])

        if s["open_tabs"]:
            for tab in s["open_tabs"]:
                self.tabwidget.addFileTab(tab)

            self.tabwidget.setCurrentIndex(s["open_tab"])


    def tabChangeCommit(self, index):
        self.setWindowTitle(self.tabwidget.tabText(index))

        if self.tabwidget.count():
            self.saveFileAction.setEnabled(True)
            self.saveAsAction.setEnabled(True)
            self.saveAllAction.setEnabled(True)
            self.closeFileAction.setEnabled(True)
            self.copyAction.setEnabled(True)
            self.cutAction.setEnabled(True)
            self.pasteAction.setEnabled(True)
            self.findAction.setEnabled(True)
            self.findNextAction.setEnabled(True)
            self.findPreviousAction.setEnabled(True)
            self.replaceAction.setEnabled(True)
            self.replaceNextAction.setEnabled(True)
            self.runAction.setEnabled(True)
            self.runWithAction.setEnabled(True)

            self.undoAction.setEnabled(self.tabwidget.widget(index).isUndoAvailable())
            self.redoAction.setEnabled(self.tabwidget.widget(index).isRedoAvailable())
            # self.copyAction.setEnabled(self.tabwidget.widget(index).copyAvailable())
        else:
            self.undoAction.setEnabled(False)
            self.redoAction.setEnabled(False)


    def newFile(self):
        f, ok = QFileDialog.getSaveFileName(self)
        if ok:
            self.tabwidget.addFileTab(f, QIODevice.WriteOnly)

    def openFile(self):
        f, ok = QFileDialog.getOpenFileName(self)
        if ok:
            self.tabwidget.addFileTab(f)

            if Settings()["open_recent_files"]:
                s = Settings()
                s["open_recent_files"].insert(0, f)
                s.write()

            else:
                Settings()["open_recent_files"] = [ f]

    def openProject(self):
        folder = QFileDialog.getExistingDirectory(self)
        if folder:
            self.projectTree.setProject(folder)

            if Settings()["open_recent_projects"]:
                s = Settings()
                s["open_recent_projects"].insert(0, folder)
                s.write()

            else:
                Settings()["open_recent_projects"] = [folder]

    def saveFile(self):
        self.tabwidget.currentWidget().fileSave.emit()

    def saveAsFile(self):
        f, ok = QFileDialog.getSaveFileName(self)

        if ok:
            self.tabwidget.currentWidget().file_path = f
            self.tabwidget.setTabText(self.tabwidget.currentIndex(), f.split("/")[-1])

    def closeFile(self):
        self.tabwidget.tabBar().tabCloseRequested.emit(self.tabwidget.currentIndex())

    def closeAllFiles(self):
        for tab in list(range(self.tabwidget.count())):
            qApp.processEvents()
            self.tabwidget.removeTab(0)


    def newWindow(self):
        Window().show()

    def undo(self):
        self.tabwidget.currentWidget().undo()

    def redo(self):
        self.tabwidget.currentWidget().redo()

    def copy(self):
        self.tabwidget.currentWidget().copy()

    def cut(self):
        self.tabwidget.currentWidget().cut()

    def paste(self):
        self.tabwidget.currentWidget().paste()


    def runScript(self):
        QProcess(self).start("python", [self.tabwidget.currentWidget().file_path])

    def runWithScript(self):
        text, ok = QInputDialog.getText(self, self.tr("Parametre(ler) girin:"), self.tr("Parametreler:"))

        if ok:
            param = [self.tabwidget.currentWidget().file_path]
            param.extend(text.split(" "))
            QProcess(self).start("python", param)


    def documentation(self):
        QDesktopServices.openUrl(QUrl("https://untitlededitor.com/documentation"))


    def closeEvent(self, event):
        super().closeEvent(event)
        s = Settings()
        if self.tabwidget.count():
            tab_list = []

            for index in list(range(self.tabwidget.count())):
                tab = self.tabwidget.widget(index)
                tab_list.append(tab.file_path)

            s["open_tabs"] = tab_list
            s["open_tab"] = self.tabwidget.currentIndex()

        else:
            s["open_tabs"] = []
            s["open_tab"] = None

        if self.projectTree.project():
            s["open_project"] = self.projectTree.project()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    QCoreApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    window = Window()
    window.show()
    sys.exit(app.exec_())