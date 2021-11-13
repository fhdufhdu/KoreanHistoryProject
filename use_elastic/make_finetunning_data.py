import pandas as pd
from func import save_pickle, load_pickle, remove_bracket, load_json, returnPreSubject, save_json

raw_csv = pd.read_csv(
    '/home/fhdufhdu/vscode/Project/data/bert_data/finetunning_bert.csv')

# finetunning_data = {
#     "paragraphs": [
#         {
#             "qas": [
#                 {
#                     "answers": [
#                         {
#                             "text": " ",
#                             "answer_start": 0
#                         }
#                     ],
#                     "id": " ",
#                     "question": " "
#                 }
#             ],
#             "context": " "
#         },
#     ]
# }
finetunning_data = {
    "version": "finetunning_bert"
}
data = []
cnt = 0
for i, row in raw_csv.iterrows():
    context = row['context']
    question = row['question']
    s_idx = row['start_index']
    e_idx = row['last_index']
    answers_text = row['answers']

    start_idx = context[s_idx:].find(answers_text)
    data_dict = {}
    paragraphs = []
    paragraph_dict = {}
    qas = []
    qas_dict = {}
    answers = []
    answers_dict = {}
    answers_dict['text'] = answers_text
    answers_dict['answer_start'] = start_idx + s_idx
    answers.append(answers_dict)
    qas_dict['answers'] = answers
    qas_dict['id'] = str(cnt)
    qas_dict['question'] = question
    qas.append(qas_dict)
    paragraph_dict['qas'] = qas
    paragraph_dict['context'] = context
    paragraphs.append(paragraph_dict)
    data_dict['paragraphs'] = paragraphs
    data_dict['title'] = answers_text
    data.append(data_dict)
    cnt += 1
    if i == 5000:
        finetunning_data['data'] = data
        save_json(
            '/home/fhdufhdu/vscode/Project/data/bert_data/finetunning_bert.json', finetunning_data)
        finetunning_data = {
            "version": "finetunning_bert_dev"
        }
        data = []
        cnt = 0

finetunning_data['data'] = data
save_json('/home/fhdufhdu/vscode/Project/data/bert_data/finetunning_bert_dev.json', finetunning_data)
