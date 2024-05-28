import dash_bootstrap_components as dbc

from src.config import config


def get_style() -> str:
    style: str = getattr(dbc.themes, config.STYLESHEET, None)
    if style is None:
        raise KeyError(f'There is not style {config.STYLESHEET}')

    return style
