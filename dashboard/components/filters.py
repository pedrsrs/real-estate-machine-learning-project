import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_daq as daq
from queries import *
from components.bairros import *
all_regioes = unique('regiao', regiao)
all_bairros = unique('bairro', regiao)
all_tipos = unique('tipo', regiao)
all_cidades = unique('cidade', regiao)

filter_bar = dbc.Col([
    html.Div(className="filter_bar", children=[
        html.Div(className="dropdown_container", children=[
            dcc.Dropdown(
                options=[{"label": tipo[0], "value": tipo[0]} for tipo in all_tipos],
                placeholder="Tipo",
                multi=True,
                id="file-dropdown"
            ),
        ]),
         html.Div(className="dropdown_container", children=[
            dcc.Dropdown(
                options=[{"label": regiao[0], "value": regiao[0]} for regiao in all_regioes],
                placeholder="Região",
                multi=True,
                id="file-dropdown-regiao"
            ),
        ]),
        html.Div(className="dropdown_container", children=[
            dcc.Dropdown(
                options=[{"label": cidade[0], "value":cidade[0]} for cidade in all_cidades],
                placeholder="Cidade",
                multi=True,
                id="file-dropdown"
            ),
        ]),
        html.Div(className="dropdown_container", children=[
            dcc.Dropdown(
                options=[{"label": bairro[0], "value": bairro[0]} for bairro in all_bairros],
                placeholder="Bairro",
                multi=True,
                id="file-dropdown"
            ),
        ]),
        html.Div(children=[
            dcc.DatePickerRange(
                start_date_placeholder_text="Start Period",
                end_date_placeholder_text="End Period",
                calendar_orientation='vertical',
                clearable=True,
                style={"font-size": "8px"}
            )
        ]),
    ]),
])
