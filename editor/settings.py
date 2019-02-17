from PyQt5.QtCore import QSettings, QDir, QFile, QObject, QIODevice, QTextStream, QDataStream
import sys
import os
import posixpath
import json

def settings():
    s = QSettings(posixpath.join(QDir.homePath(), ".editor", "hebele.ini"), QSettings.IniFormat)
    s.setIniCodec("UTF-8")
    return s


class Settings(QObject):

    json_object = {}

    def __getitem__(self, item):
        try:
            return self.json_object[item]

        except KeyError:
            return None

    def __setitem__(self, key, value):
        self.json_object[key] = value
        self.write()

    def __init__(self, path=posixpath.join(QDir.homePath(), ".editor", "hebele.json")):
        super().__init__()


        self.path = path

        if QFile().exists(self.path):
            out = QFile(self.path)

            if out.open(QIODevice.ReadOnly | QIODevice.Text):
                ts = QTextStream(out)
                self.json_object = json.loads(ts.readAll(), encoding="utf-8")


    def write(self):
        data = json.dumps(self.json_object, sort_keys=True, indent=4)
        out = QFile(self.path)

        if out.open(QIODevice.WriteOnly | QIODevice.Text):
            out.write(bytes(data, encoding="utf-8"))
            out.close()