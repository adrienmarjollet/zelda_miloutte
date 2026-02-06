"""Quest tracking system for story and side quests."""

from dataclasses import dataclass, field


@dataclass
class Quest:
    id: str
    name: str
    description: str
    objectives: list = field(default_factory=list)  # list of {"type": str, "target": str/int, "current": int, "required": int}
    rewards: dict = field(default_factory=dict)  # {"xp": int, "keys": int}
    prerequisites: list = field(default_factory=list)  # list of quest IDs
    status: str = "inactive"  # "inactive", "active", "completed"
    is_story: bool = False


class QuestManager:
    """Manages all quests and tracks progress."""

    def __init__(self):
        self.quests = {}  # id -> Quest

    def register_quest(self, quest):
        self.quests[quest.id] = quest

    def start_quest(self, quest_id):
        """Activate a quest if prerequisites are met."""
        quest = self.quests.get(quest_id)
        if quest is None or quest.status != "inactive":
            return False
        # Check prerequisites
        for prereq_id in quest.prerequisites:
            prereq = self.quests.get(prereq_id)
            if prereq is None or prereq.status != "completed":
                return False
        quest.status = "active"
        return True

    def update_objective(self, objective_type, target, amount=1):
        """Update progress on matching objectives across active quests.

        Args:
            objective_type: "kill", "collect", "talk", "visit", "defeat_boss"
            target: Target identifier (enemy type, item name, npc name, area id, boss id)
            amount: How much to increment
        """
        for quest in self.quests.values():
            if quest.status != "active":
                continue
            for obj in quest.objectives:
                if obj["type"] == objective_type and obj["target"] == target:
                    obj["current"] = min(obj["current"] + amount, obj["required"])

    def check_quest_complete(self, quest_id):
        """Check if all objectives are met for a quest."""
        quest = self.quests.get(quest_id)
        if quest is None or quest.status != "active":
            return False
        return all(obj["current"] >= obj["required"] for obj in quest.objectives)

    def complete_quest(self, quest_id):
        """Mark quest as completed. Returns rewards dict or None."""
        quest = self.quests.get(quest_id)
        if quest is None or quest.status != "active":
            return None
        if not self.check_quest_complete(quest_id):
            return None
        quest.status = "completed"
        return quest.rewards

    def get_active_quests(self):
        """Return list of active quests."""
        return [q for q in self.quests.values() if q.status == "active"]

    def get_completed_quests(self):
        return [q for q in self.quests.values() if q.status == "completed"]

    def get_quest(self, quest_id):
        return self.quests.get(quest_id)

    def get_active_objective_text(self):
        """Return a short string describing the current main objective."""
        # Prioritize story quests
        for q in self.quests.values():
            if q.status == "active" and q.is_story:
                for obj in q.objectives:
                    if obj["current"] < obj["required"]:
                        return f"{q.name}: {obj.get('description', q.description)}"
                return q.name
        # Fall back to any active quest
        active = self.get_active_quests()
        if active:
            q = active[0]
            return q.name
        return ""

    def to_dict(self):
        """Serialize quest state for saving."""
        result = {}
        for qid, quest in self.quests.items():
            result[qid] = {
                "status": quest.status,
                "objectives": [
                    {"type": o["type"], "target": o["target"],
                     "current": o["current"], "required": o["required"],
                     "description": o.get("description", "")}
                    for o in quest.objectives
                ],
            }
        return result

    def from_dict(self, data):
        """Restore quest state from save data."""
        for qid, qdata in data.items():
            quest = self.quests.get(qid)
            if quest is None:
                continue
            quest.status = qdata.get("status", quest.status)
            saved_objs = qdata.get("objectives", [])
            for i, obj in enumerate(quest.objectives):
                if i < len(saved_objs):
                    obj["current"] = saved_objs[i].get("current", 0)
