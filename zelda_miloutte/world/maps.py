# Tile types:
# 0=GRASS, 1=WALL, 2=TREE, 3=ROCK, 4=WATER, 5=FLOOR, 6=DOOR, 7=DUNGEON_ENTRANCE, 8=BOSS_DOOR, 9=SPIKES, 10=PIT, 11=DUNGEON_ENTRANCE_2
# 12=TRANSITION_N, 13=TRANSITION_S, 14=TRANSITION_E, 15=TRANSITION_W, 16=FOREST_FLOOR, 17=SAND, 18=LAVA
# 19=BARRIER_RED, 20=BARRIER_BLUE, 21=BRIDGE, 22=ICE, 23=CRACKED_ICE, 24=FROZEN_WALL, 25=SNOW

# Overworld: 30 columns x 20 rows
# West half (cols 0-14): Cozy village with houses, paths, gardens. NO enemies.
# East half (cols 15-29): Wilds with enemies, pond, dungeon entrances.
# fmt: off
OVERWORLD = [
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 5, 5, 2, 0, 0, 0, 0, 0, 0, 4, 4, 4, 0, 0, 0, 0, 0, 0, 2],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0,11, 5, 5, 2, 0, 0, 0, 0, 0, 4, 4, 4, 4, 4, 0, 0, 0, 0, 0, 2],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0, 0, 4, 4, 4, 4, 4, 0, 0, 0, 0, 0, 2],
    [2, 0, 0, 0, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 0, 0, 0, 0, 0, 0, 2],
    [2, 0, 0, 0, 2, 5, 5, 5, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
    [2, 0, 0, 0,11, 5, 5, 5, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0,14],
    [2, 0, 0, 0, 2, 5, 5, 5, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,14],
    [2, 0, 0, 0, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0,14],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,14],
    [2, 0, 2, 2, 2, 0, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,14],
    [2, 0, 2, 5, 2, 0, 0, 0, 0, 0, 2, 5, 5, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2],
    [2, 0, 2, 5, 2, 0, 0, 0, 0, 0,11, 5, 5, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 5, 5, 5, 2],
    [2, 0, 2, 6, 2, 0, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 5, 5, 5, 2],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 5, 5, 5, 2],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 5, 5, 5, 2],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
]
# fmt: on

OVERWORLD_SPAWNS = {
    "player": (3, 9),
    "enemies": [
        # All enemies in the eastern wilds (cols 15+)
        {"x": 17, "y": 8, "patrol": [(17, 8), (17, 12)]},
        {"x": 20, "y": 2, "patrol": [(18, 2), (23, 2)]},
        {"x": 24, "y": 10, "patrol": [(22, 10), (27, 10)]},
        {"x": 16, "y": 15, "patrol": [(16, 15), (22, 15)]},
        {"x": 19, "y": 5, "type": "archer", "patrol": []},
        {"x": 25, "y": 13, "type": "archer", "patrol": []},
    ],
    "items": [
        {"x": 7, "y": 11, "type": "heart"},
        {"x": 18, "y": 8, "type": "key"},
        {"x": 23, "y": 3, "type": "heart"},
    ],
    "chests": [
        {"x": 5, "y": 7, "contents": "heart"},
        {"x": 22, "y": 11, "contents": "key"},
    ],
    "signs": [
        {
            "x": 3, "y": 6,
            "text": "Welcome to Miloutte Village \u2014 Founded in the Age of the Seal.",
        },
        {
            "x": 7, "y": 9,
            "text": "The Four Seals protect our land from darkness. May they never break.",
        },
        {
            "x": 14, "y": 9,
            "text": "CAUTION: Monsters sighted beyond the village border.",
        },
        {
            "x": 20, "y": 14,
            "text": "Danger ahead! The dungeon entrance lies to the east.",
        },
        {
            "x": 26, "y": 17,
            "text": "You need a key to enter the dungeon.",
        },
    ],
    "npcs": [
        # --- Original NPCs (repositioned within village) ---
        {
            "x": 6, "y": 5, "name": "Elder Mira", "variant": "elder",
            "quest_id": "story_1",
            "dialogue": {
                "default": [
                    "Greetings, young Miloutte!",
                    "A terrible corruption is spreading from the east.",
                    "Dark creatures have overrun the Forest beyond our borders.",
                    "You must investigate. Head east to the Forest!",
                ],
                "quest_active": [
                    "The Forest lies to the east. Be careful, Miloutte!",
                ],
                "quest_done": [
                    "You've done it! The Forest is cleansed!",
                    "But I sense greater darkness in the desert beyond...",
                ],
            },
        },
        {
            "x": 2, "y": 9, "name": "Guard Bron", "variant": "guard",
            "dialogue": {
                "default": [
                    "I keep watch over the village gate.",
                    "The goblins have been getting bolder lately.",
                    "Stay inside the village border if you're not ready to fight!",
                ],
            },
            "quest_id": "side_2",
        },
        # --- New village NPCs ---
        {
            "x": 3, "y": 16, "name": "Merchant Pasha", "variant": "merchant",
            "dialogue": {
                "default": [
                    "Welcome, welcome! I am Pasha, traveling merchant.",
                    "Business has been terrible since the monsters appeared.",
                    "The trade routes to the east are completely blocked!",
                    "This corruption is recent... it started only a few moons ago.",
                    "If someone could clear the roads, perhaps trade would flow again.",
                ],
            },
        },
        {
            "x": 11, "y": 1, "name": "Historian Orin", "variant": "elder",
            "dialogue": {
                "default": [
                    "Ah, young hero! I am Orin, keeper of the village archives.",
                    "Long ago, four great Seals were forged to contain an ancient evil.",
                    "Each Seal was placed in a dungeon: Forest, Desert, Volcano, and one lost to legend.",
                    "The prophecy speaks of a cat-eared hero who would restore the Seals.",
                    "Could it be... you? The markings match the old texts perfectly!",
                    "Seek the dungeons to the east. The fate of our world depends on it.",
                ],
            },
        },
        {
            "x": 8, "y": 11, "name": "Lily", "variant": "villager",
            "dialogue": {
                "default": [
                    "Oh... hello. I'm Lily.",
                    "My brother went into the forest last week to gather herbs...",
                    "He never came back.",
                    "The elder says the forest is too dangerous now.",
                    "If you're heading east... please, keep an eye out for him?",
                ],
            },
        },
        {
            "x": 12, "y": 16, "name": "Farmer Tom\u00e9", "variant": "villager",
            "dialogue": {
                "default": [
                    "Mornin'. Name's Tom\u00e9. I tend the fields east of here.",
                    "Well... I USED to tend the fields east of here.",
                    "The soil near the border has gone black and dead.",
                    "Whatever darkness lurks in those dungeons, it's poisoning our land.",
                    "Fix the source, and maybe our crops will grow again.",
                ],
            },
        },
        {
            "x": 5, "y": 13, "name": "Little Niko", "variant": "villager",
            "dialogue": {
                "default": [
                    "Whoa!! Are you really going out there?!",
                    "My mom says the monsters will eat you up!",
                    "But I think you're super brave!",
                    "When I grow up, I wanna be a hero just like you!",
                ],
            },
        },
        {
            "x": 10, "y": 8, "name": "Keeper Fauna", "variant": "villager",
            "quest_id": "side_companion",
            "dialogue": {
                "default": [
                    "Oh, hello there! I'm Fauna, the animal keeper.",
                    "One of my little friends went missing in the forest...",
                    "A small creature, very friendly. I'm so worried!",
                    "Could you find them for me? They're somewhere in the Dark Forest.",
                ],
                "default_choices": ["I'll find them!", "Not now..."],
                "quest_active": [
                    "Please look for my little friend in the forest!",
                    "They should be somewhere in the eastern part.",
                ],
                "quest_done": [
                    "You found a companion! I'm so happy!",
                    "Take good care of them. They'll be a loyal friend!",
                ],
            },
        },
    ],
}

