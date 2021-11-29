from typing import NamedTuple


class QGConfig(NamedTuple):
    train_dataset: str = "data/History_train_After_FT_V3.csv"
    dev_dataset: str = "data/History_train_After_FT_V1.csv"

    max_sequence_length: int = 512

    epochs: int = 100
    lr: float = 5e-5
    train_batch_size: int = 2
    dev_batch_size: int = 2

    output_dir: str = "outputs/"

    grad_clip: float = 1.0
    warmup_ratio: float = 0.1

    train_log_interval: int = 100
    validation_interval: int = 1000
    save_interval: int = 1000
    random_seed: int = 0
