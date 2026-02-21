"""Tests for the QuestManager."""

import pytest
from zelda_miloutte.quest_manager import Quest, QuestManager


def _make_quest(qid="test_q", name="Test Quest", prereqs=None, objectives=None,
                rewards=None, is_story=False):
    return Quest(
        id=qid,
        name=name,
        description="A test quest.",
        objectives=objectives or [
            {"type": "kill", "target": "enemy", "current": 0, "required": 3},
        ],
        rewards=rewards or {"xp": 100},
        prerequisites=prereqs or [],
        is_story=is_story,
    )


class TestQuestRegistration:
    def test_register_and_get(self):
        qm = QuestManager()
        q = _make_quest()
        qm.register_quest(q)
        assert qm.get_quest("test_q") is q

    def test_get_nonexistent(self):
        qm = QuestManager()
        assert qm.get_quest("nope") is None


class TestQuestStart:
    def test_start_quest(self):
        qm = QuestManager()
        qm.register_quest(_make_quest())
        assert qm.start_quest("test_q") is True
        assert qm.get_quest("test_q").status == "active"

    def test_start_already_active(self):
        qm = QuestManager()
        qm.register_quest(_make_quest())
        qm.start_quest("test_q")
        assert qm.start_quest("test_q") is False

    def test_start_nonexistent(self):
        qm = QuestManager()
        assert qm.start_quest("nope") is False

    def test_start_with_unmet_prereqs(self):
        qm = QuestManager()
        q1 = _make_quest("q1")
        q2 = _make_quest("q2", prereqs=["q1"])
        qm.register_quest(q1)
        qm.register_quest(q2)
        assert qm.start_quest("q2") is False

    def test_start_with_met_prereqs(self):
        qm = QuestManager()
        q1 = _make_quest("q1")
        q2 = _make_quest("q2", prereqs=["q1"])
        qm.register_quest(q1)
        qm.register_quest(q2)
        # Complete q1
        qm.start_quest("q1")
        q1.objectives[0]["current"] = 3
        qm.complete_quest("q1")
        # Now q2 should be startable
        assert qm.start_quest("q2") is True


class TestObjectiveTracking:
    def test_update_objective(self):
        qm = QuestManager()
        q = _make_quest()
        qm.register_quest(q)
        qm.start_quest("test_q")
        qm.update_objective("kill", "enemy", 2)
        assert q.objectives[0]["current"] == 2

    def test_update_caps_at_required(self):
        qm = QuestManager()
        q = _make_quest()
        qm.register_quest(q)
        qm.start_quest("test_q")
        qm.update_objective("kill", "enemy", 100)
        assert q.objectives[0]["current"] == 3  # capped at required

    def test_update_ignores_inactive(self):
        qm = QuestManager()
        q = _make_quest()
        qm.register_quest(q)
        qm.update_objective("kill", "enemy", 5)
        assert q.objectives[0]["current"] == 0  # not active, no update

    def test_update_ignores_wrong_type(self):
        qm = QuestManager()
        q = _make_quest()
        qm.register_quest(q)
        qm.start_quest("test_q")
        qm.update_objective("collect", "enemy", 5)
        assert q.objectives[0]["current"] == 0


class TestQuestCompletion:
    def test_check_not_complete(self):
        qm = QuestManager()
        q = _make_quest()
        qm.register_quest(q)
        qm.start_quest("test_q")
        assert qm.check_quest_complete("test_q") is False

    def test_check_complete(self):
        qm = QuestManager()
        q = _make_quest()
        qm.register_quest(q)
        qm.start_quest("test_q")
        qm.update_objective("kill", "enemy", 3)
        assert qm.check_quest_complete("test_q") is True

    def test_complete_quest_returns_rewards(self):
        qm = QuestManager()
        q = _make_quest()
        qm.register_quest(q)
        qm.start_quest("test_q")
        qm.update_objective("kill", "enemy", 3)
        rewards = qm.complete_quest("test_q")
        assert rewards == {"xp": 100}
        assert q.status == "completed"

    def test_complete_quest_not_ready(self):
        qm = QuestManager()
        q = _make_quest()
        qm.register_quest(q)
        qm.start_quest("test_q")
        assert qm.complete_quest("test_q") is None

    def test_complete_quest_inactive(self):
        qm = QuestManager()
        qm.register_quest(_make_quest())
        assert qm.complete_quest("test_q") is None


class TestQuestQueries:
    def test_get_active_quests(self):
        qm = QuestManager()
        qm.register_quest(_make_quest("q1"))
        qm.register_quest(_make_quest("q2"))
        qm.start_quest("q1")
        active = qm.get_active_quests()
        assert len(active) == 1
        assert active[0].id == "q1"

    def test_get_completed_quests(self):
        qm = QuestManager()
        q = _make_quest()
        qm.register_quest(q)
        qm.start_quest("test_q")
        q.objectives[0]["current"] = 3
        qm.complete_quest("test_q")
        completed = qm.get_completed_quests()
        assert len(completed) == 1

    def test_active_objective_text_story_priority(self):
        qm = QuestManager()
        side = _make_quest("side", name="Side Quest", is_story=False)
        story = _make_quest("story", name="Main Quest", is_story=True,
                           objectives=[{"type": "talk", "target": "elder", "current": 0,
                                       "required": 1, "description": "Talk to elder"}])
        qm.register_quest(side)
        qm.register_quest(story)
        qm.start_quest("side")
        qm.start_quest("story")
        text = qm.get_active_objective_text()
        assert "Main Quest" in text


class TestQuestSerialization:
    def test_roundtrip(self):
        qm = QuestManager()
        q = _make_quest()
        qm.register_quest(q)
        qm.start_quest("test_q")
        qm.update_objective("kill", "enemy", 2)

        data = qm.to_dict()

        qm2 = QuestManager()
        qm2.register_quest(_make_quest())
        qm2.from_dict(data)

        q2 = qm2.get_quest("test_q")
        assert q2.status == "active"
        assert q2.objectives[0]["current"] == 2

    def test_multiple_objectives(self):
        q = _make_quest(objectives=[
            {"type": "kill", "target": "enemy", "current": 0, "required": 5},
            {"type": "collect", "target": "gem", "current": 0, "required": 3},
        ])
        qm = QuestManager()
        qm.register_quest(q)
        qm.start_quest("test_q")
        qm.update_objective("kill", "enemy", 5)
        # Only first objective met
        assert qm.check_quest_complete("test_q") is False
        qm.update_objective("collect", "gem", 3)
        assert qm.check_quest_complete("test_q") is True
