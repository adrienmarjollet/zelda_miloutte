"""Pixel art sprites for puzzle entities: push block, pressure plate, crystal switch, torch, barriers."""

from zelda_miloutte.sprites.pixel_art import surface_from_grid

# ── Push Block (16x16 grid at scale 2 = 32x32) ──────────────────

_PUSH_BLOCK_PAL = {
    'b': (100, 100, 110),   # base stone
    'B': (80, 80, 90),      # dark stone
    'd': (60, 60, 70),      # shadow/edge
    'l': (130, 130, 140),   # highlight
    'c': (70, 70, 80),      # crack detail
    'a': (110, 105, 100),   # accent
    '.': None,
}

_PUSH_BLOCK_GRID = [
    "dddddddddddddddd",
    "dlllllllllllllllBd",
    "dlbbbbbbbbbbbbblBd",
    "dlbbbbbbbbbbbbblBd",
    "dlbblbbbbbbblbblBd",
    "dlbbbbbbcbbbbblBd",
    "dlbbbbbbcbbbbblBd",
    "dlbbbbbbbbbbbbblBd",
    "dlbbbaabbbbbbbblBd",
    "dlbbbaabbbbbbbblBd",
    "dlbbbbbbbbcbbblBd",
    "dlbbbbbbbbcbbblBd",
    "dlbblbbbbbbblbblBd",
    "dlbbbbbbbbbbbbblBd",
    "dlBBBBBBBBBBBBBBBd",
    "dddddddddddddddd",
]

# ── Pressure Plate (16x16 grid at scale 2 = 32x32) ──────────────

_PLATE_PAL = {
    'f': (160, 140, 110),   # floor base
    'p': (140, 130, 100),   # plate border
    'P': (120, 110, 85),    # plate surface
    'h': (170, 155, 130),   # highlight
    'd': (100, 90, 70),     # dark edge
    's': (90, 80, 65),      # shadow
    '.': None,
}

_PLATE_UP_GRID = [
    "ffffffffffffffff",
    "ffffffffffffffff",
    "ffdddddddddddff",
    "fdppppppppppppdff",
    "fdpPPPPPPPPPPpdf",
    "fdpPhPPPPPhPPpdf",
    "fdpPPPPPPPPPPpdf",
    "fdpPPPPPPPPPPpdf",
    "fdpPPPPPPPPPPpdf",
    "fdpPPhPPPPPPPpdf",
    "fdpPPPPPPPhPPpdf",
    "fdpPPPPPPPPPPpdf",
    "ffdppppppppppdsf",
    "fffsssssssssssff",
    "ffffffffffffffff",
    "ffffffffffffffff",
]

_PLATE_DOWN_GRID = [
    "ffffffffffffffff",
    "ffffffffffffffff",
    "ffffffffffffffff",
    "ffssssssssssssff",
    "fsddddddddddddsf",
    "fsdPPPPPPPPPPdsf",
    "fsdPPPPPPPPPPdsf",
    "fsdPPPPPPPPPPdsf",
    "fsdPPPPPPPPPPdsf",
    "fsdPPPPPPPPPPdsf",
    "fsdPPPPPPPPPPdsf",
    "fsddddddddddddff",
    "ffffffffffffffff",
    "ffffffffffffffff",
    "ffffffffffffffff",
    "ffffffffffffffff",
]

# ── Crystal Switch (14x14 grid at scale 2 = 28x28) ──────────────

_SWITCH_PAL_ON = {
    'b': (80, 80, 90),      # base stone
    'B': (60, 60, 70),      # dark stone
    'c': (100, 200, 255),   # crystal (blue)
    'C': (60, 150, 220),    # crystal dark
    'g': (180, 230, 255),   # crystal glow
    's': (50, 50, 60),      # shadow
    '.': None,
}

_SWITCH_PAL_OFF = {
    'b': (80, 80, 90),      # base stone
    'B': (60, 60, 70),      # dark stone
    'c': (220, 80, 80),     # crystal (red)
    'C': (180, 50, 50),     # crystal dark
    'g': (255, 150, 150),   # crystal glow
    's': (50, 50, 60),      # shadow
    '.': None,
}

_SWITCH_GRID = [
    "..............",
    "..BBBBBBBBbb..",
    ".BbbbbbbbbBb..",
    ".Bb......bBb..",
    ".Bb..CC..bBb..",
    ".Bb.CccC.bBb..",
    ".Bb.CcgC.bBb..",
    ".Bb.CccC.bBb..",
    ".Bb..CC..bBb..",
    ".Bb......bBb..",
    ".BbbbbbbbbBb..",
    "..BBBBBBBBbb..",
    "...ssssssss...",
    "..............",
]

# ── Torch (14x14 grid at scale 2 = 28x28) ────────────────────

_TORCH_UNLIT_PAL = {
    'b': (100, 60, 20),     # bracket
    'B': (80, 45, 15),      # dark bracket
    'w': (139, 90, 43),     # wood
    'W': (110, 70, 30),     # dark wood
    't': (60, 50, 40),      # wick (cold)
    '.': None,
}

_TORCH_LIT_PAL = {
    'b': (100, 60, 20),     # bracket
    'B': (80, 45, 15),      # dark bracket
    'w': (139, 90, 43),     # wood
    'W': (110, 70, 30),     # dark wood
    'f': (255, 200, 50),    # flame bright
    'F': (255, 140, 30),    # flame mid
    'r': (200, 60, 20),     # flame dark
    'g': (255, 240, 130),   # flame glow
    '.': None,
}

