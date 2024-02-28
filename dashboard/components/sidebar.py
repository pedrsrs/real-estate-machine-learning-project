import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_daq as daq

def get_sidebar_layout():
    sidebar = dbc.Col([
        html.Div(className="sidebar", children=[
            html.Div(className='stateButton', id="estado",
                    children=[html.H1("Venda", className="botao"),
                        ]),
                    
            html.Div(className="sidebar-pages-container", children=[
                        dbc.NavLink(href="/geral", active="exact", className="sections-button", children=[
                            html.I(className="fa-solid fa-globe"),
                            html.A("Geral")
                        ]),
                        html.Div(className='line'),
                        dbc.NavLink(href="/bairros", active="exact", className="sections-button", children=[
                            html.I(className="fa-solid fa-map-location-dot"),
                            html.A("Bairros")
                        ]),
                        html.Div(className='line'),
                        dbc.NavLink(href="/historico", active="exact", className="sections-button", children=[
                            html.I(className="fa-solid fa-clock-rotate-left"),
                            html.A("Histórico")
                        ]),
                        html.Div(className='line'),
                        dbc.NavLink(href="/previsoes", active="exact", className="sections-button", children=[
                            html.I(className="fa-solid fa-chart-line"),
                            html.A("Previsões")
                        ]),
                        html.Div(className='line'),
                        dbc.NavLink(href="/busca-e-exportacao", active="exact", className="sections-button", children=[
                            html.I(className="fa-regular fa-paste"),
                            html.A("Busca e Exportação")
                        ]),
                        
                    ])
        ])
    ])
    return sidebar