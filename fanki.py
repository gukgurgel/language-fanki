#!/usr/bin/env python3.9
# coding=UTF-8
'''
created by Gustavo Korzune Gurgel
'''
import sys
from PyQt5.QtWidgets import (QApplication, QLabel, QWidget, QLineEdit,
                             QTextEdit, QGridLayout, QPushButton, QFrame,
                             QDesktopWidget)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import (Qt)
import translators as ts
import mkcard


class QHLine(QFrame):
    def __init__(self):
        super().__init__()
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)


class Program(QWidget):

    def __init__(self):
        super().__init__()

        self.layout = None

        '''
        self.grid = None
        self.deck = LineBox('Deck', self)
        self.sentence = LineBox('Sentence', self)
        self.tr_sentence = LineBox('Translated Sentence', self)
        self.words = LineBox('Words', self)
        self.tr_words = LineBox('Translated Words', self)
        self.synonyms = LineBox('Synonyms', self)
        self.front = TextBox('Front', self)
        self.back = TextBox('Back', self)
        self.back.edit.setFont(QFont('Helvetica', 15, weight=75))
        self.state = {
            'deck': '',
            'tr_sentence': '',
            'sentence': '',
            'words': '',
            'tr_words': '',
            'synonyms': '',
            'front': '',
            'back': ''
        }
        self.preview_btn = None
        self.add_btn = None
        self.transl_btn = None
        self.change_mode_btn = None
        self.clear_btn = None
        self.initUI()
        '''

    def initUI(self):
        self.layout = Layout(self)
        self.layout.load(self)
        self.show()

    '''
    def initUI(self):

        mid_point = QDesktopWidget().availableGeometry().center()
        grid_i = 0

        self.grid = QGridLayout()
        
        grid_i = self.add_change_mode_btn(grid_i)
        grid_i = self.deck.add(grid_i, self.grid)
        grid_i = self.sentence.add(grid_i, self.grid)
        grid_i = self.words.add(grid_i, self.grid)
        grid_i = self.synonyms.add(grid_i, self.grid)
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
        self.synonyms.edit.clear()
        self.tr_sentence.edit.clear()
        self.tr_words.edit.clear()

    def add_change_mode_btn(self, grid_i):
        self.change_mode_btn = QPushButton('Change Mode', self)
        self.change_mode_btn.setFont(QFont('Helvetica', 15))
        self.grid.addWidget(self.change_mode_btn, grid_i, 0)
        self.change_mode_btn.clicked.connect(self.button_processor)
        return grid_i + 1

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
        if sender.text() == 'Translate':
            #self.change_processor()
            translation = ts.google(
                self.state["sentence"], to_language='en')
            tr_words = ts.google(
                self.state["words"], to_language='en')
            self.tr_sentence.edit.setText(translation)
            self.tr_words.edit.setText(tr_words)
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
        grid_i = TextBox('Front', program).add(grid_i, self)
        grid_i = TextBox('Back', program).add(grid_i, self)
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
        '''
        self.objects_list = [
                'Deck', 'Sentence', 'Translated Sentence',
                'Words', 'Translated Words', 'Synonyms',
                'Translator'
                ]

        grid_i = LineBox('Sentence', program).add(grid_i, grid)
        grid_i = LineBox('Words', program).add(grid_i, grid)
        grid_i = LineBox('Synonyms', program).add(grid_i, grid)
        grid_i = Button('Translator', program).add(grid_i, grid) 
        grid_i = LineBox('Translated Sentence', program).add(grid_i, grid)
        grid_i = LineBox('Translated Words', program).add(grid_i, grid)
        '''

        self.objects_list = [
                LineBox('Sentence', program), LineBox('Words', program),
                LineBox('Synonyms', program), Button('Translator', program),
                LineBox('Translated Sentence', program), 
                LineBox('Translated Words', program)
                ]
        
        for obj in self.objects_list:
            grid_i = obj.add(grid_i, grid)

        
        return grid_i

    def preview(self, grid, program):
        pass

    def add_note(self, grid, program):
        pass



class LingvistAdvanced(LayoutType):
    def __init__(self, grid):
        super().__init__(grid)
        self.type = 'LingvistAdvanced'

    def load(self, grid, grid_i, program):
        pass

    def change(self, grid):
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
        program = self.program
        sender = program.sender()
        if sender != None:
            layout = program.layout
            pressed = sender.text()
            switcher = {
                    'Change Mode' : self.change_mode(layout, program),
                    'Translate' : self.translate(layout, program),
                    'Preview' : layout.now.preview(layout, program),
                    'Add Note' : layout.now.add_note(layout, program)
                    }

            switcher.get(pressed)


    def change_mode(self, layout, program):
        layout.now.clean()
        #layout.change()
        #layout.now.load(layout, layout.i_end_of_header, program)

    def translate(self, layout, program):
        pass

class TextBox(QTextEdit):
    def __init__(self, name, program):

        super().__init__(parent=program)
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

class LineBox(QLineEdit):
    def __init__(self, name, program):

        super().__init__(parent=program)
        name_html = ('<center><h3>' + name + '</h3></center>')
        self.label = QLabel(name_html)
        self.label.setTextFormat(2)
        self.label.setParent(program)
        self.label.setObjectName(name)
        self.setObjectName(name)
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
