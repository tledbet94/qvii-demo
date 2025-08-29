# callback.py — Play-only, single-quote demo
from dash import callback, Input, Output, State, html, no_update
from dash import ctx
from dash.dependencies import ALL 
from dash.exceptions import PreventUpdate
import json, copy

from helpers.quote_button_gen import generate_word_buttons
from helpers.translate_click import translate_click
from helpers.build_answer_row import build_answer_row

DEMO_JSON_PATH = "demo_quotes.json"
DEMO_KEY = "1"

def _load_demo_game():
    with open(DEMO_JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    row = data[DEMO_KEY]
    return {
        "quote": row["quote"],
        "target": row["target"],
        "initials": row["initials"],
        "name": row["name"],
        "occupation": row["occupation"],
        "place": row["place"],
        "time": row["time"],
        "source": row["source"],
    }

def _style_initials(initials_str: str):
    out = []
    for ch in initials_str:
        if ch == "?":
            out.append(html.Span("?", className="initials-question"))
        else:
            out.append(ch)
    return out

# 0) Seed the single demo puzzle when #page-wrapper mounts (app start)
@callback(
    Output("game-data-store", "data"),
    Input("page-wrapper", "id"),
    prevent_initial_call=False,
)
def seed_game(_):
    try:
        return _load_demo_game()
    except Exception:
        raise PreventUpdate

# 1) Build word buttons from the single quote
@callback(
    Output("word-button-container", "children"),
    Input("game-data-store", "data"),
    prevent_initial_call=False,
)
def build_buttons(game_data):
    if not game_data:
        raise PreventUpdate
    # keep signature consistent with your helper
    return generate_word_buttons(game_data["quote"], "tuesday", raw_buttons=True)

# 2) Hints are always visible
@callback(
    Output("hint-1", "children"),
    Output("hint-2", "children"),
    Output("hint-3", "children"),
    Input("game-data-store", "data"),
    prevent_initial_call=False
)
def set_hints(game_dct):
    if not game_dct:
        raise PreventUpdate
    return game_dct["occupation"], game_dct["place"], game_dct["time"]

@callback(
    Output("progress-store", "data"),
    Input("word-button-container", "children"),                # on mount
    Input({"type": "quote-word", "index": ALL}, "n_clicks"),   # on clicks
    Input("reset-button", "n_clicks"),                         # ⬅️ add this
    State("game-data-store", "data"),
    State({"type": "quote-word", "index": ALL}, "children"),
    State("progress-store", "data"),
    prevent_initial_call=True
)
def update_progress(_mounted_children, n_clicks_list, n_reset, game_dct, children_list, progress_dct):
    if not game_dct:
        raise PreventUpdate

    base = {
        "complete": False,
        "win": False,
        "lives": 3,
        "attempts": 0,
        "guessed_letters": [],
        "correct_letters": [],
        "clicked_indices": [],
    }

    # first mount → publish baseline
    if ctx.triggered_id == "word-button-container":
        return base

    # reset button → baseline
    if ctx.triggered_id == "reset-button":
        return base

    if not n_clicks_list or not any(n_clicks_list):
        return progress_dct or base

    changed = ctx.triggered_id
    if not isinstance(changed, dict) or changed.get("type") != "quote-word":
        return progress_dct or base

    idx = changed.get("index")
    progress = copy.deepcopy(progress_dct or base)
    progress.setdefault("attempts", 0)

    clicked_word = children_list[idx]
    progress = translate_click(game_dct, clicked_word, idx, progress)
    progress["clicked_indices"].append(idx)
    progress["lives"] = min(3, max(0, progress.get("lives", 3)))
    return progress
# 4) Render initials, source, answer row, and lives (???)
@callback(
    Output("initials", "children"),
    Output("source", "children"),
    Output("answer-container", "children"),
    Output("q1", "children"),
    Output("q2", "children"),
    Output("q3", "children"),
    Input("progress-store", "data"),
    State("game-data-store", "data"),
    prevent_initial_call=True
)
def render(progress, game_dct):
    if not game_dct or not progress:
        raise PreventUpdate

    if progress.get("complete"):
        initials_children = [game_dct.get("name", "")]
        source_children = game_dct.get("source", "")
    else:
        initials_children = _style_initials(game_dct.get("initials", ""))
        source_children = ""

    answer_row = build_answer_row(
        game_dct["target"],
        progress.get("correct_letters", []),
        progress.get("complete", False),
        progress.get("lives", 3),
    )

    lives = progress.get("lives", 3)
    q1 = "" if lives <= 2 else "?"
    q2 = "" if lives <= 1 else "?"
    q3 = "" if lives <= 0 else "?"

    return initials_children, source_children, answer_row, q1, q2, q3

from dash import no_update

@callback(
    Output({"type": "quote-word", "index": ALL}, "className"),
    Input({"type": "quote-word", "index": ALL}, "n_clicks"),
    State({"type": "quote-word", "index": ALL}, "className"),
    prevent_initial_call=True,
)
def style_clicked(n_clicks, current_classes):
    if not isinstance(n_clicks, list) or not isinstance(current_classes, list):
        raise PreventUpdate

    out = []
    for clicks, base in zip(n_clicks, current_classes):
        base = base or "word-button"  # fall back if generator used no class
        if (clicks or 0) > 0:
            # add the flag (idempotent)
            out.append(base if "word-clicked" in base else f"{base} word-clicked")
        else:
            # ensure it's clean before first click
            out.append(base.replace("word-clicked", "").strip())
    return out

@callback(
    Output({"type": "quote-word", "index": ALL}, "n_clicks"),
    Input("reset-button", "n_clicks"),
    State({"type": "quote-word", "index": ALL}, "n_clicks"),
    prevent_initial_call=True,
)
def reset_clicks(n_reset, current_clicks):
    if not n_reset:
        raise PreventUpdate
    length = len(current_clicks or [])
    return [0] * length
