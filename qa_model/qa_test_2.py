import sys
from os import path
import torch
from transformers import BertForQuestionAnswering, AutoTokenizer, GPT2Tokenizer
from transformers.tokenization_bert import BertTokenizer
from tokenization_kor_history import KorHistoryTokenizer
from tokenization_kobert import KoBertTokenizer

if __package__ is None:
    current_path = path.dirname(path.dirname(path.abspath(
        '/home/fhdufhdu/vscode/KoreanHistoryProject/keyword_extractor/keyword_extractor_ver_W2V.ipynb')))
    sys.path.append(current_path)
    from util.func import load_json
else:
    from ..util.func import load_json

model = BertForQuestionAnswering.from_pretrained(
    './model_wordpiece_1')
tokenizer = BertTokenizer.from_pretrained(
    './model_wordpiece_1')
tokenizer1 = KoBertTokenizer.from_pretrained('./models_old')

context = '세종은 조선전기 제4대 왕. 세종은 재위 1418∼1450. 본관은 전주. 이름은 이도, 자는 원정. 태종의 셋째아들이며, 어머니는 원경왕후 민씨이다. 비는 심온의 딸 소헌왕후이다.1408년 충녕군에 봉해지고, 1412년 충녕대군에 진봉되었으며, 1418년 6월 왕세자에 책봉되었다가 같은 해 8월에 태종의 양위를 받아 즉위하였다.'
question = '조선전기 제4대 왕은?'
print('입력한 문장 : {}'.format(question))
print('기존 Tokenizer 활용 : {}'.format([word.replace('▁', '')
      for word in tokenizer1.tokenize(question)]))
print('WordPiece+SentencePiece 활용 : {}'.format(tokenizer.tokenize(question)))
# print('기존 Vocab활용 : {}'.format(tokenizer1.tokenize(question)))
# print('Custom Vocab활용 : {}'.format(tokenizer.tokenize(question)))
inputs = tokenizer.encode_plus(
    question, context, add_special_tokens=True, return_tensors='pt')
input_ids = inputs["input_ids"].tolist()[0]
print(input_ids)
text_tokens = tokenizer.convert_ids_to_tokens(input_ids)
print(text_tokens)

answer_start_vector, answer_end_vector = model(**inputs)
as_idx = torch.argmax(answer_start_vector)
ae_idx = torch.argmax(answer_end_vector) + 1
print(as_idx, ae_idx)

answer = tokenizer.convert_tokens_to_string(text_tokens[as_idx:ae_idx])

print('문제 :', question)
print('지문 :', context)
print('예측한 답변 :', answer)
print()
