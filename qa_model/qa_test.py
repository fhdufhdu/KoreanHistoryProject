import sys
from os import path
import torch
from transformers.modeling_bert import BertForQuestionAnswering
from transformers.tokenization_bert import BertTokenizer
from tokenization_kobert import KoBertTokenizer

if __package__ is None:
    current_path = path.dirname(path.dirname(path.abspath(
        '/home/fhdufhdu/vscode/KoreanHistoryProject/keyword_extractor/keyword_extractor_ver_W2V.ipynb')))
    sys.path.append(current_path)
    from util.func import load_json
else:
    from ..util.func import load_json

model = BertForQuestionAnswering.from_pretrained('./model_wordpiece_1')
tokenizer = BertTokenizer.from_pretrained('./model_wordpiece_1')
# model = BertForQuestionAnswering.from_pretrained('./models')
# tokenizer = KoBertTokenizer.from_pretrained('./models')

data_set = load_json('custom_dev_test.json')
for idx in [i for i in range(510, 1000)]:
    pa = data_set['data'][idx]['paragraphs'][0]
    context = ''
    for qa in pa['qas']:
        context = pa['context']
        break
    
    print('지문 :', context)
    print('질문 입력 :', end='')
    question = input()
    inputs = tokenizer.encode_plus(
        question, context, add_special_tokens=True, return_tensors='pt')
    input_ids = inputs["input_ids"].tolist()[0]
    text_tokens = tokenizer.convert_ids_to_tokens(input_ids)

    answer_start_vector, answer_end_vector = model(**inputs)
    as_idx = torch.argmax(answer_start_vector)
    ae_idx = torch.argmax(answer_end_vector) + 1

    answer = tokenizer.convert_tokens_to_string(text_tokens[as_idx:ae_idx])
    print('예측한 답변 :', answer)
    print()
