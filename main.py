from PyQt5.QtWidgets import (QApplication, qApp, QWidget, QMenu, QMenuBar, QAction, QTabWidget,
                             QSplitter, QGridLayout, QHBoxLayout, QVBoxLayout, QTreeWidget, QTreeWidgetItem,
                             QInputDialog, QPushButton, QFileDialog)
from PyQt5.QtGui import QIcon, QFont, QColor, QGuiApplication, QDesktopServices
from PyQt5.QtCore import Qt, QIODevice, QCoreApplication, QUrl, QProcess, QDir, QFile
from PyQt5.Qsci import *
from editor.editor import Editor
from editor.projecttree import ProjectTree
from editor.settings import settings, Settings
from editor.mainwindow import EditorWindow
import rs
import sys
import posixpath


class Window(EditorWindow):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon("logo.png"))

        if not self.tabwidget.count():
            self.saveFileAction.setDisabled(True)
            self.saveAsAction.setDisabled(True)
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



        self.newPythonFileAction.triggered.connect(self.newCreate)
        self.newDirectoryAction.triggered.connect(self.newCreate)
        self.newPythonPackageAction.triggered.connect(self.newCreate)
        self.newHtmlFileAction.triggered.connect(self.newCreate)
        self.newCssFileAction.triggered.connect(self.newCreate)
        self.newJsFileAction.triggered.connect(self.newCreate)
        self.newJsonFileAction.triggered.connect(self.newCreate)
        self.newXmlFileAction.triggered.connect(self.newCreate)
        self.newYamlFileAction.triggered.connect(self.newCreate)
        self.newSqlFileAction.triggered.connect(self.newCreate)
        self.newMdFileAction.triggered.connect(self.newCreate)

        self.newProjectAction.triggered.connect(self.newProject)
        self.openFileAction.triggered.connect(self.openFile)
        self.openProjectAction.triggered.connect(self.openProject)
        self.saveFileAction.triggered.connect(self.saveFile)
        self.saveAsAction.triggered.connect(self.saveAsFile)
        self.closeFileAction.triggered.connect(self.closeFile)
        self.closeAllFilesAction.triggered.connect(self.closeAllFiles)
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

            project_settings = Settings(posixpath.join(s["open_project"], ".project.json"))
            if project_settings["open_tabs"]:
                for tab in project_settings["open_tabs"]:
                    self.tabwidget.addFileTab(tab)

                self.tabwidget.setCurrentIndex(project_settings["open_tab"])

        else:
            self.newFileActionMenu.setDisabled(True)

        self.openRecentMenuUpdate()


    def tabChangeCommit(self, index):
        self.setWindowTitle(self.tabwidget.tabText(index))

        if self.tabwidget.count():
            self.saveFileAction.setEnabled(True)
            self.saveAsAction.setEnabled(True)
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
        else:
            self.undoAction.setEnabled(False)
            self.redoAction.setEnabled(False)

    def newProject(self):
        text, ok = QInputDialog.getText(self, self.tr("Project"), self.tr("Project Path"),
                                        text=posixpath.join(QDir.homePath(), "PythonProjects", "untitled"))

        print(text, ok)
        if ok:
            mk = QDir().mkpath(text)
            print(mk)
            if mk:
                self.projectTree.setProject(text)


    def newCreate(self):
        path = posixpath.dirname(posixpath.join(self.projectTree.model().filePath(self.projectTree.currentIndex())))
        if path == "": path = self.projectTree.project()

        if self.sender() == self.newPlainFileAction:
            text, ok = QInputDialog.getText(self, self.tr("New File"), self.tr("Name"))
            if ok:
                self.tabwidget.addFileTab(posixpath.join(path, text))

        if self.sender() == self.newPythonFileAction:
            text, ok = QInputDialog.getText(self, self.tr("New Python File"), self.tr("Name"))
            if ok:
                if text.split(".")[-1] != ("py" or "pyw"): text += ".py"
                self.tabwidget.addFileTab(posixpath.join(path, text))

        if self.sender() == self.newDirectoryAction:
            text, ok = QInputDialog.getText(self, self.tr("New Directory"), self.tr("Name"))
            if ok:
                QDir().mkdir(posixpath.join(path, text))

        if self.sender() == self.newPythonPackageAction:
            text, ok = QInputDialog.getText(self, self.tr("New Python Package"), self.tr("Name"))
            if ok:
                QDir().mkdir(posixpath.join(path, text))
                f = QFile(posixpath.join(path, text, "__init__.py"))
                f.open(QIODevice.WriteOnly)
                f.close()

        if self.sender() == self.newHtmlFileAction:
            text, ok = QInputDialog.getText(self, self.tr("New Html File"), self.tr("Name"))
            if ok:
                if text.split(".")[-1] != "html": text += ".html"
                self.tabwidget.addFileTab(posixpath.join(path, text))

        if self.sender() == self.newCssFileAction:
            text, ok = QInputDialog.getText(self, self.tr("New Css File"), self.tr("Name"))
            if ok:
                if text.split(".")[-1] != "css": text += ".css"
                self.tabwidget.addFileTab(posixpath.join(path, text))

        if self.sender() == self.newJsFileAction:
            text, ok = QInputDialog.getText(self, self.tr("New JavaScript File"), self.tr("Name"))
            if ok:
                if text.split(".")[-1] != "js": text += ".js"
                self.tabwidget.addFileTab(posixpath.join(path, text))

        if self.sender() == self.newJsonFileAction:
            text, ok = QInputDialog.getText(self, self.tr("New Json File"), self.tr("Name"))
            if ok:
                if text.split(".")[-1] != "json": text += ".json"
                self.tabwidget.addFileTab(posixpath.join(path, text))

        if self.sender() == self.newXmlFileAction:
            text, ok = QInputDialog.getText(self, self.tr("New Xml File"), self.tr("Name"))
            if ok:
                if text.split(".")[-1] != "xml": text += ".xml"
                self.tabwidget.addFileTab(posixpath.join(path, text))

        if self.sender() == self.newYamlFileAction:
            text, ok = QInputDialog.getText(self, self.tr("New Yaml File"), self.tr("Name"))
            if ok:
                if text.split(".")[-1] != "yaml": text += ".yaml"
                self.tabwidget.addFileTab(posixpath.join(path, text))

        if self.sender() == self.newMdFileAction:
            text, ok = QInputDialog.getText(self, self.tr("New Markdown File"), self.tr("Name"))
            if ok:
                if text.split(".")[-1] != "md": text += ".md"
                self.tabwidget.addFileTab(posixpath.join(path, text))

        if self.sender() == self.newSqlFileAction:
            text, ok = QInputDialog.getText(self, self.tr("New Sqlite File"), self.tr("Name"))
            if ok:
                if text.split(".")[-1] != "sql": text += ".sql"
                self.tabwidget.addFileTab(posixpath.join(path, text))

    def openFile(self):
        f, ok = QFileDialog.getOpenFileName(self)
        if ok:
            self.tabwidget.addFileTab(f)


    def openProject(self):
        folder = QFileDialog.getExistingDirectory(self)
        if folder:
            self.projectTree.setProject(folder)

            if Settings()["open_recent_projects"]:
                s = Settings()
                s["open_recent_projects"].insert(0, folder)
                s["open_recent_projects"] = list(set(s["open_recent_projects"]))
                s.write()

            else:
                Settings()["open_recent_projects"] = [folder]

            self.openRecentMenuUpdate()

    def openRecentMenuUpdate(self):
        self.openRecentFileActionMenu.clear()
        s = Settings()
        for project in s["open_recent_projects"]:
            act = QAction(self.tr(project.split("/")[-1]), self)
            act.setProperty("projectPath", project)
            act.triggered.connect(self.openRecent)
            self.openRecentFileActionMenu.addAction(act)

    def openRecent(self):
        self.projectTree.setProject(self.sender().property("projectPath"))

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

        if self.projectTree.project():
            s["open_project"] = self.projectTree.project()

            project_settings = Settings(posixpath.join(s["open_project"], ".project.json"))

            if self.tabwidget.count():
                tab_list = []

                for index in list(range(self.tabwidget.count())):
                    tab = self.tabwidget.widget(index)
                    tab_list.append(tab.file_path)

                project_settings["open_tabs"] = tab_list
                project_settings["open_tab"] = self.tabwidget.currentIndex()

            else:
                project_settings["open_tabs"] = []
                project_settings["open_tab"] = None





if __name__ == "__main__":
    app = QApplication(sys.argv)
    QCoreApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    window = Window()
    window.show()
    sys.exit(app.exec_())