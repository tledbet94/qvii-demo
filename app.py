from dash import Dash, dcc, html
from layout import layout  # your play-page layout function
from callback import *

app = Dash(__name__, use_pages=False, suppress_callback_exceptions=True)
server = app.server
app.title = "QVII Demo – Play-only"

# Bottom tiled layer
backdrop_tile = html.Div(id="base-background")

# Foreground background + app content confined inside it
stage = html.Div(
    [
        html.Div(
            layout(),                 # ← your layout goes here
            id="page-wrapper",
            className="card-stage",
        )
    ],
    id="frame-wrapper",
    className="frame-wrapper",
)

app.layout = html.Div([dcc.Location(id="url", refresh=False), backdrop_tile, stage])

if __name__ == "__main__":
    app.run(debug=True)
