import json
import urllib.request
import re


def request(action, **params):
    return {'action': action, 'params': params, 'version': 6}


def invoke(action, **params):
    requestJson = json.dumps(request(action, **params)).encode('utf-8')
    response = json.load(urllib.request.urlopen(urllib.request.Request('http://localhost:8765', requestJson)))
    if len(response) != 2:
        raise Exception('response has an unexpected number of fields')
    if 'error' not in response:
        raise Exception('response is missing required error field')
    if 'result' not in response:
        raise Exception('response is missing required result field')
    if response['error'] is not None:
        raise Exception(response['error'])
    return response['result']


class NewCard(object):
    """Documentation for NewCard

    """
    def __init__(self):
        super().__init__()

 



def print_preview_beginn_interm(sent, tr_sent, bck, wrds):
    print('Card\'s preview:')
    print('-Front:')
    print(sent+'\n\n'+tr_sent)
    print('-Back:')
    print(bck)
    print('-Words:')
    print(wrds)


def print_preview_advanc(sent, senttwo, mean, ipa, wrds):
    print('Card\'s preview:')
    print('\ndeck->meaning:\n')
    print('-Front:')
    print(sent)
    print(ipa)
    print('-Back:')
    print(mean)
    print('\nmeaning->type:\n')
    print('-Front:')
    print(senttwo)
    print(mean)
    print('-Back:')
    print(ipa)
    print(wrds)


def add_new_note_beginn_interm():
    sentence = input('Enter original sentence: ')
    tr_sentence = input('Enter translated sentence: ')
    words = input('Enter target word(s): ')
    words_list = re.split(' +', words)  # ' +' uses one or more occuring
    # spaces as delimiter
    for word in words_list:
        sentence = re.sub(r'\b'+word+r'\b', '<b>'+'x'*len(word)+'</b>', sentence)
    tr_words = input('Enter translated target word(s): ')
    tr_words_list = re.split(' +', tr_words)
    for word in tr_words_list:
        tr_sentence = re.sub(r'\b'+word+r'\b', '<b>'+word+'</b>', tr_sentence)
    back = '<b>'
    back += input('Enter card\'s back: ')+'</b>'
    print_preview_beginn_interm(sentence, tr_sentence, back, words)
    ok = False
    add = input('Would you like to add this card to deck '+deckName+'? [y/n]: ')
    while not ok:
        if add == 'y':
            invoke('addNote', note={'deckName': deckName,
                                    'modelName': 'Beginner -- Intermediate',
                                    'fields': {'Front': sentence+'<br><br>'+tr_sentence,
                                               'Back': back,
                                               'Word': words}})
            print('Succesfully added!')
            ok = True
        elif add == 'n':
            print('Note deleted!')
            ok = True
        else:
            add = input('Answer \'y\' or \'n\', please: ')


def add_new_note_advanc():
    sentence = input('Enter original sentence: ')
    words = input('Enter target word(s): ')
    words_list = re.split(' +', words)  # ' +' uses one or more occuring
    # spaces as delimiter
    sentence_two = sentence
    for word in words_list:
        sentence = re.sub(r'\b'+word+r'\b', '<b>'+word+'</b>', sentence)
    for word in words_list:
        sentence_two = re.sub(r'\b'+word+r'\b', '<b>'+word[0] +
                              (len(word) - 2)*'x' +
                              word[-1]+'</b>', sentence_two)
        # e.g. word = mango, sentence = I ate a mango today.
        # loop above turns sentece into: I ate a <b>mxxxo</b> today.
    ipa = '<br><br><b>'
    ipa += input('Enter words\' transcription (if necessary): ')+'</b>'
    if ipa == '<br><br><b></b>':  # in case of no transcription was added
        ipa = ''
    meaning = '<b>'
    meaning += input('Enter word\'s (s\') meaning: ')+'</b>'
    print_preview_advanc(sentence, sentence_two, meaning, ipa, words)
    ok = False
    add = input('Would you like to add this card to deck '+deckName+'? [y/n]: ')
    while not ok:
        if add == 'y':
            invoke('addNote', note={'deckName': deckName,
                                    'modelName': 'Advanced (deck->meaning)',
                                    'fields': {'Sentence': sentence,
                                               'IPA': ipa,
                                               'Meaning': meaning}})
            invoke('addNote', note={'deckName': deckName,
                                    'modelName': 'Advanced (meaning->type)',
                                    'fields': {'Sentence': sentence_two,
                                               'IPA': ipa,
                                               'Word': words,
                                               'Meaning': meaning}})
            print('Succesfully added!')
            ok = True
        elif add == 'n':
            print('Note deleted!')
            ok = True
        else:
            add = input('Answer \'y\' or \'n\', please: ')

# PROGRAM PERSE #


print("In order to leave this program press Ctrl-C")
result = invoke('deckNames')
deck_ok = False
while not deck_ok:
    deckName = input('Enter deck name: ')
    deck_ok = deckName in result
    if not deck_ok:
        print("Deck \""+deckName+"\" wasn't found. Try again")

add_note = True
while add_note:
    if deckName in ['Deutsch', 'Русский']:
        add_new_note_beginn_interm()
    else:
        add_new_note_advanc()
    ok = False
    add = input('Would you like to add another note to '+deckName+'? [y/n]: ')
    while not ok:
        if add == 'y':
            add_note = True
            ok = True
        elif add == 'n':
            add_note = False
            ok = True
        else:
            add = input('Answer \'y\' or \'n\', please: ')
