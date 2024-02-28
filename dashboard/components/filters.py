import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_daq as daq

def get_filter_bar_layout():
    all_bairros = ["Castelo", "Arvoredo", "Centro"]
    all_tipos = ["Apartamento", "Casa"]
    all_cidades = ["Belo Horizonte", "Contagem", "Betim"]
    filter_bar = dbc.Col([
        html.Div(className="filter_bar", children=[
            html.Div(className="dropdown_container", children=[
                dcc.Dropdown(
                    options=[{"label": tipo, "value": tipo} for tipo in all_tipos],
                    placeholder="Tipo",
                    multi=True,
                    id="file-dropdown"
                ),
            ]),
            html.Div(className="dropdown_container", children=[
                dcc.Dropdown(
                    options=[{"label": cidade, "value":cidade} for cidade in all_cidades],
                    placeholder="Cidade",
                    multi=True,
                    id="file-dropdown"
                ),
            ]),
            html.Div(className="dropdown_container", children=[
                dcc.Dropdown(
                    options=[{"label": bairro, "value": bairro} for bairro in all_bairros],
                    placeholder="Bairro",
                    multi=True,
                    id="file-dropdown"
                ),
            ]),
        ]),
    ])
    return filter_bar