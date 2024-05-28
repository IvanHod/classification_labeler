from dash import html, dcc
import dash_bootstrap_components as dbc

algo_list = dbc.AccordionItem([
    dbc.Row([
        html.Label('Decomposition method:'),
        dbc.Col([
            dcc.Dropdown(['TSNE'], 'TSNE')
        ]),
    ]),
    dbc.Row([
        dbc.Label('Input label value for selected points'),
        dbc.Col([
            dbc.Input(id='input-label',
                      type='text',
                      class_name='form-control',
                      placeholder='Label'),
        ])
    ]),
    dbc.Alert('When you input label, select on the plot few points and they change the label '
              'and color automatically',
              class_name='alert-warning'),

], title='Algorithm')
