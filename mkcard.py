#!/usr/bin/env python3.8
# coding=UTF-8
'''
created by Gustavo Korzune Gurgel
'''
import json
import urllib.request
import re


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


class NewNote:
    '''
    New card that (possibly) will be added to the deck
    '''
    def __init__(self, deck):
        self.deck = deck
        self.sentence = ask_sentence()

    def ask_to_add(self):
        add = input('Would you like to add this note to '
                    + self.deck + '? [y/n]: ')
        while add not in ['y', 'n']:
            add = input('Answer \'y\' or \'n\', please: ')
        return add


class AdvancedNote(NewNote):
    '''
    Subclass for notes of languages
    in which the learner is advanced
    '''
    def __init__(self, deck):
        super().__init__(deck)
        self.words = ask_words()
        self.words_list = listify(self.words)
        self.ipa = ask_ipa()
        self.hidden_sentence = hide_words(self.sentence, self.words_list)
        self.meaning = ask_meaning()

    def boldify(self):
        for word in self.words_list:
            self.sentence = re.sub(r'\b'+word+r'\b',
                                   '<b>'+word+'</b>',
                                   self.sentence)

    def print_preview(self):
        print('Card\'s preview:')
        print('\ndeck->meaning:\n')
        print('-Front:')
        print(self.sentence)
        print(self.ipa)
        print('-Back:')
        print(self.meaning)
        print('\nmeaning->type:\n')
        print('-Front:')
        print(self.hidden_sentence)
        print(self.meaning)
        print('-Back:')
        print(self.ipa)
        print(self.words)

    def add(self):
        if self.ask_to_add() == 'y':
            invoke('addNote', note={'deckName': self.deck,
                                    'modelName': 'Advanced (deck->meaning)',
                                    'fields': {'Sentence': self.sentence,
                                               'IPA': self.ipa,
                                               'Meaning': self.meaning}})
            invoke('addNote', note={'deckName': self.deck,
                                    'modelName': 'Advanced (meaning->type)',
                                    'fields': {'Sentence':
                                               self.hidden_sentence,
                                               'IPA': self.ipa,
                                               'Word': self.words,
                                               'Meaning': self.meaning}})
            print('Succesfully added!')
        else:
            print('Note deleted!')


class BeginIntermNote(NewNote):
    '''
    Subclass for notes of languages
    in which the learner is beginner/intermediate
    '''
    def __init__(self, deck):
        super().__init__(deck)
        self.tr_sentence = ask_translated_sentence()
        self.words = ask_words()
        self.words_list = listify(self.words)
        self.tr_words_list = ask_tr_words()
        self.back = ask_back()

    def boldify(self):
        for word in self.words_list:
            self.sentence = re.sub(r'\b'+word+r'\b',
                                   '<b>'+'x'*len(word)+'</b>',
                                   self.sentence)

        for word in self.tr_words_list:
            self.tr_sentence = re.sub(r'\b'+word+r'\b',
                                      '<b>'+word+'</b>',
                                      self.tr_sentence)

    def print_preview(self):
        print('Card\'s preview:')
        print('-Front:')
        print(self.sentence
              + '\n\n'
              + self.tr_sentence)
        print('-Back:')
        print(self.back)
        print('-Words:')
        print(self.words)

    def add(self):
        if self.ask_to_add() == 'y':
            invoke('addNote', note={'deckName': self.deck,
                                    'modelName': 'Beginner -- Intermediate',
                                    'fields': {'Front': (self.sentence
                                                         + '<br><br>' +
                                                         self.tr_sentence),
                                               'Back': self.back,
                                               'Word': self.words}})
            print('Succesfully added!')
        else:
            print('Note deleted!')


def ask_sentence():
    return input('Enter original sentence: ')


def ask_translated_sentence():
    return input('Enter translated sentence: ')


def ask_words():
    return input('Enter target word(s): ')


def listify(words):
    return re.split(' +', words)  # ' +' for one or more occuring
    # spaces as delimiter


def ask_tr_words():
    tr_words = input('Enter translated target word(s): ')
    return listify(tr_words)


def ask_back():
    back = '<b>'
    back += input('Enter card\'s back: ')+'</b>'
    return back


def ask_ipa():
    ipa = '<br><br><b>'
    ipa += input('Enter words\' transcription (if necessary): ')+'</b>'
    if ipa == '<br><br><b></b>':  # in case of no transcription was added
        ipa = ''
    return ipa


def ask_meaning():
    meaning = '<b>'
    meaning += input('Enter word\'s (s\') meaning: ')+'</b>'
    return meaning


def hide_words(sentence, words_list):
    hidden = sentence
    for word in words_list:
        hidden = re.sub(r'\b'+word+r'\b', '<b>'+word[0] +
                        (len(word) - 2)*'x' +
                        word[-1]+'</b>', hidden)
    return hidden


def ask_deck():
    '''
    Ask to the user to which deck the note will be added
    '''
    result = invoke('deckNames')
    deck_ok = False
    while not deck_ok:
        deck_name = input('Enter deck name: ')
        deck_ok = deck_name in result
        if not deck_ok:
            print("Deck \"" + deck_name + "\" wasn't found. Try again")
    return deck_name


class Program:
    '''
    The main program
    '''
    def __init__(self):
        self.add_note = True
        self.deck = None
        self.advanced_decks = ['English']

    def start(self):
        print("In order to leave this program press Ctrl-C")
        self.deck = ask_deck()

    def add_new_note(self):
        if self.deck in self.advanced_decks:
            note = AdvancedNote(self.deck)
        else:
            note = BeginIntermNote(self.deck)
        note.boldify()
        note.print_preview()
        note.add()

    def ask_for_another_note(self):
        add = input('Would you like to add another note to '
                    + self.deck + '? [y/n]: ')
        while add not in ['y', 'n']:
            add = input('Answer \'y\' or \'n\', please: ')
        if add == 'y':
            return True         # for add another card
        return False            # for ending while loop in prog.start


def main():
    prog = Program()
    prog.start()
    while prog.ask_for_another_note():
        prog.add_new_note()


if __name__ == '__main__':
    main()
