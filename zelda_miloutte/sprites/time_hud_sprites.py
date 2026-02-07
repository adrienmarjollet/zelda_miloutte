"""Pixel art sprites for the day/night HUD indicator (sun / moon icons)."""

from .pixel_art import surface_from_grid

_SUN_PAL = {
    'y': (255, 220, 60),     # sun body
    'Y': (255, 200, 30),     # sun darker center
    'r': (255, 180, 40),     # ray
    '.': None,
}

_MOON_PAL = {
    'm': (200, 210, 240),    # moon body
    'M': (170, 180, 210),    # moon shadow
    's': (255, 255, 255),    # star highlight
    '.': None,
}

_DAWN_PAL = {
    'o': (255, 160, 60),     # warm orange
    'O': (255, 130, 40),     # darker orange
    'y': (255, 220, 80),     # yellow highlight
    '.': None,
}

_DUSK_PAL = {
    'o': (200, 100, 40),     # dusk orange
    'O': (160, 70, 30),      # darker dusk
    'r': (180, 50, 30),      # red tint
    'y': (255, 180, 60),     # gold highlight
    '.': None,
}

_SUN_GRID = [
    "...r..r..r...",
    "..r.r..r.r..",
    ".....yyy.....",
    "..r.yYYYy.r..",
    "...yyYYYyy...",
    "r..yYYYYYy..r",
    "...yyYYYyy...",
    "..r.yYYYy.r..",
    ".....yyy.....",
    "..r.r..r.r..",
    "...r..r..r...",
]

_MOON_GRID = [
    "....mmm......",
    "...mmmMm.....",
    "..mmmMMm.....",
    "..mmMMMm.....",
    "..mmMMMm.....",
    "..mmmMMm.....",
    "...mmmMm.....",
    "....mmm......",
]

_DAWN_GRID = [
    ".....yyy.....",
    "....yOOOy....",
    "...yOOOOOy...",
    "...yOOOOOy...",
    "....yOOOy....",
    ".....yyy.....",
    "ooooooooooooo",
    ".o.o.o.o.o.o.",
]

_DUSK_GRID = [
    ".....yyy.....",
    "....yOOOy....",
    "...yOOrOOy...",
    "...yOrrrOy...",
    "....yOOOy....",
    ".....yyy.....",
    "ooooooooooooo",
    ".o.o.o.o.o.o.",
]

_cache = {}


def get_sun_icon():
    if "sun" not in _cache:
        _cache["sun"] = surface_from_grid(_SUN_GRID, _SUN_PAL, 2)
    return _cache["sun"]


def get_moon_icon():
    if "moon" not in _cache:
        _cache["moon"] = surface_from_grid(_MOON_GRID, _MOON_PAL, 2)
    return _cache["moon"]


def get_dawn_icon():
    if "dawn" not in _cache:
        _cache["dawn"] = surface_from_grid(_DAWN_GRID, _DAWN_PAL, 2)
    return _cache["dawn"]


def get_dusk_icon():
    if "dusk" not in _cache:
        _cache["dusk"] = surface_from_grid(_DUSK_GRID, _DUSK_PAL, 2)
    return _cache["dusk"]