# Dungeon: 20 columns x 15 rows
# Tile types: 9=SPIKES, 10=PIT
# fmt: off
DUNGEON = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 5, 5, 5, 5, 5, 9, 5, 5, 5, 5, 5, 5, 9, 5, 5, 5, 5, 5, 1],
    [1, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 1],
    [1, 5, 5, 1, 1, 5, 5, 5,10, 5, 5,10, 5, 5, 5, 1, 1, 5, 5, 1],
    [1, 5, 5, 1, 1, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 1, 1, 5, 5, 1],
    [1, 5, 5, 5, 5, 5, 5, 5, 5, 9, 9, 5, 5, 5, 5, 5, 5, 5, 5, 1],
    [1, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 1],
    [6, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 1],
    [1, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 1],
    [1, 5, 5, 5, 5, 5, 5, 5, 5, 9, 9, 5, 5, 5, 5, 5, 5, 5, 5, 1],
    [1, 5, 5, 1, 1, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 1, 1, 5, 5, 1],
    [1, 5, 5, 1, 1, 5, 5, 5,10, 5, 5,10, 5, 5, 5, 1, 1, 5, 5, 1],
    [1, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 1],
    [1, 5, 5, 5, 5, 5, 9, 5, 5, 5, 5, 5, 5, 9, 5, 5, 5, 5, 5, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]
# fmt: on

DUNGEON_SPAWNS = {
    "player": (1, 7),
    "enemies": [
        {"x": 5, "y": 3, "patrol": [(5, 3), (8, 3)]},
        {"x": 14, "y": 11, "patrol": [(12, 11), (16, 11)]},
        {"x": 10, "y": 6, "type": "archer", "patrol": []},
    ],
    "boss": {"x": 15, "y": 7},
    "items": [
        {"x": 10, "y": 1, "type": "heart"},
    ],
    "chests": [
        {"x": 3, "y": 12, "contents": "heart"},
    ],
    "signs": [
        {"x": 5, "y": 7, "text": "The dark lord awaits beyond the gate..."},
    ],
}

