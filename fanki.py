#!/usr/bin/env python3.9
# coding=UTF-8
'''
created by Gustavo Korzune Gurgel
'''
import sys
from PyQt5.QtWidgets import (QApplication, QLabel, QWidget, QLineEdit,
                             QTextEdit, QGridLayout, QPushButton, QFrame,
                             QDesktopWidget)
from PyQt5.QtGui import (QFont, QImageReader, QTextDocument)
from PyQt5.QtCore import (QUrl, QFileInfo, QFile, QIODevice)
import translators as ts
import cycle
import note


class Program(QWidget):

    def __init__(self):
        super().__init__()
        self.layout = Layout(self)

    def initUI(self):
        self.layout.load(self)
        self.show()


class Layout(QGridLayout):
    
    def __init__(self, program):
        super().__init__()
        self.types = [Lingvist(self, program), LingvistAdvanced(self, program)]
        self.cycle = cycle.Cycle(self.types)
        self.now = self.cycle.now
        self.grid_i_after_header = 0
        self.setSpacing(8)

    def load(self, program):
        grid_i = 0  # 'i' = row of the grid
        grid_i = self.load_header(grid_i, program)
        self.now.load_body(self)
        # the loop bellow avoids a weird behavior, where the last widged
        # of the objects_list of the second layout is added on the top left 
        # layout corner of the first
        for layout_type in filter(lambda x: x != self.now, self.types):
            layout_type.clean()
        program.setLayout(self)

    def change(self):
        self.now.clean()
        self.now = self.cycle.next()
        self.now.load_body(self)
        self.now.show()

    def load_header(self, grid_i, program):
        grid_i = Button('Change Mode', program).add(grid_i, self)
        grid_i = LineBox('Deck', program).add(grid_i, self)
        self.grid_i_after_header = grid_i
        return grid_i


class LayoutType:
    def __init__(self, grid):
        self.grid = grid
        self.objects_list = []
        self.preview_objects = []

    def clean(self):
        for obj in self.objects_list:
            obj.hide()

    def show(self):
        for obj in self.objects_list:
            obj.show()

    def load_body(self, grid):
        grid_i = grid.grid_i_after_header
        for obj in self.objects_list:
            #grid_i = obj.add(grid_i, grid)
            grid_i = obj.add(grid_i, self.grid)
        return grid_i
    
class Lingvist(LayoutType):

    def __init__(self, grid, program):
        super().__init__(grid)
        self.type = 'Lingvist'
        self.objects_list = [
                LineBox('Sentence', program), LineBox('Words', program),
                LineBox('Synonyms', program), Button('Translate', program),
                LineBox('Translated Sentence', program),
                LineBox('Translated Words', program), Button('Preview', program),
                HLine(), TextBox('Front', program), TextBox('Back', program),
                Button('Add Note', program)
                ]

class LingvistAdvanced(LayoutType):
    def __init__(self, grid, program):
        super().__init__(grid)
        self.type = 'LingvistAdvanced'
        self.objects_list = [
                LineBox('Sentence', program), LineBox('Words', program),
                LineBox('Definition', program), LineBox('Synonyms', program),
                Button('Preview', program), HLine(), 
                TextBox('Incomplete Sentence', program),
                TextBox('Missing Words & Image', program),
                Button('Add Note', program)
                ]

class HLine(QFrame):
    
    def __init__(self):
        super().__init__()
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)

    def add(self, line, layout):
        layout.addWidget(self, line, 0) 
        return line + 1

class Button(QPushButton):

    def __init__(self, name, program):
        super().__init__(name, program)
        self.setParent(program)
        self.setObjectName(name)
        self.setFont(QFont('Helvetica', 15))
        self.clicked.connect(self.processor)
        self.program = program

    def add(self, line, layout):
        layout.addWidget(self, line, 0)
        return line + 1

    def processor(self):
        sender = self.program.sender()
        if sender != None:
            layout = self.program.layout
            pressed = sender.text()
            switcher = {
                    'Change Mode' : self.change_mode,
                    'Translate' : self.translate,
                    'Preview' : self.make_preview,
                    'Add Note' : self.add_note
                    }

            switcher.get(pressed)(layout, self.program)


    def change_mode(self, layout, program):
        layout.change()

    def translate(self, layout, program):
        sentence = str(program.findChild(QWidget, "Sentence").text())
        words = str(program.findChild(QWidget, "Words").text())
        tr_sentence = ts.google(
                sentence, to_language='en'
                )
        tr_words = ts.google(
                words, to_language='en'
                )
        program.findChild(QWidget, "Translated Sentence").setText(tr_sentence)
        program.findChild(QWidget, "Translated Words").setText(tr_words)

    def make_preview(self, layout, program):
        preview = note.Preview(layout, program)
        preview.make()

    def add_note(self, layout, program):
        pass

class TextBox(QTextEdit):
    def __init__(self, name, program):

        super().__init__(parent=program)
        self.setObjectName(name)
        name_html = ('<center><h2>' + name + '</h2></center>')
        self.label = QLabel(name_html)
        self.label.setTextFormat(2)
        if name == 'Back':
            self.setFont(QFont('Helvetica', 15, weight=75))
        else:    
            self.setFont(QFont('Helvetica', 15))

    def add(self, line, grid):
        grid.addWidget(self.label, line, 0)
        grid.addWidget(self, line + 1, 0)
        return line + 2

    def hide(self):
        self.label.hide()
        self.orig_hide()

    def orig_hide(self):
        return super().hide()
    
    def show(self):
        self.label.show()
        self.orig_show()

    def orig_show(self):
        return super().show()

    def canInsertFromMimeData(self, mime):
        return (mime.hasImage() 
                or mime.hasUrls() 
                or super().canInsertFromMimeData(mime))

    def insertFromMimeData(self, mime):

        if mime.hasImage():
            i = 1
            url = QUrl("dropped_image_" + str(i))
            i += 1
            self.dropImage(url, mime.imageData())
        elif mime.hasUrls():
            for url in mime.urls():
                info = QFileInfo.info(url.toLocalFile()) 
                ext = info.suffix().lower().encode('latin-1')
                if ext in QImageReader.supportedImageFormats():
                    self.dropImage(url, info.filePath())
                else:
                    self.dropTextFile(url)
        else:
            super().insertFromMimeData(mime)


    def dropImage(self, url, image):
        if not image.isNull():
            self.document().addResource(QTextDocument.ImageResource, url, image)
            self.textCursor().insertImage(url.toString())

    def dropTextFile(self, url):
        file = QFile(url.toLocalFile())
        if file.open(QIODevice.QReadOnly | QIODevice.QText):
            self.textCursor().insertText(file.readAll())

class LineBox(QLineEdit):
    def __init__(self, name, program):

        super().__init__(parent=program)
        self.setObjectName(name)
        name_html = ('<center><h3>' + name + '</h3></center>')
        self.label = QLabel(name_html)
        self.label.setTextFormat(2)
        self.setFont(QFont('Helvetica', 15))

    def add(self, line, grid):
        grid.addWidget(self.label, line, 0)
        grid.addWidget(self, line + 1, 0)
        return line + 2

    def hide(self):
        self.label.hide()
        self.orig_hide()

    def orig_hide(self):
        return super().hide()

    def show(self):
        self.label.show()
        self.orig_show()

    def orig_show(self):
        return super().show()

def main():
    app = QApplication(sys.argv)
    prog = Program()
    prog.initUI()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
