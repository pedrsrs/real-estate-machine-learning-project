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
median_area = get_median("area")
count = get_count()
metro_quadrado = valor_metro_quadrado()
    
metros_quadrados = calculate_sqr_meters(metro_quadrado)
bairro_layout = dbc.Col([
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
                html.Div(className="graph-bar", id=ids.BAR_CHART_BAIRROS, children=[
                    bar_chart 
                ])
            ]),
             dbc.Col(
            md=4,  # Set the column width for medium screens and larger
            children=[
                html.Div(className="graph-bar", children=[
                    dcc.Graph(
                        id='pie-chart',
                        figure=px.pie(
                            df2,
                            values='percentage',
                            names='regiao',
                            title='Distribuição por Região',
                            hole=0.6,  
                            opacity=1  
                        ),
                        style={'width': '100%', 'height': '100%'}
                    )
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

