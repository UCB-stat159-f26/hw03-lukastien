import matplotlib.pyplot as plt

REQUIRED_COLUMNS = ["player_age", "age_difference", "result"]
RESULT_STYLES = {"W": ("Win", "#1f77b4"), "L": ("Loss", "#d62728")}


def _check_columns(matches):
    """Make sure the data frame came from get_player_matches()."""
    missing = [col for col in REQUIRED_COLUMNS if col not in matches.columns]
    if missing:
        raise ValueError(
            f"matches is missing columns: {missing}. "
            "Create it with get_player_matches()."
        )


def _scatter_by_result(ax, matches):
    """Draw one scatter layer per result, so the legend is automatic."""
    for result, (label, color) in RESULT_STYLES.items():
        subset = matches[matches["result"] == result]
        ax.scatter(subset["player_age"], subset["age_difference"],
                   c=color, s=18, alpha=0.7, label=label)


def _style_axes(ax, title):
    """Add the reference line, axis labels, title and legend."""
    ax.axhline(0, color="gray", linewidth=0.8)
    ax.set_xlabel("Player's age")
    ax.set_ylabel("Player's age minus opponent's age")
    ax.set_title(title)
    ax.legend(title="Result")


def plot_age_gap(matches, title="Age gap vs. player age"):
    """Scatter plot of age gap against player age, colored by win/loss.

    Parameters
    ----------
    matches : pandas.DataFrame
        Output of get_player_matches().
    title : str, optional
        Plot title.

    Returns
    -------
    matplotlib.figure.Figure
    """
    _check_columns(matches)
    fig, ax = plt.subplots(figsize=(10, 6))
    _scatter_by_result(ax, matches)
    _style_axes(ax, title)
    return fig