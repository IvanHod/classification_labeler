import base64
from typing import Any

import dash
import numpy as np
from dash import Input, Output, Patch, State
from dash_extensions.enrich import DashLogger

import pandas as pd

from src import plotting
from src.components.layout import layout
from src.memory import CPUMemory
from src.services import files, decomposition, labels as labels_pkg
from src.styles import get_style

memory = CPUMemory()


app = dash.Dash(__name__, title='Разметка данных', external_stylesheets=[get_style()])
app.layout = layout


def make_alert(output: list[Any],
               fail_msg: str | None = None,
               success_msg: str | None = None
               ) -> tuple[Any, bool, str, bool, str]:

    if fail_msg:
        return *output, True, fail_msg, False, ''

    if success_msg:
        return *output, False, '', True, success_msg

    return *output, False, '', False, ''


@app.callback(
    Output('target_column_name', 'options', allow_duplicate=True),
    Output('source-file_name', 'options', allow_duplicate=True),
    Output('alert-fail', 'is_open', allow_duplicate=True),
    Output('alert-fail', 'children', allow_duplicate=True),
    Output('alert-success', 'is_open', allow_duplicate=True),
    Output('alert-success', 'children', allow_duplicate=True),
    Input('source-file', 'contents'),
    State('source-file', 'filename'),
    Input('source-file_name', 'value'),
    prevent_initial_call=True,
)
def on_file_uploaded_or_selected(file: str, file_name: str, source_file_name: str):
    """
    Output -> set DataFrame columns

    :param file:
    :param file_name:
    :param source_file_name:
    :return:
    """
    file_list = files.load_csv_names(include_absent=True)

    if not file and not source_file_name:
        return make_alert([[], file_list])

    ext = file_name.rsplit('.', 1)[-1] if file_name else None
    if ext is not None and ext not in {'csv', }:
        return make_alert([[], file_list], fail_msg=f'It is accessed to upload .csv files, your file is "{ext}"')

    if file:
        __, file = file.split(',')
        file = base64.b64decode(file)

    df: pd.DataFrame = files.load_df(file, source_file_name)
    memory.set_initial_df(df)
    if file is not None:
        # if user uploaded file, then save the file and update list of uploaded files
        files.save_df(df, file_name, as_output=False)  # save file as input
        file_list = files.load_csv_names(include_absent=True)

    columns = files.get_df_columns(df)

    return make_alert([columns, file_list],
                      success_msg=f'File "{file_name}" was uploaded. Now select the target column')


@app.callback(
    Output('graph-scatergl', 'figure', allow_duplicate=True),
    Output('alert-fail', 'is_open', allow_duplicate=True),
    Output('alert-fail', 'children', allow_duplicate=True),
    Output('alert-success', 'is_open', allow_duplicate=True),
    Output('alert-success', 'children', allow_duplicate=True),
    Input('target_column_name', 'value'),
    prevent_initial_call=True,
)
def on_target_selected(target_column: str):
    """
    Output -> draw graph (plot)

    :param target_column:
    :return:
    """
    fig_patch = Patch()
    if not target_column:
        return make_alert([fig_patch])

    df: pd.DataFrame = memory.get_initial_df()

    df_decomposed = decomposition.decompose(df, target_column=target_column)
    memory.set_target_column(target_column)
    memory.set_decomposition_df(df_decomposed)

    fig = plotting.plot(df_decomposed, target_column)
    fig_patch['data'] = fig.data

    return make_alert([fig], success_msg='Your decomposition plot was draw. Now open "Algorithm" tab.')


@app.callback(
    Output('graph-scatergl', 'figure', allow_duplicate=True),
    Output('alert-fail', 'is_open', allow_duplicate=True),
    Output('alert-fail', 'children', allow_duplicate=True),
    Output('alert-success', 'is_open', allow_duplicate=True),
    Output('alert-success', 'children', allow_duplicate=True),
    State('input-label', 'value'),
    Input('graph-scatergl', 'selectedData'),
    prevent_initial_call=True
)
def on_highlight_point(label: str, selected_data: dict[str, list]):
    """
    Output -> redraw graph (plot)

    :param label:
    :param selected_data:
    :return:
    """
    fig_patch = Patch()

    if selected_data is None or label is None:
        return make_alert([fig_patch])

    # get indices in selected area and update these labels with new label
    indices = np.array(list(map(lambda v: v['customdata'][0], selected_data['points'])))
    n_points = indices.shape[0]
    labels_pkg.update_labels(memory, label, indices)

    target_column: str = memory.get_target_column()
    df_decomposed: pd.DataFrame = memory.get_decomposition_df()

    fig = plotting.plot(df_decomposed, target_column)
    fig_patch['data'] = fig.data

    return make_alert([fig_patch], success_msg=f'The {n_points} points was relabeled to {label}')


@app.callback(
    Output('hidden-save-div', 'children', allow_duplicate=True),
    Output('alert-fail', 'is_open', allow_duplicate=True),
    Output('alert-fail', 'children', allow_duplicate=True),
    Output('alert-success', 'is_open', allow_duplicate=True),
    Output('alert-success', 'children', allow_duplicate=True),
    State('input-output-file_name', 'value'),
    Input('btn-save_results', 'n_clicks'),
)
def save_data(filename: str, __) -> tuple:
    """
    Output -> is alert

    :param filename:
    :param __:
    :return:
    """
    if filename is None:
        return make_alert([''], fail_msg='File name is empty')

    df: pd.DataFrame = memory.get_output_df()
    files.save_df(df, file_name=filename, as_output=True)

    return make_alert([f'Filename: {filename}'], success_msg=f'The file {filename} was save in output folder')


if __name__ == "__main__":
    app.run_server(debug=True)
