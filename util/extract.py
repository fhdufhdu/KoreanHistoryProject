import json
import pandas as pd
from tqdm import tqdm
import sys
from os import path
import numpy as np
from tqdm import tqdm
from gensim.models import Word2Vec
from Embeder import SentenceEmbeder
from sklearn.metrics.pairwise import cosine_similarity

if __package__ is None:
    current_path = path.dirname(path.dirname(path.abspath(
        '/home/fhdufhdu/vscode/KoreanHistoryProject/keyword_extractor/keyword_extractor_ver_W2V.ipynb')))
    sys.path.append(current_path)
    from func import save_pickle, load_pickle, get_tokenized_sentences, remove_duplicated_keyword, save_json
else:
    from func import save_pickle, load_pickle, get_tokenized_sentences, remove_duplicated_keyword, save_json


title_list, sent_list = get_tokenized_sentences('.', True)
title_doc_list = load_pickle('/home/fhdufhdu/vscode/Project/data/keyword_extractor_data/title_doc_list.pickle')


# embedding_model = Word2Vec(sent_list, size=100, window = 5, min_count=1, workers=4, iter=50, sg=1)
# save_pickle('w2v_model/w2v.pickle', embedding_model)

w2v_model = load_pickle('/home/fhdufhdu/vscode/Project/KoreanHistoryProject/keyword_extractor/w2v_model/w2v.pickle')
bert_embeder = SentenceEmbeder(10)

def get_keyword(title, words, w2v, bert):
    # bert
    _, title_vector = bert.encode([title])
    _, noun_vectors = bert.encode(words)
    title_vector = title_vector[0]

    title_embedding_ = [[value.item() for value in title_vector]]
    candicates_embedding_ = [[value.item() for value in noun_vector]
                             for noun_vector in noun_vectors]
    distances = cosine_similarity(title_embedding_, candicates_embedding_)
    b_similar_list = [(words[i], sim) for i, sim in enumerate(distances[0])]

    # word2vec
    w_similar_list = []
    for word in words:
        try:
            w_similar_list.append(
                (word, w2v.wv.similarity(w1=title_list[0], w2=word)))
        except:
            continue

    final_list = []
    for (w_t, w_s), (_, b_s) in zip(w_similar_list, b_similar_list):
        final_list.append((w_t, w_s + b_s))

    final_list = sorted(final_list, key=lambda sim: sim[1], reverse=True)

    return final_list

quiz_title_list = pd.read_csv('/home/hsoh0423/vscode/HistoryQA/sorted_title_preQuiz.csv')
quiz_title_list2 = []

for i in quiz_title_list['title']:
    quiz_title_list2.append(i)
quiz_title_list2 = list(set(quiz_title_list2))

qas_dict = {}
qas_dict['data'] = []
count = 0
for i in quiz_title_list2:
    doc_idx = 0
    sent_idx = 0
    
    while sent_idx < len(title_doc_list):
        title = title_list[sent_idx]
        title_with_doc, doc = title_doc_list[sent_idx]
        sent = sent_list[sent_idx]

        if i == title:
            qas_set = {}
            qas_set['title'] = title
            qas_set['doc'] = doc
            qas_set['answer'] = title
            qas_dict['data'].append(qas_set)
            if title == title_with_doc:
                keywords = get_keyword(title, remove_duplicated_keyword(sent), w2v_model, bert_embeder)[:5]
                for keyword, _ in keywords:
                    qas_set = {}
                    qas_set['title'] = title
                    qas_set['doc'] = doc
                    qas_set['answer'] = keyword
                    qas_dict['data'].append(qas_set)
                count += 1
        sent_idx += 1
    print('progress : {}/{}'.format(count, len(quiz_title_list2)))
save_json('as_set_test.json', qas_dict)