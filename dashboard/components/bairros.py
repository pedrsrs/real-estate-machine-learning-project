import plotly.express as px
from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import psycopg2
all_tipos = ["tipo1", "tipo2", "tipo3"]
layout = dbc.Col([
    dbc.Row([
        dbc.Col(md=3, children=[
            html.Div(className="stat-cards", children=[
                html.A("Valor do Metro Quadrado:", className="stat-description"),
                html.P("R$1.234,00", className="stat-value")
            ])
        ]),
        dbc.Col(md=3, children=[
            html.Div(className="stat-cards", children=[
                html.A("Valor Mediano:", className="stat-description"),
                html.P("R$350.000,00", className="stat-value")
            ])
        ]),
        dbc.Col(md=3, children=[
            html.Div(className="stat-cards", children=[
                html.A("Área Mediana:", className="stat-description"),
                html.P("110m²", className="stat-value")
            ])
        ]),
        dbc.Col(md=3, children=[
            html.Div(className="stat-cards", children=[
                html.A("Quantidade de Anúncios:", className="stat-description"),
                html.P("4.321", className="stat-value")
            ])
        ]),
    ], className="stats"),
    dbc.Row([
        dbc.Col(md=12, children=[
            html.Div(className="orderby-bar", children=[
                html.Div(children=[
                    dcc.Dropdown(
                        options=[{"label": tipo, "value": tipo} for tipo in all_tipos],
                        placeholder="Tipo",
                        id="orderby-dropdown"
                    ),
                ]),
            ])
        ])
        ])
    ])