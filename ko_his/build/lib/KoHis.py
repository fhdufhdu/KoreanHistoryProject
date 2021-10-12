import torch
from transformers import BertForQuestionAnswering
from transformers import BertTokenizer

DEFAULT_PATH = '/home/fhdufhdu/vscode/Project/data/models/model_bert'

class KoHisQnA:
    def __init__(self, model_path=DEFAULT_PATH, tokenizer_path=DEFAULT_PATH):
        self.change_path(model_path, tokenizer_path)

    def change_path(self, model_path, tokenizer_path) -> None:
        self.model_path = model_path
        self.tokenizer_path = tokenizer_path

        try:
            del self.model, self.tokenizer
        except:
            print('...initailizing...')

        self.model = BertForQuestionAnswering.from_pretrained(self.model_path)
        self.tokenizer = BertTokenizer.from_pretrained(self.tokenizer_path)

    def do_ask_to_model(self, question, context, add_special_tokens=True, return_tensors='pt') -> tuple:
        inputs = self.tokenizer.encode_plus(
            question, context, add_special_tokens=add_special_tokens, return_tensors=return_tensors)

        # 모델에 데이터 집어넣기
        answer_start_vector, answer_end_vector = self.model(**inputs)
        as_idx = torch.argmax(answer_start_vector)
        ae_idx = torch.argmax(answer_end_vector) + 1

        # 정답을 구하기 위한 과기
        input_ids = inputs["input_ids"].tolist()[0]
        text_tokens = self.tokenizer.convert_ids_to_tokens(input_ids)
        answer = self.tokenizer.convert_tokens_to_string(
            text_tokens[as_idx:ae_idx])

        return (int(as_idx), int(ae_idx), answer)


'''
========================
         사용방법
========================
qa = KoHisQnA()
print(qa.do_ask_to_model('조선시대 4대 왕은?', '세종은 조선전기 제4대 왕. 세종은 재위 1418∼1450. 본관은 전주. 이름은 이도, 자는 원정. 태종의 셋째아들이며, 어머니는 원경왕후 민씨이다. 비는 심온의 딸 소헌왕후이다.1408년 충녕군에 봉해지고, 1412년 충녕대군에 진봉되었으며, 1418년 6월 왕세자에 책봉되었다가 같은 해 8월에 태종의 양위를 받아 즉위하였다.'))
'''
qa = KoHisQnA()
print(qa.do_ask_to_model('조선시대 4대 왕은?', '세종은 조선전기 제4대 왕. 세종은 재위 1418∼1450. 본관은 전주. 이름은 이도, 자는 원정. 태종의 셋째아들이며, 어머니는 원경왕후 민씨이다. 비는 심온의 딸 소헌왕후이다.1408년 충녕군에 봉해지고, 1412년 충녕대군에 진봉되었으며, 1418년 6월 왕세자에 책봉되었다가 같은 해 8월에 태종의 양위를 받아 즉위하였다.'))
