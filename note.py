import re
from PyQt5.QtWidgets import QWidget


class Preview:

    def __init__(self, layout, program):
        mode = layout.now.type
        note = Note(mode, program)
        self.front = note.prev_front
        self.back = note.prev_back

class Note:

    def __init__(self, mode, program):
        switch = {
                "Lingvist" : LingvistNote,
                "LingvistAdvanced" : LingvistAdvancedNote
                }

        note = switch.get(mode)(program)
        (self.front, self.back) = note.make_note()
        (self.prev_front, self.prev_back)  = note.make_prev()



class LingvistNote(Note):
    
    def __init__(self, program):
        self.program = program 

    def make_prev(self):
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

        return (front, back)

    def make_note(self):
        program = self.program

        deck = program.findChild(QWidget, "Deck").text()
        front = program.findChild(QWidget, "Missing Target Words").toHTML()
        back = program.findChild(QWidget, "Full Sentence").toHTML()
        synonyms = '<b>Synonyms</b>: ' + program.findChild(QWidget, "Synonyms").text()

        note = {'deckName': deck,
                'modelName': 'Fanki: Lingvist',
                'fields': {'Front': front,
                           'Back': back,
                           'Synonyms' : synonyms}}
        return note


class LingvistAdvancedNote(Note):
    
    def __init__(self, program):
        self.program = program 

    def make_prev(self):
        return ('', '')

    def make_note(self):
        return ('', '')

def listify(s):
    return re.split(' +', s)  # ' +' for one or more occuring
    # spaces as delimiter for a string
