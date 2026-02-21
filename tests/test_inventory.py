"""Tests for the Inventory system."""

import pytest
from zelda_miloutte.data.inventory import (
    Inventory,
    InventoryItem,
    get_item,
    ITEMS,
    CATEGORY_CONSUMABLE,
    CATEGORY_EQUIPMENT,
    EQUIP_SLOTS,
    MAX_INVENTORY_SLOTS,
)


class TestInventoryBasics:
    def test_empty_inventory(self):
        inv = Inventory()
        assert inv.get_all() == []
        assert inv.count("potion") == 0

    def test_add_item(self):
        inv = Inventory()
        assert inv.add("potion", 3) is True
        assert inv.count("potion") == 3

    def test_add_stacks(self):
        inv = Inventory()
        inv.add("potion", 2)
        inv.add("potion", 3)
        assert inv.count("potion") == 5

    def test_remove_item(self):
        inv = Inventory()
        inv.add("potion", 5)
        assert inv.remove("potion", 3) is True
        assert inv.count("potion") == 2

    def test_remove_all(self):
        inv = Inventory()
        inv.add("potion", 3)
        assert inv.remove("potion", 3) is True
        assert inv.count("potion") == 0
        assert inv.get_all() == []

    def test_remove_insufficient(self):
        inv = Inventory()
        inv.add("potion", 2)
        assert inv.remove("potion", 5) is False
        assert inv.count("potion") == 2  # unchanged

    def test_remove_nonexistent(self):
        inv = Inventory()
        assert inv.remove("potion") is False

    def test_get_all(self):
        inv = Inventory()
        inv.add("potion", 3)
        inv.add("bomb", 1)
        items = dict(inv.get_all())
        assert items == {"potion": 3, "bomb": 1}

    def test_max_slots(self):
        inv = Inventory()
        for i in range(MAX_INVENTORY_SLOTS):
            assert inv.add(f"item_{i}") is True
        # 21st unique item should fail
        assert inv.add("one_more") is False

    def test_existing_stack_not_blocked_by_slot_limit(self):
        inv = Inventory()
        for i in range(MAX_INVENTORY_SLOTS):
            inv.add(f"item_{i}")
        # Adding to existing stack should still work
        assert inv.add("item_0", 5) is True


class TestEquipment:
    def test_equip_weapon(self):
        inv = Inventory()
        inv.add("iron_sword")
        assert inv.equip_item("iron_sword") is True
        assert inv.equipment["weapon"] == "iron_sword"
        assert inv.count("iron_sword") == 0

    def test_equip_swap(self):
        inv = Inventory()
        inv.add("wooden_sword")
        inv.add("iron_sword")
        inv.equip_item("wooden_sword")
        inv.equip_item("iron_sword")
        assert inv.equipment["weapon"] == "iron_sword"
        assert inv.count("wooden_sword") == 1  # Old weapon returned to inventory

    def test_equip_nonexistent_fails(self):
        inv = Inventory()
        assert inv.equip_item("iron_sword") is False

    def test_equip_consumable_fails(self):
        inv = Inventory()
        inv.add("potion")
        assert inv.equip_item("potion") is False

    def test_unequip(self):
        inv = Inventory()
        inv.add("iron_sword")
        inv.equip_item("iron_sword")
        assert inv.unequip_item("weapon") is True
        assert inv.equipment["weapon"] is None
        assert inv.count("iron_sword") == 1

    def test_unequip_empty_slot(self):
        inv = Inventory()
        assert inv.unequip_item("weapon") is False

    def test_unequip_invalid_slot(self):
        inv = Inventory()
        assert inv.unequip_item("invalid_slot") is False

    def test_get_equipped(self):
        inv = Inventory()
        inv.add("iron_sword")
        inv.equip_item("iron_sword")
        equipped = inv.get_equipped("weapon")
        assert equipped is not None
        assert equipped.item_id == "iron_sword"

    def test_get_equipped_empty(self):
        inv = Inventory()
        assert inv.get_equipped("weapon") is None


class TestStatBonuses:
    def test_attack_bonus(self):
        inv = Inventory()
        inv.add("iron_sword")
        inv.equip_item("iron_sword")
        assert inv.get_stat_bonus("attack") == 3

    def test_defense_bonus(self):
        inv = Inventory()
        inv.add("wooden_shield")
        inv.equip_item("wooden_shield")
        assert inv.get_stat_bonus("defense") == 1

    def test_stacked_bonuses(self):
        inv = Inventory()
        inv.add("iron_sword")
        inv.add("power_ring")
        inv.equip_item("iron_sword")
        inv.equip_item("power_ring")
        assert inv.get_stat_bonus("attack") == 5  # 3 + 2

    def test_no_bonus_empty(self):
        inv = Inventory()
        assert inv.get_stat_bonus("attack") == 0

    def test_speed_bonus(self):
        inv = Inventory()
        inv.add("swift_boots")
        inv.equip_item("swift_boots")
        assert inv.get_stat_bonus("speed") == 30

    def test_has_burn(self):
        inv = Inventory()
        inv.add("flame_blade")
        inv.equip_item("flame_blade")
        assert inv.has_burn() is True

    def test_no_burn(self):
        inv = Inventory()
        inv.add("iron_sword")
        inv.equip_item("iron_sword")
        assert inv.has_burn() is False


class TestSerialization:
    def test_roundtrip(self):
        inv = Inventory()
        inv.add("potion", 5)
        inv.add("bomb", 2)
        inv.add("iron_sword")
        inv.equip_item("iron_sword")

        data = inv.to_dict()
        inv2 = Inventory.from_dict(data)

        assert inv2.count("potion") == 5
        assert inv2.count("bomb") == 2
        assert inv2.equipment["weapon"] == "iron_sword"

    def test_from_dict_none(self):
        inv = Inventory.from_dict(None)
        assert inv.get_all() == []

    def test_from_dict_legacy_format(self):
        """Old save format was just a dict of stacks."""
        data = {"potion": 3, "bomb": 1}
        inv = Inventory.from_dict(data)
        assert inv.count("potion") == 3
        assert inv.count("bomb") == 1


class TestItemRegistry:
    def test_get_item_exists(self):
        item = get_item("potion")
        assert item is not None
        assert item.name == "Potion"
        assert item.category == CATEGORY_CONSUMABLE

    def test_get_item_nonexistent(self):
        assert get_item("nonexistent_item") is None

    def test_equipment_has_slot(self):
        item = get_item("iron_sword")
        assert item is not None
        assert item.equip_slot == "weapon"
        assert item.category == CATEGORY_EQUIPMENT

    def test_sell_price_half_buy(self):
        item = get_item("potion")
        assert item.sell_price == max(1, item.buy_price // 2)
