import dash
import psycopg2
from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from components import bairros, sidebar, dashboards, filters, exportacao

def main() -> None:

    content = html.Div(id="page-content")
    styles = []
    external_stylesheets = ['assets/styles.css']

    app = dash.Dash(__name__, external_stylesheets=styles + external_stylesheets + [dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME])
    app.title = "Dashboard"
    app.config.suppress_callback_exceptions = True
    app.scripts.config.serve_locally = True
    server = app.server

    content = html.Div(id="page-content")

    app.layout = dbc.Container(children=[
        html.Div(style={"display": "flex"}, children=[
            dcc.Location(id='url'),
            html.Div(style={"flex": "0 0 auto", "width": "13vw"}, children=[
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

    @app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
    def render_page(pathname):
        if pathname == '/' or pathname == '/bairros':
            return bairros.layout
        if pathname == '/busca-e-exportacao':
            return exportacao.layout
        
    app.run_server(port=8051, debug=True)

if __name__ == '__main__':
    main()
