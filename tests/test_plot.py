import matplotlib.pyplot as plt
import pandas as pd
import pytest

from tennisplot.plot import plot_age_gap


def make_matches():
    return pd.DataFrame({
        "player_age": [20.0, 21.0, 22.0],
        "age_difference": [-2.0, 1.0, 0.5],
        "result": ["W", "L", "W"],
    })


def test_plot_has_labels_and_one_layer_per_result():
    fig = plot_age_gap(make_matches(), title="Test")
    ax = fig.axes[0]
    assert ax.get_xlabel() == "Player's age"
    assert ax.get_title() == "Test"
    assert len(ax.collections) == 2
    plt.close(fig)


def test_plot_rejects_wrong_input():
    with pytest.raises(ValueError, match="missing"):
        plot_age_gap(pd.DataFrame({"x": [1]}))