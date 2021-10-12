import sys
from os import path
from xml.etree.ElementTree import parse
from konlpy.tag import Mecab

from jamo import h2j, j2hcj

if True:
    project_dir = '/home/fhdufhdu/vscode/KoreanHistoryProject'
    sys.path.append(project_dir)
    from util.func import remove_bracket, load_pickle, add_text_on_file


def get_in_braket(doc):
    words = []

    start_idx = -1
    for i in range(len(doc)):
        if doc[i] == '(':
            start_idx = i
        if start_idx != -1 and doc[i] == ')':
            words.append(doc[start_idx:i+1])
            start_idx = -1

    return words


books = parse('data/books.xml').getroot()
stratums = parse('data/stratums.xml').getroot()
people = parse('data/people.xml').getroot()

books = books.findall('문헌')
books_ = []
for book in books:
    book_names = [book.findtext('서명')]
    if book.findtext('표제_한글') is not None:
        book_names.append(book.findtext('표제_한글'))
    for book_name in book_names:
        for i in range(10):
            book_name = book_name.replace(
                'v0{}'.format(i), '').replace(' ', '')
        for i in range(100, -1, -1):
            book_name = book_name.replace('v{}'.format(i), '').replace(' ', '')
        in_words = get_in_braket(book_name)
        books_.append(remove_bracket(book_name))
        for in_word in in_words:
            books_.append(in_word.replace('(', '').replace(')', ''))

stratums = stratums.findall('관직명')
stratums = [remove_bracket(x.findtext('관직')) for x in stratums]

people = people.findall('인물')
people = [remove_bracket(x.findtext('TITLENAME')) for x in people]

result_dict = {}

title_doc_list = load_pickle('../keyword_extractor/data/title_doc_list.pickle')
for title, doc in title_doc_list:
    result_dict[title] = 0
    add_text_on_file('sentences.txt', doc+'\n')

for elem in books_ + stratums + people:
    if elem.find('?') > -1 or elem.find('···') > -1:
        continue
    result_dict[elem] = 0

# for v in result_dict.keys():
#     add_text_on_file('sentences.txt', v+'\n')


# def get_jongsung_TF(sample_text):
#     sample_text_list = list(sample_text)
#     last_word = sample_text_list[-1]
#     last_word_jamo_list = list(j2hcj(h2j(last_word)))
#     last_jamo = last_word_jamo_list[-1]
#     jongsung_TF = "T"
#     if last_jamo in ['ㅏ', 'ㅑ', 'ㅓ', 'ㅕ', 'ㅗ', 'ㅛ', 'ㅜ', 'ㅠ', 'ㅡ', 'ㅣ', 'ㅘ', 'ㅚ', 'ㅙ', 'ㅝ', 'ㅞ', 'ㅢ', 'ㅐ,ㅔ', 'ㅟ', 'ㅖ', 'ㅒ']:
#         jongsung_TF = "F"

#     return jongsung_TF


# with open("./user-nnp.csv", 'r', encoding='utf-8') as f:
#     file_data = f.readlines()
# file_data = []
# word_list = result_dict.keys()

# cnt = 0
# for word in word_list:
#     try:
#         jongsung_TF = get_jongsung_TF(word)
#         word = word.replace(',', ' ')
#         if word.find(',') > -1:
#             print(word)
#         line = None
#         if jongsung_TF:
#             line = '{},1786,3546,0,NNP,*,{},{},*,*,*,*\n'.format(
#                 word, jongsung_TF, word)
#         else:
#             line = '{},1786,3545,0,NNP,*,{},{},*,*,*,*\n'.format(
#                 word, jongsung_TF, word)
#         add_text_on_file('nnp.csv', line)
#     except:
#         continue

# for idx, line in enumerate(file_data):
#     elems = line.split(',')
#     elems[3] = '0'
#     new_line = ''
#     for elem in elems:
#         new_line += elem + ','
#     file_data[idx] = new_line[0:len(new_line)-1]


# with open("./user-nnp.csv", 'w', encoding='utf-8') as f:
#     for line in file_data:
#         f.write(line)
