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

# ── Tile Variants (2-3 per grass/floor/sand type) ────────────────

# Variant grids swap a few detail characters for visual variety.
# Selected by position hash so the same tile always looks the same.

GRASS_GRID_V2 = [
    "gGggggggGggggdgg",
    "ggggdggggggGgggg",
    "ggggggggdgggggGg",
    "gGgggggggggggggg",
    "ggdgggggGggggggg",
    "gggggggggggGgggg",
    "ggggGgggggdggggg",
    "ggdggggggggggGgg",
    "gggggGgggggggggg",
    "ggggggdggggGgggg",
    "gGgggggggdgggggg",
    "ggggggGgggggggdg",
    "gggdggggggGggggg",
    "ggggggggdggggggg",
    "gGggggggggggdgGg",
    "ggggGgggdggggggg",
]

FLOOR_GRID_V2 = [
    "fffFffffffflffff",
    "fflfffffffffffff",
    "fffffffffffFffff",
    "fFfffffcffffffff",
    "ffffffffflfffff",
    "fffffffFffffffff",
    "fffffffffffflFff",
    "fflfffffffffffff",
    "fffFffffffflffff",
    "ffffffffffffffff",
    "ffFfffffcfffffff",
    "fffffffffflfffff",
    "ffffffffffffffff",
    "fFffflfffFfffflf",
    "ffffffffffffffff",
    "fflffffffffFffff",
]

SAND_GRID_V2 = [
    "sssSssssslssssss",
    "sssssrsssssssSss",
    "slssssssssssssss",
    "ssSssssssSssssss",
    "ssssssssssssslss",
    "ssssslsssssSssss",
    "ssSssssssssslsss",
    "sssssssSssssssss",
    "sslssssssssssSss",
    "ssssssssrsssssss",
    "sSssslsssssSssss",
    "ssssssssssssssss",
    "ssssSsssslssssss",
    "sssssssssssssSss",
    "slsssssSssssssss",
    "ssssssssslssSsss",
]

_VARIANT_DATA = {
    0: [(GRASS_GRID, _GRASS_PAL), (GRASS_GRID_V2, _GRASS_PAL)],
    5: [(FLOOR_GRID, _FLOOR_PAL), (FLOOR_GRID_V2, _FLOOR_PAL)],
    17: [(SAND_GRID, _SAND_PAL), (SAND_GRID_V2, _SAND_PAL)],
}

# ── Pre-built surfaces (created on first access) ─────────────────

_tile_cache = {}
_variant_cache = {}


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


def get_tile_surface_variant(tile_type_value, tile_x, tile_y):
    """Return a variant tile surface chosen by position hash.

    Falls back to the base surface for tiles without variants.
    """
    variants = _VARIANT_DATA.get(tile_type_value)
    if not variants:
        return get_tile_surface(tile_type_value)

    # Deterministic variant selection based on position
    variant_idx = (tile_x * 7 + tile_y * 13) % len(variants)
    cache_key = (tile_type_value, variant_idx)
    if cache_key in _variant_cache:
        return _variant_cache[cache_key]

    grid, palette = variants[variant_idx]
    surf = surface_from_grid(grid, palette, scale=2)
    _variant_cache[cache_key] = surf
    return surf


# ── Barrier and Bridge grids (puzzle tiles) ──────────────────────
# These are imported from puzzle_sprites but we define simple versions here
# for the tile_sprites system to keep the tile data self-contained.

_BARRIER_RED_TILE_PAL = {
    'r': (200, 50, 50),
    'R': (150, 30, 30),
    'g': (255, 100, 100),
    'd': (100, 20, 20),
}

BARRIER_RED_TILE_GRID = [
    "ddRRRRRRRRRRRRdd",
    "dRrrrrrrrrrrrrRd",
    "RrrgrrrrrrrgrrRR",
    "RrrrrrgrrrrrrrRR",
    "RrrrrrrrrrrgrrRR",
    "RrgrrrrrrrrrrRRR",
    "RrrrrgrrrrgrrrRR",
    "RrrrrrrrrrrrrrRR",
    "RrrrrgrrrrrrrRRR",
    "RrgrrrrrrrgrrRRR",
    "RrrrrrrrrrrrrrRR",
    "RrrrrgrrrrgrrrRR",
    "RrrrrrrrrrrrrrRR",
    "RrrgrrrrrrrgrrRR",
    "dRrrrrrrrrrrrrRd",
    "ddRRRRRRRRRRRRdd",
]

