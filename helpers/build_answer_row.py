# utils/build_answer_row.py
from dash import html

def build_answer_row(target: str, correct: str, game_over: bool, lives: bool) -> html.Div:
    tiles = []
    class_name = "hidden-letter"  # default class for letters not guessed yet
    for i, letter in enumerate(target.lower()):
        if game_over and lives > 0:
            if lives == 3:
                class_name = "gold-letter"
            elif lives == 2:
                class_name = "silver-letter"
            elif lives == 1:
                class_name = "bronze-letter"
        else:
            if letter in correct:
                class_name = "base-letter"
            else:
                class_name = "hidden-letter"
        tiles.append(
            html.Div(                                   # tile frame
                html.Span(
                    letter.upper(),                             # ← real letter here
                    className=class_name,
                ),
                className="letter-backdrop",
            )
        )
    return html.Div(tiles, id="answer-row", className="answer-row")
