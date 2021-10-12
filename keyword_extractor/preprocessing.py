import sys
from os import path

if __package__ is None:
    current_path = path.dirname(path.dirname(path.abspath(__file__)))
    sys.path.append(current_path)
    from util.func import save_pickle, load_pickle, remove_bracket, load_json
else:
    from ..util.func import save_pickle, load_pickle, remove_bracket, load_json


def remove(doc, is_title):
    doc = remove_bracket(doc)
    if is_title == False:
        doc = doc.replace('『', '').replace(
            '』', '').replace('‘', '').replace('’', '').replace('「', '').replace('」', '').replace('·', ',').replace('“', '').replace('”', '')
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
            doc = doc.replace(remove_word, '')
    return doc


title_doc_list = []
for i in range(15):
    history_dict = load_json('../crawler/data/history_{}.json'.format(i))
    history_list = history_dict['list']
    for dict_ in history_list:
        if dict_['title'].find('세종') > -1:
            print(dict_['document_ver2'])
        title_doc_list.append(
            (remove(dict_['title'], True), remove(dict_['document_ver2'], False)))
    print(remove(dict_['title'], True), remove(dict_['document_ver2'], False))
# save_pickle('data/title_doc_list.pickle', title_doc_list)

# document_ = load_pickle('data/title_doc_list.pickle')
# print(len(document_))
# save_docs = []
# for idx, doc in enumerate(document_):
#     if idx % 10000 == 0 and idx != 0:
#         save_pickle(
#             'data/title_doc_list_{}.pickle'.format(int(idx/10000)), save_docs)
#         print(save_docs[0], '\n')
#         del save_docs
#         save_docs = []
#     save_docs.append(doc)
# save_pickle(
#     'data/title_doc_list_{}.pickle'.format(int(idx/10000 + 1)), save_docs)
# print(save_docs[0], '\n')

# document_ = load_pickle('data/title_doc_list.pickle')
# for idx, doc in enumerate(document_):
#     if doc[0] == '박금철':
#         print(doc)


# document_ = load_pickle('data/document_list.pickle')
# save_docs = [기
# for idx, doc in enumerate(document_):
#     if idx % 10000 == 0 and idx != 0:
#         save_pickle(
#             'data/document_list_part{}.pickle'.format(int(idx/10000)), save_docs)
#         print(save_docs[0], '\n')
#         del save_docs
#         save_docs = []
#     save_docs.append(doc)
# save_pickle(
#     'data/document_list_part{}.pickle'.format(int(idx/10000 + 1)), save_docs)
# print(save_docs[0], '\n')

# for i in tqdm(range(1, 10)):
#     document_ = load_pickle('data/document_list_part{}.pickle'.format(i))
#     # for doc in document_:
#     #     print(doc)
#     result_docs = []
#     for doc in tqdm(document_):
#         doc = remove_bracket(doc)
#         doc = doc.replace('『', '').replace(
#             '』', '').replace('‘', '').replace('’', '').replace('「', '').replace('」', '').replace('·', ',').replace('“', '').replace('”', '')
#         for j in range(10):
#             doc = doc.replace('0{})'.format(j), '')
#         idx = doc.find('키워드')
#         if idx >= 0:
#             remove_word = None
#             for k in range(idx, len(doc)):
#                 if doc[k] == ' ':
#                     remove_word = doc[idx:k]
#                     break
#             doc = doc.replace(remove_word, '')
#         result_docs.append(doc)
#     save_pickle('data/document_list_part{}.pickle'.format(i), result_docs)
#     print(result_docs[0], '\n')


# # %%
# embedding_model = Word2Vec(tokenized_sentences, size=100,
#                            window=5, min_count=1, workers=4, iter=100, sg=1)


# # %%
# with open('w2v_model/21_07_20.pickle', 'wb') as f:
#     pickle.dump(embedding_model, f)

# with open('w2v_model/21_07_20.pickle', 'rb') as f:
#     similar_list = pickle.load(f)


# # %%
# words = get_cdks_with_parser(document_list[0])
# similar_list = []
# for word in words:
#     similar_list.append(
#         (word, embedding_model.wv.similarity(w1=title[0], w2=word)))
# similar_list = sorted(similar_list, key=lambda sim: sim[1], reverse=True)

# print(similar_list)