_BARRIER_BLUE_TILE_PAL = {
    'r': (50, 100, 200),
    'R': (30, 60, 150),
    'g': (100, 160, 255),
    'd': (20, 40, 100),
}

BARRIER_BLUE_TILE_GRID = [
    "ddRRRRRRRRRRRRdd",
    "dRrrrrrrrrrrrrRd",
    "RrrgrrrrrrrgrrRR",
    "RrrrrrgrrrrrrrRR",
    "RrrrrrrrrrrgrrRR",
    "RrgrrrrrrrrrrRRR",
    "RrrrrgrrrrgrrrRR",
    "RrrrrrrrrrrrrrRR",
    "RrrrrgrrrrrrrRRR",
    "RrgrrrrrrrgrrRRR",
    "RrrrrrrrrrrrrrRR",
    "RrrrrgrrrrgrrrRR",
    "RrrrrrrrrrrrrrRR",
    "RrrgrrrrrrrgrrRR",
    "dRrrrrrrrrrrrrRd",
    "ddRRRRRRRRRRRRdd",
]

_BRIDGE_TILE_PAL = {
    'w': (139, 90, 43),
    'W': (120, 75, 35),
    'b': (100, 60, 20),
    'g': (50, 40, 30),
}

BRIDGE_TILE_GRID = [
    "bwwwgwwwgwwwgwwwb",
    "bwwwgwwwgwwwgwwwb",
    "bWWWgWWWgWWWgWWWb",
    "bwwwgwwwgwwwgwwwb",
    "bwwwgwwwgwwwgwwwb",
    "bWWWgWWWgWWWgWWWb",
    "bwwwgwwwgwwwgwwwb",
    "bwwwgwwwgwwwgwwwb",
    "bWWWgWWWgWWWgWWWb",
    "bwwwgwwwgwwwgwwwb",
    "bwwwgwwwgwwwgwwwb",
    "bWWWgWWWgWWWgWWWb",
    "bwwwgwwwgwwwgwwwb",
    "bwwwgwwwgwwwgwwwb",
    "bWWWgWWWgWWWgWWWb",
    "bwwwgwwwgwwwgwwwb",
]

# ── Ice tile grids and palettes ────────────────────────────────────

_ICE_PAL = {
    'i': (100, 180, 230),    # ice base
    'I': (80, 150, 210),     # darker ice
    'l': (140, 210, 250),    # light highlight
    'r': (120, 200, 245),    # ripple/reflection
}

ICE_GRID = [
    "iIiiiiiiiiiiiiIi",
    "iiiiilriiIiiiiii",
    "iiIiiiiiiiiilrii",
    "iiiiriiiiiiiiiIi",
    "iiiiiiiliiIiiiii",
    "iiIiiiiiiiiiiiir",
    "iiiiiriiiiIiiiii",
    "iIiiiiiliiiiiiii",
    "iiiiiiiiiirliiIi",
    "iiIiiiiiiiiiiiir",
    "iiiilriiiiiIiiii",
    "iIiiiiiiiiiiiiir",
    "iiiiiiiiliiiiiii",
    "iiIiiiiiiiilriIi",
    "iiiiiiiiiiiiiiii",
    "iIiiirliiiiIiiii",
]

_CRACKED_ICE_PAL = {
    'i': (140, 200, 230),    # cracked ice base
    'I': (110, 170, 210),    # darker
    'c': (80, 120, 160),     # crack line
    'l': (180, 220, 245),    # light spot
}

CRACKED_ICE_GRID = [
    "iIiiiiciiiiiiIii",
    "iiiiccliiIiiiiii",
    "iiIiiicciiiiciii",
    "iiiciciiiciiiiii",
    "iiiiiccciiIiiiii",
    "iiIiiiciciiiciic",
    "iciiiciiiiiIiici",
    "iciiiiciiiiiciic",
    "iIiciicccciiiiIi",
    "iiIiiiciciiiciic",
    "iiiiciiiiiIiiici",
    "iIiiciciciiiciic",
    "iiiiiiciciiiiiii",
    "iiIiiciiiiciciIi",
    "iiicciiiiiiiiiii",
    "iIiiiciiiiIiiiii",
]

