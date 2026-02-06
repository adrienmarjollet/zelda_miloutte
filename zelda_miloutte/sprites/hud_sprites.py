"""Pixel art sprites for HUD elements (hearts, key icon)."""

from zelda_miloutte.sprites.pixel_art import surface_from_grid

# ── Heart palettes ────────────────────────────────────────────────
_FULL_PAL = {
    'r': (220, 40, 40),
    'R': (180, 20, 20),
    'l': (255, 100, 100),
    '.': None,
}

_HALF_PAL = {
    'r': (220, 40, 40),     # left half (full)
    'R': (180, 20, 20),
    'l': (255, 100, 100),
    'd': (100, 30, 30),     # right half (dark / empty)
    'D': (70, 20, 20),
    '.': None,
}

_EMPTY_PAL = {
    'e': (60, 60, 60),
    'E': (40, 40, 40),
    '.': None,
}

_KEY_PAL = {
    'y': (255, 210, 60),
    'Y': (210, 170, 30),
    'l': (255, 240, 130),
    'h': (180, 130, 20),
    '.': None,
}

# ── Grids (10x10 for hearts at scale 2 = 20x20, matching HUD_HEART_SIZE) ──

_HEART_FULL = [
    ".rr..rr...",
    "rlrrrrrlr.",
    "rrrrrrrrrr",
    "rrrrrrrrrr",
    ".rrrrrrrr.",
    ".rrrrrrrr.",
    "..rrrrrr..",
    "...rRrr...",
    "....Rr....",
    ".........."]

_HEART_HALF = [
    ".rr..dd...",
    "rlrrddDdr.",
    "rrrrrddDdd",
    "rrrrrddddd",
    ".rrrrdddd.",
    ".rrrrdddd.",
    "..rrrddd..",
    "...rDdd...",
    "....Dd....",
    ".........."]

_HEART_EMPTY = [
    ".ee..ee...",
    "eEeeeeeEe.",
    "eeeeeeeeee",
    "eeeeeeeeee",
    ".eeeeeeee.",
    ".eeeeeeee.",
    "..eeeeee..",
    "...eEee...",
    "....Ee....",
    ".........."]

# ── Key icon (10x10 at scale 2 = 20x20) ──────────────────────────
_KEY_ICON = [
    "..yyyy....",
    ".yhllyy...",
    ".ylhhly...",
    ".yyllyy...",
    "..yyyy....",
    "...yy.....",
    "...yy.....",
    "...yyy....",
    "...yy.....",
    "...yyy....",
]

# ── Build surfaces ────────────────────────────────────────────────
_cache = {}


def get_hud_heart_full():
    if "full" not in _cache:
        _cache["full"] = surface_from_grid(_HEART_FULL, _FULL_PAL, 2)
    return _cache["full"]


def get_hud_heart_half():
    if "half" not in _cache:
        _cache["half"] = surface_from_grid(_HEART_HALF, _HALF_PAL, 2)
    return _cache["half"]


def get_hud_heart_empty():
    if "empty" not in _cache:
        _cache["empty"] = surface_from_grid(_HEART_EMPTY, _EMPTY_PAL, 2)
    return _cache["empty"]


def get_hud_key_icon():
    if "key" not in _cache:
        _cache["key"] = surface_from_grid(_KEY_ICON, _KEY_PAL, 2)
    return _cache["key"]
