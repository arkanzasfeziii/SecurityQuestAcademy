"""Content-integrity tests for the assertion-engine quests' 100-level lists each:
CryptoQuest, ReverseQuest, WebHackQuest. Mirrors test_standalone_cyberquest_levels.py
but validates via eval_python_assertions since these levels are define-then-assert
style rather than print-and-compare style.
"""

import pytest

from games import cryptoquest, reversequest, webhackquest
from games.base import eval_python_assertions

REQUIRED_KEYS = {
    "id",
    "title",
    "description",
    "challenge",
    "hint",
    "solution",
    "test_code",
    "explanation",
    "points",
    "category",
}

QUESTS = [
    ("cryptoquest", cryptoquest),
    ("reversequest", reversequest),
    ("webhackquest", webhackquest),
]

ALL_LEVELS = [
    pytest.param(quest_name, lvl, id=f"{quest_name}-level-{lvl['id']}")
    for quest_name, mod in QUESTS
    for lvl in mod.LEVELS
]


@pytest.mark.parametrize("quest_name,mod", QUESTS, ids=[q[0] for q in QUESTS])
def test_exactly_100_levels(quest_name, mod):
    assert len(mod.LEVELS) == 100


@pytest.mark.parametrize("quest_name,mod", QUESTS, ids=[q[0] for q in QUESTS])
def test_level_ids_are_sequential_and_unique(quest_name, mod):
    ids = [lvl["id"] for lvl in mod.LEVELS]
    assert ids == list(range(1, 101))


@pytest.mark.parametrize("quest_name,mod", QUESTS, ids=[q[0] for q in QUESTS])
def test_every_level_has_required_fields(quest_name, mod):
    for lvl in mod.LEVELS:
        missing = REQUIRED_KEYS - lvl.keys()
        assert not missing, f"{quest_name} level {lvl.get('id')} missing {missing}"


@pytest.mark.parametrize("quest_name,mod", QUESTS, ids=[q[0] for q in QUESTS])
def test_every_level_awards_positive_points(quest_name, mod):
    for lvl in mod.LEVELS:
        assert lvl["points"] > 0, f"{quest_name} level {lvl['id']} has non-positive points"


@pytest.mark.parametrize("quest_name,level", ALL_LEVELS)
def test_documented_solution_passes_its_own_test_code(quest_name, level):
    ok, error = eval_python_assertions(level["solution"], level["test_code"])
    assert ok, f"{quest_name} level {level['id']} ('{level['title']}'): {error}"
