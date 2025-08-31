from dash import html, dcc

# lives display
q_display = html.Div(
    id="q-display",
    children=[
        html.Div(html.Span("?", id="q1", className="gold-q"),   className="q-mark-container"),
        html.Div(html.Span("?", id="q2", className="silver-q"), className="q-mark-container"),
        html.Div(html.Span("?", id="q3", className="bronze-q"), className="q-mark-container"),
    ],
    style={"display": "flex", "justifyContent": "center", "alignItems": "center", "gap": "clamp(64px, 3vw, 20px)"},
)

reset_button = html.Div(
    html.Button(
        "Reset",
        id="reset-button",
        n_clicks=0,
        style={
            "padding": "10px 16px",
            "borderRadius": "10px",
            "border": "2px outset grey",
            "background": "grey",
            "cursor": "pointer",
            "fontWeight": "600",
        },
        className="word-button",  
    ),
    style={"display": "flex", "justifyContent": "center"},
)

def layout():
    return html.Div(
        [
            # ⬇️ minimal state used by callbacks
            dcc.Store(id="game-data-store"),
            dcc.Store(id="progress-store"),

            # initials plaque
            html.Div(
                className="gold-plate",
                style={"--plate-w": "330px", "--plate-h": "30px"},
                children=html.Div(
                    id="initials",
                    className="base-letter-initials",
                    style={"display": "flex", "justifyContent": "center", "alignItems": "center", "color": "white"},
                ),
            ),
            html.Div(id="word-button-container", style={"display": "flex", "flexWrap": "wrap", "justifyContent": "center"}),
            html.Div(id="answer-container"),
            html.Div(
                [
                    html.Div(id="hint-1", className="base-letter"),
                    html.Div(id="hint-2", className="base-letter"),
                    html.Div(id="hint-3", className="base-letter"),
                ],
                style={"textAlign": "center", "display": "flex", "flexDirection": "column", "alignItems": "center", "gap": "20px"},
            ),
            q_display,

            html.Span(id="source", className="base-letter-small"),
            reset_button
        ],
        style={"display": "flex", "flexDirection": "column", "alignItems": "center", "rowGap": "12px"},
        className="play-stack"
    )
