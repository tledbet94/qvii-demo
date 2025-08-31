from dash import Dash, dcc, html
from layout import layout
from callback import *

app = Dash(
    __name__,
    use_pages=False,
    suppress_callback_exceptions=True,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1, viewport-fit=cover"}],
)
server = app.server
app.title = "QVII Demo – Play-only"

app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        html.Div(id="base-background"),
        html.Div(
            [html.Div(layout(), id="page-wrapper", className="card-stage")],
            id="frame-wrapper",
            className="frame-wrapper",
            # your background callback should keep setting: {"--card-url": "url('/assets/...')"}
        ),
    ]
)

if __name__ == "__main__":
    app.run(debug=True)
