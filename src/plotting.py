import pandas as pd
import plotly.express as px

from src import config


def plot(df_decomposed: pd.DataFrame, target_column: str):
    df_decomposed[target_column] = df_decomposed[target_column].astype(str)
    fig = px.scatter(df_decomposed,
                     custom_data='index',
                     x='Factor 1',
                     y='Factor 2',
                     hover_data=['index'],
                     labels={'Factor 1': config.PLOT_XAXIS_LABEL, 'Factor 2': config.PLOT_YAXIS_LABEL},
                     color=target_column,
                     title=config.PLOT_TITLE,
                     height=600,
                     )

    fig.update_layout(title_x=0.5)
    if config.STYLESHEET == 'SKETCHY':
        fig.update_layout(
            font=dict(
                family='Neucha',
                size=config.PLOT_FONT_SIZE
            )
        )

    return fig
