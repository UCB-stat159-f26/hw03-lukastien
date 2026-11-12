# tennisplot

A small Python package that downloads a tennis player's career matches from
[tennisabstract.com](https://www.tennisabstract.com) and plots the age gap
between the player and each opponent, in the style of the NYT's Serena
Williams visualization.

## Installation

```bash
pip install git+https://github.com/UCB-stat159-f26/hw03-lukastien.git
```

## Usage

In the plot, the y-axis is the player's age minus the opponent's age, so
positive values mean the player was older than the opponent. Points are
colored by win or loss. In a script, call `plt.show()` after
`plot_age_gap(...)` to display the figure; in a notebook it appears
automatically.

```python
from tennisplot import get_player_matches, plot_age_gap

# Serena Williams data and plot
serena = get_player_matches("serena williams")
plot_age_gap(serena, title="Serena Williams")

# Rafael Nadal data and plot
rafa = get_player_matches("Rafael Nadal")
plot_age_gap(rafa, title="Rafael Nadal")

# An unknown player raises a clear error
get_player_matches("GastonSanchez")
# ValueError: Player 'GastonSanchez' was not found on tennisabstract.com. ...
```

## Public functions

- `get_player_matches(player_name)`: returns a DataFrame with one row per
  match (`date`, `tournament`, `round`, `opponent`, `result`, `player_age`,
  `opponent_age`, `age_difference`).
- `plot_age_gap(matches, title=...)`: scatter plot of the player's age (x)
  against the age difference (y), colored by win or loss.

## Running the tests

```bash
pip install -e ".[dev]"
pytest
```
The tests use mock data and never contact tennisabstract.com.


## Data notes

- Data comes from two tennisabstract.com files per player: the career match
  file and the player file, which holds the birth date and any recent matches.
- Coverage differs by player. For example, Rafael Nadal's data ends in 2018,
  so career length and win rates should not be compared across players
  without checking the date range.
- Qualifying-round matches are included.


## Reflections

