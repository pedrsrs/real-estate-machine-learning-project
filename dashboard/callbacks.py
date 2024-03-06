# callbacks.py

from dash.dependencies import Input, Output
from components import bairros, exportacao
import pandas as pd
from dash import html, dcc
import psycopg2
from queries import *

def register_callbacks(app):
    @app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
    def render_page(pathname):
        if pathname == '' or pathname == '/bairros':
            return bairros.layout
        if pathname == '/busca-e-exportacao':
            return exportacao.layout

    @app.callback(
        Output('datatable-row-ids-container', 'children'),
        [Input('datatable-row-ids', 'derived_virtual_row_ids'),
         Input('datatable-row-ids', 'selected_row_ids'),
         Input('datatable-row-ids', 'active_cell')]
    )
    def update_graphs(rows, derived_virtual_selected_rows, active_cell):
        df = count_bairros()
    
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

            for column in ["contagem"] if column in dff
        ]