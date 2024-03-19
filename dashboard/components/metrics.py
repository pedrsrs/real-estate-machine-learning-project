import plotly.express as px
from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
from queries import *

#METROS_QUADRADOS = valor_metro_quadrado()

def render_sqr_meters(app: Dash, metros_quadrados) -> html.Div:
    return round(metros_quadrados["valor"].sum() / metros_quadrados["valor"].count(), 2)