from io import StringIO
from pathlib import Path

import pandas as pd

from src import config

MSG_NO_FILE = 'Absent'


def load_csv_names(extension: str = 'csv', include_absent: bool = True) -> list[str]:
    path = Path(config.INPUT_PATH)
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)

    files = []
    if include_absent:
        files.append(MSG_NO_FILE)

    return files + list(map(lambda v: v.name, path.glob(f'*.{extension}')))


def load_df(file: bytes, file_name: str) -> pd.DataFrame:
    if file:
        df = pd.read_csv(StringIO(file.decode('utf-8')))
    else:
        # we always write index, so it must be zero (0) column
        df = pd.read_csv(config.INPUT_PATH / file_name, index_col=0)

    return df


def get_df_columns(df: pd.DataFrame) -> list[str]:
    return list(df.columns)


def save_df(df: pd.DataFrame,
            file_name: str,
            sep: str = ',',
            index: bool = True,
            as_output: bool = True) -> None:

    if not file_name.endswith('.csv'):
        file_name = f'{file_name}.csv'

    path = config.OUTPUT_PATH if as_output else config.INPUT_PATH
    path_full = path / file_name

    if path_full.exists():
        if as_output and not config.OVERRIDE_OUTPUT:
            raise ValueError(f'There is such file "{file_name}" in output folder "{str(path)}"')
        elif not as_output and not config.OVERRIDE_INPUT:
            raise ValueError(f'There is such file "{file_name}" in input folder "{str(path)}"')

    df.to_csv(str(path_full), sep=sep, index=index)
