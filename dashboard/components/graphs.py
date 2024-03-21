from dash import html, dcc, callback
from dash.dependencies import Input, Output
from queries import *
from components.filters import *
import ids

df = bairros_contagem()

bar_chart = dcc.Graph(
                    style={"width":"90%", "height":"90%"},
                    id='bar-chart',
                    figure={
                        'data': [
                            {'x': df["bairro"].head(15), 'y': df["contagem"].head(15), 'type': 'bar', 'name': 'Bar Chart'}
                        ],
                        'layout': {
                            'title': 'Anúncios por Bairro',
                            'xaxis': {'title': 'Bairro'},
                            'yaxis': {'title': 'Contagem'},
                            'plot_bgcolor': 'rgba(0, 0, 0, 0)', 
                            'paper_bgcolor': 'rgba(0, 0, 0, 0)', 
                        }
                    }
                )

@callback(Output(ids.BAR_CHART_BAIRROS, 'children'),
        [Input(ids.DROPDOWN_BAIRRO, 'value')],
        prevent_initial_call=True)
    
def update_bar_chart(bairros) -> html.Div:
    if not bairros:
        filtered_data = df
    else:
        filtered_data = df[df['bairro'].isin(bairros)]
        print(bairros)
    if filtered_data.shape[0] == 0:
        return html.Div("No data found")
    
    return dcc.Graph(
            id='bar-chart',
            style={"width":"90%", "height":"90%"},
            figure={
                'data': [
                    {'x': filtered_data["bairro"].head(15), 'y': filtered_data["contagem"].head(15), 'type': 'bar', 'name': 'Bar Chart'}
                ],
                'layout': {
                    'title': 'Anúncios por Bairro',
                    'xaxis': {'title': 'Bairro'},
                    'yaxis': {'title': 'Contagem'},
                    'plot_bgcolor': 'rgba(0, 0, 0, 0)', 
                    'paper_bgcolor': 'rgba(0, 0, 0, 0)', 
                }
            }
        )
        