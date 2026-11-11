import requests

BASE_URL = "https://www.tennisabstract.com/jsmatches/{name}{suffix}.js"
HEADERS = {"User-Agent": "tennisplot (UC Berkeley STAT 159 homework)"}


def _build_url(player_name, career=True):
    """Return the career JS URL (default) or the player-info JS URL."""
    suffix = "Career" if career else ""
    return BASE_URL.format(name=_normalize_name(player_name), suffix=suffix)


def _normalize_name(player_name):
    """Turn 'serena williams' or 'SerenaWilliams' into 'SerenaWilliams'."""
    words = player_name.strip().split()
    if not words:
        raise ValueError("Player name must not be empty.")
    return "".join(word[0].upper() + word[1:] for word in words)


def _download_js(url, player_name):
    """Download a JS file; raise a clear error if the player is not found."""
    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
    except requests.RequestException as error:
        raise ConnectionError(f"Could not reach tennisabstract.com: {error}") from error
    if response.status_code == 404:
        raise ValueError(
            f"Player '{player_name}' was not found on tennisabstract.com. "
            "Check the spelling, e.g. 'Serena Williams'."
        )
    response.raise_for_status()
    return response.text