import re
from PyQt5.QtWidgets import QWidget


class Preview:

    def __init__(self, layout, program):
        mode = layout.now.type
        self.note = Note(mode, program)

    def make(self):
        self.note.type.prev()
        
class Note:

    def __init__(self, mode, program):
        switch = {
                "Lingvist" : LingvistNote,
                "LingvistAdvanced" : LingvistAdvancedNote
                }

        self.type = switch.get(mode)(program)
        content = self.type.make()

class LingvistNote(Note):
    
    def __init__(self, program):
        self.program = program 

    def prev(self):
        program = self.program
        sentence = program.findChild(QWidget, "Sentence").text()
        words = program.findChild(QWidget, "Words").text()
        tr_sentence = program.findChild(QWidget, "Translated Sentence").text()
        tr_words = program.findChild(QWidget, "Translated Words").text()

        for word in listify(words):
            sentence = re.sub(r"\b"+word+r"\b",
                    "<b>"+word+"</b>",
                    sentence)

        for tr_word in listify(tr_words):
            tr_sentence = re.sub(r"\b"+tr_word+r"\b",
                    "<b>"+tr_word+"</b>",
                    tr_sentence)

        front = sentence + '<br><br>' + tr_sentence
        back = ' -> ' + words

        program.findChild(QWidget, "Front").setHtml(front)
        program.findChild(QWidget, "Back").setText(back)


    def make(self):
        program = self.program

        deck = program.findChild(QWidget, "Deck").text()
        front = program.findChild(QWidget, "Front").toHtml()
        back = program.findChild(QWidget, "Back").toHtml()
        synonyms = '<b>Synonyms</b>: ' + program.findChild(QWidget, "Synonyms").text()
        notes = [{'deckName': deck,
                  'modelName': 'Fanki: Lingvist',
                  'fields': {'Front': front,
                             'Back': back,
                             'Synonyms' : synonyms}}]
        return notes


class LingvistAdvancedNote(Note):
    
    def __init__(self, program):
        self.program = program 

    def prev(self):
        program = self.program
        sentence = program.findChild(QWidget, "Sentence").text()
        words = program.findChild(QWidget, "Words").text()
        definition = '<b>Definition</b>: ' + program.findChild(QWidget, "Definition").text()

        for word in listify(words):
            sentence = re.sub(r"\b"+word+r"\b",
                    "<b>[...]</b>",
                    sentence)

        incomp_sentence = sentence + "</br></br>" + definition 
        miss_words = '<b> -> ' + words + '</b>'

        print (program.findChild(QWidget, "Incomplete Sentence"))

        program.findChild(QWidget, "Incomplete Sentence").setHtml(incomp_sentence)
        program.findChild(QWidget, "Missing Words & Image").setHtml(miss_words)


    def make(self):
        return ('', '')

def listify(s):
    return re.split(' +', s)  # ' +' for one or more occuring
    # spaces as delimiter for a string
