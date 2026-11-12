import pytest

import tennisplot.data as data

CAREER_JS = (
    'var morematchmx = [["19951030", "Canadian Open", "Carpet", "W", "L", "", "", '
    '"WC", "Q1", "6-1 6-1", "3", "Anne Miller", "149", "7", "", "R", "19770119", '
    '"", "USA", "0", "", "", "", "", "", "", "1995-W-WT-CAN-02A-1995-013"]]'
)


def fake_download(url, player_name):
    if url.endswith("Career.js"):
        return CAREER_JS
    return "var dob=19810926;"


def test_get_player_matches_returns_clean_frame(monkeypatch):
    monkeypatch.setattr(data, "_download_js", fake_download)
    frame = data.get_player_matches("serena williams")
    assert list(frame.columns) == data.OUTPUT_COLUMNS
    assert len(frame) == 1
    assert frame["opponent"].iloc[0] == "Anne Miller"
    assert frame["result"].iloc[0] == "L"


def test_unknown_player_raises_clear_error(monkeypatch):
    def fake_not_found(url, player_name):
        raise ValueError(f"Player '{player_name}' was not found")

    monkeypatch.setattr(data, "_download_js", fake_not_found)
    with pytest.raises(ValueError, match="not found"):
        data.get_player_matches("Gaston Sanchez")
        
def test_get_player_matches_includes_recent_matches(monkeypatch):
    recent_js = (
        'var dob=19810926; var matchmx = [["20260629", "Wimbledon", "Grass", "G", '
        '"W", "", "", "WC", "R128", "6-3 6-4", "3", "Maya Joint", "87", "", "", '
        '"R", "20060416"]];'
    )

    def fake_download(url, player_name):
        return CAREER_JS if url.endswith("Career.js") else recent_js

    monkeypatch.setattr(data, "_download_js", fake_download)
    frame = data.get_player_matches("serena williams")
    assert len(frame) == 2
    assert frame["date"].iloc[-1].year == 2026