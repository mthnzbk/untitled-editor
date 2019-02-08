from PyQt5.Qsci import QsciScintilla, QsciLexerPython, QsciAPIs
from PyQt5.QtGui import QImage, QColor, QFont, QBrush, QPen, QPainter, QFontMetrics
from PyQt5.QtCore import QSize
import sys


class Editor(QsciScintilla):
    def __init__(self):
        super().__init__()
        self.setEolVisibility(False)
        self.setEdgeMode(QsciScintilla.EdgeBackground)
        self.setEdgeColumn(80)
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
        self.setMarginType(0, QsciScintilla.NumberMargin)
        self.setMarginWidth(0, 48)
        self.setMarginMarkerMask(1, 0b00010)
        self.setText(
            "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
        # sym_0 = QImage("point.png").scaled(QSize(16, 16))
        # self.markerDefine(sym_0, 0)
        # self.markerDefine(sym_0, 1)
        # self.edit.setMarginLineNumbers(0, True)
        # self.marginClicked.connect(lambda x, y, z: self.markerAdd(y, x))
        # self.setMarginSensitivity(1, True)
        self.setFolding(QsciScintilla.CircledFoldStyle)
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
        lex = QsciLexerPython()
        api = QsciAPIs(lex)
        f = QFont("Monaco")
        f.setPointSize(10)
        lex.setFont(f)
        self.setLexer(lex)


    def paintEvent(self, event):
        super().paintEvent(event)
        f = QFont("Monaco")
        f.setPointSize(10)
        painter = QPainter(self.viewport())
        # painter.begin(self.viewport())
        painter.setPen(QPen(QColor("#0000ff")))
        point = QFontMetrics(f).averageCharWidth()*80
        painter.drawLine(point + self.marginWidth(0) + self.marginWidth(1) + self.marginWidth(2), 0,
                         point + self.marginWidth(0) + self.marginWidth(1) + self.marginWidth(2), self.height())
        # painter.end()
