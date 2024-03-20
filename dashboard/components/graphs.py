import dash
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import dash_daq as daq
from queries import bairros_contagem

def barchart(app: Dash) -> html.Div:
    df = bairros_contagem()
    @app.callback(
        Output('graph-bar-bairros', 'children'),
        Input('bairro-dropdown', 'value')
    )
    def update_bar_chart(bairros) -> html.Div:
        if bairros is None:
            filtered_data = df
        else:
            filtered_data = df[df['bairro'].isin(bairros)]
        if filtered_data.shape[0] == 0:
            return html.Div("No data found")
        return html.Div(className="graph-bar", id='graph-bar-bairros', style={"justify-content":"center"}, children=[
            dcc.Graph(
                style={"width":"90%", "height":"90%"},
                id='bar-chart',
                figure={
                    'data': [
                        {'x': filtered_data["bairro"], 'y': filtered_data["contagem"], 'type': 'bar', 'name': 'Bar Chart'}
                    ],
                    'layout': {
                        'xaxis': {'title': 'Bairro'},
                        'yaxis': {'title': 'Contagem'},
                        'plot_bgcolor': 'rgba(0, 0, 0, 0)', 
                        'paper_bgcolor': 'rgba(0, 0, 0, 0)', 
                    }
                }
            )
        ])
    return html.Div(className="graph-bar", id='graph-bar-bairros', style={"justify-content":"center"}, children=[
            dcc.Graph(
                style={"width":"90%", "height":"90%"},
                id='bar-chart',
                figure={
                    'data': [
                        {'x': df["bairro"], 'y': df["contagem"], 'type': 'bar', 'name': 'Bar Chart'}
                    ],
                    'layout': {
                        'xaxis': {'title': 'Bairro'},
                        'yaxis': {'title': 'Contagem'},
                        'plot_bgcolor': 'rgba(0, 0, 0, 0)', 
                        'paper_bgcolor': 'rgba(0, 0, 0, 0)', 
                    }
                }
            )
        ])