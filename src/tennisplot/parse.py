import json
import re

import pandas as pd

MATCH_COLUMNS = {
    0: "date",
    1: "tournament",
    4: "result",
    8: "round",
    11: "opponent",
    16: "opponent_info",
}

def _extract_birth_date(player_js):
    """Read the player's date of birth from the player-info JS file."""
    match = re.search(r"var\s+dob\s*=\s*(\d{8})", player_js)
    if match is None:
        raise ValueError("Could not find the player's birth date.")
    return pd.to_datetime(match.group(1), format="%Y%m%d")

def _extract_match_rows(js_text, variable="morematchmx"):
    """Pull a match array (morematchmx by default) out of the JS text."""
    marker = re.search(rf"var\s+{variable}\s*=\s*", js_text)
    if marker is None:
        raise ValueError("No match data found: is this a valid player?")
    rows, _ = json.JSONDecoder().raw_decode(js_text, marker.end())
    return rows

def _extract_recent_rows(player_js):
    """Matches newer than the career file; empty list if there are none."""
    try:
        return _extract_match_rows(player_js, variable="matchmx")
    except ValueError:
        return []


def _rows_to_frame(rows):
    """Keep only the columns we need, selected by position."""
    data = [[row[index] for index in MATCH_COLUMNS] for row in rows]
    frame = pd.DataFrame(data, columns=list(MATCH_COLUMNS.values()))
    frame["date"] = pd.to_datetime(frame["date"], format="%Y%m%d")
    return frame

def _years_between(start, end):
    """Elapsed years from start to end (works for scalars or Series)."""
    return (end - start).dt.days / 365.25


def _compute_opponent_age(frame):
    """Opponent age: from a birth date (women's files) or as given (men's)."""
    info = frame["opponent_info"]
    is_birth_date = info.str.fullmatch(r"\d{8}")
    birth = pd.to_datetime(info.where(is_birth_date), format="%Y%m%d", errors="coerce")
    age_from_birth = _years_between(birth, frame["date"])
    age_given = pd.to_numeric(info.where(~is_birth_date), errors="coerce")
    return age_from_birth.fillna(age_given)


def _add_ages(frame, birth_date):
    """Add player_age, opponent_age and age_difference columns."""
    frame = frame.copy()
    frame["player_age"] = _years_between(birth_date, frame["date"])
    frame["opponent_age"] = _compute_opponent_age(frame)
    frame["age_difference"] = frame["player_age"] - frame["opponent_age"]
    return frame