_FROZEN_WALL_PAL = {
    'w': (60, 100, 160),     # frozen wall base
    'W': (40, 70, 130),      # dark frozen brick
    'l': (90, 140, 200),     # light ice highlight
    'm': (30, 50, 100),      # mortar
    'c': (120, 180, 230),    # crystal sparkle
}

FROZEN_WALL_GRID = [
    "mmmmmmmmmmmmmmmmm",
    "wWwwclcwwWwwclcww",
    "wWwwwlwwwWwwwlwww",
    "wWwwwlwwwWwwwlwww",
    "mmmmmmmmmmmmmmmmm",
    "wlcwwWwwwlcwwWwww",
    "wwlwwWwwwwlwwWwww",
    "wwlwwWwwwwlwwWwww",
    "mmmmmmmmmmmmmmmmm",
    "wWwwclcwwWwwclcww",
    "wWwwwlwwwWwwwlwww",
    "wWwwwlwwwWwwwlwww",
    "mmmmmmmmmmmmmmmmm",
    "wlcwwWwwwlcwwWwww",
    "wwlwwWwwwwlwwWwww",
    "wwlwwWwwwwlwwWwww",
]

_SNOW_PAL = {
    's': (230, 235, 245),    # snow base
    'S': (210, 218, 230),    # shadow
    'l': (245, 248, 255),    # light highlight
    'f': (200, 210, 225),    # frost detail
}

SNOW_GRID = [
    "sSssssssssssssss",
    "sssslssssSsssslss",
    "ssSsssssssssssSss",
    "ssssfsssssssssss",
    "slsssssSssssssss",
    "ssssssssssfsssss",
    "ssSsssssssssslss",
    "ssssslsssssSssss",
    "sSssssfsssssssss",
    "sssssssssSssslss",
    "ssSsssssssssssss",
    "ssssfsssssssSsss",
    "slsssssSssssssss",
    "ssssssssssfsssss",
    "ssSsssslssssssSs",
    "sssssssssSssssss",
]

# ── Cracked Wall tile grid and palette ─────────────────────────────

_CRACKED_WALL_PAL = {
    'w': (130, 130, 120),   # cracked wall base
    'W': (100, 100, 90),    # darker brick
    'l': (150, 150, 140),   # lighter brick
    'm': (80, 80, 75),      # mortar
    'c': (60, 55, 50),      # crack line
    'C': (50, 45, 40),      # deep crack
}

CRACKED_WALL_GRID = [
    "mmmmmmmmmmmmmmmmm",
    "wWwwwllwwWwwwllww",
    "wWwwwllwwWcwwllww",
    "wWwwcllwwWcwwllww",
    "mmmcCmmmmcCmmmmmm",
    "wllwcWwwwllcwWwww",
    "wllwwCwwwllcwWwww",
    "wllwwWcwwllwcWwww",
    "mmmmmmcCmmmcCmmmm",
    "wWwwwlcwwWwcwllww",
    "wWwwwCcwwWwcwllww",
    "wWwwwllcwWcwwllww",
    "mmmmmmmcCcmmmmmmm",
    "wllwwWwwcllwwWwww",
    "wllwwWwwwllwwWwww",
    "wllwwWwwwllwwWwww",
]

# ── Secret Floor tile grid and palette ─────────────────────────────

_SECRET_FLOOR_PAL = {
    'f': (140, 120, 160),   # mystic purple-gray base
    'F': (120, 100, 140),   # darker tile
    'l': (165, 145, 185),   # light accent
    'g': (180, 160, 200),   # glow accent
    's': (100, 80, 120),    # subtle rune marks
}

SECRET_FLOOR_GRID = [
    "fFffflffsFFfffflf",
    "ffffffffffffffff",
    "ffFffffffflfffff",
    "ffffsfffffffffff",
    "flffffffFfffffff",
    "fffffsfffffffgff",
    "fffffffsfgfFffff",
    "ffffffssfflfffff",
    "fFfffffsfgffffff",
    "ffffsfffffffffff",
    "ffffffflffffffff",
    "ffsFffffffffffff",
    "fffffffffFffffff",
    "fflfffsgffffffff",
    "ffsfffffffflFfff",
    "fFffffffffffflff",
]

