import re
from PyQt5.QtWidgets import QWidget
import os

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

    def return_images(self, content, field):
        # find images in the markdown create json with the path
        # and name of the image file and remove it from the markdown

        imgs_name = re.findall(r"(?<=\!\[image\]\()\w+(?=\))", content)
        content = re.sub(r"\!\[image\]\(\w+\)","", content)
        imgs_parsed = []
        
        path_to_media = '/tmp/'

        for name in imgs_name:
            now = {
                    "path": path_to_media + name,
                    "filename": name,
                    "fields": [field]
                  }
            imgs_parsed.append(now)
        return (imgs_parsed, content)
        #return (imgs_parsed, 

    def markdown_to_html(self, field):
        # transform **{word}** in {{c1::word}},
        # **word** in <b>word</b> and \n in <br>

        # avoid weird behavior, where whitespaces are replaced by \n by the toMarkdown method 
        field = re.sub(r"(?<!(\n))(\n{1}\*{2})(?!(\n))", "**", field)
        field = re.sub(r"(?<!(\n))(\*{2}\n{1})(?!(\n))", "**", field)
        field = re.sub(r"(?<!(\n))(\n{1})(?!(\n))", " ", field)

        # cloze
        field = re.sub( r"\*{2}\{([^*\}]*)\}\*{2}"
                      , r"{{c1::\1}}"
                      , field)

        # real bold text
        field = re.sub( r"\*{2}([^*\}]*)\*{2}"
                      , r"<b>\1</b>"
                      , field)

        # new line
        field = re.sub(r"\n","<br>", field) 

        # remove some unexpected <br> tags at the and of the front field (added by
        # image?)
        field = re.sub(r"(<br>)+$","<br><br>", field) 

        return field


class LingvistNote(Note):
    
    def __init__(self, program):
        self.program = program 

    def prev(self):
        program = self.program
        sentence = str(program.findChild(QWidget, "Sentence").text())
        words = program.findChild(QWidget, "Words").text()
        tr_sentence = str(program.findChild(QWidget, "Translated Sentence").text())
        tr_words = program.findChild(QWidget, "Translated Words").text()

        for word in listify(words):
            sentence = re.sub(r"\b"+word+r"\b",
                    "<b>{"+word+"}</b>",
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
        front = program.findChild(QWidget, "Front").toMarkdown()
        back = program.findChild(QWidget, "Back").toPlainText()
        (imgs_front, front) = self.return_images(front, "Front")
        front = self.markdown_to_html(front)

        # boldfy the text of back
        back = '<b>' + back + '</b>'

        synonyms = '<b>Synonyms</b>: ' + program.findChild(QWidget, "Synonyms").text()
        

        notes = [{'deckName': deck,
                  'modelName': 'Fanki: Lingvist',
                  'fields': {'Front': front,
                             'Back': back,
                             'Synonyms' : synonyms},
                  'picture': imgs_front}]
                  
        return notes


class LingvistAdvancedNote(Note):
    
    def __init__(self, program):
        self.program = program 

    def prev(self):
        program = self.program
        sentence = str(program.findChild(QWidget, "Sentence").text())
        words = program.findChild(QWidget, "Words").text()
        definition = '<b>Definition</b>: ' + program.findChild(QWidget, "Definition").text()

        for word in listify(words):
            sentence = re.sub(r"\b"+word+r"\b",
                    "<b>{"+word+"}</b>",
                    sentence)

        incomp_sentence = sentence + "<br><br>" + definition 
        miss_words = ' -> ' + words

        program.findChild(QWidget, "Incomplete Sentence").setHtml(incomp_sentence)
        program.findChild(QWidget, "Missing Words & Image").setHtml(miss_words)


    def make(self):
        program = self.program

        deck = program.findChild(QWidget, "Deck").text()
        incomp_sentence = program.findChild(QWidget, "Incomplete Sentence").toMarkdown()
        missing_words = program.findChild(QWidget, "Missing Words & Image").toMarkdown()
        (imgs_is, incomp_sentence) = self.return_images(incomp_sentence, "Incomplete Sentence")
        (imgs_mw, missing_words) = self.return_images(missing_words, "Missing Words & Image")
        incomp_sentence_direct = self.markdown_to_html(incomp_sentence)
        incomp_sentence_reverse = self.markdown_to_html_rev(incomp_sentence)
        missing_words = self.markdown_to_html(missing_words)

        synonyms = '<b>Synonyms</b>: ' + program.findChild(QWidget, "Synonyms").text()
        

        notes = [{'deckName': deck,
                  'modelName': 'Fanki: LingvistAdvanced',
                  'fields': {'Incomplete Sentence': incomp_sentence_direct,
                             'Missing Words & Image': missing_words,
                             'Synonyms' : synonyms},
                  'picture': imgs_is + imgs_mw},
                  {'deckName': deck,
                  'modelName': 'Fanki: LingvistAdvanced (Reverse)',
                  'fields': {'Missing Words & Image': missing_words,
                             'Incomplete Sentence': incomp_sentence_reverse,
                             'Synonyms' : synonyms},
                  'picture': imgs_is + imgs_mw}]
                  
        return notes

    def markdown_to_html_rev(self, field):
        # transform **word** in {{c1::word}} and \n in <br>

        # cloze or bold to html bold

        # avoid weird behavior, where new lines are added by the toMarkdown method 
        field = re.sub(r"(?<!(\n))(\n{1}\*{2})(?!(\n))", "**", field)
        field = re.sub(r"(?<!(\n))(\*{2}\n{1})(?!(\n))", "**", field)
        field = re.sub(r"(?<!(\n))(\n{1})(?!(\n))", " ", field)

        field = re.sub( r"\*{2}\{?([^*\}]*)\}?\*{2}"
                      , r"<b>\1</b>"
                      , field)

        # new line 
        field = re.sub(r"\n","<br>", field) 

        # removethere are some unexpected <br> tags (added by
        # image?)
        field = re.sub(r"(<br>)+$","<br><br>", field) 

        return field


def listify(s):

    return re.split(r'\s+', s) # spaces as delimiter for a string
