import sentencepiece as spm
import sys
import os
from os import path

if True:
    project_dir = '/home/fhdufhdu/vscode/KoreanHistoryProject'
    sys.path.append(project_dir)
    from util.func import load_json, load_text, add_text_on_file, save_text


def get_sentence_list(dict_):
    data_list = dict_['data']
    result = []
    for data in data_list:
        for paragraph in data['paragraphs']:
            result.append(paragraph['context'])
            for qa in paragraph['qas']:
                result.append(qa['question'])
    return result


korquad_train = load_json('data/KorQuAD_v1.0_train.json')
korquad_dev = load_json('data/KorQuAD_v1.0_dev.json')
sentences = load_text('sentences.txt')

for idx, sentence in enumerate(sentences):
    sentences[idx] = sentence.replace('\n', '')

sentences += get_sentence_list(korquad_train) + get_sentence_list(korquad_dev)

for sentence in sentences:
    add_text_on_file('train_tokenizer.txt', sentence+'\n')

# import sentencepiece as spm

# # spm_train --input=data/train_tokenizer.txt  --model_prefix=sentencepiece/sp --vocab_size=32000 character_coverage=1.0 --model_type="unigram"

# input_file = 'train_tokenizer.txt'
# vocab_size = 119547

# sp_model_root = 'sentencepiece'
# if not os.path.isdir(sp_model_root):
#     os.mkdir(sp_model_root)
# sp_model_name = 'tokenizer_%d' % (vocab_size)
# sp_model_path = os.path.join(sp_model_root, sp_model_name)
# model_type = 'unigram'  # 학습할 모델 선택, unigram이 더 성능이 좋음'bpe'
# character_coverage = 1.0  # 전체를 cover 하기 위해, default=0.9995
# # user_defined_symbols = '[PAD],[UNK],[CLS],[SEP],[MASK],[BOS],[EOS],[UNK0],[UNK1],[UNK2],[UNK3],[UNK4],[UNK5],[UNK6],[UNK7],[UNK8],[UNK9],[unused0],[unused1],[unused2],[unused3],[unused4],[unused5],[unused6],[unused7],[unused8],[unused9],[unused10],[unused11],[unused12],[unused13],[unused14],[unused15],[unused16],[unused17],[unused18],[unused19],[unused20],[unused21],[unused22],[unused23],[unused24],[unused25],[unused26],[unused27],[unused28],[unused29],[unused30],[unused31],[unused32],[unused33],[unused34],[unused35],[unused36],[unused37],[unused38],[unused39],[unused40],[unused41],[unused42],[unused43],[unused44],[unused45],[unused46],[unused47],[unused48],[unused49],[unused50],[unused51],[unused52],[unused53],[unused54],[unused55],[unused56],[unused57],[unused58],[unused59],[unused60],[unused61],[unused62],[unused63],[unused64],[unused65],[unused66],[unused67],[unused68],[unused69],[unused70],[unused71],[unused72],[unused73],[unused74],[unused75],[unused76],[unused77],[unused78],[unused79],[unused80],[unused81],[unused82],[unused83],[unused84],[unused85],[unused86],[unused87],[unused88],[unused89],[unused90],[unused91],[unused92],[unused93],[unused94],[unused95],[unused96],[unused97],[unused98],[unused99]'
# user_defined_symbols = '[PAD],[UNK],[CLS],[SEP],[MASK],[BOS],[EOS]'

# input_argument = '--input=%s --model_prefix=%s --vocab_size=%s --user_defined_symbols=%s --model_type=%s --character_coverage=%s'
# cmd = input_argument % (input_file, sp_model_path, vocab_size,
#                         user_defined_symbols, model_type, character_coverage)

# spm.SentencePieceTrainer.Train(cmd)
# print('train done')

# # sp = spm.SentencePieceProcessor()
# # sp.Load('{}.model'.format('sentencepiece/tokenizer_32000'))

# # tokens = sp.encode_as_pieces(
# #     '5·1경기장은 1989년 5월 1일 노동절에 준공되었다. 착공 당시에는 ‘능라도경기장’으로 불리다가 1989년 4월 중앙인민위원회 정령으로 ‘인민대경기장’이라고 명명하였으나, 이틀 뒤 중앙인민위원회 정령을 다시 발표하면서 현재의 명칭으로 개칭되었다.연면적 20만7000㎡에 15만석 규모의 주경기장과 각종 보조경기장, 3개의 축구훈련장, 실내연습장을 갖추고 있다. 제13차 세계청년학생축전의 개회 및 폐회식장으로 이용된 바 있다.')
# # ids = sp.encode_as_ids('5·1경기장은 1989년 5월 1일 노동절에 준공되었다. 착공 당시에는 ‘능라도경기장’으로 불리다가 1989년 4월 중앙인민위원회 정령으로 ‘인민대경기장’이라고 명명하였으나, 이틀 뒤 중앙인민위원회 정령을 다시 발표하면서 현재의 명칭으로 개칭되었다.연면적 20만7000㎡에 15만석 규모의 주경기장과 각종 보조경기장, 3개의 축구훈련장, 실내연습장을 갖추고 있다. 제13차 세계청년학생축전의 개회 및 폐회식장으로 이용된 바 있다.')

# # print(ids)
# # print(tokens)

# # tokens = sp.decode_pieces(tokens)
# # ids = sp.decode_ids(ids)

# # print(ids)
# # print(tokens)


# # from tokenization_kor_history import KorHistoryTokenizer

# # tokenizer = KorHistoryTokenizer(
# #     vocab_file='sentencepiece/tokenizer_32000.model', vocab_txt='vocab.txt')

# # tokenizer.tokenize('가군')


# vocab = load_text('sentencepiece/tokenizer_119547.vocab')
# for idx, word in enumerate(vocab):
#     add_text_on_file('vocab.txt', word.split('\t')[0]+'\n')
