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
    def __init__(self, deck, sentence):
        self.deck = deck
        self.sentence = sentence


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
    def __init__(self, deck, sentence, tr_sentence, words, tr_words):
        super().__init__(deck, sentence)
        self.tr_sentence = tr_sentence
        self.words = words
        self.words_list = listify(self.words)
        self.tr_words_list = listify(tr_words)

    def boldify(self):
        for word in self.words_list:
            self.sentence = re.sub(r'\b'+word+r'\b',
                                   '<b>'+'x'*len(word)+'</b>',
                                   self.sentence)

        for word in self.tr_words_list:
            self.tr_sentence = re.sub(r'\b'+word+r'\b',
                                      '<b>'+word+'</b>',
                                      self.tr_sentence)


def add(deck, front, back, words):
    invoke('addNote', note={'deckName': deck,
                            'modelName': 'Beginner -- Intermediate',
                            'fields': {'Front': front,
                                       'Back': back,
                                       'Word': words}})
    print('Succesfully added!')


def listify(words):
    return re.split(' +', words)  # ' +' for one or more occuring
    # spaces as delimiter


def hide_words(sentence, words_list):
    hidden = sentence
    for word in words_list:
        hidden = re.sub(r'\b'+word+r'\b', '<b>'+word[0] +
                        (len(word) - 2)*'x' +
                        word[-1]+'</b>', hidden)
    return hidden
