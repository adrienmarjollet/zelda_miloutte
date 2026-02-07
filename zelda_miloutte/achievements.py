"""Achievement system for tracking player accomplishments across saves."""

from dataclasses import dataclass, field


@dataclass
class Achievement:
    """A single achievement definition."""
    id: str
    name: str
    description: str
    icon_id: str
    unlocked: bool = False


# All achievement definitions
ACHIEVEMENT_DEFS = [
    Achievement("first_blood", "First Blood", "Defeat your first enemy.", "sword"),
    Achievement("monster_slayer", "Monster Slayer", "Defeat 50 enemies.", "sword"),
    Achievement("boss_hunter", "Boss Hunter", "Defeat all bosses.", "trophy"),
    Achievement("treasure_hunter", "Treasure Hunter", "Open all chests.", "chest"),
    Achievement("speed_demon", "Speed Demon", "Complete the game in under 30 minutes.", "clock"),
    Achievement("untouchable", "Untouchable", "Defeat a boss without taking damage.", "shield"),
    Achievement("completionist", "Completionist", "Achieve 100% completion.", "star"),
    Achievement("explorer", "Explorer", "Visit all areas.", "compass"),
    Achievement("quest_master", "Quest Master", "Complete all quests.", "scroll"),
    Achievement("level_10", "Level 10", "Reach level 10.", "star"),
]

# Total bosses in the game
ALL_BOSS_IDS = ["boss_1", "boss_2", "forest_guardian", "sand_worm", "inferno_drake"]

# All areas in the game
ALL_AREA_IDS = ["overworld", "forest", "desert", "volcano"]

# Total chests across the game (approximate; counted from map spawns)
TOTAL_CHESTS = 20


class AchievementManager:
    """Tracks achievement state and checks for unlock conditions."""

    def __init__(self):
        self.achievements = {}
        for defn in ACHIEVEMENT_DEFS:
            self.achievements[defn.id] = Achievement(
                id=defn.id,
                name=defn.name,
                description=defn.description,
                icon_id=defn.icon_id,
                unlocked=False,
            )
        # Tracking counters
        self.total_kills = 0
        self.total_chests_opened = 0
        self.visited_areas = set()
        self.defeated_bosses = set()
        self.completed_quests = set()
        self.play_time = 0.0  # seconds
        self.game_completed = False

        # Per-boss damage tracking for "untouchable"
        self._boss_fight_no_damage = False
        self._in_boss_fight = False

        # Pending popup notifications
        self.pending_popups = []

    def unlock(self, achievement_id):
        """Unlock an achievement if not already unlocked. Returns True if newly unlocked."""
        ach = self.achievements.get(achievement_id)
        if ach is None or ach.unlocked:
            return False
        ach.unlocked = True
        self.pending_popups.append(ach)
        return True

    def get_unlocked_count(self):
        """Return number of unlocked achievements."""
        return sum(1 for a in self.achievements.values() if a.unlocked)

    def get_total_count(self):
        """Return total number of achievements."""
        return len(self.achievements)

    # ── Event handlers ───────────────────────────────────────────────

    def on_enemy_kill(self):
        """Called when any enemy is killed."""
        self.total_kills += 1
        if self.total_kills >= 1:
            self.unlock("first_blood")
        if self.total_kills >= 50:
            self.unlock("monster_slayer")

    def on_boss_kill(self, boss_id):
        """Called when a boss is defeated."""
        self.defeated_bosses.add(boss_id)
        # Check untouchable
        if self._in_boss_fight and self._boss_fight_no_damage:
            self.unlock("untouchable")
        self._in_boss_fight = False
        # Check boss hunter
        if self.defeated_bosses >= set(ALL_BOSS_IDS):
            self.unlock("boss_hunter")
        self._check_completionist()

    def on_chest_open(self):
        """Called when a chest is opened."""
        self.total_chests_opened += 1
        if self.total_chests_opened >= TOTAL_CHESTS:
            self.unlock("treasure_hunter")
        self._check_completionist()

    def on_area_enter(self, area_id):
        """Called when the player enters a new area."""
        self.visited_areas.add(area_id)
        if self.visited_areas >= set(ALL_AREA_IDS):
            self.unlock("explorer")
        self._check_completionist()

    def on_quest_complete(self, quest_id):
        """Called when a quest is completed."""
        self.completed_quests.add(quest_id)

    def on_all_quests_complete(self, total_quests):
        """Called to check if all quests are done."""
        if len(self.completed_quests) >= total_quests and total_quests > 0:
            self.unlock("quest_master")
        self._check_completionist()

    def on_level_up(self, new_level):
        """Called when the player levels up."""
        if new_level >= 10:
            self.unlock("level_10")

    def on_game_complete(self):
        """Called when the game is completed (final boss defeated)."""
        self.game_completed = True
        if self.play_time <= 30 * 60:  # 30 minutes in seconds
            self.unlock("speed_demon")
        self._check_completionist()

    def on_boss_fight_start(self):
        """Called when a boss fight begins."""
        self._in_boss_fight = True
        self._boss_fight_no_damage = True

    def on_player_damaged_in_boss_fight(self):
        """Called when the player takes damage during a boss fight."""
        if self._in_boss_fight:
            self._boss_fight_no_damage = False

    def update_play_time(self, dt):
        """Update the tracked play time."""
        self.play_time += dt

    def _check_completionist(self):
        """Check if 100% completion is reached."""
        all_bosses = self.defeated_bosses >= set(ALL_BOSS_IDS)
        all_areas = self.visited_areas >= set(ALL_AREA_IDS)
        all_chests = self.total_chests_opened >= TOTAL_CHESTS
        if all_bosses and all_areas and all_chests and self.game_completed:
            self.unlock("completionist")

    # ── Serialization ────────────────────────────────────────────────

    def to_dict(self):
        """Serialize for saving."""
        return {
            "unlocked": [aid for aid, a in self.achievements.items() if a.unlocked],
            "total_kills": self.total_kills,
            "total_chests_opened": self.total_chests_opened,
            "visited_areas": list(self.visited_areas),
            "defeated_bosses": list(self.defeated_bosses),
            "completed_quests": list(self.completed_quests),
            "play_time": self.play_time,
            "game_completed": self.game_completed,
        }

    def from_dict(self, data):
        """Restore from save data."""
        if data is None:
            return
        for aid in data.get("unlocked", []):
            if aid in self.achievements:
                self.achievements[aid].unlocked = True
        self.total_kills = data.get("total_kills", 0)
        self.total_chests_opened = data.get("total_chests_opened", 0)
        self.visited_areas = set(data.get("visited_areas", []))
        self.defeated_bosses = set(data.get("defeated_bosses", []))
        self.completed_quests = set(data.get("completed_quests", []))
        self.play_time = data.get("play_time", 0.0)
        self.game_completed = data.get("game_completed", False)
