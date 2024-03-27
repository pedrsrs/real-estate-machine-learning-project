from dash import html, dcc, callback
from dash.dependencies import Input, Output
from queries import *
import ids
import pandas as pd

metros_quadrados = valor_metro_quadrado()
result = round(metros_quadrados["valor"].sum() / metros_quadrados["valor"].count(), 2)

metro_quadrado = html.P("R$"+str(result), className="stat-value")

@callback(Output(ids.METRIC_METRO_QUADRADO, 'children'),
        [Input(ids.DROPDOWN_BAIRRO, 'value')],
        prevent_initial_call=True)
    
def update_bar_chart(bairros):
    if not bairros:
        filtered_data = metros_quadrados
    else:
        filtered_data = metros_quadrados[metros_quadrados['bairro'].isin(bairros)]

    if filtered_data.shape[0] == 0:
        return html.Div("No data found")
    
    result = round(filtered_data["valor"].sum() / filtered_data["valor"].count(), 2)

    
    return html.P("R$"+str(result), className="stat-value")


dados = all_data()
median_price = html.P("R$"+str(dados["valor"].median()), className="stat-value")

@callback(Output(ids.METRIC_MEDIAN_PRICE, 'children'),
        [Input(ids.DROPDOWN_BAIRRO, 'value')],
        prevent_initial_call=True)
    
def update_medium_price(bairros):
    if not bairros:
        filtered_data = dados
    else:
        filtered_data = dados[dados['bairro'].isin(bairros)]

    if filtered_data.shape[0] == 0:
        return html.Div("No data found")
    
    result = filtered_data["valor"].median()
    
    return html.P("R$"+str(result), className="stat-value")

dados = all_data()
median_area = html.P(str(dados["area"].median())+"m2", className="stat-value")

@callback(Output(ids.METRIC_MEDIAN_AREA, 'children'),
        [Input(ids.DROPDOWN_BAIRRO, 'value')],
        prevent_initial_call=True)
    
def update_medium_area(bairros):
    if not bairros:
        filtered_data = dados
    else:
        filtered_data = dados[dados['bairro'].isin(bairros)]

    if filtered_data.shape[0] == 0:
        return html.Div("No data found")
    
    result = filtered_data["area"].median()
    
    return html.P(str(result)+"m2", className="stat-value")


anuncios = get_count()
anuncios_qtd = html.P(str(len(anuncios)), className="stat-value")

@callback(Output(ids.METRIC_QTD_ANUNCIOS, 'children'),
        [Input(ids.DROPDOWN_BAIRRO, 'value')],
        prevent_initial_call=True)
    
def update_qtd_anuncios(bairros):
    if not bairros:
        filtered_data = anuncios
    else:
        filtered_data = anuncios[anuncios['bairro'].isin(bairros)]

    if filtered_data.shape[0] == 0:
        return html.Div("No data found")
    
    result = len(filtered_data)
    
    return html.P(str(result), className="stat-value")