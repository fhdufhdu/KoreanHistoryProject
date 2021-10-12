from typing import NamedTuple


class QGConfig(NamedTuple):
    train_dataset: str = "KorQuad_train_V1.csv"
    dev_dataset: str = "KorQuad_dev_V1.csv"

    max_sequence_length: int = 512

    epochs: int = 100
    lr: float = 5e-5
    train_batch_size: int = 2
    dev_batch_size: int = 2

    output_dir: str = "outputs/"

    grad_clip: float = 1.0
    warmup_ratio: float = 0.1

    train_log_interval: int = 50
    validation_interval: int = 3000
    save_interval: int = 3000
    random_seed: int = 0
