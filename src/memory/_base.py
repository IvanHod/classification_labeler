from abc import ABC

import pandas as pd


class AbstractMemory(ABC):
    def set_initial_df(self, df: pd.DataFrame) -> None:
        raise NotImplementedError()

    def get_initial_df(self) -> pd.DataFrame:
        raise NotImplementedError()

    def set_target_column(self, target_column: str):
        raise NotImplementedError()

    def get_target_column(self) -> str:
        raise NotImplementedError()

    def set_decomposition_df(self, df: pd.DataFrame):
        raise NotImplementedError()

    def get_decomposition_df(self) -> pd.DataFrame:
        raise NotImplementedError()

    def update_labels(self, labels: pd.Series | None = None) -> None:
        raise NotImplementedError()

    def get_labels(self) -> pd.Series:
        raise NotImplementedError()

    def get_output_df(self) -> pd.DataFrame:
        raise NotImplementedError()
