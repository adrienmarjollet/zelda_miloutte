"""Pixel art tile surfaces for the tilemap."""

import pygame
from zelda_miloutte.sprites.pixel_art import surface_from_grid

# ── Palettes ──────────────────────────────────────────────────────
_GRASS_PAL = {
    'g': (76, 153, 0),      # base grass
    'G': (60, 130, 0),      # darker grass
    'd': (90, 168, 20),     # light accent
    'f': (50, 110, 10),     # flower/detail
}

_WALL_PAL = {
    'w': (140, 140, 140),   # wall base
    'W': (110, 110, 110),   # darker brick
    'l': (160, 160, 160),   # lighter brick
    'm': (90, 90, 90),      # mortar
}

_TREE_PAL = {
    't': (30, 100, 30),     # dark leaves
    'T': (20, 80, 20),      # darker leaves
    'l': (45, 120, 40),     # light leaves
    'b': (100, 60, 20),     # bark/trunk
}

_ROCK_PAL = {
    'r': (100, 100, 100),   # rock base
    'R': (80, 80, 80),      # dark rock
    'l': (130, 130, 130),   # highlight
    's': (60, 60, 60),      # shadow
}

_WATER_PAL = {
    'w': (50, 100, 200),    # water base
    'W': (40, 80, 180),     # dark water
    'l': (80, 140, 230),    # light ripple
    'r': (100, 160, 240),   # highlight ripple
}

_FLOOR_PAL = {
    'f': (160, 140, 110),   # floor base
    'F': (140, 120, 90),    # darker floor
    'l': (175, 155, 125),   # light accent
    'c': (120, 100, 75),    # crack
}

_DOOR_PAL = {
    'd': (160, 120, 60),    # door wood
    'D': (130, 95, 40),     # dark wood
    'h': (100, 70, 30),     # handle/detail
    'l': (180, 145, 80),    # light wood
}

_ENTRANCE_PAL = {
    'b': (120, 80, 30),     # brown base
    'B': (90, 55, 15),      # dark brown
    'a': (60, 40, 20),      # arch dark
    'l': (150, 110, 50),    # light accent
    'k': (20, 20, 20),      # keyhole / darkness
}

_BOSS_DOOR_PAL = {
    'p': (120, 40, 160),    # purple base
    'P': (90, 20, 130),     # dark purple
    'g': (180, 60, 220),    # glow accent
    'k': (20, 10, 30),      # darkness
    's': (200, 100, 240),   # shimmer
}

_SPIKES_PAL = {
    'f': (100, 90, 80),     # dark floor base
    'F': (80, 70, 60),      # darker floor
    's': (140, 140, 140),   # silver spike
    'S': (110, 110, 110),   # dark spike base
    't': (180, 180, 180),   # spike tip (bright)
    'b': (60, 55, 50),      # very dark base
}

_PIT_PAL = {
    'k': (0, 0, 0),         # pure black center
    'd': (30, 25, 20),      # very dark edge
    'e': (50, 40, 30),      # darker brown edge
    'c': (70, 60, 50),      # cracked edge
    'f': (100, 90, 80),     # floor color border
}

_ENTRANCE2_PAL = {
    'b': (80, 150, 200),    # ice blue base
    'B': (60, 120, 180),    # dark ice blue
    'a': (40, 80, 120),     # arch dark
    'l': (120, 200, 240),   # light ice accent
    'k': (20, 40, 60),      # keyhole / darkness
}

_FOREST_FLOOR_PAL = {
    'f': (40, 80, 30),      # dark mossy green base
    'F': (30, 60, 20),      # darker moss
    'm': (50, 90, 35),      # moss accent
    'd': (35, 70, 25),      # dark spot
}

_SAND_PAL = {
    's': (210, 180, 120),   # sandy tan base
    'S': (190, 160, 100),   # darker sand
    'l': (230, 200, 140),   # light sand
    'r': (180, 150, 90),    # rock/pebble
}

_LAVA_PAL = {
    'l': (200, 60, 20),     # lava orange base
    'L': (150, 40, 10),     # dark lava
    'y': (255, 200, 50),    # bright yellow highlight
    'r': (220, 100, 30),    # red-orange
}

# ── Grids (16x16 each) ───────────────────────────────────────────

