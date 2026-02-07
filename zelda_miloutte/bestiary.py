"""Bestiary (monster encyclopedia) that auto-fills when enemies are encountered."""


# All enemy/boss type definitions for the bestiary
BESTIARY_DEFS = {
    # Regular enemies (9 types)
    "Enemy": {
        "name": "Goblin",
        "lore": "A common creature corrupted by dark magic. They patrol in small groups and chase anything that moves.",
        "hp": 2,
        "attack": 1,
        "is_boss": False,
    },
    "Archer": {
        "name": "Goblin Archer",
        "lore": "A cunning goblin that keeps its distance and fires arrows. It flees when cornered.",
        "hp": 2,
        "attack": 1,
        "is_boss": False,
    },
    "ShadowStalker": {
        "name": "Shadow Stalker",
        "lore": "A wraith-like entity that can teleport short distances. It strikes from the shadows without warning.",
        "hp": 3,
        "attack": 1,
        "is_boss": False,
    },
    "VineSnapper": {
        "name": "Vine Snapper",
        "lore": "A carnivorous plant corrupted by forest magic. It roots itself in place and spits thorns at prey.",
        "hp": 2,
        "attack": 1,
        "is_boss": False,
    },
    "Scorpion": {
        "name": "Scorpion",
        "lore": "A large desert scorpion with a venomous stinger. It is swift and relentless in pursuit.",
        "hp": 3,
        "attack": 1,
        "is_boss": False,
    },
    "Mummy": {
        "name": "Mummy",
        "lore": "An ancient guardian wrapped in cursed bandages. Slow but extremely durable and hits hard.",
        "hp": 6,
        "attack": 2,
        "is_boss": False,
    },
    "FireImp": {
        "name": "Fire Imp",
        "lore": "A small demon wreathed in flame. It darts around leaving burning trails on the ground.",
        "hp": 4,
        "attack": 2,
        "is_boss": False,
    },
    "MagmaGolem": {
        "name": "Magma Golem",
        "lore": "A hulking construct of molten rock. It lumbers slowly but hurls fireballs from afar.",
        "hp": 8,
        "attack": 3,
        "is_boss": False,
    },
    "IceWraith": {
        "name": "Ice Wraith",
        "lore": "A spectral being of frozen mist. It can phase through attacks and freezes the air around it.",
        "hp": 3,
        "attack": 1,
        "is_boss": False,
    },
    # Bosses (4 types)
    "Boss": {
        "name": "Dark Lord",
        "lore": "The corrupted overlord dwelling beneath the village. In phase two, it charges with devastating force.",
        "hp": 6,
        "attack": 2,
        "is_boss": True,
        "phases": "Phase 1: Pursues relentlessly. Phase 2: Charges at high speed when HP drops below half.",
    },
    "ForestGuardian": {
        "name": "Forest Guardian",
        "lore": "Once a noble protector of the woods, now twisted by corruption. It summons vine snappers to aid it.",
        "hp": 10,
        "attack": 2,
        "is_boss": True,
        "phases": "Phase 1: Melee attacks with root slams. Phase 2: Summons vine snappers and becomes more aggressive.",
    },
    "SandWorm": {
        "name": "Sand Worm",
        "lore": "A colossal worm that burrows beneath the desert sands. It is invulnerable while underground.",
        "hp": 12,
        "attack": 2,
        "is_boss": True,
        "phases": "Phase 1: Surfaces to attack, then burrows. Phase 2: More frequent emergence with devastating slam attacks.",
    },
    "InfernoDrake": {
        "name": "Inferno Drake",
        "lore": "An ancient dragon of fire that guards the volcano seal. Its breath can melt stone and its meteors rain destruction.",
        "hp": 16,
        "attack": 3,
        "is_boss": True,
        "phases": "Phase 1: Fire breath and melee charges. Phase 2: Summons meteor strikes across the arena.",
    },
}

# Total unique creature types
TOTAL_CREATURES = len(BESTIARY_DEFS)


class BestiaryEntry:
    """A single bestiary entry for one creature type."""

    def __init__(self, type_id, data):
        self.type_id = type_id
        self.name = data["name"]
        self.lore = data["lore"]
        self.hp = data["hp"]
        self.attack = data["attack"]
        self.is_boss = data["is_boss"]
        self.phases = data.get("phases", "")
        self.discovered = False
        self.kill_count = 0


class BestiaryManager:
    """Manages bestiary entries and discovery state."""

    def __init__(self):
        self.entries = {}
        for type_id, data in BESTIARY_DEFS.items():
            self.entries[type_id] = BestiaryEntry(type_id, data)

    def discover(self, enemy_class_name):
        """Mark an enemy type as discovered. Called on first encounter."""
        entry = self.entries.get(enemy_class_name)
        if entry and not entry.discovered:
            entry.discovered = True
            return True
        return False

    def record_kill(self, enemy_class_name):
        """Increment kill count for an enemy type."""
        entry = self.entries.get(enemy_class_name)
        if entry:
            entry.kill_count += 1

    def get_discovered_count(self):
        """Return number of discovered entries."""
        return sum(1 for e in self.entries.values() if e.discovered)

    def get_total_count(self):
        """Return total entries."""
        return len(self.entries)

    def get_ordered_entries(self):
        """Return entries in display order: regular enemies first, then bosses."""
        regulars = [e for e in self.entries.values() if not e.is_boss]
        bosses = [e for e in self.entries.values() if e.is_boss]
        return regulars + bosses

    # ── Serialization ────────────────────────────────────────────────

    def to_dict(self):
        """Serialize for saving."""
        result = {}
        for type_id, entry in self.entries.items():
            result[type_id] = {
                "discovered": entry.discovered,
                "kill_count": entry.kill_count,
            }
        return result

    def from_dict(self, data):
        """Restore from save data."""
        if data is None:
            return
        for type_id, edata in data.items():
            entry = self.entries.get(type_id)
            if entry:
                entry.discovered = edata.get("discovered", False)
                entry.kill_count = edata.get("kill_count", 0)
