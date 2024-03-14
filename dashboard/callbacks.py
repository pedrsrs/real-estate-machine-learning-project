# callbacks.py

from dash.dependencies import Input, Output
from components import bairros, exportacao
import pandas as pd
from dash import html, dcc
import psycopg2
from queries import *
from components.bairros import *
from dash import Dash, dash_table, dcc, html, Input, Output, callback

def register_callbacks(app):
    @app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
    def render_page(pathname):
        if pathname == '' or pathname == '/bairros':
            return bairros.layout
        if pathname == '/busca-e-exportacao':
            return exportacao.layout
    @app.callback(
    Output('datatable-interactivity', 'style_data_conditional'),
    Input('datatable-interactivity', 'selected_columns')
    )
    def update_styles(selected_columns):
        if selected_columns is None:
            return []
        else:
            return [{
                'if': {'column_id': i},
                'background_color': '#D2F3FF'
            } for i in selected_columns]
    @app.callback(
        Output('datatable-row-ids-container', 'children'),
        [Input('datatable-row-ids', 'derived_virtual_row_ids'),
         Input('datatable-row-ids', 'selected_row_ids'),
         Input('datatable-row-ids', 'active_cell')]
    )
    def update_graphs(rows, derived_virtual_selected_rows, active_cell):
        df = bairros_contagem()
    
        if derived_virtual_selected_rows is None:
            derived_virtual_selected_rows = []

        dff = df if rows is None else pd.DataFrame(rows)

        colors = ['#7FDBFF' if i in derived_virtual_selected_rows else '#0074D9'
                for i in range(len(dff))]

        return [
            dcc.Graph(
                id=column,
                figure={
                    "data": [
                        {
                            "x": dff["bairro"],
                            "y": dff[column],
                            "type": "bar",
                            "marker": {"color": colors},
                        }
                    ],
                    "layout": {
                        "xaxis": {"automargin": True},
                        "yaxis": {
                            "automargin": True,
                            "title": {"text": column}
                        },
                        "height": 250,
                        "margin": {"t": 10, "l": 10, "r": 10},
                    },
                },
            )

            for column in ['contagem', 'median_value', 'median_area'] if column in dff
        ]
    @app.callback(
        Output('dd-output-container', 'children'),
        Input('file-dropdown-regiao', 'regiao')
    )
    def update_output(regiao):
        initialize_dfs(regiao)