# ── Animated Water Frame Grids (3 frames) ────────────────────────
# Ripple positions shift between frames to simulate wave motion.

_WATER_PAL_F2 = {
    'w': (45, 95, 195),     # slightly darker base
    'W': (35, 75, 175),     # dark water
    'l': (85, 145, 235),    # light ripple shifted
    'r': (105, 165, 245),   # highlight ripple
}

_WATER_PAL_F3 = {
    'w': (55, 105, 205),    # slightly lighter base
    'W': (42, 82, 185),     # dark water
    'l': (75, 135, 225),    # light ripple shifted
    'r': (95, 155, 240),    # highlight ripple
}

WATER_GRID_F2 = [
    "wWwwwwwwwwWwwwww",
    "wwwwwlrwwwwwWwww",
    "wWwlrrwwwwwwwwww",
    "wwwwwlwwwWwwwwww",
    "wwwWwwwwwwlrwwww",
    "wWwwwlrwwwwwwwww",
    "wwwwwwwlwwwwwWww",
    "wwwWwwwwwlrwwwww",
    "wWwwwwwlrrwwwwWw",
    "wwwwwWwwwlwwwwww",
    "wwwwwwlrwwwwwwww",
    "wWwwlrrwwwWwwwww",
    "wwwwwwlwwwwwwWww",
    "wwwWwwwwwlrwwwww",
    "wWwwwwwwwwwwwwww",
    "wwwwwWwwlrwWwwww",
]

WATER_GRID_F3 = [
    "wwwWwwwlrwWwwwww",
    "wWwwwwwwwwwwwwWw",
    "wwwwwwlrwwwWwwww",
    "wWwwlrrwwwwwwwww",
    "wwwwwwlwwwwwwWww",
    "wwwWwwwwwlrwwwww",
    "wWwwwlrrwwwwwwww",
    "wwwwwwwlwwWwwwww",
    "wWwwwwwwwwwlrwww",
    "wwwwlrrwwwwwwwWw",
    "wWwwwwlwwwwwwwww",
    "wwwwwwwwwlrWwwww",
    "wWwwwlrwwwwwwwww",
    "wwwwwwwwwWwwwwww",
    "wwwWwwlrwwwwwWww",
    "wWwwwwwwwwWwwwww",
]

# ── Animated Lava Frame Grids (3 frames) ─────────────────────────
# Bubbling pattern: yellow highlights shift and pulse.

_LAVA_PAL_F2 = {
    'l': (210, 65, 25),     # lava orange base (brighter)
    'L': (155, 45, 12),     # dark lava
    'y': (255, 220, 70),    # brighter yellow highlight
    'r': (230, 110, 35),    # red-orange
}

_LAVA_PAL_F3 = {
    'l': (190, 55, 18),     # lava orange base (dimmer)
    'L': (140, 35, 8),      # dark lava
    'y': (255, 180, 40),    # dimmer yellow highlight
    'r': (210, 90, 25),     # red-orange
}

LAVA_GRID_F2 = [
    "lLllllyrlllLllll",
    "lllyrlllllllllll",
    "llLllllllllyrLll",
    "llllllyrlllllLll",
    "lrllllllyllllLll",
    "llllyrlllllrlllr",
    "llLlllllyrllllll",
    "lLllyrllllLlllll",
    "lllllllllLllyrll",
    "lyLlllyrllllllll",
    "llllllllllryLlll",
    "lllLlllyrllllrll",
    "lyrllllllllLllll",
    "lLlllyrlllllllLl",
    "lllrlllLlyrllrll",
    "lLllllllllllyrll",
]

LAVA_GRID_F3 = [
    "llLlyrllllLlllll",
    "lllllllyrllrlLll",
    "lLlllllllyrllrll",
    "lllyrllllllLllll",
    "llLlllyrllllllll",
    "lyrlllllllLlyrll",
    "lllLlyrllllllrll",
    "lLlllllllyrLllll",
    "lyrllLlllllllrll",
    "llllllyrlllLllll",
    "llLlllllyrllllrl",
    "lyrlLlllllyrllll",
    "lllllLyrllllllrl",
    "lLyrllllllrlllLl",
    "lllllyrLllllllrl",
    "lLllllllyrllLlll",
]