# Dungeon 2 (Ice Temple): 20 columns x 15 rows
# fmt: off
DUNGEON2 = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 1],
    [1, 5, 5, 9, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 9, 5, 5, 1],
    [1, 5, 5, 5, 5, 5, 3, 3, 5, 5, 5, 5, 3, 3, 5, 5, 5, 5, 5, 1],
    [1, 5, 5, 5, 5, 5, 3, 3, 5, 5, 5, 5, 3, 3, 5, 5, 5, 5, 5, 1],
    [1, 5, 5, 5, 5, 5, 5, 5, 5,10,10, 5, 5, 5, 5, 5, 5, 5, 5, 1],
    [1, 5, 5, 5, 5, 5, 5, 5, 5,10,10, 5, 5, 5, 5, 5, 5, 5, 5, 1],
    [6, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 1],
    [1, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 1],
    [1, 5, 5, 5, 5, 5, 5, 5, 5,10,10, 5, 5, 5, 5, 5, 5, 5, 5, 1],
    [1, 5, 5, 5, 5, 5, 3, 3, 5, 5, 5, 5, 3, 3, 5, 5, 5, 5, 5, 1],
    [1, 5, 5, 5, 5, 5, 3, 3, 5, 5, 5, 5, 3, 3, 5, 5, 5, 5, 5, 1],
    [1, 5, 5, 9, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 9, 5, 5, 1],
    [1, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]
# fmt: on

DUNGEON2_SPAWNS = {
    "player": (1, 7),
    "enemies": [
        {"x": 3, "y": 3, "patrol": [(3, 3), (5, 3)]},
        {"x": 15, "y": 11, "patrol": [(13, 11), (17, 11)]},
        {"x": 10, "y": 2, "type": "archer", "patrol": []},
        {"x": 10, "y": 12, "type": "archer", "patrol": []},
    ],
    "boss": {"x": 15, "y": 7},
    "items": [
        {"x": 5, "y": 7, "type": "heart"},
        {"x": 10, "y": 1, "type": "key"},
    ],
    "chests": [
        {"x": 3, "y": 12, "contents": "heart"},
    ],
    "signs": [
        {"x": 4, "y": 7, "text": "The ice demon guards this frozen sanctum!"},
    ],
}

