import dash
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import dash_daq as daq
from queries import *

df = bairro_metro_quadrado()
def barchart(app: Dash) -> html.Div:
    @app.callback(
        Output('graph-bar-bairros', 'children'),
        Input('bairro-dropdown', 'value')
    )
    def update_bar_chart(bairros: list[str]) -> html.Div:
        filtered_data = df.query("bairro in @bairros")
        return html.Div(className="graph-bar", id='graph-bar-bairros', style={"justify-content":"center"}, children=[
            dcc.Graph(
                style={"width":"90%", "height":"90%"},
                id='bar-chart',
                figure={
                    'data': [
                        {'x': filtered_data["bairro"].head(15), 'y': filtered_data["contagem"].head(15), 'type': 'bar', 'name': 'Bar Chart'}
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
    return html.Div(id='bar-chart')