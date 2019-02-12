from PyQt5.Qsci import *
from PyQt5.QtGui import QKeySequence, QColor, QFont, QBrush, QPen, QPainter, QFontMetrics, QKeyEvent
from PyQt5.QtCore import QSize, QFile, QTextStream, QIODevice, Qt, pyqtSignal, QTimer
from PyQt5.QtWidgets import QMenu, QAction
import sys


class Editor(QsciScintilla):

    saveState = None
    fileSave = pyqtSignal()

    def __init__(self, parent=None, file_path=None, mode=QIODevice.ReadOnly):
        super().__init__()
        self.parent = parent
        self.file_path = file_path
        self.file_mode = mode
        self.font = QFont("Monaco")
        self.font.setPointSize(10)
        self.setFont(self.font)

        self.setEolVisibility(False)
        self.setEdgeMode(QsciScintilla.EdgeBackground)
        self.setEdgeColumn(120)
        self.setIndentationsUseTabs(False)
        self.setIndentationGuides(True)
        self.setTabIndents(True)
        self.setAutoIndent(True)
        self.setAutoCompletionCaseSensitivity(False)
        self.setAutoCompletionThreshold(2)
        self.setAutoCompletionReplaceWord(True)
        self.setAutoCompletionSource(QsciScintilla.AcsAll)
        self.setCaretLineVisible(True)
        self.setCaretLineBackgroundColor(QColor("#abc"))
        self.setFolding(QsciScintilla.CircledFoldStyle)
        self.setMarginType(0, QsciScintilla.NumberMargin)
        self.setMarginWidth(0, 48)
        self.setMarginMarkerMask(1, 0b00010)
        self.setUtf8(True)
        # sym_0 = QImage("point.png").scaled(QSize(16, 16))
        # self.markerDefine(sym_0, 0)
        # self.markerDefine(sym_0, 1)
        # self.edit.setMarginLineNumbers(0, True)
        # self.marginClicked.connect(lambda x, y, z: self.markerAdd(y, x))
        # self.setMarginSensitivity(1, True)
        # print(self.markerAdd(1, 1))
        # self.setMarginBackgroundColor(1, QColor("#abc"))
        self.setMarginType(1, QsciScintilla.SymbolMargin)
        self.setMarginWidth(1, "000")

        self.setTabWidth(4)
        if sys.platform == "win32":
            self.setEolMode(QsciScintilla.EolWindows)
        elif sys.platform == "linux":
            self.setEolMode(QsciScintilla.EolUnix)
        elif sys.platform == "darwin":
            self.setEolMode(QsciScintilla.EolMac)


        self.lexerSelect()

        self.file = QFile(self.file_path)
        if self.file.open(self.file_mode | QIODevice.Text):
            text = QTextStream(self.file)
            text.setCodec("UTF-8")
            self.setText(text.readAll())

        self.autosave_timer = QTimer(self)
        self.autosave_timer.timeout.connect(self.autoSaveCommit)
        self.autosave_timer.start(5000)


        self.windowTitleChanged.connect(self.tabTextChange)
        self.textChanged.connect(self.saveStateControl)
        self.fileSave.connect(self._fileSave)

    def autoSaveCommit(self):
        if not self.saveState and self.saveState != None:
            self._fileSave()


    def saveStateControl(self):
        self.parent.parent.undoAction.setEnabled(self.isUndoAvailable())
        self.parent.parent.redoAction.setEnabled(self.isRedoAvailable())
        self.saveState = False


    def _fileSave(self):
        file = QFile(self.file_path)
        if file.open(QIODevice.WriteOnly | QIODevice.Text):
            file.write(bytes(self.text(), encoding="utf-8"))
            file.flush()
            file.close()

        self.saveState = True


    def lexerSelect(self):
        if self.file_path:
            file_type = self.file_path.split(".")[-1]
            file_name = self.file_path.split("/")[-1]
            self.setWindowTitle(file_name)

            if file_type == "py":
                lex = QsciLexerPython()
                lex.setFont(self.font)
                self.setLexer(lex)

            elif file_type == "css":
                lex = QsciLexerCSS()
                lex.setFont(self.font)
                self.setLexer(lex)

            elif file_type == "js":
                lex = QsciLexerJavaScript()
                lex.setFont(self.font)
                self.setLexer(lex)

            elif file_type == "md":
                lex = QsciLexerMarkdown()
                lex.setFont(self.font)
                self.setLexer(lex)

            elif file_type == "json":
                lex = QsciLexerJSON()
                lex.setFont(self.font)
                self.setLexer(lex)

            elif file_type == "yaml":
                lex = QsciLexerYAML()
                lex.setFont(self.font)
                self.setLexer(lex)

            elif file_type == "html":
                lex = QsciLexerHTML()
                lex.setFont(self.font)
                self.setLexer(lex)

            else:
                self.setLexer(None)



    def contextMenuEvent(self, event):
        menu = QMenu()

        return self.parent.parent.editMenu.exec(event.globalPos())

    def tabTextChange(self, title):
        index = self.parent.indexOf(self)
        self.parent.setTabText(index, title)


    def paintEvent(self, event):
        super().paintEvent(event)
        # f = QFont("Monaco")
        # f.setPointSize(10)
        painter = QPainter(self.viewport())
        # painter.begin(self.viewport())
        painter.setPen(QPen(QColor("#0000ff")))
        point = QFontMetrics(self.font).averageCharWidth() * 120
        painter.drawLine(point + self.marginWidth(0) + self.marginWidth(1) + self.marginWidth(2), 0,
                         point + self.marginWidth(0) + self.marginWidth(1) + self.marginWidth(2), self.height())
        # painter.end()
