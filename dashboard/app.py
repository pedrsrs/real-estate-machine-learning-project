# app.py
import dash
import dash_bootstrap_components as dbc
from layouts import render_layout
from callbacks import register_callbacks

external_stylesheets = ['assets/styles.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets + [dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME])
app.title = "Dashboard"
app.config.suppress_callback_exceptions = True
app.scripts.config.serve_locally = True
server = app.server

app.layout = render_layout(app)

register_callbacks(app)

if __name__ == '__main__':
    app.run_server(port=8051, debug=True)
