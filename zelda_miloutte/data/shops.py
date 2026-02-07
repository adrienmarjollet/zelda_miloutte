"""Shop data — stock lists for each merchant location."""


# Each shop entry: {"name": display name, "items": [item_id, ...]}
# Prices come from the item registry in inventory.py.

SHOPS = {
    "village_general": {
        "name": "Village General Store",
        "greeting": "Welcome, traveler! Take a look at my wares.",
        "items": [
            "potion",
            "antidote",
            "speed_boost",
            "iron_shield",
            "steel_sword",
        ],
    },
    "desert_merchant": {
        "name": "Desert Trader",
        "greeting": "Rare goods from across the sands...",
        "items": [
            "potion",
            "hi_potion",
            "antidote",
            "fire_ward",
            "desert_cloak",
            "flame_blade",
        ],
    },
    "volcano_merchant": {
        "name": "Volcano Outpost",
        "greeting": "Only the strongest survive here. Gear up.",
        "items": [
            "hi_potion",
            "elixir",
            "fire_ward",
            "speed_boost",
            "dragon_mail",
            "inferno_edge",
        ],
    },
}


def get_shop(shop_id):
    """Return shop data dict or None."""
    return SHOPS.get(shop_id)
