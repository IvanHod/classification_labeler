from dash import html
import dash_bootstrap_components as dbc


output_list = dbc.AccordionItem([
    dbc.Label('Выходные данные:'),
    dbc.Row([
        dbc.Label('Наименование выходного файла'),
        dbc.Col([
            dbc.Input(id='input-output-file_name',
                      type='text',
                      class_name='form-control',
                      placeholder='The name of output *.csv file'),
        ], class_name='col-12')
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Button('Сохранить в csv файл', id='btn-save_results', n_clicks=0, class_name='btn btn-success')
        ], class_name='d-grid')
    ], class_name='mt-2'),
    dbc.Row([
        dbc.Col([
            html.Div(id='hidden-save-div', style={'display': 'none'})
        ], class_name='d-grid')
    ])
], title='Output')
