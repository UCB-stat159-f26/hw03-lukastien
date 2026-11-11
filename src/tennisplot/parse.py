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

def _extract_match_rows(career_js):
    """Pull the morematchmx array out of the career JS text."""
    marker = re.search(r"var\s+morematchmx\s*=\s*", career_js)
    if marker is None:
        raise ValueError("No match data found: is this a valid player?")
    rows, _ = json.JSONDecoder().raw_decode(career_js, marker.end())
    return rows


def _rows_to_frame(rows):
    """Keep only the columns we need, selected by position."""
    data = [[row[index] for index in MATCH_COLUMNS] for row in rows]
    frame = pd.DataFrame(data, columns=list(MATCH_COLUMNS.values()))
    frame["date"] = pd.to_datetime(frame["date"], format="%Y%m%d")
    return frame