GRASS_GRID = [
    "ggggGgggggggggGg",
    "gggggggdggGggggg",
    "ggGggggggggggdgg",
    "ggggdggggggggggg",
    "gggggggGgggggggg",
    "ggggggggggdgggGg",
    "gGgggggggggggggg",
    "ggggggdggggGgggg",
    "gggGgggggggggdgg",
    "ggggggggGggggggg",
    "ggdgggggggggGggg",
    "gggggGgggggggggg",
    "ggggggggdggggggg",
    "gGgggggggggdgggg",
    "ggggggGggggggggg",
    "ggggdggggggGgggg",
]

WALL_GRID = [
    "mmmmmmmmmmmmmmmmm",
    "wWwwwllwwWwwwllww",
    "wWwwwllwwWwwwllww",
    "wWwwwllwwWwwwllww",
    "mmmmmmmmmmmmmmmmm",
    "wllwwWwwwllwwWwww",
    "wllwwWwwwllwwWwww",
    "wllwwWwwwllwwWwww",
    "mmmmmmmmmmmmmmmmm",
    "wWwwwllwwWwwwllww",
    "wWwwwllwwWwwwllww",
    "wWwwwllwwWwwwllww",
    "mmmmmmmmmmmmmmmmm",
    "wllwwWwwwllwwWwww",
    "wllwwWwwwllwwWwww",
    "wllwwWwwwllwwWwww",
]

TREE_GRID = [
    "....ttlltt......",
    "...tTTtllTTt....",
    "..tTTTTllTTTt...",
    ".tTTtTTttTtTTt..",
    "tTTttTTllTttTTt.",
    "tTtTTTTllTTTtTt.",
    ".tTTTTTTTTTTTt..",
    "..ttTTTTTTTtt...",
    "....ttTTtt......",
    "......bb........",
    "......bb........",
    ".....bbb........",
    "......bb........",
    "......bb........",
    "......bb........",
    ".....bbbb.......",
]

ROCK_GRID = [
    "................",
    "....rrrrrr......",
    "..rrlllrrrrr....",
    ".rrllrrrrrrRr...",
    "rrlrrrrrrrRRr...",
    "rrrrrrrrrrRRRr..",
    "rrrrrrrRRRRRr...",
    "rrrrRRRRRRRRr...",
    "rrrRRRRRRRRrs...",
    "rrRRRRRRRRrss...",
    ".rRRRRRRRrrss...",
    ".rrRRRrrrrss....",
    "..rrrrrrrss.....",
    "...rrrrrsss.....",
    "....sssss.......",
    "................",
]

WATER_GRID = [
    "wwwWwwwwwwWwwwww",
    "wWwwwwlwwwwwwWww",
    "wwwwlrrwwwWwwwww",
    "wWwwwlwwwwwwwwww",
    "wwwwwwwwlwwwWwww",
    "wwwWwwlrrwwwwwww",
    "wWwwwwwlwwwwwwWw",
    "wwwwwwwwwwlwwwww",
    "wwwwwWwwlrrWwwww",
    "wWwwwwwwwlwwwwww",
    "wwwwwwwwwwwwwwWw",
    "wwwWwwlwwwwWwwww",
    "wWwwwlrrwwwwwwww",
    "wwwwwwlwwwWwwwww",
    "wwwwwwwwwwwwwWww",
    "wWwwwWwwwwWwwwww",
]

FLOOR_GRID = [
    "fFffflfffFfffflf",
    "ffffffffffffffff",
    "ffFffffffflfffff",
    "ffffffffffffffff",
    "flffffffFfffffff",
    "ffffffffffffffff",
    "fffffffcfffFffff",
    "ffffffccfflfffff",
    "fFfffffcffffffff",
    "ffffffffffffffff",
    "ffffffflffffffff",
    "fffFffffffffffff",
    "fffffffffFffffff",
    "fflfffffffffffff",
    "fffffffffffflFff",
    "fFffffffffffflff",
]

