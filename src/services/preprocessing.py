import pandas as pd

from src.services import import_tool


def encode(df: pd.DataFrame, method_name: str, columns: list[str] = None):
    if columns is None:
        columns = df.select_dtypes(include=['object', 'category']).columns.tolist()

    res = df.copy()
    for col in columns:
        instance = import_tool.import_model(method_name)
        res[col] = instance.fit_transform(df[col])

    return res


def impute(df: pd.DataFrame, method_name: str):
    instance = import_tool.import_model(method_name)

    res = instance.fit_transform(df)
    res = pd.DataFrame(res, index=df.index, columns=df.columns)

    return res


def normalize(df: pd.DataFrame, method_name: str, columns: list[str] = None):
    if columns is None:
        columns = df.select_dtypes(include='number').columns.tolist()

    instance = import_tool.import_model(method_name)

    res = df.copy()
    values_scaled = instance.fit_transform(df[columns])
    res[columns] = values_scaled

    return res
