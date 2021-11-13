from elasticsearch import Elasticsearch
from konlpy.tag import Mecab
from KoHis import KoHisQnA

es = Elasticsearch("http://202.31.202.147:6006")
qa = KoHisQnA()

# 검색어

while(True):
    search_sentence = input("질문입력 : ")
    mecab_tokenizer = Mecab()
    nouns_list = mecab_tokenizer.nouns(search_sentence)

    for noun in nouns_list:
        docs = es.search(index='history_dict',
                         body={
                             "size": 2,
                             "query": {
                                 "multi_match": {
                                     "query": noun,
                                     "fields": ["title", "intro", "content", "search"]
                                 }
                             }
                         })
        for doc in docs['hits']['hits']:
            context = doc['_source']['document']
            for i in range(int((len(doc) / 500)) + 1):
                temp_context = context[500*i:500*(i+1)-1]
                answer = qa.do_ask_to_model(search_sentence, temp_context)
                temp_context = temp_context.split(".")
                answer_context = ''
                for j in range(len(temp_context) - 1):
                    answer_context = answer_context + temp_context[j] + '.'
                #start = answer[0] - 100 if answer[0] - 100 >= 0 else 0
                #end = answer[0] + 100 if answer[0] + 100 < 500 else 499

                print('답변:', answer[2])
                print('문서:', answer_context)
                print()
