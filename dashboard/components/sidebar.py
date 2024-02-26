import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

def get_sidebar_layout():
    sidebar = dbc.Col([
        html.Div(className="sidebar", children=[
            dbc.Button(id="estado",
                    children=[html.H1("Venda", className="botao")
                        ], style={'background-color': '#07A182'}),
            html.H1("Geral", className="text-primary"),
            html.H1("Bairros", className="text-primary"),
            html.H1("Previsões", className="text-primary"),
            html.H1("Busca e Exportação", className="text-primary"),
        ])
    ])
    return sidebar