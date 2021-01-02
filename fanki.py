#!/usr/bin/env python3.8
# coding=UTF-8
'''
created by Gustavo Korzune Gurgel
'''
import json
import urllib.request
import re
import sys
from PyQt5.QtWidgets import (QApplication, QLabel, QWidget, QLineEdit,
                             QTextEdit, QGridLayout, QPushButton, QFrame)


def request(action, **params):
    return {'action': action, 'params': params, 'version': 6}


def invoke(action, **params):
    requestJson = json.dumps(request(action, **params)).encode('utf-8')
    response = json.load(urllib.request.urlopen(
        urllib.request.Request('http://localhost:8765', requestJson)))
    if len(response) != 2:
        raise Exception('response has an unexpected number of fields')
    if 'error' not in response:
        raise Exception('response is missing required error field')
    if 'result' not in response:
        raise Exception('response is missing required result field')
    if response['error'] is not None:
        raise Exception(response['error'])
    return response['result']


class QHLine(QFrame):
    def __init__(self):
        super().__init__()
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)


class Program(QWidget):

    def __init__(self):
        super().__init__()

        self.grid = None
        self.sentence = None
        self.tr_sentence = None
        self.words = None
        self.initUI()

    def initUI(self):

        self.sentence = TextBox('Sentence')
        self.tr_sentence = TextBox('Translated Sentence')
        self.words = LineBox('Words')

        self.grid = QGridLayout()
        self.grid.setSpacing(5)

        self.addBoxes(self.sentence, 1)
        self.addBoxes(self.tr_sentence, 2)
        self.addBoxes(self.words, 3)
        self.grid.addWidget(QHLine(), 7, 0, 7, 1)

        self.setLayout(self.grid)

        self.setGeometry(300, 300, 350, 300)
        self.show()

    def addBoxes(self, box, line):

        self.grid.addWidget(box.label, 2*line - 1, 0)
        self.grid.addWidget(box.edit, 2*line, 0)


class TextBox:
    def __init__(self, name):

        name_html = ('<center><h1>' + name + '</h1></center>')
        self.label = QLabel(name_html)
        self.label.setTextFormat(2)
        self.edit = QTextEdit()


class LineBox:
    def __init__(self, name):

        name_html = ('<center><h1>' + name + '</h1></center>')
        self.label = QLabel(name_html)
        self.label.setTextFormat(2)
        self.edit = QLineEdit()

    # def button_click(self):
    #     # shost is a QString object
    #     shost = self.text()
    #     print(shost)


def main():
    app = QApplication(sys.argv)
    prog = Program()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
