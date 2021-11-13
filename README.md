# KoreanHistoryProject

Transformer의 encoder(BERT)와 decoder(GPT2)를 활용하여 만든 역사QA 및 역사 퀴즈 생성 프로젝트입니다.

## 1. QA시스템

'BERT multilingual + Custom Tokenizer'를 활용한 Q&A 모델입니다.
KorQuAD 1.0을 통해 정답을 맞출 수 있도록 학습하였습니다.
퀴즈 생성 모델에서 나온 문제로 fine tunning을 한번 더 거쳤습니다.

## 2. 퀴즈 생성

'GPT2 multilingual + 한국어 위키 데이터 + 한국민족대백과사전 데이터'로 fine tunning을 거친 모델입니다.
KorQuAD 1.0을 통해 문맥에서 답에 맞는 질문을 생성하도록 학습하였습니다.
