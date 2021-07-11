from embedding.models.sent_eval import BERTEmbeddingEvaluator
model = BERTEmbeddingEvaluator(tune_model_fname="./embedding/data/sentence-embeddings/bert/tune-ckpt",
                               pretrain_model_fname="./embedding/data/sentence-embeddings/bert/pretrain-ckpt/bert.model",
                               options_fname="./embedding/data/sentence-embeddings/bert/pretrain-ckpt/options.json",
                               vocab_fname="./embedding/data/sentence-embeddings/bert/pretrain-ckpt/bert-vocab.txt",
                               max_characters_per_token=30, dimension=256, num_labels=2)