# ── Animated Waterfall Grids (3 frames) ──────────────────────────
# Vertical flow pattern that scrolls downward.

_WATERFALL_PAL = {
    'w': (60, 120, 210),    # waterfall base
    'W': (40, 90, 180),     # dark flow
    'f': (90, 160, 240),    # foam/mist
    's': (120, 180, 255),   # splash highlight
}

WATERFALL_GRID_F1 = [
    "wWwfwWwfwWwfwWwf",
    "wWwwwWwwwWwwwWww",
    "fwWwfwWwfwWwfwWw",
    "wwWwwwWwwwWwwwWw",
    "wfwWwfwWwfwWwfwW",
    "wwwWwwwWwwwWwwwW",
    "wWwfwWwfwWwfwWwf",
    "wWwwwWwwwWwwwWww",
    "fwWwfwWwfwWwfwWw",
    "wwWwwwWwwwWwwwWw",
    "wfwWwfwWwfwWwfwW",
    "wwwWwwwWwwwWwwwW",
    "wWwfwWwfwWwfwWwf",
    "wWwwwWwwwWwwwWww",
    "sfsfsfsfsfsfsfsf",
    "ssssssssssssssss",
]

WATERFALL_GRID_F2 = [
    "wwWwwwWwwwWwwwWw",
    "wfwWwfwWwfwWwfwW",
    "wwwWwwwWwwwWwwwW",
    "wWwfwWwfwWwfwWwf",
    "wWwwwWwwwWwwwWww",
    "fwWwfwWwfwWwfwWw",
    "wwWwwwWwwwWwwwWw",
    "wfwWwfwWwfwWwfwW",
    "wwwWwwwWwwwWwwwW",
    "wWwfwWwfwWwfwWwf",
    "wWwwwWwwwWwwwWww",
    "fwWwfwWwfwWwfwWw",
    "wwWwwwWwwwWwwwWw",
    "wfwWwfwWwfwWwfwW",
    "fsfsfsfsfsfsfsfs",
    "ssssssssssssssss",
]

WATERFALL_GRID_F3 = [
    "fwWwfwWwfwWwfwWw",
    "wwWwwwWwwwWwwwWw",
    "wfwWwfwWwfwWwfwW",
    "wwwWwwwWwwwWwwwW",
    "wWwfwWwfwWwfwWwf",
    "wWwwwWwwwWwwwWww",
    "fwWwfwWwfwWwfwWw",
    "wwWwwwWwwwWwwwWw",
    "wfwWwfwWwfwWwfwW",
    "wwwWwwwWwwwWwwwW",
    "wWwfwWwfwWwfwWwf",
    "wWwwwWwwwWwwwWww",
    "fwWwfwWwfwWwfwWw",
    "wwWwwwWwwwWwwwWw",
    "sfsfsfsfsfsfsfss",
    "ssssssssssssssss",
]

# ── Grass sway grids (for interaction animation) ─────────────────

_GRASS_SWAY_PAL = {
    'g': (76, 153, 0),
    'G': (60, 130, 0),
    'd': (100, 178, 30),    # brighter accent for sway
    'f': (50, 110, 10),
    's': (90, 168, 20),     # sway highlight
}

GRASS_SWAY_GRID_F1 = [
    "ggggGgggggggggGg",
    "gggsgggdggGggggg",
    "ggGggggggggsgdgg",
    "ggsgdggggggsgggg",
    "gggggsgGgggggggg",
    "ggggggggssdgggGg",
    "gGggggggsggggggg",
    "ggsgggdggssggggg",
    "gggGsggggggsgdgg",
    "ggsggsgsgggggGgg",
    "ggdgsggsggggGggg",
    "gggsgGgggsgggggg",
    "gggggsggdggsgggs",
    "gGgsgsgggggdgggg",
    "gggggsGgggsgggsg",
    "ggggdsggsggGsggg",
]

