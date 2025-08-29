"""quote_button_gen.py

Utility that tokenises the quote and builds the clickable word‑buttons.
Each letter inside a button is wrapped in a <span> so that we can colour
letters individually after each guess.
"""
import re
from typing import List
from dash import html

# word with internal ’ or -  OR a single punctuation mark
TOKEN_RE = re.compile(r"[A-Za-z0-9]+(?:['’\-][A-Za-z0-9]+)*|[^\w\s]")


def tokenize_quote(quote: str) -> List[str]:
    """Split *quote* into tokens and merge trailing punctuation.

    Example → "Hello, world!"  →  ["Hello,", "world!"]
    """
    raw = TOKEN_RE.findall(quote)
    merged: List[str] = []

    for tok in raw:
        # If the token is *only* punctuation, append it to previous word
        if re.fullmatch(r"[^\w\s]+", tok) and merged:
            merged[-1] += tok  # glue to previous
        else:
            merged.append(tok)
    return merged


# ── private helper ──────────────────────────────────────────────────────

def _spanify(token: str, w_idx: int):
    """Return a list of <span> components – one per character."""
    spans = []
    for c_idx, ch in enumerate(token):
        # lower‑case char for the class – useful for CSS selectors
        lower = ch.lower()
        base_cls = "letter"  # always present
        if lower.isalpha():
            base_cls += f" l-{lower}"
        spans.append(
            html.Span(
                ch,
                id={"type": "quote-letter", "index": f"{w_idx}-{c_idx}"},
                className=base_cls,
                **{"data-char": lower},
            )
        )
    return spans


# ── public API ─────────────────────────────────────────────────────────

def generate_word_buttons(
        quote: str,
        weekday: str,
        *,
        get_classes: bool = False,
        raw_buttons: bool = False,          # ← NEW
):

    wk        = weekday.lower()
    tokens    = tokenize_quote(quote)
    base_cls  = f"word-button"

    # ── just return the classes ────────────────────────────────────────
    if get_classes:
        return [base_cls] * len(tokens)

    # ── build the actual buttons ───────────────────────────────────────
    buttons = [
        html.Button(
            _spanify(tok, w_idx),
            id={"type": "quote-word", "index": w_idx},
            n_clicks=0,
            className=base_cls,
            **{"data-index": w_idx},
        )
        for w_idx, tok in enumerate(tokens)
    ]

    return html.Div(buttons, className="w-button-container")