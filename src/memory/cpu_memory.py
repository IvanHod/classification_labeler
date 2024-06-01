import pandas as pd

from src.memory._base import AbstractMemory


class CPUMemory(AbstractMemory):
    _df_init: pd.DataFrame | None = None
    _df_decomposed: pd.DataFrame | None = None
    _target_column: str | None = None

    _exclude_columns: list[str] = None
    _labels: pd.Series | None = None

    def set_initial_df(self, df: pd.DataFrame) -> None:
        self._df_init = df

    def set_exclude_columns(self, columns: list[str]) -> None:
        self._exclude_columns = columns or []

    def get_initial_df(self) -> pd.DataFrame:
        if self._df_init is None:
            raise ValueError('First call "set_initial_df" method')

        return self._df_init

    def get_df(self) -> pd.DataFrame:
        df = self.get_initial_df()

        if self._exclude_columns:
            columns = list(filter(lambda c: c not in self._exclude_columns, df.columns))
            df = df[columns]

        return df

    def set_target_column(self, target_column: str):
        self._target_column = target_column

        self.update_labels()

    def get_target_column(self) -> str:
        if self._df_init is None:
            raise ValueError('First call "set_target_column" method')

        return self._target_column

    def set_decomposition_df(self, df: pd.DataFrame):
        self._df_decomposed = df

    def get_decomposition_df(self) -> pd.DataFrame:
        if self._df_init is None:
            raise ValueError('First call "set_decomposition_df" method')

        df_decomposed = self._df_decomposed
        if self._labels is not None:
            df_decomposed[self._target_column] = self._labels

        return df_decomposed

    def update_labels(self, labels: pd.Series | None = None) -> None:
        if labels is None and self._target_column in self._df_init:
            labels = self._df_init[self._target_column].copy()

        self._labels = labels

    def get_labels(self) -> pd.Series:
        if self._labels is None:
            raise ValueError('First call "update_labels" method')

        return self._labels.copy()

    def get_output_df(self) -> pd.DataFrame:
        df = self.get_initial_df().copy(deep=True)

        labels = self.get_labels()

        df[self._target_column] = labels

        return df
