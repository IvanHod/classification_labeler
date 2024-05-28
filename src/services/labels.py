import numpy as np
import pandas as pd

from src.memory._base import AbstractMemory


def update_labels(memory: AbstractMemory, label: str, indices: np.ndarray) -> pd.Series:
    label = str(label)

    target_column: str = memory.get_target_column()
    labels: pd.Series = memory.get_labels()
    labels.loc[indices] = label

    memory.update_labels(labels)

    return labels
