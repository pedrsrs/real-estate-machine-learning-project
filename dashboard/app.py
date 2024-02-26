import dash 
from dash import html, dcc
import dash_bootstrap_components as dbc

styles = []
external_stylesheets = ['assets/styles.css']

app = dash.Dash(__name__, external_stylesheets=styles + [external_stylesheets])

app.config.suppress_callback_exceptions = True
app.scripts.config.serve_locally = True
server = app.server