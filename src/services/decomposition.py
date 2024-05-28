import pandas as pd


_decomposition_methods_mapping = {
    'TSNE': 'sklearn.manifold.TSNE',
    'PCA': 'sklearn.decomposition.PCA',
    'KernelPCA': 'sklearn.decomposition.KernelPCA',
    'NMF': 'sklearn.decomposition.NMF',
    'FactorAnalysis': 'sklearn.decomposition.FactorAnalysis',
}


def decompose(df: pd.DataFrame,
              target_column: str,
              method_name: str = 'TSNE',
              method_params: dict[str, int | float | str] = None) -> pd.DataFrame:

    if method_params is None:
        method_params = {}
    method_params = method_params | {'n_components': 2}

    if method_name not in _decomposition_methods_mapping:
        names = ', '.join(list(_decomposition_methods_mapping.keys()))
        raise KeyError(f'There is no such method {method_name}. Select one of possible: "{names}"')

    method_path: str = _decomposition_methods_mapping[method_name]
    model_path, model_name = method_path.rsplit('.', 1)

    model = getattr(__import__(model_path, fromlist=[model_name]), model_name)
    instance = model(**method_params)

    X = df.drop(columns=[target_column], errors='ignore')\
        .select_dtypes(include='number')\
        .fillna(0)

    X_embedded = instance.fit_transform(X)
    df_tsne = pd.DataFrame(X_embedded, columns=['Factor 1', 'Factor 2'], index=df.index)
    df_tsne['index'] = df.index
    df_tsne[target_column] = df[target_column]

    return df_tsne
