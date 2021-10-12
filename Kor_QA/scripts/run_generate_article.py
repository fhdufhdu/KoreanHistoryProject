from argparse import ArgumentParser

import json
import torch
from tokenizers import SentencePieceBPETokenizer
from torch.utils.data import DataLoader
from tqdm import tqdm
from transformers import GPT2LMHeadModel, PreTrainedTokenizerFast

from korquad_qg.config import QGConfig
from korquad_qg.dataset import MAX_QUESTION_SPACE, MIN_QUESTION_SPACE, QAExample, QGDecodingDataset, load_as_dataset

parser = ArgumentParser()
parser.add_argument("-m", "--model-path", type=str, required=True)
parser.add_argument("-s", "--num-samples", type=int)
parser.add_argument("-b", "--num-beams", type=int, default=5)

def main():
    config = QGConfig()
    args = parser.parse_args()

    # tokenizer = PreTrainedTokenizerFast(tokenizer_file=config.vocab_path)
    tokenizer = SentencePieceBPETokenizer.from_file(
        vocab_filename=config.vocab_path, merges_filename=config.tokenizer_merges_path, add_prefix_space=False
    )
    model = GPT2LMHeadModel.from_pretrained(config.gpt_model_hub_name)
    # model.resize_token_embeddings(len(tokenizer))
    model.load_state_dict(torch.load(args.model_path, map_location="cpu"))
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model = model.to(device)

    dataset_path = "/home/wowns/data/KoreanHistoryProject/vocab/data/custom_data/as_set.json"
    examples = load_as_dataset(dataset_path)
    examples = examples[60000:]

    # examples = [
    #     QAExample(
    #         "강윤소는 고려후기 원종폐립사건 당시의 관리. 폐립 강윤소는 원래 신안공왕전의 가노로 처음에 환자가 되었는데, 몽고어 해독을 잘하였다.교활하고 아첨을 잘하며, 원종의 총애를 받았다. 낭장에 올라 여러 번 원나라에 사신으로 다녀온 공이 있어 장군으로 승진되었으며, 1268년김준의 무리를 죽일 때 평소 가까웠던 임연에게 김준을 죽이도록 하여 일등공신이 되고, 대장군에 올랐다.1269년 임연이 왕의 폐립을 꾀하여 안경공왕창을 세우고 원종을 용암궁에 유폐시킬 때, 이미 왕을 배반했으나 원종이 곧 복위하여 원나라에 가게 되자, 임연의 심복이 되어 스스로 왕을 호종, 돌아와 상장군에 올랐다.세자 왕심이 고관의 자제를 이끌고 원나라에 갈 때 왕의 폐립사건 때문에 뽑히지 않았으나 자의로 원나라에 가서 개체주 하고, 귀국한 뒤에는 스스로 원나라의 사신처럼 행세하며, 왕을 보고도 절을 하지 않았다.왕이 노하였으나 제어할 수가 없었고, 유사도 감히 힐난하지 못하였다. 원나라에 있을 때 홍다구에게 아부하여, 고려에는 많은 군량의 저축이 있다고 거짓말을 함으로써 원나라가 고려에 사신을 보내 군량을 독촉하게 하였다.1275년 군부판서와 응양군상장군에 올랐는데 그 신분이 천례출신이라 하여 감찰사의 탄핵으로 면직되었다가, 이어 밀직부사에 올랐다.1279년 대장군 김자정과 함께 사패를 사칭하여 많은 민전을 빼앗다가 발각되어 신흥창에 몰수당하였으며, 1283년 판삼사사로 물러났다.",
    #         "폐립",
    #     ),
    # ]

    dataset = QGDecodingDataset(examples, tokenizer, config.max_sequence_length)
    dataloader = DataLoader(dataset, batch_size=1)

    model = model.to(device)
    model.eval()

    generated_results = []

    for i, batch in tqdm(enumerate(dataloader), desc="generate", total=len(dataloader)):
        input_ids, attention_mask = (v.to(device) for v in batch)
        origin_seq_len = input_ids.size(-1)

        decoded_sequences = model.generate(
            input_ids=input_ids,
            attention_mask=attention_mask,
            max_length=origin_seq_len + MAX_QUESTION_SPACE,
            min_length=origin_seq_len + MIN_QUESTION_SPACE,
            pad_token_id=0,
            bos_token_id=1,
            eos_token_id=2,
            do_sample=True,
            num_beams=5,
            repetition_penalty=1.3,
            no_repeat_ngram_size=3,
            num_return_sequences=3,
        )

        for decoded_tokens in decoded_sequences.tolist():
            decoded_question_text = tokenizer.decode(decoded_tokens[origin_seq_len:])
            decoded_question_text = decoded_question_text.split("</s>")[0].replace("<s>", "")
            generated_results.append(
                (examples[i].context, examples[i].answer, examples[i].question, decoded_question_text)
            )

    result = {}
    result['data'] = []

    with open("./as_generate_set2.json", "w") as f:
        for context, answer, question, generated_question in generated_results:
            example = {}
            example['doc'] = context
            example['answer'] = answer
            example['generated_question'] = generated_question
            result['data'].append(example)

            # print(f"문맥\t{context}\n")
            # print(f"답변\t{answer}\n")
            # print(f"생성된 질문\t{generated_question}\n")
            # if question is not None:
            #     print(f"실제 질문\t{question}")
            # print()
        
        json.dump(result, f, indent=4)


if __name__ == "__main__":
    main()