from dash import html, dcc
import dash_bootstrap_components as dbc
from queries import *
import ids

all_regioes = unique('regiao')
all_bairros = unique('bairro')
all_tipos = unique('tipo')
all_cidades = unique('cidade')
    
filter_layout = dbc.Col([
        html.Div(className="filter_bar", children=[
            html.Div(className="dropdown_container", children=[
                dcc.Dropdown(
                    options=[{"label": tipo, "value": tipo} for tipo in all_tipos],
                    placeholder="Tipo",
                    multi=True,
                    id=ids.DROPDOWN_TIPO,
                    className='custom-dropdown'
                ),
            ]),
            html.Div(className="dropdown_container", children=[
                dcc.Dropdown(
                    options=[{"label": regiao, "value": regiao} for regiao in all_regioes],
                    placeholder="Região",
                    multi=True,
                    id=ids.DROPDOWN_REGIAO,
                    className='custom-dropdown'
                ),
            ]),
            html.Div(className="dropdown_container", children=[
                dcc.Dropdown(
                    options=[{"label": cidade, "value":cidade} for cidade in all_cidades],
                    placeholder="Cidade",
                    multi=True,
                    id=ids.DROPDOWN_CIDADE,
                    className='custom-dropdown'
                ),
            ]),
            html.Div(className="dropdown_container", children=[
                dcc.Dropdown(
                    options=[{"label": bairro, "value": bairro} for bairro in all_bairros],
                    placeholder="Bairro",
                    multi=True,
                    id=ids.DROPDOWN_BAIRRO,
                    className='custom-dropdown'
                ),
            ]),
            html.Div(children=[
                dcc.DatePickerRange(
                    start_date_placeholder_text="Data Inicial",
                    end_date_placeholder_text="Data Final",
                    calendar_orientation='vertical',
                    clearable=True,
                    style={"font-size": "8px"}
                )
            ]),
        ]),
    ])
