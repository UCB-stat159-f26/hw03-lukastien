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

When I looked at the first few lines of the raw JS files, I noticed that the
women's and men's files store the opponent column differently. In Serena's
file it holds the opponent's date of birth (like `19770119`), and in Rafa's
file it already holds an age (like `22.26`). My package checks whether each
value is an eight-digit date or an age, so one function works for both. I
also thought a player's own birth date would be in their profile, and it
was. It's in a separate player file, so every player needs two downloads.

Testing was new for me. Because of `monkeypatch`, my tests replace the real
download function with a fake one that gives back a small piece of mock data,
so I can test everything (parsing, ages, columns, and the error for a bad
name) without using the internet. The mock rows came from the assignment, so
I knew what the right answers should be.

There is less data for Rafa than for Serena. His data ends in 2018, even
after I added the recent matches. In both plots there is a lot more blue
(wins) than red (losses), and Serena's win rate is a bit higher: 83% for
Serena and 82% for Rafa. But since the data for Rafa is incomplete, I can't
tell if he was just as dominant as Serena in his later years, so I can't
claim from these plots that she was more dominant.

By doing Homework 3, the things I wanted to show in Homework 2 are now
reproducible for basically any player. Homework 2 was a script for one
player with her birth date and file paths written into the code. Now you
just give the package a name, and it gives a clear error message if the
player isn't found.

