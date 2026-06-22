"""Tests for configuration and game registry."""

from securityquest.config import GAMES, TOOL_NAME


def test_tool_name():
    assert TOOL_NAME == "SecurityQuestAcademy"


def test_seven_games_registered():
    assert len(GAMES) == 7


def test_each_game_has_required_fields():
    required = {"id", "name", "module", "color", "description", "levels", "topics"}
    for game in GAMES:
        assert required.issubset(game.keys()), f"{game['name']} missing fields"


def test_game_ids_sequential():
    ids = [g["id"] for g in GAMES]
    assert ids == list(range(1, 8))


def test_all_games_have_100_levels():
    for game in GAMES:
        assert game["levels"] == "100", f"{game['name']} doesn't have 100 levels"


def test_game_names():
    names = [g["name"] for g in GAMES]
    expected = ["CyberQuest", "BashQuest", "WindowsQuest", "CiscoQuest",
                "CryptoQuest", "ReverseQuest", "WebHackQuest"]
    assert names == expected
