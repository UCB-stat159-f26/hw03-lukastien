BASE_URL = "https://www.tennisabstract.com/jsmatches/{name}Career.js"


def _normalize_name(player_name):
    """Turn 'serena williams' or 'SerenaWilliams' into 'SerenaWilliams'."""
    words = player_name.strip().split()
    if not words:
        raise ValueError("Player name must not be empty.")
    return "".join(word[0].upper() + word[1:] for word in words)


def _build_url(player_name):
    """Return the career JS URL for a player name."""
    return BASE_URL.format(name=_normalize_name(player_name))