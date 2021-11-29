import json
import pickle
from typing_extensions import final
from koalanlp.Util import initialize, finalize
from koalanlp.proc import Parser
from koalanlp import API
from tqdm import tqdm


def save_json(file_name, dict_):
    with open(file_name, 'w', encoding='utf-8') as file:
        json.dump(dict_, file, indent='\t', ensure_ascii=False)


def load_json(file_name):
    dict_ = None
    with open(file_name, 'r') as file:
        dict_ = json.load(file)
    return dict_


def save_text(file_name, text=''):
    f = open(file_name, 'w')
    f.write(text)
    f.close()


def save_text_list(file_name, text_list):
    f = open(file_name, 'w')
    if text_list != None:
        for text_elem in text_list:
            f.write(text_elem)
            f.write('\n')
    f.close()


def load_text(file_name) -> list:
    text_list = []
    with open(file_name, 'r') as f:
        while True:
            line = f.readline()
            if not line:
                break
            text_list.append(line)
        f.close()
    return text_list


def add_text_on_file(file_name, text):
    with open(file_name, 'a', encoding='utf-8-sig') as f:
        f.write(text)
        f.close()


def save_pickle(file_name, obj):
    with open(file_name, 'wb') as f:
        pickle.dump(obj, f)


def load_pickle(file_name):
    with open(file_name, 'rb') as f:
        obj = pickle.load(f)
        return obj


def returnPreSubject(korean_word):
    CHOSUNG_LIST = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ',
                    'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
    JUNGSUNG_LIST = ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ',
                     'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ']
    JONGSUNG_LIST = [' ', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ',
                     'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']

    NUMBER_LIST = ['영', '일', '이', '삼', '사', '오', '육', '칠', '팔', '구']
    ENG_LIST = ['에이', '비', '씨', '디', '이', '에프', '지', '에이치', '아이', '제이', '케이', '엘',
                '엠', '엔', '오', '피', '큐', '알', '에스', '티', '유', '브이', '더블유', '엑스', '와이', '제트']
    if korean_word is not None and len(korean_word) > 0:
        w = korean_word[len(korean_word)-1]  # 마지막 글자 획득

        # 영어인 경우 구분해서 작성함.
        if '가' <= w <= '힣':
            # 588개 마다 초성이 바뀜.
            ch1 = (ord(w) - ord('가'))//588
            # 중성은 총 28가지 종류
            ch2 = ((ord(w) - ord('가')) - (588*ch1)) // 28
            ch3 = (ord(w) - ord('가')) - (588*ch1) - 28*ch2
            if ch3 == 0:
                return '는'
            else:
                return '은'
        elif '0' <= w <= '9':  # 숫자일 경우
            return returnPreSubject(NUMBER_LIST[ord(w)-ord('0')])
        elif type(w) is int and 0 <= w <= 9:
            return returnPreSubject(NUMBER_LIST[w])
        elif 'a' <= w <= 'z':  # 영문일 경우
            return returnPreSubject(ENG_LIST[ord(w)-ord('a')])
        elif 'A' <= w <= 'Z':
            return returnPreSubject(ENG_LIST[ord(w)-ord('A')])
        else:
            return returnPreSubject(korean_word[:len(korean_word)-1])

    return '는'  # 디폴트로 '는' 리턴


def remove_bracket(doc):
    remove_list = []

    start_idx = -1
    for i in range(len(doc)):
        if doc[i] == '(':
            start_idx = i
        if start_idx != -1 and doc[i] == ')':
            remove_list.append(doc[start_idx:i+1])
            start_idx = -1
    start_idx = -1
    for i in range(len(doc)):
        if doc[i] == '[':
            start_idx = i
        if start_idx != -1 and doc[i] == ']':
            remove_list.append(doc[start_idx:i+1])
            start_idx = -1
    start_idx = -1
    for i in range(len(doc)):
        if doc[i] == '{':
            start_idx = i
        if start_idx != -1 and doc[i] == '}':
            remove_list.append(doc[start_idx:i+1])
            start_idx = -1

    for remove_word in remove_list:
        doc = doc.replace(remove_word, '')

    return doc


def remove_duplicated_keyword(keywords):
    temp_dict = {}
    for k in keywords:
        temp_dict[k] = 0
    keywords = list(temp_dict.keys())
    return keywords


class DependencyParser:
    first_init = False

    def __init__(self):
        if DependencyParser.first_init is False:
            self.close()
            self.init()
            DependencyParser.first_init = True

    def init(self):
        initialize(hnn='LATEST')
        self.parser = Parser(API.HNN)

    def close(self):
        finalize()

    def get_cdks_with_parser(self, doc):
        parsed = self.parser(doc)

        candidates = []
        for sentence in parsed:
            for dep in sentence.getDependencies():
                for it in dep.getDependent():
                    if it.tag == 'NNG' or it.tag == 'NNP':
                        candidates.append(it.surface)
        self.close()

        return remove_duplicated_keyword(candidates)

    def get_cdks_with_parsers(self, title_doc_list):
        try:
            start_idx = int(load_text('log/current_idx.txt')[0])
        except:
            start_idx = 0
        current_idx = 0
        for title, doc in tqdm(title_doc_list):
            if current_idx < start_idx:
                current_idx += 1
                continue
            try:
                print(title, len(doc))
                parsed = self.parser(doc)
            except Exception as e:
                self.close()
                self.init()
                add_text_on_file('log/error_log.txt',
                                 "{}///{}\n\n".format(title, doc))
                current_idx += 1
                save_text('log/current_idx.txt', "{}".format(current_idx))
                continue

            # 또는 parser.analyze(...), parser.invoke(...)
            w_candidates = ''
            b_candidates = ''
            for sentence in parsed:
                for dep in sentence.getDependencies():
                    for it in dep.getDependent():
                        w_candidates += it.surface + '///'
                        if (it.tag == 'NNG' or it.tag == 'NNP'):
                            b_candidates += it.surface + '///'

            add_text_on_file('data/b_sentence_list.txt',
                             title+'///'+b_candidates+'\n')
            add_text_on_file('data/w_sentence_list.txt',
                             title+'///'+w_candidates+'\n')

            current_idx += 1
            save_text('log/current_idx.txt', "{}".format(current_idx))
            del w_candidates, b_candidates


def get_tokenized_sentences(data_directory_path, is_for_bert=True):
    PREFIX = 'b'
    if is_for_bert is False:
        PREFIX = 'w'

    raw_sent_list = load_text(
        '/home/hsoh0423/vscode/HistoryQA/b_sentence_list_1.txt'.format(data_directory_path, PREFIX))

    title_list = []
    sent_list = []
    for sent in raw_sent_list:
        temp_list = sent.split("///")
        title = temp_list[0]
        words = temp_list[1:len(temp_list)]
        title_list.append(title)
        sent_list.append(words)

    return title_list, sent_list
