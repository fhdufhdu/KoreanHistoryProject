from koalanlp.Util import initialize, finalize
from gensim.models import Word2Vec
from koalanlp.proc import Parser
from koalanlp import API
import numpy as np
from tqdm import tqdm
import pickle
import sys
from os import path
from multiprocessing import Process
from konlp.kma.klt2000 import klt2000

if __package__ is None:
    current_path = path.dirname(path.dirname(path.abspath(__file__)))
    sys.path.append(current_path)
    from util.func import save_pickle, load_pickle, DependencyParser, add_text_on_file
else:
    from ..util.func import save_pickle, load_pickle, DependencyParser, add_text_on_file


# parser = DependencyParser()
# title_doc_list = load_pickle('data/title_doc_list.pickle')
# parser.get_cdks_with_parsers(title_doc_list)


title_doc_list = load_pickle('data/title_doc_list.pickle')
k = klt2000()
for title, doc in tqdm(title_doc_list):
    nouns = k.nouns(doc)
    b_candidates = ''
    for noun in nouns:
        b_candidates += noun + '///'
    del nouns
    nouns = k.morphs(doc)
    w_candidates = ''
    for noun in nouns:
        w_candidates += noun + '///'
    add_text_on_file('data/b_sentence_list_1.txt',
                     title+'///'+b_candidates+'\n')
    add_text_on_file('data/w_sentence_list_1.txt',
                     title+'///'+w_candidates+'\n')
    
# k = klt2000()
# simple_txt = '흰꼬리수리는 수리과에 속하는 조류. 흰꼬리수리는 학명은 Haliaeetus albicilla (LINNAEUS)이다.수리류는 전 세계에서 218종이 알려져 있으나 우리나라에서는 21종이 알려져 있다. 이 중에서 흰꼬리수리·참수리·독수리·검독수리 등 4종은 매우 희귀한 종들로서 지구상에서 사라져가고 있는, 국제적으로 보호가 요청되고 있는 종들이므로 1982년 천연기념물 제243호로 지정하여 보호하고 있다.북반구 전역의 넓은 범위와 그린란드에 분포하며 결빙 후 일부의 집단은 남하, 이동하여 월동한다. 해안절벽·간석지·하천부지 부근에 살며 우리나라에서는 11∼3월에 모습을 나타내는 드문 겨울새이다.1산1란이 보통이고 35일간 알품기를 한 뒤 28∼35일간 육추(育雛)주 01)한다. 물고기·새·짐승 등을 포식한다. 몸길이는 수컷이 약 80㎝, 암컷은 95㎝이며, 날개의 길이는 182∼230㎝인 크고 육중한 수리이다. 황갈색의 머리와 백색의 꼬리를 제외하고는 균일한 어두운 갈색이다.낙동강하구언 건설 이전인 1950년대와 1960년대까지만 하여도 낙동강하구에는 10여 마리의 독수리·참수리·흰꼬리수리·검독수리 등 혼성군을 볼 수 있었으며, 그 밖의 지역, 한강 하구, 한강 서울수역 등지에서도 흰꼬리수리나 검독수리 등은 쉽게 눈에 띄었던 종들이었다.'
# print(k.nouns(simple_txt))
# print(k.morphs(simple_txt))

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
