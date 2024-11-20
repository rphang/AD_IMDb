from flask_caching import Cache
from dash import Dash, html, dcc, page_registry, page_container
import dash_bootstrap_components as dbc

import plotly.express as px

from data.loader import loadBasics

basicsDf = loadBasics()

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP], use_pages=True)
cache = Cache(app.server, config={'CACHE_TYPE': 'SimpleCache'})

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2("TP AD", className="display-4"),
        html.Hr(),
        html.P(
            """
            Analyse sur la base de données IMDB des films, séries et acteurs.
            """, className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink(page["name"], href=page["relative_path"], active="exact") for page in page_registry.values()
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)


content = page_container
content.style = CONTENT_STYLE

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


def startDashApp():
    app.run(debug=True)