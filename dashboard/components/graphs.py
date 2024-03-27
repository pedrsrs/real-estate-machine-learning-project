from dash import html, dcc, callback
from dash.dependencies import Input, Output
import plotly.express as px
from queries import *
from components.filters import *
import ids

df = bairros_contagem()
df2 = regions_percentage()

pie_chart = dcc.Graph(
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

bar_chart = dcc.Graph(
                    style={"width":"90%", "height":"90%"},
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

    if filtered_data.shape[0] == 0:
        return html.Div("No data found")
    
    return dcc.Graph(
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

@callback(Output(ids.PIE_CHART, 'children'),
        [Input(ids.DROPDOWN_BAIRRO, 'value')],
        prevent_initial_call=True)
    
def update_pie_chart(bairros) -> html.Div:
    if not bairros:
        filtered_data = df2
    else:
        filtered_data = df2[df2['bairro'].isin(bairros)]

    if filtered_data.shape[0] == 0:
        return html.Div("No data found")
    
    filtered_data.groupby('regiao')['percentage'].sum()
    
    return dcc.Graph(
                figure=px.pie(
                    filtered_data,
                    values='percentage',
                    names='regiao',
                    title='Distribuição por Região',
                    hole=0.6,  
                    opacity=1  
                ),
                style={'width': '100%', 'height': '100%'}
                )
        