GRASS_SWAY_GRID_F2 = [
    "gggGsggggsggggGg",
    "gsgggsgdggGgsggg",
    "ggGgsggsggggsdgg",
    "gsgsdggsggggggsg",
    "ggsggsgGsggggggs",
    "gsgggggsggdggsGg",
    "gGgsgggggsggggsg",
    "gsggsgdggsGsggsg",
    "gsgGgsggggsggdgg",
    "gggsgsgsGgsggggs",
    "gsdgggssgsgGgsgg",
    "ggsggGsggsgggsgg",
    "gsggggssdgssgggs",
    "sGgggssggsgdsggg",
    "gsggsgGsgsgggsgG",
    "sgsgdsggsgggGsgg",
]

# ── Animated tile frame data ─────────────────────────────────────
# Maps TileType enum value -> list of (grid, palette) for each frame.
# Frame 0 is the default from _TILE_DATA.

_ANIMATED_TILE_FRAMES = {
    # Water: 3 frames, cycle every 0.5s
    4: [
        (WATER_GRID, _WATER_PAL),
        (WATER_GRID_F2, _WATER_PAL_F2),
        (WATER_GRID_F3, _WATER_PAL_F3),
    ],
    # Lava: 3 frames, cycle every 0.4s
    18: [
        (LAVA_GRID, _LAVA_PAL),
        (LAVA_GRID_F2, _LAVA_PAL_F2),
        (LAVA_GRID_F3, _LAVA_PAL_F3),
    ],
}

# Tile type -> cycle period in seconds
ANIMATED_TILE_PERIODS = {
    4: 0.5,    # Water cycles every 0.5s
    18: 0.4,   # Lava cycles every 0.4s
    28: 0.5,   # Waterfall cycles every 0.5s
}

# Set of tile type values that are animated
ANIMATED_TILE_TYPES = set(ANIMATED_TILE_PERIODS.keys())

_animated_frame_cache = {}


def get_animated_tile_frame(tile_type_value, frame_index):
    """Return the surface for an animated tile at the given frame index.

    Surfaces are cached after first creation.
    """
    frames = _ANIMATED_TILE_FRAMES.get(tile_type_value)
    if not frames:
        return get_tile_surface(tile_type_value)

    frame_index = frame_index % len(frames)
    cache_key = (tile_type_value, frame_index)
    if cache_key in _animated_frame_cache:
        return _animated_frame_cache[cache_key]

    grid, palette = frames[frame_index]
    surf = surface_from_grid(grid, palette, scale=2)
    _animated_frame_cache[cache_key] = surf
    return surf


def get_grass_sway_frame(frame_index):
    """Return a grass tile surface for sway animation (0 or 1)."""
    cache_key = ('grass_sway', frame_index % 2)
    if cache_key in _animated_frame_cache:
        return _animated_frame_cache[cache_key]

    grids = [GRASS_SWAY_GRID_F1, GRASS_SWAY_GRID_F2]
    surf = surface_from_grid(grids[frame_index % 2], _GRASS_SWAY_PAL, scale=2)
    _animated_frame_cache[cache_key] = surf
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
    19: (BARRIER_RED_TILE_GRID, _BARRIER_RED_TILE_PAL),    # BARRIER_RED
    20: (BARRIER_BLUE_TILE_GRID, _BARRIER_BLUE_TILE_PAL),  # BARRIER_BLUE
    21: (BRIDGE_TILE_GRID, _BRIDGE_TILE_PAL),              # BRIDGE
    22: (ICE_GRID, _ICE_PAL),                              # ICE
    23: (CRACKED_ICE_GRID, _CRACKED_ICE_PAL),              # CRACKED_ICE
    24: (FROZEN_WALL_GRID, _FROZEN_WALL_PAL),              # FROZEN_WALL
    25: (SNOW_GRID, _SNOW_PAL),                            # SNOW
    26: (CRACKED_WALL_GRID, _CRACKED_WALL_PAL),            # CRACKED_WALL
    27: (SECRET_FLOOR_GRID, _SECRET_FLOOR_PAL),             # SECRET_FLOOR
    28: (WATERFALL_GRID_F1, _WATERFALL_PAL),                # WATERFALL
}

# Add waterfall animation frames
_ANIMATED_TILE_FRAMES[28] = [
    (WATERFALL_GRID_F1, _WATERFALL_PAL),
    (WATERFALL_GRID_F2, _WATERFALL_PAL),
    (WATERFALL_GRID_F3, _WATERFALL_PAL),
]