# Forest: 30 columns x 20 rows
# fmt: off
FOREST_MAP = [
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,12,12,12,12, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [2,16,16,16,16, 2,16,16,16,16,16,16, 2,16,16,16,16, 2,16,16,16,16,16, 2,16,16,16,16,16, 2],
    [2,16,16,16,16, 2,16,16,16,16,16,16, 2,16,16,16,16, 2,16,16,16,16,16, 2,16,16,16,16,16, 2],
    [2,16,16,16,16,16,16,16, 2, 2, 2,16,16,16,16,16,16,16,16, 2, 2,16,16,16,16,16, 2, 2, 2, 2],
    [2,16,16,16,16,16,16,16, 2,16,16,16,16,16,16, 2, 2,16,16,16,16,16,16,16,16,16, 2,16,16, 2],
    [2, 2,16,16,16,16,16,16,16,16,16,16,16,16,16,16, 2,16,16,16,16,16,16,16,16,16,16,16,16, 2],
    [2,16,16,16,16, 2,16,16,16,16, 2, 2,16,16,16,16,16,16,16, 2,16,16,16,16, 2, 2,16,16,16, 2],
    [2,16,16,16,16, 2,16,16,16,16, 2,16,16,16,16,16,16,16,16, 2,16,16,16,16,16,16,16,16,16, 2],
    [15,16,16,16,16,16,16,16,16,16,16,16,16,16,16, 2,16,16,16,16,16,16,16, 2, 2,16,16,16,16, 2],
    [15,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16, 7,16,16,16,16, 2],
    [15,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16, 2, 2,16,16,16,16, 2],
    [15,16,16,16,16,16,16,16,16,16,16,16,16,16,16, 2,16,16,16, 2,16,16,16,16,16,16,16,16,16, 2],
    [15,16,16,16,16, 2,16,16,16,16, 2,16,16,16,16,16,16,16,16, 2,16,16,16,16,16,16,16,16,16, 2],
    [2,16,16,16,16, 2,16,16,16,16, 2, 2,16,16,16,16,16,16,16,16,16,16,16, 2,16,16,16,16,16, 2],
    [2, 2,16,16,16,16,16,16,16,16,16,16,16,16,16, 2, 2,16,16,16,16,16,16,16,16,16,16,16,16, 2],
    [2,16,16,16,16,16,16,16, 2,16,16,16,16,16,16,16, 2,16,16,16,16,16,16,16,16,16, 2,16,16, 2],
    [2,16,16,16,16,16,16,16, 2, 2, 2,16,16,16,16,16,16,16,16, 2, 2,16,16,16,16,16,16,16,16, 2],
    [2,16,16,16,16, 2,16,16,16,16,16,16, 2,16,16,16,16, 2,16,16,16,16,16, 2,16,16,16,16,16, 2],
    [2,16,16,16,16, 2,16,16,16,16,16,16, 2,16,16,16,16, 2,16,16,16,16,16, 2,16,16,16,16,16, 2],
    [2, 2, 2, 2, 2, 2,13,13,13,13,13, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
]
# fmt: on

FOREST_SPAWNS = {
    "player": (3, 3),
    "enemies": [
        {"x": 8, "y": 5, "type": "shadow_stalker"},
        {"x": 15, "y": 8, "type": "shadow_stalker"},
        {"x": 22, "y": 4, "type": "shadow_stalker"},
        {"x": 10, "y": 12, "type": "shadow_stalker"},
        {"x": 6, "y": 9, "type": "vine_snapper"},
        {"x": 18, "y": 14, "type": "vine_snapper"},
        {"x": 25, "y": 7, "type": "vine_snapper"},
        {"x": 12, "y": 3, "patrol": [(12, 3), (16, 3)]},  # regular goblin
        {"x": 20, "y": 15, "patrol": [(18, 15), (24, 15)]},  # regular goblin
    ],
    "items": [
        {"x": 12, "y": 8, "type": "heart"},
        {"x": 20, "y": 15, "type": "key"},
    ],
    "chests": [
        {"x": 15, "y": 5, "contents": "heart"},
        {"x": 5, "y": 17, "contents": "key"},
    ],
    "signs": [
        {"x": 5, "y": 9, "text": "Welcome to the Dark Forest. Tread carefully..."},
        {"x": 22, "y": 9, "text": "The forest dungeon lies ahead."},
    ],
    "npcs": [
        {
            "x": 3, "y": 9, "name": "Hermit Sylva", "variant": "villager",
            "quest_id": "story_2",
            "dialogue": {
                "default": [
                    "I am Sylva, hermit of the forest.",
                    "The corruption here is unnatural...",
                    "A dark guardian has taken root deep within.",
                    "Enter the dungeon and cleanse this place!",
                ],
                "default_choices": ["I'll do it!", "Not yet..."],
                "quest_active": [
                    "The Forest Guardian lurks in the dungeon to the east.",
                    "Be careful, young one...",
                ],
                "quest_done": [
                    "You defeated the Forest Guardian! The forest breathes again.",
                    "But I sense a deeper evil stirring in the desert to the south...",
                ],
            },
        },
    ],
    "companion_spawn": {"x": 20, "y": 12},
}

# Desert: 30 columns x 20 rows
# fmt: off
DESERT_MAP = [
    [2, 2, 2, 2, 2, 2,12,12,12,12,12, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [2,17,17,17,17,17,17,17,17,17,17,17,17, 2,17,17,17,17,17, 2,17,17,17,17,17, 2, 2, 2,17, 2],
    [2,17,17,17,17,17,17,17,17,17,17,17,17, 2,17,17,17,17,17, 2,17,17,17,17,17,17,17,17,17, 2],
    [2,17,17, 1, 1, 1,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17, 2],
    [2,17,17, 1,17, 1,17,17, 3, 3,17,17,17,17,17,17, 2, 2,17,17,17,17,17,17,17, 3,17,17,17, 2],
    [2,17,17, 1, 1, 1,17,17,17,17,17,17,17,17,17,17, 2,17,17,17,17,17,17,17,17,17,17,17,17, 2],
    [2,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17, 3,17,17,17,17,17, 7,17, 2],
    [2,17,17,17,17,17,17, 3,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17, 2],
    [2,17,17,17,17,17,17,17,17,17,17,17,17,17,17, 1, 1, 1,17,17,17,17,17,17,17,17,17,17,17,14],
    [2,17,17, 3,17,17,17,17,17,17,17,17,17,17,17, 1,17, 1,17,17,17,17,17,17,17,17,17,17,17,14],
    [2,17,17,17,17,17,17,17,17,17,17,17,17,17,17, 1, 1, 1,17,17,17,17,17,17,17,17,17,17,17,14],
    [2,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17, 3,17,17,17,17,14],
    [2,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,14],
    [2,17,17,17,17,17,17,17,17,17,17, 3, 3,17,17,17,17,17,17,17,17,17, 2, 2,17,17,17,17,17, 2],
    [2,17,17, 1, 1, 1,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17, 2,17,17,17,17,17,17, 2],
    [2,17,17, 1,17, 1,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17, 2],
    [2,17,17, 1, 1, 1,17,17,17,17,17,17,17,17,17, 3,17,17,17,17,17,17,17,17,17,17,17,17,17, 2],
    [2,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17, 2,17,17,17,17,17,17,17, 2],
    [2,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17, 2,17,17,17,17,17,17,17, 2],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
]
# fmt: on

DESERT_SPAWNS = {
    "player": (3, 3),
    "enemies": [
        {"x": 5, "y": 5, "type": "scorpion"},
        {"x": 12, "y": 8, "type": "scorpion"},
        {"x": 20, "y": 4, "type": "scorpion"},
        {"x": 25, "y": 14, "type": "scorpion"},
        {"x": 8, "y": 12, "type": "mummy"},
        {"x": 18, "y": 10, "type": "mummy"},
        {"x": 22, "y": 16, "type": "mummy"},
        {"x": 15, "y": 3, "patrol": [(13, 3), (18, 3)]},
    ],
    "items": [
        {"x": 10, "y": 10, "type": "heart"},
        {"x": 25, "y": 6, "type": "key"},
    ],
    "chests": [
        {"x": 4, "y": 4, "contents": "heart"},
        {"x": 16, "y": 16, "contents": "key"},
    ],
    "signs": [
        {"x": 5, "y": 8, "text": "The scorching desert. Stay hydrated..."},
        {"x": 26, "y": 6, "text": "Ancient ruins hold secrets of the desert dungeon."},
    ],
    "npcs": [
        {
            "x": 4, "y": 4, "name": "Dr. Ankhet", "variant": "merchant",
            "quest_id": "story_3",
            "dialogue": {
                "default": [
                    "Ah, a visitor! I am Dr. Ankhet, archaeologist.",
                    "This desert hides an ancient tomb beneath the sands.",
                    "A terrible Sand Worm guards the seal within.",
                    "If the seal breaks, the volcano to the east will erupt!",
                ],
                "default_choices": ["I'll stop it!", "Tell me more..."],
                "quest_active": [
                    "The tomb entrance is to the east. Find the Sand Worm!",
                    "You'll need a key to enter.",
                ],
                "quest_done": [
                    "The Sand Worm is defeated! But it may be too late...",
                    "The volcano seal is already weakening. You must go east!",
                ],
            },
        },
    ],
}

# Volcano: 30 columns x 20 rows
# fmt: off
VOLCANO_MAP = [
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [2, 5, 5, 5, 5, 5, 5, 5, 2, 5, 5, 5, 5, 5, 5, 5, 2, 5, 5, 5, 5, 5, 5, 5, 5, 2, 2, 2, 5, 2],
    [2, 5, 5, 5, 5, 5, 5, 5, 2, 5, 5, 5, 5, 5, 5, 5, 2, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 2],
    [2, 5, 5,18,18, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 2],
    [2, 5, 5,18,18, 5, 5, 5, 5, 5, 5, 3, 3, 5, 5, 5, 5, 2, 2, 5, 5, 5, 5, 5, 5, 3, 5, 5, 5, 2],
    [2, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 2, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 2],
    [2, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 3, 5, 5, 5, 5, 5, 7, 5, 2],
    [2, 5, 5, 5, 5, 5, 5, 3, 5, 5, 5,18,18,18, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 2],
    [15, 5, 5, 5, 5, 5, 5, 5, 5, 5,18,18,18,18,18, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 2],
    [15, 5, 5, 3, 5, 5, 5, 5, 5, 5,18,18,18,18,18, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 2],
    [15, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,18,18,18, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 2],
    [15, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 3, 5, 5, 5, 5, 2],
    [15, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 2],
    [2, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 3, 3, 5, 5, 5, 5, 5, 5, 5, 5, 5, 2, 2, 5, 5, 5, 5, 5, 2],
    [2, 5, 5,18,18,18, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 2, 5, 5, 5, 5, 5, 5, 2],
    [2, 5, 5,18,18,18, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 2],
    [2, 5, 5,18,18,18, 5, 5, 5, 5, 5, 5, 5, 5, 5, 3, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 2],
    [2, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 2, 5, 5, 5, 5, 5, 5, 5, 2],
    [2, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 2, 5, 5, 5, 5, 5, 5, 5, 2],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
]
# fmt: on

VOLCANO_SPAWNS = {
    "player": (3, 3),
    "enemies": [
        {"x": 5, "y": 5, "type": "fire_imp"},
        {"x": 12, "y": 3, "type": "fire_imp"},
        {"x": 20, "y": 8, "type": "fire_imp"},
        {"x": 25, "y": 15, "type": "fire_imp"},
        {"x": 8, "y": 10, "type": "magma_golem"},
        {"x": 18, "y": 14, "type": "magma_golem"},
        {"x": 22, "y": 5, "type": "magma_golem"},
        {"x": 15, "y": 7, "patrol": [(13, 7), (18, 7)]},
    ],
    "items": [
        {"x": 10, "y": 10, "type": "heart"},
        {"x": 25, "y": 6, "type": "key"},
    ],
    "chests": [
        {"x": 5, "y": 2, "contents": "heart"},
        {"x": 16, "y": 16, "contents": "key"},
    ],
    "signs": [
        {"x": 5, "y": 8, "text": "The volcano's heat is unbearable. Watch out for lava!"},
        {"x": 26, "y": 6, "text": "The final dungeon awaits the brave."},
    ],
    "npcs": [
        {
            "x": 3, "y": 9, "name": "Old Warrior Kael", "variant": "guard",
            "quest_id": "story_5",
            "dialogue": {
                "default": [
                    "I am Kael, the last warrior of Mount Inferno.",
                    "The Inferno Drake has broken free of its prison.",
                    "Only you can restore the seal, young hero.",
                    "Enter the volcano dungeon and end this!",
                ],
                "default_choices": ["For Miloutte!", "I need to prepare..."],
                "quest_active": [
                    "The dungeon entrance lies to the east.",
                    "Face the Inferno Drake and restore the seal!",
                ],
                "quest_done": [
                    "You've done it! The seal is restored!",
                    "The land is saved, hero of Miloutte!",
                ],
            },
        },
    ],
}

# Area registry
AREAS = {
    "overworld": {
        "map": OVERWORLD,
        "spawns": OVERWORLD_SPAWNS,
        "music": "overworld",
        "name": "Miloutte Village",
        "connections": {
            "east": {"area": "forest", "spawn_edge": "west"},
        },
    },
    "forest": {
        "map": FOREST_MAP,
        "spawns": FOREST_SPAWNS,
        "music": "forest",
        "name": "Dark Forest",
        "connections": {
            "west": {"area": "overworld", "spawn_edge": "east"},
            "south": {"area": "desert", "spawn_edge": "north"},
            "north": {"area": "frozen_peaks", "spawn_edge": "south"},
        },
    },
    "desert": {
        "map": DESERT_MAP,
        "spawns": DESERT_SPAWNS,
        "music": "desert",
        "name": "Scorching Desert",
        "connections": {
            "north": {"area": "forest", "spawn_edge": "south"},
            "east": {"area": "volcano", "spawn_edge": "west"},
        },
    },
    "volcano": {
        "map": VOLCANO_MAP,
        "spawns": VOLCANO_SPAWNS,
        "music": "volcano",
        "name": "Mount Inferno",
        "connections": {
            "west": {"area": "desert", "spawn_edge": "east"},
        },
    },
    "frozen_peaks": {
        "map": None,  # set below after FROZEN_PEAKS_MAP is defined
        "spawns": None,
        "music": "frozen_peaks",
        "name": "Frozen Peaks",
        "connections": {
            "south": {"area": "forest", "spawn_edge": "north"},
        },
    },
}

# Forest Dungeon: 20 columns x 15 rows
# fmt: off
FOREST_DUNGEON = [
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [2, 5, 5, 5, 5, 5, 2, 5, 5, 5, 5, 5, 5, 2, 5, 5, 5, 5, 5, 2],
    [2, 5, 5, 5, 5, 5, 2, 5, 5, 9, 5, 5, 5, 2, 5, 5, 5, 5, 5, 2],
    [2, 5, 5, 2, 2, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 2, 2, 5, 5, 2],
    [2, 5, 5, 2, 2, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 2, 2, 5, 5, 2],
    [2, 5, 5, 5, 5, 5, 5, 5, 5, 9, 9, 5, 5, 5, 5, 5, 5, 5, 5, 2],
    [2, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 2],
    [6, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 2],
    [2, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 2],
    [2, 5, 5, 5, 5, 5, 5, 5, 5, 9, 9, 5, 5, 5, 5, 5, 5, 5, 5, 2],
    [2, 5, 5, 2, 2, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 2, 2, 5, 5, 2],
    [2, 5, 5, 2, 2, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 2, 2, 5, 5, 2],
    [2, 5, 5, 5, 5, 5, 2, 5, 5, 5, 5, 5, 5, 2, 5, 5, 5, 5, 5, 2],
    [2, 5, 5, 5, 5, 5, 2, 5, 5, 9, 5, 5, 5, 2, 5, 5, 5, 5, 5, 2],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
]
# fmt: on

FOREST_DUNGEON_SPAWNS = {
    "player": (1, 7),
    "enemies": [
        {"x": 5, "y": 3, "type": "vine_snapper"},
        {"x": 14, "y": 11, "type": "vine_snapper"},
        {"x": 10, "y": 2, "patrol": [(8, 2), (12, 2)]},
        {"x": 10, "y": 12, "patrol": [(8, 12), (12, 12)]},
    ],
    "boss": {"x": 15, "y": 7},
    "items": [
        {"x": 10, "y": 1, "type": "heart"},
        {"x": 3, "y": 7, "type": "key"},
    ],
    "chests": [
        {"x": 3, "y": 3, "contents": "heart"},
        {"x": 3, "y": 11, "contents": "key"},
    ],
    "signs": [
        {"x": 4, "y": 7, "text": "The Forest Guardian protects these ancient woods..."},
        {"x": 10, "y": 7, "text": "Beware its roots and summoned vines!"},
    ],
}

# Desert Dungeon: 20 columns x 15 rows
# fmt: off
DESERT_DUNGEON = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 5, 5, 5, 5, 5, 1, 5, 5, 5, 5, 5, 5, 1, 5, 5, 5, 5, 5, 1],
    [1, 5, 5, 5, 5, 5, 1, 5, 5, 9, 5, 5, 5, 1, 5, 5, 5, 5, 5, 1],
    [1, 5, 5, 1, 1, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 1, 1, 5, 5, 1],
    [1, 5, 5, 1, 1, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 1, 1, 5, 5, 1],
    [1, 5, 5, 5, 5, 5, 5, 5, 5, 9, 9, 5, 5, 5, 5, 5, 5, 5, 5, 1],
    [1, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 1],
    [6, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 1],
    [1, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 1],
    [1, 5, 5, 5, 5, 5, 5, 5, 5, 9, 9, 5, 5, 5, 5, 5, 5, 5, 5, 1],
    [1, 5, 5, 1, 1, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 1, 1, 5, 5, 1],
    [1, 5, 5, 1, 1, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 1, 1, 5, 5, 1],
    [1, 5, 5, 5, 5, 5, 1, 5, 5, 5, 5, 5, 5, 1, 5, 5, 5, 5, 5, 1],
    [1, 5, 5, 5, 5, 5, 1, 5, 5, 9, 5, 5, 5, 1, 5, 5, 5, 5, 5, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]
# fmt: on

DESERT_DUNGEON_SPAWNS = {
    "player": (1, 7),
    "enemies": [
        {"x": 5, "y": 3, "type": "scorpion"},
        {"x": 14, "y": 11, "type": "scorpion"},
        {"x": 10, "y": 2, "type": "mummy"},
        {"x": 10, "y": 12, "patrol": [(8, 12), (12, 12)]},
    ],
    "boss": {"x": 15, "y": 7},
    "items": [
        {"x": 10, "y": 1, "type": "heart"},
        {"x": 3, "y": 7, "type": "key"},
    ],
    "chests": [
        {"x": 3, "y": 3, "contents": "heart"},
        {"x": 3, "y": 11, "contents": "key"},
    ],
    "signs": [
        {"x": 4, "y": 7, "text": "The Sand Worm lurks beneath the desert floor..."},
        {"x": 10, "y": 7, "text": "Strike when it surfaces!"},
    ],
}

# Volcano Dungeon: 20 columns x 15 rows
# fmt: off
VOLCANO_DUNGEON = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 1],
    [1, 5, 5, 5, 5, 5, 5, 5, 5,18,18, 5, 5, 5, 5, 5, 5, 5, 5, 1],
    [1, 5, 5, 1, 1, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 1, 1, 5, 5, 1],
    [1, 5, 5, 1, 1, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 1, 1, 5, 5, 1],
    [1, 5, 5, 5, 5, 5, 5, 5, 5,18,18, 5, 5, 5, 5, 5, 5, 5, 5, 1],
    [1, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 1],
    [6, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 1],
    [1, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 1],
    [1, 5, 5, 5, 5, 5, 5, 5, 5,18,18, 5, 5, 5, 5, 5, 5, 5, 5, 1],
    [1, 5, 5, 1, 1, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 1, 1, 5, 5, 1],
    [1, 5, 5, 1, 1, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 1, 1, 5, 5, 1],
    [1, 5, 5, 5, 5, 5, 5, 5, 5,18,18, 5, 5, 5, 5, 5, 5, 5, 5, 1],
    [1, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]
