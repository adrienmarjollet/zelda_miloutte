"""Quest definitions for story and side quests."""

from zelda_miloutte.quest_manager import Quest


def get_all_quests():
    """Return list of all quest definitions."""
    return STORY_QUESTS + SIDE_QUESTS


def _obj(obj_type, target, required, description=""):
    return {"type": obj_type, "target": target, "current": 0, "required": required, "description": description}


# ── Story Quests (main chain) ────────────────────────────────────

STORY_QUESTS = [
    Quest(
        id="story_1",
        name="The Elder's Warning",
        description="Talk to the village elder about the spreading corruption.",
        objectives=[_obj("talk", "elder", 1, "Talk to the Elder")],
        rewards={"xp": 50},
        prerequisites=[],
        is_story=True,
    ),
    Quest(
        id="story_2",
        name="Cleanse the Forest",
        description="Defeat the Forest Guardian to stop the corruption.",
        objectives=[_obj("defeat_boss", "forest_guardian", 1, "Defeat the Forest Guardian")],
        rewards={"xp": 150},
        prerequisites=["story_1"],
        is_story=True,
    ),
    Quest(
        id="story_3",
        name="Desert Secrets",
        description="Travel to the desert and find the archaeologist.",
        objectives=[_obj("talk", "archaeologist", 1, "Find the archaeologist in the desert")],
        rewards={"xp": 75},
        prerequisites=["story_2"],
        is_story=True,
    ),
    Quest(
        id="story_4",
        name="Tomb of the Sand King",
        description="Enter the desert tomb and defeat the Sand Worm.",
        objectives=[_obj("defeat_boss", "sand_worm", 1, "Defeat the Sand Worm")],
        rewards={"xp": 200},
        prerequisites=["story_3"],
        is_story=True,
    ),
    Quest(
        id="story_5",
        name="Into the Fire",
        description="The volcano seal is breaking. Enter the volcano.",
        objectives=[_obj("visit", "volcano", 1, "Enter the volcano")],
        rewards={"xp": 100},
        prerequisites=["story_4"],
        is_story=True,
    ),
    Quest(
        id="story_6",
        name="The Inferno's End",
        description="Defeat the Inferno Drake and restore the seal.",
        objectives=[_obj("defeat_boss", "inferno_drake", 1, "Defeat the Inferno Drake")],
        rewards={"xp": 300},
        prerequisites=["story_5"],
        is_story=True,
    ),
]

# ── Side Quests ──────────────────────────────────────────────────

SIDE_QUESTS = [
    Quest(
        id="side_1",
        name="Lost Pendant",
        description="Find the lost pendant in the Forest and return it.",
        objectives=[
            _obj("collect", "pendant", 1, "Find the pendant in the Forest"),
            _obj("talk", "pendant_owner", 1, "Return the pendant"),
        ],
        rewards={"xp": 100, "keys": 1},
        prerequisites=["story_1"],
    ),
    Quest(
        id="side_2",
        name="Goblin Slayer",
        description="Defeat 10 enemies in the overworld.",
        objectives=[_obj("kill", "enemy", 10, "Defeat 10 enemies")],
        rewards={"xp": 120},
        prerequisites=[],
    ),
    Quest(
        id="side_3",
        name="Pest Control",
        description="Clear out 5 vine snappers from the forest.",
        objectives=[_obj("kill", "vine_snapper", 5, "Defeat 5 vine snappers")],
        rewards={"xp": 100},
        prerequisites=["story_1"],
    ),
    Quest(
        id="side_4",
        name="The Herbalist",
        description="Collect 3 desert herbs for the herbalist NPC.",
        objectives=[_obj("collect", "desert_herb", 3, "Collect 3 desert herbs")],
        rewards={"xp": 150},
        prerequisites=["story_3"],
    ),
    Quest(
        id="side_5",
        name="Frozen Relic",
        description="Find the hidden chest in the volcano dungeon.",
        objectives=[_obj("collect", "frozen_relic", 1, "Find the hidden chest")],
        rewards={"xp": 200},
        prerequisites=["story_5"],
    ),
    Quest(
        id="side_companion",
        name="A Lost Friend",
        description="Find a lost companion in the forest. A villager mentioned seeing a small creature nearby.",
        objectives=[
            _obj("talk", "companion_keeper", 1, "Talk to the animal keeper in the village"),
            _obj("find", "companion", 1, "Find the lost companion in the forest"),
        ],
        rewards={"xp": 100},
        prerequisites=["story_1"],
    ),
    Quest(
        id="side_6",
        name="Monster Hunter",
        description="Defeat all 4 bosses across the land.",
        objectives=[
            _obj("defeat_boss", "boss_1", 1, "Defeat the Dark Lord"),
            _obj("defeat_boss", "boss_2", 1, "Defeat the Ice Demon"),
            _obj("defeat_boss", "forest_guardian", 1, "Defeat the Forest Guardian"),
            _obj("defeat_boss", "sand_worm", 1, "Defeat the Sand Worm"),
        ],
        rewards={"xp": 500},
        prerequisites=[],
    ),
]
