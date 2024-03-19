# layouts.py
from dash import html, dcc
import dash_bootstrap_components as dbc
from components import sidebar, filters

def render_layout(app):
    content = html.Div(id="page-content")

    return dbc.Container(children=[
        html.Div(style={"display": "flex"}, children=[
            dcc.Location(id='url'),
            html.Div(style={"flex": "0 0 auto", "width": "14vw"}, children=[
                sidebar.sidebar_layout(app)
            ]),
            html.Div(style={"flex": "1"}, children=[
                html.Div(style={"padding": "20px"}, children=[
                    html.Div(id="page-content-output"),
                    filters.filters_layout(app),
                    content
                ])
            ])
        ])
    ], fluid=True, style={"padding": "0px"}, className="dbc")