# fmt: on

VOLCANO_DUNGEON_SPAWNS = {
    "player": (1, 7),
    "enemies": [
        {"x": 5, "y": 3, "type": "fire_imp"},
        {"x": 14, "y": 11, "type": "fire_imp"},
        {"x": 10, "y": 2, "type": "fire_imp"},
        {"x": 10, "y": 12, "patrol": [(8, 12), (12, 12)]},
    ],
    "boss": {"x": 15, "y": 7},
    "items": [
        {"x": 10, "y": 1, "type": "heart"},
        {"x": 3, "y": 7, "type": "key"},
    ],
    "chests": [
        {"x": 3, "y": 3, "contents": "heart"},
        {"x": 3, "y": 11, "contents": "key"},
    ],
    "signs": [
        {"x": 4, "y": 7, "text": "The Inferno Drake guards the volcano's heart..."},
        {"x": 10, "y": 7, "text": "Face the final trial!"},
    ],
}

# Frozen Peaks: 30 columns x 20 rows
# 22=ICE, 23=CRACKED_ICE, 24=FROZEN_WALL, 25=SNOW
# fmt: off
FROZEN_PEAKS_MAP = [
    [24,24,24,24,24,24,24,24,24,24,24,24,24,24,24,24,24,24,24,24,24,24,24,24,24,24,24,24,24,24],
    [24,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,24],
    [24,25,25,25,25,25,24,25,25,25,25,25,25,24,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,24],
    [24,25,25,25,25,25,25,25,22,22,22,25,25,25,25,25,25,24,24,25,25,25,25,25,25, 3,25,25,25,24],
    [24,25,25,24,24,25,25,25,22,22,22,25,25,25,25,25,25,24,25,25,25,25,25,25,25,25,25,25,25,24],
    [24,25,25,24,24,25,25,25,22,22,22,25,25,25,25,25,25,25,25,25,25, 3,25,25,25,25,25, 7,25,24],
    [24,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,24],
    [24,25,25,25,25,25,25, 3,25,25,25,25,25,25,25,24,24,25,25,25,25,25,25,25,25,25,25,25,25,24],
    [24,25,25,25,25,25,25,25,25,23,23,25,25,25,25,24,25,25,25,25,25,25,22,22,22,25,25,25,25,24],
    [24,25,25, 3,25,25,25,25,25,23,23,25,25,25,25,25,25,25,25,25,25,25,22,22,22,25,25,25,25,24],
    [24,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,22,22,22,25,25,25,25,24],
    [24,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,24],
    [24,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25, 3,25,25,25,25,24],
    [24,25,25,25,25,25,24,24,25,25,25,25,25,25,25,25,25,25,25,25,25,24,24,25,25,25,25,25,25,24],
    [24,25,25,24,24,25,24,25,25,25,25,25,25,25,25,25,25,25,25,25,25,24,25,25,25,25,25,25,25,24],
    [24,25,25,24,24,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,24],
    [24,25,25,25,25,25,25,25,25,25,25,25, 3,25,25,25,25,25,25,25,25,25,25,25,25,24,25,25,25,24],
    [24,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,24,25,25,25,24],
    [24,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,24],
    [24,24,24,24,24,24,24,24,24,24,24,24,24,13,13,13,13,24,24,24,24,24,24,24,24,24,24,24,24,24],
]
# fmt: on

