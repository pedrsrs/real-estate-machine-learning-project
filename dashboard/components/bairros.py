import plotly.express as px
from dash import html, dcc
import dash_bootstrap_components as dbc
from queries import *
from components.metrics import *
from components.graphs import *
import ids 
import plotly.graph_objects as go

all_tipos = ["Anúncios", "Área", "Valor"]

df2 = regions_percentage()
median_property_price = get_median("valor")
count = get_count()
     
bairro_layout = dbc.Col([
        dbc.Row([
            dbc.Col(md=3, children=[
                html.Div(className="stat-cards", children=[
                    html.A("Valor do Metro Quadrado:", className="stat-description"),
                    html.Div(id=ids.METRIC_METRO_QUADRADO, children=[metro_quadrado])
                ])
            ]),
            dbc.Col(md=3, children=[
                html.Div(className="stat-cards", children=[
                    html.A("Valor Mediano:", className="stat-description"),
                    html.Div(id=ids.METRIC_MEDIAN_PRICE, children=[median_price])
                ])
            ]),
            dbc.Col(md=3, children=[
                html.Div(className="stat-cards", children=[
                    html.A("Área Mediana:", className="stat-description"),
                    html.Div(id=ids.METRIC_MEDIAN_AREA, children=[median_area])
                ])
            ]),
            dbc.Col(md=3, children=[
                html.Div(className="stat-cards", children=[
                    html.A("Quantidade de Anúncios:", className="stat-description"),
                    html.Div(id=ids.METRIC_QTD_ANUNCIOS, children=[anuncios_qtd])
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
                html.Div(className="graph-bar", id=ids.BAR_CHART_BAIRROS, children=[
                    bar_chart 
                ])
            ]),
             dbc.Col(
            md=4,  
            children=[
                html.Div(className="graph-bar", id=ids.PIE_CHART, children=[
                    pie_chart
                ])
            ]
        )
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

