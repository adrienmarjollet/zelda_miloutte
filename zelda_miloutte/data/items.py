"""Item definitions for the inventory system.

Each item is defined as a dict with:
  - name: Display name
  - description: Short description text
  - item_type: "equipment" or "consumable"
  - equip_slot: For equipment: "weapon", "shield", "ring", "boots"
  - icon_id: String key for sprite lookup
  - stats: Dict of stat modifiers (attack, defense, speed, burn, etc.)
  - tier: "starter", "mid", "endgame" — for drop table weighting
  - effect: For consumables — dict describing the effect
"""

# ── Equipment items ──────────────────────────────────────────────

WOODEN_SWORD = {
    "id": "wooden_sword",
    "name": "Wooden Sword",
    "description": "A basic training sword.",
    "item_type": "equipment",
    "equip_slot": "weapon",
    "icon_id": "wooden_sword",
    "stats": {"attack": 1},
    "tier": "starter",
}

IRON_SWORD = {
    "id": "iron_sword",
    "name": "Iron Sword",
    "description": "A sturdy iron blade. +3 ATK",
    "item_type": "equipment",
    "equip_slot": "weapon",
    "icon_id": "iron_sword",
    "stats": {"attack": 3},
    "tier": "mid",
}

FLAME_BLADE = {
    "id": "flame_blade",
    "name": "Flame Blade",
    "description": "Burns foes on hit. +4 ATK",
    "item_type": "equipment",
    "equip_slot": "weapon",
    "icon_id": "flame_blade",
    "stats": {"attack": 4, "burn": True},
    "tier": "endgame",
}

WOODEN_SHIELD = {
    "id": "wooden_shield",
    "name": "Wooden Shield",
    "description": "A light wooden buckler. +1 DEF",
    "item_type": "equipment",
    "equip_slot": "shield",
    "icon_id": "wooden_shield",
    "stats": {"defense": 1},
    "tier": "starter",
}

GUARDIAN_SHIELD = {
    "id": "guardian_shield",
    "name": "Guardian Shield",
    "description": "Forged by the ancients. +2 DEF",
    "item_type": "equipment",
    "equip_slot": "shield",
    "icon_id": "guardian_shield",
    "stats": {"defense": 2},
    "tier": "mid",
}

MIRROR_SHIELD = {
    "id": "mirror_shield",
    "name": "Mirror Shield",
    "description": "Reflects weak projectiles. +3 DEF",
    "item_type": "equipment",
    "equip_slot": "shield",
    "icon_id": "mirror_shield",
    "stats": {"defense": 3},
    "tier": "endgame",
}

POWER_RING = {
    "id": "power_ring",
    "name": "Power Ring",
    "description": "Channels raw strength. +2 ATK",
    "item_type": "equipment",
    "equip_slot": "ring",
    "icon_id": "power_ring",
    "stats": {"attack": 2},
    "tier": "mid",
}

FIRE_RING = {
    "id": "fire_ring",
    "name": "Fire Ring",
    "description": "Burns enemies on contact.",
    "item_type": "equipment",
    "equip_slot": "ring",
    "icon_id": "fire_ring",
    "stats": {"attack": 1, "burn": True},
    "tier": "mid",
}

SAGE_RING = {
    "id": "sage_ring",
    "name": "Sage Ring",
    "description": "Wise enchantment. +1 ATK +1 DEF",
    "item_type": "equipment",
    "equip_slot": "ring",
    "icon_id": "sage_ring",
    "stats": {"attack": 1, "defense": 1},
    "tier": "endgame",
}

LEATHER_BOOTS = {
    "id": "leather_boots",
    "name": "Leather Boots",
    "description": "Light and flexible. +15 SPD",
    "item_type": "equipment",
    "equip_slot": "boots",
    "icon_id": "leather_boots",
    "stats": {"speed": 15},
    "tier": "starter",
}

SWIFT_BOOTS = {
    "id": "swift_boots",
    "name": "Swift Boots",
    "description": "Wind-enchanted boots. +30 SPD",
    "item_type": "equipment",
    "equip_slot": "boots",
    "icon_id": "swift_boots",
    "stats": {"speed": 30},
    "tier": "mid",
}

WINGED_BOOTS = {
    "id": "winged_boots",
    "name": "Winged Boots",
    "description": "Almost like flying. +50 SPD",
    "item_type": "equipment",
    "equip_slot": "boots",
    "icon_id": "winged_boots",
    "stats": {"speed": 50},
    "tier": "endgame",
}

# ── Consumable items ─────────────────────────────────────────────

POTION = {
    "id": "potion",
    "name": "Potion",
    "description": "Restores 5 HP.",
    "item_type": "consumable",
    "icon_id": "potion",
    "stats": {},
    "tier": "starter",
    "effect": {"type": "heal", "amount": 5},
}

ELIXIR = {
    "id": "elixir",
    "name": "Elixir",
    "description": "Fully restores HP.",
    "item_type": "consumable",
    "icon_id": "elixir",
    "stats": {},
    "tier": "endgame",
    "effect": {"type": "full_heal"},
}

ANTIDOTE = {
    "id": "antidote",
    "name": "Antidote",
    "description": "Cures poison.",
    "item_type": "consumable",
    "icon_id": "antidote",
    "stats": {},
    "tier": "starter",
    "effect": {"type": "cure_poison"},
}

BOMB = {
    "id": "bomb",
    "name": "Bomb",
    "description": "Explodes for AoE damage.",
    "item_type": "consumable",
    "icon_id": "bomb",
    "stats": {},
    "tier": "mid",
    "effect": {"type": "bomb", "damage": 3, "radius": 64},
}

# ── Lookup tables ────────────────────────────────────────────────

ALL_ITEMS = {
    "wooden_sword": WOODEN_SWORD,
    "iron_sword": IRON_SWORD,
    "flame_blade": FLAME_BLADE,
    "wooden_shield": WOODEN_SHIELD,
    "guardian_shield": GUARDIAN_SHIELD,
    "mirror_shield": MIRROR_SHIELD,
    "power_ring": POWER_RING,
    "fire_ring": FIRE_RING,
    "sage_ring": SAGE_RING,
    "leather_boots": LEATHER_BOOTS,
    "swift_boots": SWIFT_BOOTS,
    "winged_boots": WINGED_BOOTS,
    "potion": POTION,
    "elixir": ELIXIR,
    "antidote": ANTIDOTE,
    "bomb": BOMB,
}

# Items that enemies can drop (weighted by tier)
ENEMY_DROP_TABLE = {
    "starter": [("potion", 5), ("antidote", 2), ("wooden_sword", 1), ("leather_boots", 1)],
    "mid": [("potion", 4), ("bomb", 3), ("iron_sword", 1), ("guardian_shield", 1),
            ("power_ring", 1), ("swift_boots", 1), ("fire_ring", 1)],
    "endgame": [("elixir", 3), ("bomb", 3), ("flame_blade", 1), ("mirror_shield", 1),
                ("sage_ring", 1), ("winged_boots", 1)],
}

# Chest loot by tier
CHEST_LOOT_TABLE = {
    "starter": ["wooden_sword", "wooden_shield", "leather_boots", "potion"],
    "mid": ["iron_sword", "guardian_shield", "swift_boots", "power_ring", "fire_ring", "bomb"],
    "endgame": ["flame_blade", "mirror_shield", "winged_boots", "sage_ring", "elixir"],
}


def get_item_def(item_id):
    """Return the item definition dict for the given item ID, or None."""
    return ALL_ITEMS.get(item_id)
