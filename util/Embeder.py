'''
코버트 실행 환경
python==3.6
torch==1.7.1
transforers==3.5.1
'''

import torch
from torch import nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader

import gluonnlp as nlp
import numpy as np

from KoBERT.kobert.utils import get_tokenizer
from KoBERT.kobert.pytorch_kobert import get_pytorch_kobert_model

from transformers import AdamW
from transformers.optimization import get_cosine_schedule_with_warmup

from tqdm import tqdm

'''
[버트 데이터셋 클래스]
버트 토크나이저와 문장리스트를 받아서 버트에 넣을 수 있는
token ids, segment ids, attention masking을 생성
'''
class BERTDataset(Dataset):
    def __init__(self, dataset, bert_tokenizer, max_len,
                 pad=True, pair=True):
        transform = nlp.data.BERTSentenceTransform(
            bert_tokenizer, max_seq_length=max_len, pad=pad, pair=pair)

        self.sentences = [transform([d]) for d in dataset]
    def __getitem__(self, i):
        return self.sentences[i]

    def __len__(self):
        return (len(self.sentences))


# 토큰 및 세그먼트 임베딩과 마스킹 클래스
class SentenceEmbeder:
    PAD = True
    PAIR = False
    BATCH_SIZE = 2

    def __init__(self, max_len):
        self.MAX_LEN = max_len
        self.device = torch.device("cuda:0")
        bertmodel, self.vocab = get_pytorch_kobert_model()
        self.bertmodel = bertmodel.to(self.device)
        tokenizer = get_tokenizer()
        self.tokenizer = nlp.data.BERTSPTokenizer(
            tokenizer, self.vocab, lower=False)

    def gen_attention_mask(self, token_ids, valid_length):
        attention_mask = torch.zeros_like(token_ids)
        for i, v in enumerate(valid_length):
            attention_mask[i][:v] = 1
        return attention_mask.float()

    def encode(self, sent_list):
        data_train = BERTDataset(
            sent_list, self.tokenizer, self.MAX_LEN, SentenceEmbeder.PAD, SentenceEmbeder.PAIR)
        train_dataloader = torch.utils.data.DataLoader(
            data_train, batch_size=SentenceEmbeder.BATCH_SIZE, num_workers=5)

        r_s = []
        r_p = []
        for token_ids, valid_length, segment_ids in train_dataloader:
            token_ids = token_ids.long().to(self.device)
            segment_ids = segment_ids.long().to(self.device)
            valid_length = valid_length.to(self.device)
            attention_mask = self.gen_attention_mask(token_ids, valid_length)
            sequence, pooler = self.bertmodel(
                token_ids, attention_mask, segment_ids)

            for s, p in zip(sequence, pooler):
                r_s.append(s)
                r_p.append(p)
            del token_ids, segment_ids, valid_length, attention_mask,
            torch.cuda.empty_cache()
        return r_s, r_p
