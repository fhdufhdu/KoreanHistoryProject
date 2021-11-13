import sys
from os import path
import unicodedata

from func import save_pickle, load_pickle, remove_bracket, load_json, returnPreSubject, save_json


def remove(doc, is_title):
    doc = remove_bracket(doc)
    if is_title == False:
        doc = doc.replace('『', '').replace(
            '』', '').replace('‘', '').replace('’', '').replace('「', '').replace('」', '').replace('·', ',').replace('“', '').replace('”', '').replace('《', '').replace('》', '')
    for j in range(10):
        doc = doc.replace('0{})'.format(j), '')
    if is_title == False:
        idx = doc.find('키워드')
        if idx >= 0:
            remove_word = None
            for k in range(idx, len(doc)):
                if doc[k] == ' ':
                    remove_word = doc[idx:k]
                    break
            doc = doc
    return filterout_hanja_greek(doc)


def filterout_hanja_greek(s):
    r = ""
    for c in s:
        if not c.isalpha():
            r += c
            continue
        unicodename = unicodedata.name(c)
        if unicodename.startswith("GREEK") or unicodename.startswith("CJK"):
            continue
        r += c
    return r


for i in range(15):
    print(i)
    history_dict = load_json(
        '/home/fhdufhdu/vscode/Project/data/history_dict/data/history_{}.json'.format(i))
    history_list = history_dict['list']
    for history in history_list:
        del history['document'], history['document_ver2']
        title = history['title']
        intros = history['intro']
        contents = history['content']

        document = ''
        for intro in intros:
            t = intro[0]
            c = intro[1].replace(' / ', ',')

            document += title + '의 ' + t +\
                returnPreSubject(t) + ' ' + c + '이다. '

        for content in contents:
            t = content[0]
            c = content[1]

            if t == '정의':
                c = c[0:c.find('키워드')+1]
                document += title + returnPreSubject(title) + ' ' + c + '. '
            elif t == '내용':
                document += title + returnPreSubject(title) + ' ' + c + '. '
            elif t == '참고문헌':
                document += title + '의 ' + t +\
                    returnPreSubject(t) + ' ' + c + '. '
            else:
                document += c + '. '

        document = remove(document, False)
        history['document'] = document.replace('\n            ', ' ').replace(
            '  ', ' ').replace('..', '.')
        history['search'] = (title + ' ') * 100

    save_json(
        '/home/fhdufhdu/vscode/Project/data/history_dict/data/history_m_{}.json'.format(i), history_dict)
