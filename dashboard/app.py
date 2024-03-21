import dash
import dash_bootstrap_components as dbc
from components.layouts import render_layout

def main() -> None:
    external_stylesheets = ['assets/styles.css']

    app = dash.Dash(__name__, external_stylesheets=external_stylesheets + [dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME])
    app.title = "Dashboard"
    app.config.suppress_callback_exceptions = True
    app.scripts.config.serve_locally = True

    app.layout = render_layout(app)
    app.run_server(port=8051, debug=True)

if __name__ == '__main__':
    main()