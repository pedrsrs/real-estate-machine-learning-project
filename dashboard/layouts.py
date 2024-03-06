# layouts.py

from dash import html
import dash_bootstrap_components as dbc
from components import sidebar, filters
from dash import html, dcc

content = html.Div(id="page-content")

layout = dbc.Container(children=[
    html.Div(style={"display": "flex"}, children=[
        dcc.Location(id='url'),
        html.Div(style={"flex": "0 0 auto", "width": "14vw"}, children=[
            sidebar.sidebar
        ]),
        html.Div(style={"flex": "1"}, children=[
            html.Div(style={"padding": "20px"}, children=[
                html.Div(id="page-content-output"),
                filters.filter_bar,
                content
            ])
        ])
    ])
], fluid=True, style={"padding": "0px"}, className="dbc")
