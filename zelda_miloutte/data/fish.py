"""Fish data for the fishing minigame.

Each fish has: name, area, rarity, difficulty (0-1), heal_value, sell_price, sprite_id.
Difficulty affects reel minigame: smaller sweet spot, faster bar movement.
"""


class FishData:
    """Definition of a single fish species."""

    def __init__(self, fish_id, name, area, rarity, difficulty,
                 heal_value, sell_price, sprite_id=None):
        self.fish_id = fish_id
        self.name = name
        self.area = area          # area_id where this fish can be caught
        self.rarity = rarity      # "common", "uncommon", "rare"
        self.difficulty = difficulty  # 0.0 (easy) to 1.0 (very hard)
        self.heal_value = heal_value
        self.sell_price = sell_price
        self.sprite_id = sprite_id or fish_id

    @property
    def rarity_weight(self):
        """Weight for random selection — common fish appear more often."""
        return {
            "common": 60,
            "uncommon": 30,
            "rare": 10,
        }.get(self.rarity, 60)


# ── Master fish registry ──────────────────────────────────────────

FISH = {}


def _register(fish_id, name, area, rarity, difficulty, heal_value, sell_price):
    fish = FishData(fish_id, name, area, rarity, difficulty, heal_value, sell_price)
    FISH[fish_id] = fish
    return fish


# ── Village / Overworld ───────────────────────────────────────────
_register("bass",        "Bass",         "overworld", "common",   0.2, 2,  5)
_register("trout",       "Trout",        "overworld", "common",   0.25, 2, 6)
_register("golden_carp", "Golden Carp",  "overworld", "rare",     0.7, 4,  30)

# ── Forest ────────────────────────────────────────────────────────
_register("mossy_pike",  "Mossy Pike",   "forest",    "common",   0.3, 2,  8)
_register("magic_carp",  "Magic Carp",   "forest",    "rare",     0.75, 6, 35)

# ── Desert ────────────────────────────────────────────────────────
_register("sand_eel",    "Sand Eel",     "desert",    "common",   0.35, 2,  10)
_register("oasis_perch", "Oasis Perch",  "desert",    "uncommon", 0.5, 3,  18)
_register("ancient_fish","Ancient Fish", "desert",    "rare",     0.8, 6,  45)

# ── Volcano ───────────────────────────────────────────────────────
_register("lava_trout",  "Lava Trout",   "volcano",   "uncommon", 0.55, 3, 22)
_register("magma_fish",  "Magma Fish",   "volcano",   "rare",     0.85, 8, 50)


def get_fish(fish_id):
    """Look up a fish by ID."""
    return FISH.get(fish_id)


def get_fish_for_area(area_id):
    """Return list of FishData available in the given area."""
    return [f for f in FISH.values() if f.area == area_id]


def pick_random_fish(area_id):
    """Weighted random selection of a fish for the given area.

    Returns FishData or None if no fish exist in that area.
    """
    import random
    candidates = get_fish_for_area(area_id)
    if not candidates:
        return None
    weights = [f.rarity_weight for f in candidates]
    return random.choices(candidates, weights=weights, k=1)[0]
