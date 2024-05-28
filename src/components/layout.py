from dash import html
import dash_bootstrap_components as dbc

from src.components.controls import controls
from src.components.graph import graph

layout = dbc.Container([
    html.H1('Classification Labeler'),
    html.Hr(),
    dbc.Row([
        dbc.Col(controls, class_name='col-4'),
        dbc.Col([graph, ], class_name='col-8')
    ], align='center'),
    dbc.Alert(
        "Done",
        id="alert-success",
        is_open=False,
        color='success',
        duration=4000,
        class_name='mt-4',
    ),
    dbc.Alert(
        "Fail",
        id="alert-fail",
        is_open=False,
        color='danger',
        duration=4000,
        class_name='mt-4',
    ),
], fluid=True)
