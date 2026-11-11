import pandas as pd
import pytest

from tennisplot.parse import (
    _extract_birth_date,
    _extract_match_rows,
    _rows_to_frame,
)

FEMALE_JS = """var morematchmx = [["19951030", "Canadian Open", "Carpet", "W", "L", "", "", "WC", "Q1", "6-1 6-1", "3", "Anne Miller", "149", "7", "", "R", "19770119", "", "USA", "0", "", "", "", "", "", "", "1995-W-WT-CAN-02A-1995-013"],
  ["19970307", "Indian Wells", "Hard", "W", "L", "", "", "WC", "Q1", "6-4 6-0", "3", "Alexia Dechaume Balleret", "87", "", "", "R", "19700503", "", "FRA", "0", "", "", "", "", "", "", "1997-W-WT-USA-02A-1997-006"]]"""

MALE_JS = """var morematchmx = [["20010910", "Spain F10", "Hard", "S", "L", "", "", "WC", "R32", "2-6 7-5 6-2", "3", "Guillermo Platel", "731", "", "", "R", "22.264202601", "", "ESP", "0", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "2001-M-FU-ESP-10A-2001-002", "", "1", "1"],
  ["20010917", "Seville CH", "Clay", "C", "W", "", "", "WC", "R32", "6-4 6-4", "3", "Israel Matos Gil", "751", "", "Q", "U", "18.7597535934", "", "ESP", "0", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "2001-784-015", "", "1", "1"]]"""


def test_extract_rows_female():
    rows = _extract_match_rows(FEMALE_JS)
    assert len(rows) == 2
    assert rows[0][11] == "Anne Miller"


def test_extract_rows_male():
    rows = _extract_match_rows(MALE_JS)
    assert len(rows) == 2
    assert rows[1][11] == "Israel Matos Gil"


def test_rows_to_frame_female():
    frame = _rows_to_frame(_extract_match_rows(FEMALE_JS))
    assert frame["date"].iloc[0] == pd.Timestamp("1995-10-30")
    assert frame["result"].tolist() == ["L", "L"]
    assert frame["opponent_info"].iloc[0] == "19770119"


def test_rows_to_frame_male():
    frame = _rows_to_frame(_extract_match_rows(MALE_JS))
    assert frame["result"].tolist() == ["L", "W"]
    assert frame["opponent_info"].iloc[0] == "22.264202601"


def test_missing_match_data_raises():
    with pytest.raises(ValueError):
        _extract_match_rows("var something_else = 1;")


def test_extract_birth_date():
    assert _extract_birth_date("var dob=19810926;") == pd.Timestamp("1981-09-26")