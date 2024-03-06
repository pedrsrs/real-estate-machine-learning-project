import plotly.express as px
from dash import html, dcc, dash_table
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import psycopg2
from queries import *

df = bairros_contagem()

layout = dbc.Col([
     dbc.Row([
        dbc.Col(md=12, children=[
            dash_table.DataTable(
            id='datatable-row-ids',
            columns=[
                {'name': i, 'id': i, 'deletable': True} for i in df.columns
                # omit the id column
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
            page_current= 0,
            page_size= 10,
        ),
        html.Div(id='datatable-row-ids-container')
            ]),
        ])
        ], style={"backgroun-color": "red"})


