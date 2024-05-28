import plotly.graph_objects as go

from dash import dcc


graph = dcc.Graph(id='graph-scatergl', figure=go.Figure())