DOOR_GRID = [
    "DDDDDDddddDDDDDD",
    "DllddDDddDDddllD",
    "DllddDDddDDddllD",
    "DDDDDDddddDDDDDD",
    "DdddDDDDDDDDdddD",
    "DdddDDhhhhDDdddD",
    "DDDDDDhkkdDDDDDD",
    "DlldDDhkkdDDdllD",
    "DlldDDddddDDdllD",
    "DDDDDDddddDDDDDD",
    "DdddDDDDDDDDdddD",
    "DdddDDddddDDdddD",
    "DDDDDDddddDDDDDD",
    "DllddDDddDDddllD",
    "DllddDDddDDddllD",
    "DDDDDDddddDDDDDD",
]

ENTRANCE_GRID = [
    "BBBBBaaaaaBBBBBB",
    "BBBaakkkkkaaBBBB",
    "BBaakkkkkkkaaaBB",
    "BaakkkkkkkkkaaBB",
    "BakkkkkkkkkkkaB.",
    "aakkkkkkkkkkkaa.",
    "aakkkkkkkkkkkaa.",
    "aakkkkkkkkkkkaa.",
    "aakkkkkkkkkkkaa.",
    "aakkkkkkkkkkkaa.",
    "BakkkkkkkkkkkaBB",
    "BaakkkkkkkkkaaBB",
    "BBaakkkkkkkaaaBB",
    "BBBaakkkkkaaBBBB",
    "BBBBBaaaaaBBBBBB",
    "BBlBBBBBBBBBBlBB",
]

BOSS_DOOR_GRID = [
    "PPPPPPppppPPPPPP",
    "PPPppgssgpppPPPP",
    "PPppssssssspPPPP",
    "PppsskkkkssppPPP",
    "PpssskkkkssspPP.",
    "ppssskkkkssspp..",
    "ppssskkkkssspp..",
    "ppsssgssgssspp..",
    "ppssssssssssp...",
    "ppsssgssgssspp..",
    "PpssskkkkssspPP.",
    "PppsskkkkssppPPP",
    "PPppssssssspPPPP",
    "PPPppgssgpppPPPP",
    "PPPPPPppppPPPPPP",
    "PPsPPPPPPPPPsPPP",
]

SPIKES_GRID = [
    "ffffFffffffFffff",
    "fffFffffffffffFf",
    "fffffffFFfffffff",
    "ffffffbSSbffffff",
    "ffffFbSttSbFffff",
    "fffffbSttSbfffff",
    "ffffFfbSSbfFffff",
    "fffbSSbffbSSbfff",
    "ffFbSttSbSttSbFf",
    "fffbSttSbSttSbff",
    "ffffbSSbfbSSbfff",
    "fffffFbSSbFfffff",
    "fFffffbttbffffFf",
    "fffffffSSfffffff",
    "ffffffFbbFffffff",
    "fFffffFffFffffFf",
]

PIT_GRID = [
    "fffffcccccffffff",
    "ffffceeeedcfffff",
    "fffceddddddcffff",
    "ffcedddkkdddcfff",
    "ffceddkkkkddcfff",
    "fcedkkkkkkkdecff",
    "fcedkkkkkkkkdcff",
    "fcedkkkkkkkkdcff",
    "fcedkkkkkkkkdcff",
    "fcedkkkkkkkdecff",
    "ffceddkkkkddcfff",
    "ffcedddkkdddcfff",
    "fffceddddddcffff",
    "ffffceeeedcfffff",
    "fffffcccccffffff",
    "ffffffffffffffff",
]

ENTRANCE2_GRID = [
    "BBBBBaaaaaBBBBBB",
    "BBBaakkkkkaaBBBB",
    "BBaakkkkkkkaaaBB",
    "BaakkkkkkkkkaaBB",
    "BakkkkkkkkkkkaB.",
    "aakkkkkkkkkkkaa.",
    "aakkkkkkkkkkkaa.",
    "aakkkkkkkkkkkaa.",
    "aakkkkkkkkkkkaa.",
    "aakkkkkkkkkkkaa.",
    "BakkkkkkkkkkkaBB",
    "BaakkkkkkkkkaaBB",
    "BBaakkkkkkkaaaBB",
    "BBBaakkkkkaaBBBB",
    "BBBBBaaaaaBBBBBB",
    "BBlBBBBBBBBBBlBB",
]

