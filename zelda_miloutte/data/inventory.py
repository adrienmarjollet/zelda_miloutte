"""Inventory system with equipment slots, consumables, and shop support.

Provides:
  - InventoryItem: item definition (template)
  - Inventory: player inventory with stacks + equipment slots
  - Master item registry with get_item()
  - Equipment stat bonuses
"""


# Item categories
CATEGORY_CONSUMABLE = "consumable"
CATEGORY_EQUIPMENT = "equipment"
CATEGORY_KEY_ITEM = "key_item"

# Equipment slot names
EQUIP_SLOTS = ("weapon", "shield", "ring", "boots")

# Maximum inventory stacks
MAX_INVENTORY_SLOTS = 20


class InventoryItem:
    """Represents an item definition (template, not a stack)."""

    def __init__(self, item_id, name, description, category=CATEGORY_CONSUMABLE,
                 buy_price=0, effect=None, icon=None, equip_slot=None,
                 stats=None, tier="starter"):
        """
        Args:
            item_id: Unique string identifier (e.g. "potion")
            name: Display name
            description: Short description shown in shop/inventory
            category: One of CATEGORY_* constants
            buy_price: Base purchase price in gold
            effect: Dict describing the item effect, e.g. {"heal": 4}
            icon: Optional icon identifier for sprite lookup
            equip_slot: For equipment: "weapon", "shield", "ring", "boots"
            stats: Dict of stat modifiers (attack, defense, speed, burn, etc.)
            tier: "starter", "mid", or "endgame"
        """
        self.item_id = item_id
        self.name = name
        self.description = description
        self.category = category
        self.buy_price = buy_price
        self.sell_price = max(1, buy_price // 2)
        self.effect = effect or {}
        self.icon = icon or item_id
        self.equip_slot = equip_slot
        self.stats = stats or {}
        self.tier = tier


# ── Master item registry ─────────────────────────────────────────────────────

ITEMS = {}


def _register(item_id, name, description, category=CATEGORY_CONSUMABLE,
              buy_price=0, effect=None, icon=None, equip_slot=None,
              stats=None, tier="starter"):
    item = InventoryItem(item_id, name, description, category, buy_price,
                         effect, icon, equip_slot, stats, tier)
    ITEMS[item_id] = item
    return item


# ── Consumables ──────────────────────────────────────────────────────────────

_register("potion", "Potion", "Restores 5 HP.",
          buy_price=15, effect={"heal": 5}, tier="starter")
_register("hi_potion", "Hi-Potion", "Restores 8 HP.",
          buy_price=40, effect={"heal": 8}, tier="mid")
_register("antidote", "Antidote", "Cures poison.",
          buy_price=10, effect={"cure": "poison"}, tier="starter")
_register("elixir", "Elixir", "Fully restores HP.",
          buy_price=100, effect={"heal_full": True}, tier="endgame")
_register("fire_ward", "Fire Ward", "Resist fire for 30s.",
          buy_price=30, effect={"resist": "fire", "duration": 30}, tier="mid")
_register("speed_boost", "Speed Tonic", "Move faster for 20s.",
          buy_price=25, effect={"speed": 1.5, "duration": 20}, tier="mid")
_register("bomb", "Bomb", "Explodes for AoE damage.",
          buy_price=20, effect={"bomb": True, "damage": 3, "radius": 64}, tier="mid")

# ── Equipment: Weapons ───────────────────────────────────────────────────────

_register("wooden_sword", "Wooden Sword", "A basic training sword. +1 ATK",
          CATEGORY_EQUIPMENT, buy_price=30, equip_slot="weapon",
          stats={"attack": 1}, tier="starter")
_register("iron_sword", "Iron Sword", "A sturdy iron blade. +3 ATK",
          CATEGORY_EQUIPMENT, buy_price=80, equip_slot="weapon",
          stats={"attack": 3}, tier="mid",
          effect={"attack": 3})
_register("steel_sword", "Steel Sword", "Fine steel. +2 ATK",
          CATEGORY_EQUIPMENT, buy_price=80, equip_slot="weapon",
          stats={"attack": 2}, tier="mid",
          effect={"attack": 2})
_register("flame_blade", "Flame Blade", "Burns foes on hit. +4 ATK",
          CATEGORY_EQUIPMENT, buy_price=200, equip_slot="weapon",
          stats={"attack": 4, "burn": True}, tier="endgame",
          effect={"attack": 4})
_register("inferno_edge", "Inferno Edge", "Volcanic fury. +3 ATK",
          CATEGORY_EQUIPMENT, buy_price=300, equip_slot="weapon",
          stats={"attack": 3}, tier="endgame",
          effect={"attack": 3})

# ── Equipment: Shields ───────────────────────────────────────────────────────

_register("wooden_shield", "Wooden Shield", "A light wooden buckler. +1 DEF",
          CATEGORY_EQUIPMENT, buy_price=25, equip_slot="shield",
          stats={"defense": 1}, tier="starter",
          effect={"defense": 1})
_register("iron_shield", "Iron Shield", "Solid iron protection. +1 DEF",
          CATEGORY_EQUIPMENT, buy_price=60, equip_slot="shield",
          stats={"defense": 1}, tier="mid",
          effect={"defense": 1})
_register("guardian_shield", "Guardian Shield", "Forged by the ancients. +2 DEF",
          CATEGORY_EQUIPMENT, buy_price=120, equip_slot="shield",
          stats={"defense": 2}, tier="mid",
          effect={"defense": 2})
_register("mirror_shield", "Mirror Shield", "Reflects weak projectiles. +3 DEF",
          CATEGORY_EQUIPMENT, buy_price=250, equip_slot="shield",
          stats={"defense": 3}, tier="endgame",
          effect={"defense": 3})
_register("desert_cloak", "Desert Cloak", "Woven from desert fiber. +2 DEF",
          CATEGORY_EQUIPMENT, buy_price=120, equip_slot="shield",
          stats={"defense": 2}, tier="mid",
          effect={"defense": 2})
_register("dragon_mail", "Dragon Mail", "Dragonscale armor. +3 DEF",
          CATEGORY_EQUIPMENT, buy_price=250, equip_slot="shield",
          stats={"defense": 3}, tier="endgame",
          effect={"defense": 3})

# ── Equipment: Rings ─────────────────────────────────────────────────────────

_register("power_ring", "Power Ring", "Channels raw strength. +2 ATK",
          CATEGORY_EQUIPMENT, buy_price=100, equip_slot="ring",
          stats={"attack": 2}, tier="mid")
_register("fire_ring", "Fire Ring", "Burns enemies on contact. +1 ATK",
          CATEGORY_EQUIPMENT, buy_price=120, equip_slot="ring",
          stats={"attack": 1, "burn": True}, tier="mid")
_register("sage_ring", "Sage Ring", "Wise enchantment. +1 ATK +1 DEF",
          CATEGORY_EQUIPMENT, buy_price=180, equip_slot="ring",
          stats={"attack": 1, "defense": 1}, tier="endgame")

# ── Equipment: Boots ─────────────────────────────────────────────────────────

_register("leather_boots", "Leather Boots", "Light and flexible. +15 SPD",
          CATEGORY_EQUIPMENT, buy_price=30, equip_slot="boots",
          stats={"speed": 15}, tier="starter")
_register("swift_boots", "Swift Boots", "Wind-enchanted boots. +30 SPD",
          CATEGORY_EQUIPMENT, buy_price=80, equip_slot="boots",
          stats={"speed": 30}, tier="mid")
_register("winged_boots", "Winged Boots", "Almost like flying. +50 SPD",
          CATEGORY_EQUIPMENT, buy_price=200, equip_slot="boots",
          stats={"speed": 50}, tier="endgame")


def get_item(item_id):
    """Look up an item definition by ID. Returns InventoryItem or None."""
    return ITEMS.get(item_id)


# ── Drop tables ──────────────────────────────────────────────────────────────

# Enemy inventory drops (weighted: (item_id, weight))
ENEMY_INV_DROP_TABLE = {
    "starter": [("potion", 5), ("antidote", 2), ("wooden_sword", 1), ("leather_boots", 1)],
    "mid": [("potion", 4), ("bomb", 3), ("iron_sword", 1), ("guardian_shield", 1),
            ("power_ring", 1), ("swift_boots", 1), ("fire_ring", 1)],
    "endgame": [("elixir", 3), ("bomb", 3), ("flame_blade", 1), ("mirror_shield", 1),
                ("sage_ring", 1), ("winged_boots", 1)],
}

# Chest loot by tier
CHEST_INV_LOOT = {
    "starter": ["wooden_sword", "wooden_shield", "leather_boots", "potion"],
    "mid": ["iron_sword", "guardian_shield", "swift_boots", "power_ring", "fire_ring", "bomb"],
    "endgame": ["flame_blade", "mirror_shield", "winged_boots", "sage_ring", "elixir"],
}


# ── Inventory class ──────────────────────────────────────────────────────────

class Inventory:
    """Player inventory — stack-based items plus equipment slots.

    Backward-compatible with the shop system (add/remove/count/get_all).
    Also supports equipment slots for equip/unequip.
    """

    def __init__(self):
        self._stacks = {}  # item_id -> quantity
        self.equipment = {slot: None for slot in EQUIP_SLOTS}  # slot -> item_id or None

    # ── Stack-based interface (used by shops) ────────────────────────

    def add(self, item_id, quantity=1):
        """Add items to inventory. Returns True if added (always succeeds for now)."""
        # Enforce max slots for non-stacking new items
        if item_id not in self._stacks and len(self._stacks) >= MAX_INVENTORY_SLOTS:
            return False
        self._stacks[item_id] = self._stacks.get(item_id, 0) + quantity
        return True

    def remove(self, item_id, quantity=1):
        """Remove items. Returns True if successful, False if not enough."""
        current = self._stacks.get(item_id, 0)
        if current < quantity:
            return False
        current -= quantity
        if current <= 0:
            self._stacks.pop(item_id, None)
        else:
            self._stacks[item_id] = current
        return True

    def count(self, item_id):
        """Return quantity of an item."""
        return self._stacks.get(item_id, 0)

    def get_all(self):
        """Return list of (item_id, quantity) tuples for non-zero stacks."""
        return [(iid, qty) for iid, qty in self._stacks.items() if qty > 0]

    def get_all_items(self):
        """Return list of (item_id, quantity, InventoryItem) for display."""
        result = []
        for iid, qty in self._stacks.items():
            if qty > 0:
                defn = get_item(iid)
                if defn is not None:
                    result.append((iid, qty, defn))
        return result

    # ── Equipment interface ──────────────────────────────────────────

    def equip_item(self, item_id):
        """Equip an item from inventory into its equipment slot.

        If something is already equipped, swap it back into inventory.
        Returns True if equipped successfully.
        """
        defn = get_item(item_id)
        if defn is None or defn.category != CATEGORY_EQUIPMENT:
            return False
        slot = defn.equip_slot
        if slot not in EQUIP_SLOTS:
            return False
        if not self.remove(item_id):
            return False

        # If something is already in the slot, put it back
        old = self.equipment[slot]
        if old is not None:
            self.add(old)

        self.equipment[slot] = item_id
        return True

    def unequip_item(self, slot):
        """Unequip item from a slot back into inventory. Returns True if successful."""
        if slot not in EQUIP_SLOTS:
            return False
        item_id = self.equipment[slot]
        if item_id is None:
            return False
        if not self.add(item_id):
            return False  # inventory full
        self.equipment[slot] = None
        return True

    def get_equipped(self, slot):
        """Return InventoryItem for the equipped item in a slot, or None."""
        item_id = self.equipment.get(slot)
        if item_id is None:
            return None
        return get_item(item_id)

    def get_stat_bonus(self, stat_name):
        """Return total bonus for a stat from all equipped items."""
        total = 0
        for slot in EQUIP_SLOTS:
            item_id = self.equipment[slot]
            if item_id is not None:
                defn = get_item(item_id)
                if defn is not None:
                    total += defn.stats.get(stat_name, 0)
        return total

    def has_burn(self):
        """Check if any equipped item grants burn effect."""
        for slot in EQUIP_SLOTS:
            item_id = self.equipment[slot]
            if item_id is not None:
                defn = get_item(item_id)
                if defn is not None and defn.stats.get("burn"):
                    return True
        return False

    def use_consumable(self, item_id, player):
        """Use a consumable item. Returns True if used successfully.

        For bombs, returns True — caller must create explosion entity.
        """
        defn = get_item(item_id)
        if defn is None or defn.category != CATEGORY_CONSUMABLE:
            return False
        if self.count(item_id) <= 0:
            return False

        effect = defn.effect
        used = False

        if "heal" in effect:
            if player.hp < player.max_hp:
                player.heal(effect["heal"])
                used = True
        elif "heal_full" in effect:
            if player.hp < player.max_hp:
                player.hp = player.max_hp
                used = True
        elif "cure" in effect:
            status_name = effect["cure"]
            if status_name in player.status_effects:
                del player.status_effects[status_name]
            used = True  # consume even if not afflicted
        elif "bomb" in effect:
            used = True  # explosion handled by gameplay state
        elif "speed" in effect:
            player.apply_status("speed_boost", effect.get("duration", 20),
                                {"multiplier": effect["speed"]})
            used = True
        elif "resist" in effect:
            player.apply_status(f"resist_{effect['resist']}", effect.get("duration", 30))
            used = True

        if used:
            self.remove(item_id)
        return used

    # ── Serialization ────────────────────────────────────────────────

    def to_dict(self):
        """Serialize for save files."""
        return {
            "stacks": dict(self._stacks),
            "equipment": dict(self.equipment),
        }

    @classmethod
    def from_dict(cls, data):
        """Deserialize from save files."""
        inv = cls()
        if data is None:
            return inv
        # Support old format (plain dict of stacks)
        if isinstance(data, dict) and "stacks" not in data and "equipment" not in data:
            inv._stacks = dict(data)
            return inv
        inv._stacks = dict(data.get("stacks", {}))
        equipment_data = data.get("equipment", {})
        for slot in EQUIP_SLOTS:
            inv.equipment[slot] = equipment_data.get(slot)
        return inv
