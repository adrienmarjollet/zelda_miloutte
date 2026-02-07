"""Pixel art sprites for gold coins (pickup item and HUD icon)."""

from zelda_miloutte.sprites.pixel_art import surface_from_grid

# ── Gold coin palette ────────────────────────────────────────────────
_GOLD_PAL = {
    'o': (140, 100, 10),     # dark gold outline
    'g': (255, 200, 50),     # gold
    'G': (210, 160, 25),     # darker gold
    'l': (255, 235, 130),    # highlight
    'L': (255, 245, 180),    # bright highlight
    'd': (170, 120, 15),     # shadow
    '.': None,
}

# ── Gold pickup frames (16x16, 2 frames for bob) ────────────────────
_GOLD_0 = [
    "................",
    "......oooo......",
    "....ooGGGGoo....",
    "...oGGggggGGo...",
    "..oGglllllgGGo..",
    "..oGgLlllgggGo..",
    "..oGglllllgGGo..",
    "..oGGggggggGo...",
    "..oGGGGGGGGGo...",
    "...oGGGddGGo....",
    "....ooGGGGoo....",
    "......oooo......",
    "................",
    "................",
    "................",
    "................",
]

_GOLD_1 = [
    "................",
    "................",
    "......oooo......",
    "....ooGGGGoo....",
    "...oGGggggGGo...",
    "..oGglllllgGGo..",
    "..oGgLlllgggGo..",
    "..oGglllllgGGo..",
    "..oGGggggggGo...",
    "..oGGGGGGGGGo...",
    "...oGGGddGGo....",
    "....ooGGGGoo....",
    "......oooo......",
    "................",
    "................",
    "................",
]

# ── HUD coin icon (10x10 at scale 2 = 20x20) ───────────────────────
_HUD_COIN = [
    "..oooo....",
    ".oGGGGo...",
    "oGglllGo..",
    "oGgLlgGo..",
    "oGglllGo..",
    "oGGgggGo..",
    "oGGGGGGo..",
    ".oGGdGo...",
    "..oooo....",
    "..........",
]

# ── Build surfaces ──────────────────────────────────────────────────
_gold_cache = None
_hud_coin_cache = None


def get_gold_frames():
    """Return [frame0, frame1] for gold pickup item."""
    global _gold_cache
    if _gold_cache is not None:
        return _gold_cache
    _gold_cache = [surface_from_grid(g, _GOLD_PAL, 1) for g in (_GOLD_0, _GOLD_1)]
    return _gold_cache


def get_hud_coin_icon():
    """Return the HUD coin icon surface."""
    global _hud_coin_cache
    if _hud_coin_cache is not None:
        return _hud_coin_cache
    _hud_coin_cache = surface_from_grid(_HUD_COIN, _GOLD_PAL, 2)
    return _hud_coin_cache
