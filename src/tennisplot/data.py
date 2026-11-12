from .fetch import _build_url, _download_js
from .parse import (
    _add_ages,
    _extract_birth_date,
    _extract_match_rows,
    _extract_recent_rows,
    _rows_to_frame,
)

OUTPUT_COLUMNS = [
    "date", "tournament", "round", "opponent", "result",
    "player_age", "opponent_age", "age_difference",
]


def get_player_matches(player_name):
    """Return a player's career matches from tennisabstract.com.

    Parameters
    ----------
    player_name : str
        e.g. "serena williams", "Serena Williams" or "SerenaWilliams".

    Returns
    -------
    pandas.DataFrame
        One row per match, with the player's age, the opponent's age, their
        difference (player minus opponent) and the result ("W" or "L").

    Raises
    ------
    ValueError
        If the player is not found on tennisabstract.com.
    """
    career_js = _download_js(_build_url(player_name), player_name)
    player_js = _download_js(_build_url(player_name, career=False), player_name)
    rows = _extract_match_rows(career_js) + _extract_recent_rows(player_js)
    frame = _rows_to_frame(rows)
    frame = _add_ages(frame, _extract_birth_date(player_js))
    complete = frame.dropna(subset=["player_age", "opponent_age"])
    return complete[OUTPUT_COLUMNS].reset_index(drop=True)