from PyQt5.QtCore import QSettings, QDir, QFile, QObject, QJsonDocument, QJsonValue, QByteArray, QIODevice
import sys
import os
import json

def settings():
    s = QSettings(os.path.join(QDir.homePath(), ".editor", "hebele.ini"), QSettings.IniFormat)
    s.setIniCodec("UTF-8")
    return s


class Settings(QObject):
    def __init__(self):
        super().__init__()

        self.path = os.path.join(QDir.homePath(), ".editor", "hebele.json")



    def read(self):
        doc = QJsonDocument()
        out = QFile(self.path)

        if out.open(QIODevice.ReadOnly | QIODevice.Text):
            data = out.readAll()

        doc = doc.fromJson(self.data)
        obj = doc.object()

        return obj


    def write(self):
        doc = QJsonDocument()
        self.data = doc.toJson()
        out = QFile(self.path)

        if out.open(QIODevice.WriteOnly | QIODevice.Text):
            out.write(self.data)
            out.close()