"""Content-integrity tests for CiscoQuest's 100 levels — the one packaged
game that never had a dedicated test file for its LEVELS data (CryptoQuest/
ReverseQuest/WebHackQuest have test_quest_levels.py; the standalone games
have their own). CiscoQuest uses the "cisco" engine (match_cisco_command
against an "accepted" list) rather than exec-and-compare."""

import pytest

from games import ciscoquest
from games.base import match_cisco_command

REQUIRED_KEYS = {
    "id", "title", "description", "challenge", "hint",
    "solution", "accepted", "explanation", "points", "category",
}

# Words play_python_assert_level / play_cisco_level treat as control
# commands rather than submitted input — a level whose solution or accepted
# list happens to equal one of these could never actually be typed and
# accepted as an answer.
CONTROL_WORDS = {"done", "hint", "skip", "solution"}


def test_exactly_100_levels_sequential_ids():
    assert len(ciscoquest.LEVELS) == 100
    ids = [lvl["id"] for lvl in ciscoquest.LEVELS]
    assert ids == list(range(1, 101))


def test_every_level_has_required_fields_and_positive_points():
    for lvl in ciscoquest.LEVELS:
        missing = REQUIRED_KEYS - lvl.keys()
        assert not missing, f"level {lvl['id']} missing {missing}"
        assert lvl["points"] > 0
        assert isinstance(lvl["accepted"], list) and lvl["accepted"]


@pytest.mark.parametrize("level", ciscoquest.LEVELS, ids=lambda lvl: f"level-{lvl['id']}")
def test_documented_solution_is_matched_by_its_own_accepted_list(level):
    assert match_cisco_command(level["solution"], level["accepted"]), (
        f"level {level['id']} ('{level['title']}'): solution {level['solution']!r} "
        f"not matched by its own accepted list {level['accepted']!r}"
    )


@pytest.mark.parametrize("level", ciscoquest.LEVELS, ids=lambda lvl: f"level-{lvl['id']}")
def test_no_accepted_command_collides_with_a_control_word(level):
    for cmd in level["accepted"]:
        assert cmd.strip().lower() not in CONTROL_WORDS, (
            f"level {level['id']} ('{level['title']}'): accepted command {cmd!r} "
            f"would be swallowed as a menu command instead of a submitted answer"
        )