_TORCH_UNLIT_GRID = [
    "..............",
    "..............",
    "......tt......",
    "......tt......",
    "..............",
    "..............",
    ".....bwwb.....",
    ".....bwwb.....",
    ".....BWWb.....",
    ".....BWWb.....",
    ".....BWWb.....",
    ".....BWWb.....",
    "....BBBBBb....",
    "..............",
]

_TORCH_LIT_GRID = [
    "......gf......",
    ".....gffg.....",
    "....gfFFfg....",
    "....fFrrFf....",
    ".....FrrF.....",
    "......rr......",
    ".....bwwb.....",
    ".....bwwb.....",
    ".....BWWb.....",
    ".....BWWb.....",
    ".....BWWb.....",
    ".....BWWb.....",
    "....BBBBBb....",
    "..............",
]

# ── Barrier Red (16x16 grid at scale 2 = 32x32) ─────────────────

_BARRIER_RED_PAL = {
    'r': (200, 50, 50),     # red crystal
    'R': (150, 30, 30),     # dark red
    'g': (255, 100, 100),   # red glow
    'd': (100, 20, 20),     # dark base
    'f': (160, 140, 110),   # floor (transparent peek)
    '.': None,
}

_BARRIER_RED_GRID = [
    "ddRRRRRRRRRRRRdd",
    "dRrrrrrrrrrrrrRd",
    "RrrgrrrrrrrgrrR",
    "RrrrrrgrrrrrrrR",
    "RrrrrrrrrrgrrR",
    "RrgrrrrrrrrrrR",
    "RrrrrgrrrrgrrrR",
    "RrrrrrrrrrrrrR",
    "RrrrrgrrrrrrrR",
    "RrgrrrrrrrgrrR",
    "RrrrrrrrrrrrrrR",
    "RrrrrgrrrrgrrrR",
    "RrrrrrrrrrrrrR",
    "RrrgrrrrrrrgrrR",
    "dRrrrrrrrrrrrrRd",
    "ddRRRRRRRRRRRRdd",
]

# ── Barrier Blue (16x16 grid at scale 2 = 32x32) ────────────────

_BARRIER_BLUE_PAL = {
    'r': (50, 100, 200),    # blue crystal
    'R': (30, 60, 150),     # dark blue
    'g': (100, 160, 255),   # blue glow
    'd': (20, 40, 100),     # dark base
    '.': None,
}

_BARRIER_BLUE_GRID = [
    "ddRRRRRRRRRRRRdd",
    "dRrrrrrrrrrrrrRd",
    "RrrgrrrrrrrgrrR",
    "RrrrrrgrrrrrrrR",
    "RrrrrrrrrrgrrR",
    "RrgrrrrrrrrrrR",
    "RrrrrgrrrrgrrrR",
    "RrrrrrrrrrrrrR",
    "RrrrrgrrrrrrrR",
    "RrgrrrrrrrgrrR",
    "RrrrrrrrrrrrrrR",
    "RrrrrgrrrrgrrrR",
    "RrrrrrrrrrrrrR",
    "RrrgrrrrrrrgrrR",
    "dRrrrrrrrrrrrrRd",
    "ddRRRRRRRRRRRRdd",
]

# ── Bridge (16x16 grid at scale 2 = 32x32) ──────────────────────

_BRIDGE_PAL = {
    'w': (139, 90, 43),     # wood plank
    'W': (120, 75, 35),     # dark plank
    'b': (100, 60, 20),     # beam
    'g': (50, 40, 30),      # gap between planks
    '.': None,
}

_BRIDGE_GRID = [
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

# ── Cache ────────────────────────────────────────────────────────

_cache = {}


def _get_cached(key, grid, palette, scale=2):
    if key not in _cache:
        _cache[key] = surface_from_grid(grid, palette, scale)
    return _cache[key]


def get_push_block():
    """Return push block sprite (32x32)."""
    return _get_cached('push_block', _PUSH_BLOCK_GRID, _PUSH_BLOCK_PAL, 2)


def get_pressure_plate_up():
    """Return pressure plate (raised/inactive) sprite (32x32)."""
    return _get_cached('plate_up', _PLATE_UP_GRID, _PLATE_PAL, 2)


def get_pressure_plate_down():
    """Return pressure plate (pressed/active) sprite (32x32)."""
    return _get_cached('plate_down', _PLATE_DOWN_GRID, _PLATE_PAL, 2)


def get_crystal_switch_on():
    """Return crystal switch (blue/on state) sprite (28x28)."""
    return _get_cached('switch_on', _SWITCH_GRID, _SWITCH_PAL_ON, 2)


def get_crystal_switch_off():
    """Return crystal switch (red/off state) sprite (28x28)."""
    return _get_cached('switch_off', _SWITCH_GRID, _SWITCH_PAL_OFF, 2)


def get_torch_unlit():
    """Return unlit torch sprite (28x28)."""
    return _get_cached('torch_unlit', _TORCH_UNLIT_GRID, _TORCH_UNLIT_PAL, 2)


def get_torch_lit():
    """Return lit torch sprite (28x28)."""
    return _get_cached('torch_lit', _TORCH_LIT_GRID, _TORCH_LIT_PAL, 2)


def get_barrier_red():
    """Return red barrier tile sprite (32x32)."""
    return _get_cached('barrier_red', _BARRIER_RED_GRID, _BARRIER_RED_PAL, 2)


def get_barrier_blue():
    """Return blue barrier tile sprite (32x32)."""
    return _get_cached('barrier_blue', _BARRIER_BLUE_GRID, _BARRIER_BLUE_PAL, 2)


def get_bridge():
    """Return bridge tile sprite (32x32)."""
    return _get_cached('bridge', _BRIDGE_GRID, _BRIDGE_PAL, 2)
