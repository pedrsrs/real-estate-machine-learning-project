# callbacks.py
from dash.dependencies import Input, Output
from components import bairros, exportacao, filters

def register_callbacks(app):
    @app.callback(Output('page-content', 'children'), 
                  [Input('url', 'pathname')])
    def render_page(pathname):
        if pathname == '' or pathname == '/bairros':
            return bairros.bairros_layout(app)
        if pathname == '/busca-e-exportacao':
            return exportacao.exportacao_layout(app)

    
