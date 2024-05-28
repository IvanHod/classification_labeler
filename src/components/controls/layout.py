import dash_bootstrap_components as dbc

from src.components.controls import data_list, algo_list, output_list


controls = dbc.Card(
    dbc.Accordion([
        data_list,
        algo_list,
        output_list
    ])
)
