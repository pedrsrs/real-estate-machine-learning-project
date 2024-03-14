import plotly.express as px
from dash import html, dcc, dash_table
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import psycopg2
from components.bairros import *
from queries import *
from dash import Dash, dash_table, dcc, html, Input, Output, callback

df = bairros_contagem(regiao)

layout = dbc.Col([
    
        dbc.Col(md=12, style={"height":"100vh"},children=[
            dash_table.DataTable(
                id='datatable-interactivity',  # Corrected ID here
                columns=[
                    {'name': i, 'id': i, 'deletable': True} for i in df.columns
                    if i != 'id'
                ],
                data=df.to_dict('records'),
                editable=True,
                filter_action="native",
                sort_action="native",
                sort_mode='multi',
                row_selectable='multi',
                row_deletable=True,
                selected_rows=[],
                page_action='native',
                page_current=0,
                page_size=15,
            ),
            html.Div(id='datatable-interactivity-container')
        ]),
    
])

