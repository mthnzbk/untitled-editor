from PyQt5.QtCore import QSettings, QDir
import sys
import os

def settings():
    s = QSettings(os.path.join(QDir.homePath(), ".editor", "hebele.ini"), QSettings.IniFormat)
    s.setIniCodec("UTF-8")
    return s