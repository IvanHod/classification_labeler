from dash import html, dcc
import dash_bootstrap_components as dbc

from src.services import files

init_files_names = files.load_csv_names(include_absent=True)


data_list = dbc.AccordionItem([
    dbc.Row([
        dbc.Col([
            dcc.Upload(id='source-file',
                       children=html.Div([
                           'Drag and Drop or ',
                           html.A('Select Files...')
                       ]),
                       style={
                           'width': '100%',
                           'height': '60px',
                           'lineHeight': '60px',
                           'borderWidth': '1px',
                           'borderStyle': 'dashed',
                           'borderRadius': '5px',
                           'textAlign': 'center',
                           'margin': '10px',
                           'cursor': 'pointer'
                       },
                       multiple=False)
        ], class_name='col-12')
    ]),
    dbc.Label('Or select file from uploaded ones:'),
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(init_files_names, files.MSG_NO_FILE, id='source-file_name')
        ], class_name='col-12')
    ]),
    dbc.Row([
        dbc.Label('Exclude features:'),
        dbc.Col([
            dcc.Dropdown(['-'], '-', id='feature_column_names_exclude', multi=True)
        ], class_name='col-12')
    ], class_name='mt-2'),
    dbc.Row([
        dbc.Label('Target column:'),
        dbc.Col([
            dcc.Dropdown(['-'], '-', id='target_column_name')
        ], class_name='col-12')
    ], class_name='mt-2'),
    dbc.Alert(
        "After you select the target column, it will take a while, while the server to decompose your data."
        "Please wait and do not click any button",
        id="alert-success",
        is_open=True,
        color='warning',
        class_name='mt-2',
    )
], title='Data')
