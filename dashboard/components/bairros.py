# Import necessary libraries
import plotly.express as px
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from queries import *
from components.metrics import *
from components.graphs import *

all_tipos = ["Anúncios", "Área", "Valor"]

df = bairros_contagem()
df2 = regions_percentage()
median_property_price = get_median("valor")
median_area = get_median("area")
count = get_count()
metro_quadrado = valor_metro_quadrado()

def bairros_layout(app):
            
    metros_quadrados = render_sqr_meters(app, metro_quadrado)
    return dbc.Col([
        dbc.Row([
            dbc.Col(md=3, children=[
                html.Div(className="stat-cards", id='metric_metro_quadrado', children=[
                    html.A("Valor do Metro Quadrado:", className="stat-description"),
                    html.P("R$"+str(metros_quadrados), className="stat-value")
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
                        placeholder="Filtragem",
                        id="orderby-dropdown"
                    ),
                ])
            ])
        ]),
        dbc.Row([
            dbc.Col(md=8, children=[
                html.Div(className="graph-bar", children=[
                    barchart(app)
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
