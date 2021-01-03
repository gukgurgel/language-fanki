#!/usr/bin/env python3.8
# coding=UTF-8
'''
created by Gustavo Korzune Gurgel
'''
import re
import sys
from PyQt5.QtWidgets import (QApplication, QLabel, QWidget, QLineEdit,
                             QTextEdit, QGridLayout, QPushButton, QFrame,
                             QDesktopWidget)
from PyQt5.QtGui import QFont
from googletrans import Translator
import mkcard


class QHLine(QFrame):
    def __init__(self):
        super().__init__()
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)


class Program(QWidget):

    def __init__(self):
        super().__init__()

        self.grid = None
        self.deck = LineBox('Deck')
        self.sentence = LineBox('Sentence')
        self.tr_sentence = LineBox('Translated Sentence')
        self.words = LineBox('Words')
        self.tr_words = LineBox('Translated Words')
        self.front = TextBox('Front')
        self.back = TextBox('Back')
        self.back.edit.setFont(QFont('Helvetica', 15, weight=75))
        self.preview_btn = None
        self.add_btn = None
        self.transl_btn = None
        self.clear_btn = None
        self.translator = Translator(service_urls=['translate.googleapis.com'])
        self.initUI()

    def initUI(self):

        mid_point = QDesktopWidget().availableGeometry().center()
        grid_i = 1

        self.grid = QGridLayout()

        grid_i = self.deck.add(grid_i, self.grid)
        grid_i = self.sentence.add(grid_i, self.grid)
        grid_i = self.words.add(grid_i, self.grid)
        grid_i = self.add_translation_btn(grid_i)
        grid_i = self.tr_sentence.add(grid_i, self.grid)
        grid_i = self.tr_words.add(grid_i, self.grid)
        self.grid.addWidget(QHLine(), grid_i, 0)
        grid_i += 1
        grid_i = self.add_preview_btn(grid_i)
        grid_i = self.front.add(grid_i, self.grid)
        grid_i = self.back.add(grid_i, self.grid)
        grid_i = self.add_add_btn(grid_i)
        grid_i = self.add_clear_btn(grid_i)

        self.setLayout(self.grid)
        self.setGeometry(mid_point.x(),
                         0,
                         int(mid_point.x() / 2),
                         mid_point.y())
        self.show()

    def clear_fields(self):
        self.sentence.edit.clear()
        self.words.edit.clear()
        self.tr_sentence.edit.clear()
        self.tr_words.edit.clear()

    def add_translation_btn(self, grid_i):
        self.transl_btn = QPushButton('Translate', self)
        self.transl_btn.setFont(QFont('Helvetica', 15))
        self.grid.addWidget(self.transl_btn, grid_i, 0)
        self.transl_btn.clicked.connect(self.button_processor)
        return grid_i + 1

    def add_preview_btn(self, grid_i):
        self.preview_btn = QPushButton('Preview', self)
        self.preview_btn.setFont(QFont('Helvetica', 15))
        self.grid.addWidget(self.preview_btn, grid_i, 0)
        self.preview_btn.clicked.connect(self.button_processor)
        return grid_i + 1

    def add_add_btn(self, grid_i):
        self.add_btn = QPushButton('Add Note', self)
        self.add_btn.setFont(QFont('Helvetica', 15))
        self.grid.addWidget(self.add_btn, grid_i, 0)
        self.add_btn.clicked.connect(self.button_processor)
        return grid_i + 1

    def add_clear_btn(self, grid_i):
        self.clear_btn = QPushButton('Clear All', self)
        self.clear_btn.setFont(QFont('Helvetica', 15))
        self.grid.addWidget(self.clear_btn, grid_i, 0)
        self.clear_btn.clicked.connect(self.button_processor)
        return grid_i + 1

    def button_processor(self):
        sender = self.sender()
        if sender.text() == 'Translate':
            orig = self.sentence.edit.text()
            self.sentence.edit.setText(orig)
            words = self.words.edit.text()
            self.words.edit.setText(words)
            translation = self.translator.translate(orig, dest='en')
            tr_words = self.translator.translate(words, dest='en')
            self.tr_sentence.edit.setText(translation.text)
            self.tr_sentence.edit.displayText()
            self.tr_words.edit.setText(tr_words.text)
            self.tr_words.edit.displayText()
        if sender.text() == 'Preview':
            deck = self.deck.edit.text()
            sentence = self.sentence.edit.text()
            translation = self.tr_sentence.edit.text()
            words = self.words.edit.text()
            tr_words = self.tr_words.edit.text()
            note = mkcard.BeginIntermNote(deck, sentence, translation,
                                          words, tr_words)
            note.boldify()
            self.front.edit.setHtml(note.sentence + '<br><br>'
                                    + note.tr_sentence)
            self.back.edit.setText(' -> ' + words)
        if sender.text() == 'Add Note':
            deck = self.deck.edit.text()
            front = self.front.edit.toHtml()
            back = '<b>'
            back += self.back.edit.toPlainText() + '</b>'
            words = self.words.edit.text()
            mkcard.add(deck, front, back, words)
            self.clear_fields()
        if sender.text() == 'Clear All':
            self.clear_fields()
            self.front.edit.clear()
            self.back.edit.clear()


class TextBox:
    def __init__(self, name):

        name_html = ('<center><h2>' + name + '</h2></center>')
        self.label = QLabel(name_html)
        self.label.setTextFormat(2)
        self.edit = QTextEdit()
        self.edit.setFont(QFont('Helvetica', 15))

    def add(self, line, grid):
        grid.addWidget(self.label, line, 0)
        grid.addWidget(self.edit, line + 1, 0)
        return line + 2


class LineBox:
    def __init__(self, name):

        name_html = ('<center><h2>' + name + '</h2></center>')
        self.label = QLabel(name_html)
        self.label.setTextFormat(2)
        self.edit = QLineEdit()
        self.edit.setFont(QFont('Helvetica', 15))

    def add(self, line, grid):
        grid.addWidget(self.label, line, 0)
        grid.addWidget(self.edit, line + 1, 0)
        return line + 2


def main():
    app = QApplication(sys.argv)
    prog = Program()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
