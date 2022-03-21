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
from PyQt5.QtCore import (Qt, QUrl, QFileInfo, QFile, QIODevice)
import translators as ts
import note


class QHLine(QFrame):
    def __init__(self):
        super().__init__()
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)


class Program(QWidget):

    def __init__(self):
        super().__init__()

        self.layout = Layout(self)

    def initUI(self):
        self.layout.load(self)
        self.show()

    '''
    def update_status(self):
        self.state["deck"] = self.deck.edit.text()
        self.state["sentence"] = self.sentence.edit.text()
        self.state["synonyms"] = self.synonyms.edit.text()
        self.state["tr_words"] = self.tr_words.edit.text()
        self.state["front"] = self.front.edit.toHtml()
        self.state["back"] = '<b>' + self.back.edit.toPlainText() + '</b>'
        self.state["words"] = self.words.edit.text()
        self.state["tr_sentence"] = self.tr_sentence.edit.text()

    def button_processor(self):
        sender = self.sender()
        if sender.text() == 'Preview':
            #self.change_processor()
            note = mkcard.BeginIntermNote(self.state["deck"],
                                          self.state["sentence"],
                                          self.state["tr_sentence"],
                                          self.state["words"],
                                          self.state["tr_words"],
                                          self.state["synonyms"])
            note.boldify()
            self.front.edit.setHtml(note.sentence + '<br><br>'
                                    + note.tr_sentence + '<br><br>'
                                    + "<b>Synonmys</b>: " +
                                    note.synonyms)
            self.back.edit.setText(' -> ' + self.state["words"])
            #self.change_processor()
        if sender.text() == 'Add Note':
            front, back, synonyms = mkcard.pre_make_fields(
                self.state["sentence"], self.state["tr_sentence"],
                self.state["words"], self.state["tr_words"],
                self.state["synonyms"]
            )

            mkcard.add(self.state["deck"],
                       front,
                       self.state["back"],
                       synonyms)

            self.clear_fields()

        if sender.text() == 'Clear All':
            self.clear_fields()
            self.front.edit.clear()
            self.back.edit.clear()

        if sender.text() == 'Change Mode':
            for i in range(self.grid.count()):
                print(i)
                self.grid.itemAt(i).widget().hide()
                self.layout.change()
    '''


class Layout(QGridLayout):
    
    def __init__(self, program):
        super().__init__()
        self.setObjectName('Layout')
        self.now = Lingvist(self)
        self.i_end_of_header = 0
        mid_point = QDesktopWidget().availableGeometry().center()
        program.setGeometry(mid_point.x(),
                            0,
                            int(mid_point.x() / 2),
                            mid_point.y())

    def load(self, program):
        grid_i = 0  # 'i' = row of the grid
        grid_i = self.load_header(grid_i, program)
        self.i_end_of_header = grid_i
        grid_i = self.now.load(self, grid_i, program)
        self.load_footer(grid_i, program)
        program.setLayout(self)

    def change(self):
        self.now = self.now.change(self)

    def load_header(self, grid_i, program):
        grid_i = Button('Change Mode', program).add(grid_i, self)
        grid_i = LineBox('Deck', program).add(grid_i, self)
        return grid_i

    def load_footer(self, grid_i, program):
        self.addWidget(QHLine(), grid_i, 0) 
        grid_i += 1
        # add line separating input fields from the note preview

        grid_i = Button('Preview', program).add(grid_i, self)
        grid_i = TextBox('Missing Target Words', program).add(grid_i, self)
        grid_i = TextBox('Full Sentence', program).add(grid_i, self)
        grid_i = Button('Add Note', program).add(grid_i, self)

class LayoutType:
    def __init__(self, grid):
        self.grid = grid
        self.objects_list = []

    def clean(self):
        for obj in self.objects_list:
            obj.hide()



class Lingvist(LayoutType):

    # grid == layout

    def __init__(self, grid):
        super().__init__(grid)
        self.type = 'Lingvist'

    def change(self, grid):
        return LingvistAdvanced(grid)

    def load(self, grid, grid_i, program):

        # the order of the objects in the list follows the order in which
        # the objects are going to be shown
        self.objects_list = [
                LineBox('Sentence', program), LineBox('Words', program),
                LineBox('Synonyms', program), Button('Translate', program),
                LineBox('Translated Sentence', program), 
                LineBox('Translated Words', program)
                ]
        
        for obj in self.objects_list:
            grid_i = obj.add(grid_i, grid)

        
        return grid_i


class LingvistAdvanced(LayoutType):
    def __init__(self, grid):
        super().__init__(grid)
        self.type = 'LingvistAdvanced'

    def load(self, grid, grid_i, program):
        
        self.objects_list = [
                LineBox('Sentence', program), LineBox('Words', program),
                LineBox('Definition', program), LineBox('Synonyms', program),
                LineBox('Link to Image', program)
                ]
        
        for obj in self.objects_list:
            grid_i = obj.add(grid_i, grid)

    def change(self, grid):
        return Lingvist(grid)

    def add_note(self, layout, program):
        pass



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
        layout.now.clean()
        layout.change()
        layout.now.load(layout, layout.i_end_of_header, program)

    def translate(self, layout, program):
        sentence = program.findChild(QWidget, "Sentence").text()
        words = program.findChild(QWidget, "Words").text()
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
        #front = program.findChild(QWidget, "Front")
        program.findChild(QWidget, "Missing Target Words").setHtml(preview.front)
        program.findChild(QWidget, "Full Sentence").setText(preview.back)

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
        self.super().hide()

    def canInsertFromMimeData(self, mime):
        return (mime.hasImage() 
                or mime.hasUrls() 
                or self.super().canInsertFromMimeData(mime))

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
            self.super().insertFromMimeData(mime)


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


def main():
    app = QApplication(sys.argv)
    prog = Program()
    prog.initUI()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