FROZEN_PEAKS_SPAWNS = {
    "player": (3, 3),
    "enemies": [
        {"x": 5, "y": 5, "type": "ice_wraith"},
        {"x": 12, "y": 8, "type": "ice_wraith"},
        {"x": 20, "y": 4, "type": "ice_wraith"},
        {"x": 25, "y": 12, "type": "ice_wraith"},
        {"x": 8, "y": 12, "type": "frost_golem"},
        {"x": 18, "y": 10, "type": "frost_golem"},
        {"x": 22, "y": 16, "type": "frost_golem"},
        {"x": 15, "y": 3, "patrol": [(13, 3), (18, 3)]},
    ],
    "items": [
        {"x": 10, "y": 10, "type": "heart"},
        {"x": 25, "y": 5, "type": "key"},
    ],
    "chests": [
        {"x": 4, "y": 4, "contents": "heart"},
        {"x": 16, "y": 16, "contents": "key"},
    ],
    "signs": [
        {"x": 5, "y": 8, "text": "The Frozen Peaks. Ice clings to every surface..."},
        {"x": 26, "y": 5, "text": "A hidden cavern lies somewhere in this frozen wasteland."},
    ],
    "npcs": [
        {
            "x": 4, "y": 14, "name": "Frost Hermit", "variant": "elder",
            "quest_id": "story_7",
            "dialogue": {
                "default": [
                    "Brrr... you've made it to the Frozen Peaks, hero.",
                    "I am the Frost Hermit, last keeper of the ice.",
                    "A Crystal Dragon has awakened deep in the Ice Cavern.",
                    "It guards a secret fourth seal, one lost to legend.",
                    "You must enter the cavern and stop it!",
                ],
                "default_choices": ["I'll face it!", "Tell me more..."],
                "quest_active": [
                    "The Ice Cavern entrance is to the east.",
                    "Beware the ice tiles... they are treacherous.",
                ],
                "quest_done": [
                    "The Crystal Dragon is defeated! All four seals are restored!",
                    "You are truly the hero of legend, Miloutte!",
                ],
            },
        },
    ],
}

