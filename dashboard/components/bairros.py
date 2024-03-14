import plotly.express as px
from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import psycopg2
from queries import *

conn = psycopg2.connect(
    dbname="real-estate-db",
    user="user",
    password="passwd",
    host="localhost",
    port="5432"
)
regiao=None

def initialize_dfs(regiao):
    df = bairros_contagem(regiao)
    df2 = regions_percentage(regiao)
    median_property_price = get_median("valor", regiao)
    median_area = get_median("area", regiao)
    count = get_count(regiao)
    metro_quadrado = valor_metro_quadrado(regiao)

    return df, df2, median_property_price, median_area, count, metro_quadrado

df, df2, median_property_price, median_area, count, metro_quadrado = initialize_dfs(regiao)

all_tipos = ["tipo1", "tipo2", "tipo3"]
layout = dbc.Col([
    dbc.Row([
        dbc.Col(md=3, children=[
            html.Div(className="stat-cards", children=[
                html.A("Valor do Metro Quadrado:", className="stat-description"),
                html.P("R$"+str(metro_quadrado), className="stat-value")
            ])
        ]),
        dbc.Col(md=3, children=[
            html.Div(className="stat-cards", children=[
                html.A("Valor Mediano:", className="stat-description"),
                html.P("R$"+str(median_property_price), className="stat-value")
            ])
        ]),
        dbc.Col(md=3, children=[
            html.Div(className="stat-cards", children=[
                html.A("Área Mediana:", className="stat-description"),
                html.P(str(median_area)+"m²", className="stat-value")
            ])
        ]),
        dbc.Col(md=3, children=[
            html.Div(className="stat-cards", children=[
                html.A("Quantidade de Anúncios:", className="stat-description"),
                html.P(count, className="stat-value")
            ])
        ]),
    ], className="stats"),
        dbc.Row([
            dbc.Col(md=12, children=[
                html.Div(className="orderby-bar", children=[
                        dcc.Dropdown(
                            options=[{"label": tipo, "value": tipo} for tipo in all_tipos],
                            placeholder="Tipo",
                            id="orderby-dropdown"
                        ),
                ])
            ])
        ]),
    dbc.Row([
        dbc.Col(md=8, children=[
            html.Div(className="graph-bar", style={"justify-content":"center"}, children=[
                    dcc.Graph(
                        style={"width":"90%", "height":"90%"},
                        id='bar-chart',
                        figure={
                            'data': [
                                {'x': df["bairro"], 'y': df["contagem"], 'type': 'bar', 'name': 'Bar Chart'}
                            ],
                            'layout': {
                                'xaxis': {'title': 'Categories'},
                                'yaxis': {'title': 'Values'},
                                'plot_bgcolor': 'rgba(0, 0, 0, 0)', 
                                'paper_bgcolor': 'rgba(0, 0, 0, 0)', 
                            }
                        }
                    )
            ])
        ]),
        dbc.Col(md=4, children=[
            html.Div(className="graph-bar", children=[
                html.Div([
                dcc.Graph(
                    id='pie-chart',
                    figure=px.pie(df2, values='percentage', names='regiao', title='Neighborhood Distribution'),
                )
            ])
            ])
        ])
    ]),
    dbc.Row([
        dbc.Col(md=6, children=[
            html.Div(className="graph-bar", children=[

            ])
        ]),
        dbc.Col(md=6, children=[
            html.Div(className="graph-bar", children=[

            ])
        ])
    ]),
])

conn.close()




