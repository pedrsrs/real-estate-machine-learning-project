from dash import html
from queries import *

def calculate_sqr_meters(metros_quadrados):
    metros_quadrado = valor_metro_quadrado()
    return round(metros_quadrados["valor"].sum() / metros_quadrados["valor"].count(), 2)