from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from components import sidebar
from dash.dependencies import Input, Output
from components.bairros import *
from components.filters import *
from queries import *

def render_layout(app: Dash) -> html.Div:

    @app.callback(Output('page-content', 'children'), 
                  [Input('url', 'pathname')])
    def render_page(pathname):
        if pathname == '' or pathname == '/bairros':
            return bairro_layout
        
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
                    filter_layout,
                    content
                ])
            ])
        ])
    ], fluid=True, style={"padding": "0px"}, className="dbc")


