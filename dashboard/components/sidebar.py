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
                        html.A(href="google.com", className="sections-button", children=[
                            html.I(className="fa-solid fa-globe"),
                            html.A("Geral", className="text-primary")
                        ]),
                        html.Div(className='line'),
                        html.A(href="google.com", className="sections-button", children=[
                            html.I(className="fa-solid fa-map-location-dot"),
                            html.A("Bairros", className="text-primary")
                        ]),
                        html.Div(className='line'),
                        html.A(href="google.com", className="sections-button", children=[
                            html.I(className="fa-solid fa-clock-rotate-left"),
                            html.A("Histórico", className="text-primary")
                        ]),
                        html.Div(className='line'),
                        html.A(href="google.com", className="sections-button", children=[
                            html.I(className="fa-solid fa-chart-line"),
                            html.A("Previsões", className="text-primary")
                        ]),
                        html.Div(className='line'),
                        html.A(href="google.com", className="sections-button", children=[
                            html.I(className="fa-regular fa-paste"),
                            html.A("Busca e Exportação", className="text-primary")
                        ]),
                        
                    ])
        ])
    ])
    return sidebar