# Ice Cavern Dungeon: 20 columns x 15 rows
# Uses ICE(22), CRACKED_ICE(23), FROZEN_WALL(24) tiles
# fmt: off
ICE_CAVERN = [
    [24,24,24,24,24,24,24,24,24,24,24,24,24,24,24,24,24,24,24,24],
    [24,22,22,22,22,22,24,22,22,22,22,22,22,24,22,22,22,22,22,24],
    [24,22,22,23,22,22,24,22,22,22,22,22,22,24,22,22,22,23,22,24],
    [24,22,22,22,22,22,22,22,22,24,24,22,22,22,22,24,24,22,22,24],
    [24,22,22,24,24,22,22,22,22,22,22,22,22,22,22,24,24,22,22,24],
    [24,22,22,22,22,22,22,22,22,23,23,22,22,22,22,22,22,22,22,24],
    [24,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,24],
    [ 6,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,24],
    [24,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,24],
    [24,22,22,22,22,22,22,22,22,23,23,22,22,22,22,22,22,22,22,24],
    [24,22,22,24,24,22,22,22,22,22,22,22,22,22,22,24,24,22,22,24],
    [24,22,22,22,22,22,22,22,22,24,24,22,22,22,22,22,22,22,22,24],
    [24,22,22,23,22,22,24,22,22,22,22,22,22,24,22,22,22,23,22,24],
    [24,22,22,22,22,22,24,22,22,22,22,22,22,24,22,22,22,22,22,24],
    [24,24,24,24,24,24,24,24,24,24,24,24,24,24,24,24,24,24,24,24],
]
# fmt: on

ICE_CAVERN_SPAWNS = {
    "player": (1, 7),
    "enemies": [
        {"x": 5, "y": 3, "type": "ice_wraith"},
        {"x": 14, "y": 11, "type": "ice_wraith"},
        {"x": 10, "y": 2, "type": "frost_golem"},
        {"x": 10, "y": 12, "patrol": [(8, 12), (12, 12)]},
    ],
    "boss": {"x": 15, "y": 7},
    "items": [
        {"x": 10, "y": 1, "type": "heart"},
        {"x": 3, "y": 7, "type": "key"},
    ],
    "chests": [
        {"x": 3, "y": 3, "contents": "heart"},
        {"x": 3, "y": 11, "contents": "key"},
    ],
    "signs": [
        {"x": 4, "y": 7, "text": "The Crystal Dragon slumbers in the frozen depths..."},
        {"x": 10, "y": 7, "text": "Beware the cracking ice beneath your feet!"},
    ],
}

# Patch AREAS with frozen_peaks data (defined after the map constant)
AREAS["frozen_peaks"]["map"] = FROZEN_PEAKS_MAP
AREAS["frozen_peaks"]["spawns"] = FROZEN_PEAKS_SPAWNS