# Transition tiles use grass grid (invisible to player)
TRANSITION_GRID = [
    "ggggGgggggggggGg",
    "gggggggdggGggggg",
    "ggGggggggggggdgg",
    "ggggdggggggggggg",
    "gggggggGgggggggg",
    "ggggggggggdgggGg",
    "gGgggggggggggggg",
    "ggggggdggggGgggg",
    "gggGgggggggggdgg",
    "ggggggggGggggggg",
    "ggdgggggggggGggg",
    "gggggGgggggggggg",
    "ggggggggdggggggg",
    "gGgggggggggdgggg",
    "ggggggGggggggggg",
    "ggggdggggggGgggg",
]

FOREST_FLOOR_GRID = [
    "fFfffmfffFfffmff",
    "ffffffffffffffff",
    "ffFffffffmffffff",
    "ffdfffffffffffff",
    "fmffffffFfffffff",
    "ffffffffffffffff",
    "fffffffmfffFffff",
    "ffffffmffmffffff",
    "fFfffffmffffffff",
    "ffffffffffffffff",
    "ffffffmfffffffff",
    "fffFffffffffffff",
    "fffffffffFffffff",
    "ffmfffffffffffff",
    "fffffffffffmfFff",
    "fFffffffffffmfff",
]

SAND_GRID = [
    "sSsssslssssSssss",
    "ssssssssssssssss",
    "ssSsssssslssssss",
    "sssssrssssssssss",
    "slsssssssSssssss",
    "ssssssssssssssss",
    "sssssslssssSssss",
    "sssssssssslsssss",
    "sSssssssssssssss",
    "ssssssssrsssssss",
    "sssssslssssssSss",
    "sssSssssssssssss",
    "sssssssssSssssss",
    "sslsssssssssssss",
    "sssssssssssslsFs",
    "sSsssssssssslsss",
]

LAVA_GRID = [
    "lLllllyrlllLllll",
    "lllrllllllllllll",
    "llLllllylllllrll",
    "llllllrlllyLllll",
    "lyLllllllllllLll",
    "llllrllllyllllll",
    "llllllyLlllllrll",
    "lLllllrllllLllyl",
    "llllyllllLllllrl",
    "lrLlllllllyllLll",
    "lllylllrllllllll",
    "lllLllllllLlllyl",
    "llllllLylllrllll",
    "lLlllrllllyllLll",
    "llyllllLlllllrll",
    "lLllrllllylllLyl",
]

# ── Pre-built surfaces (created on first access) ─────────────────

_tile_cache = {}


def get_tile_surface(tile_type_value):
    """Return a 32x32 surface for the given TileType integer value.

    Surfaces are cached after first creation.
    """
    if tile_type_value in _tile_cache:
        return _tile_cache[tile_type_value]

    grid, palette = _TILE_DATA[tile_type_value]
    surf = surface_from_grid(grid, palette, scale=2)
    _tile_cache[tile_type_value] = surf
    return surf


# Map TileType enum values to (grid, palette)
_TILE_DATA = {
    0: (GRASS_GRID, _GRASS_PAL),
    1: (WALL_GRID, _WALL_PAL),
    2: (TREE_GRID, _TREE_PAL),
    3: (ROCK_GRID, _ROCK_PAL),
    4: (WATER_GRID, _WATER_PAL),
    5: (FLOOR_GRID, _FLOOR_PAL),
    6: (DOOR_GRID, _DOOR_PAL),
    7: (ENTRANCE_GRID, _ENTRANCE_PAL),
    8: (BOSS_DOOR_GRID, _BOSS_DOOR_PAL),
    9: (SPIKES_GRID, _SPIKES_PAL),
    10: (PIT_GRID, _PIT_PAL),
    11: (ENTRANCE2_GRID, _ENTRANCE2_PAL),
    12: (TRANSITION_GRID, _GRASS_PAL),  # TRANSITION_N
    13: (TRANSITION_GRID, _GRASS_PAL),  # TRANSITION_S
    14: (TRANSITION_GRID, _GRASS_PAL),  # TRANSITION_E
    15: (TRANSITION_GRID, _GRASS_PAL),  # TRANSITION_W
    16: (FOREST_FLOOR_GRID, _FOREST_FLOOR_PAL),
    17: (SAND_GRID, _SAND_PAL),
    18: (LAVA_GRID, _LAVA_PAL),
}
