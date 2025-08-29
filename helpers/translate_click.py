# helpers/translate_click.py
from typing import Any, Dict, List

def _token_to_str(token: Any) -> str:
    if isinstance(token, str):
        return token.lower()
    if isinstance(token, dict):
        return str(token.get("props", {}).get("children", "")).lower()
    if isinstance(token, (list, tuple)):
        return "".join(_token_to_str(t) for t in token)
    return str(token).lower()

def translate_click(
    game_dct: Dict[str, Any],
    word: Any,
    index: int,
    progress_dct: Dict[str, Any],
) -> Dict[str, Any]:
    token = _token_to_str(word)

    # ensure required keys exist (minimal demo state)
    progress_dct.setdefault("attempts", 0)
    progress_dct.setdefault("lives", 3)
    progress_dct.setdefault("guessed_letters", [])
    progress_dct.setdefault("correct_letters", [])
    progress_dct.setdefault("complete", False)
    progress_dct.setdefault("win", False)

    progress_dct["attempts"] += 1

    # ---- OPTIONAL: mark button as clicked only if we're tracking classes ----
    btn_classes = progress_dct.get("button_classes")
    if isinstance(btn_classes, list) and 0 <= index < len(btn_classes):
        if "word-clicked" not in btn_classes[index]:
            btn_classes[index] = (btn_classes[index] + " word-clicked").strip()

    correct = False
    new_guessed: List[str] = []

    # harvest newly guessed letters
    for letter in token:
        if letter not in progress_dct["guessed_letters"]:
            new_guessed.append(letter)
            progress_dct["guessed_letters"].append(letter)

    target_lower = game_dct["target"].lower()
    for letter in new_guessed:
        if letter in target_lower:
            correct = True
            if letter not in progress_dct["correct_letters"]:
                progress_dct["correct_letters"].append(letter)

    # miss branch
    if not correct:
        progress_dct["lives"] = max(progress_dct["lives"] - 1, 0)
        if progress_dct["lives"] == 0:
            progress_dct["complete"] = True
    # hit branch
    else:
        if all(ch in progress_dct["correct_letters"] for ch in target_lower):
            progress_dct["complete"] = True
            progress_dct["win"] = True

    return progress_dct
