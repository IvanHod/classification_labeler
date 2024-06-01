import pandas as pd

from src.services import preprocessing, import_tool

_decomposition_methods_mapping = {
    'TSNE': 'sklearn.manifold.TSNE',
    'PCA': 'sklearn.decomposition.PCA',
    'KernelPCA': 'sklearn.decomposition.KernelPCA',
    'NMF': 'sklearn.decomposition.NMF',
    'FactorAnalysis': 'sklearn.decomposition.FactorAnalysis',
}


def decompose(
        df: pd.DataFrame,
        target_column: str,
        method_name: str = 'TSNE',
        method_params: dict[str, int | float | str] = None,
        encode_method: str | None = 'sklearn.preprocessing.LabelEncoder',
        impute_method: str | None = 'sklearn.impute.KNNImputer',
        scale_method: str | None = 'sklearn.preprocessing.StandardScaler'
) -> pd.DataFrame:
    """

    :param df: source DataFrame without "exclude columns"
    :param target_column: name of target column
    :param method_name: decomposition method name.
        Passed method must be in mapping "_decomposition_methods_mapping"
    :param method_params: parameters for decomposition method
        For now I did not add this field into interface
    :param encode_method: full path of encoding method to encode object or categorical features
    :param impute_method: full path of impute method to impute nan values
    :param scale_method: full path of scale method to scale only numerical columns
    :return:
    """

    if method_params is None:
        method_params = {}
    method_params = method_params | {'n_components': 2}

    if method_name not in _decomposition_methods_mapping:
        names = ', '.join(list(_decomposition_methods_mapping.keys()))
        raise KeyError(f'There is no such method {method_name}. Select one of possible: "{names}"')

    object_columns: list[str] = df.select_dtypes(include=['object', 'category']).columns.tolist()
    object_columns = list(set(object_columns) | {target_column, })
    if encode_method and object_columns:
        df = preprocessing.encode(df, encode_method, columns=object_columns)

    nan_columns = df.columns[df.isna().any(axis=0)].tolist()
    if impute_method and nan_columns:
        df = preprocessing.impute(df, impute_method)

    if scale_method:
        columns_to_scale = list(filter(lambda c: c not in object_columns, df.columns))
        df = preprocessing.normalize(df, scale_method, columns=columns_to_scale)

    X = df.drop(columns=[target_column], errors='ignore')\
        .select_dtypes(include='number')\
        .fillna(0)

    import_model: str = _decomposition_methods_mapping[method_name]
    instance = import_tool.import_model(import_model, **method_params)

    X_embedded = instance.fit_transform(X)
    df_tsne = pd.DataFrame(X_embedded, columns=['Factor 1', 'Factor 2'], index=df.index)
    df_tsne['index'] = df.index
    df_tsne[target_column] = df[target_column]

    return df_tsne
