"""Pixel art sprites for Magma Golem (slow tank with lava cracks)."""

from .pixel_art import surface_from_grid

# ── Palette ───────────────────────────────────────────────────────
_PAL = {
    'o': (20, 20, 20),        # dark outline
    'r': (100, 50, 30),       # dark brown/gray rocky body
    'R': (80, 40, 25),        # darker rock
    'c': (200, 60, 20),       # lava crack red
    'C': (255, 120, 30),      # bright lava orange
    'e': (255, 140, 50),      # glowing orange eyes
    'g': (60, 35, 20),        # very dark gray/brown
    '.': None,
}

# ── Down frames ───────────────────────────────────────────────────
_DOWN_0 = [
    "....oooooo....",
    "...orrrrrro...",
    "..orRRRRRRro..",
    "..orReRReRro..",
    ".orRRcccRRRro.",
    ".orRRCCCRRRro.",
    ".orRRcccRRRro.",
    ".orRRRRRRRRro.",
    "..orRRRRRRro..",
    "..orRgcgRRro..",
    "...orRcRRro...",
    "....orrrro....",
    ".....oooo.....",
    "..............",
]

_DOWN_1 = [
    "....oooooo....",
    "...orrrrrro...",
    "..orRRRRRRro..",
    "..orReRReRro..",
    ".orRRcccRRRro.",
    ".orRRCCCRRRro.",
    ".orRRcccRRRro.",
    ".orRRRRRRRRro.",
    "..orRRRRRRro..",
    "..orRgcgRRro..",
    "...orRcRRro...",
    "....orrrro....",
    ".....oooo.....",
    "..............",
]

# ── Up frames ─────────────────────────────────────────────────────
_UP_0 = [
    ".....oooo.....",
    "....orrrro....",
    "...orRcRRro...",
    "..orRgcgRRro..",
    "..orRRRRRRro..",
    ".orRRRRRRRRro.",
    ".orRRcccRRRro.",
    ".orRRCCCRRRro.",
    ".orRRcccRRRro.",
    "..orReRReRro..",
    "..orRRRRRRro..",
    "...orrrrrro...",
    "....oooooo....",
    "..............",
]

_UP_1 = [
    ".....oooo.....",
    "....orrrro....",
    "...orRcRRro...",
    "..orRgcgRRro..",
    "..orRRRRRRro..",
    ".orRRRRRRRRro.",
    ".orRRcccRRRro.",
    ".orRRCCCRRRro.",
    ".orRRcccRRRro.",
    "..orReRReRro..",
    "..orRRRRRRro..",
    "...orrrrrro...",
    "....oooooo....",
    "..............",
]

# ── Left frames ───────────────────────────────────────────────────
_LEFT_0 = [
    "....oooooo....",
    "...orrrrrro...",
    "..orRRRRRRro..",
    "..orReRRRRro..",
    ".orRRcRRRRRro.",
    ".orRRCcRRRRro.",
    ".orRRcRRRRRro.",
    ".orRRRRRRRRro.",
    "..orRRgcRRro..",
    "..orRRRcRRro..",
    "...orRRRRro...",
    "....orrrro....",
    ".....oooo.....",
    "..............",
]

_LEFT_1 = [
    "....oooooo....",
    "...orrrrrro...",
    "..orRRRRRRro..",
    "..orReRRRRro..",
    ".orRRcRRRRRro.",
    ".orRRCcRRRRro.",
    ".orRRcRRRRRro.",
    ".orRRRRRRRRro.",
    "..orRRgcRRro..",
    "..orRRRcRRro..",
    "...orRRRRro...",
    "....orrrro....",
    ".....oooo.....",
    "..............",
]

# ── Right frames ──────────────────────────────────────────────────
_RIGHT_0 = [
    "....oooooo....",
    "...orrrrrro...",
    "..orRRRRRRro..",
    "..orRRRReRro..",
    ".orRRRRRcRRro.",
    ".orRRRRcCRRro.",
    ".orRRRRRcRRro.",
    ".orRRRRRRRRro.",
    "..orRRcgRRro..",
    "..orRRcRRRro..",
    "...orRRRRro...",
    "....orrrro....",
    ".....oooo.....",
    "..............",
]

_RIGHT_1 = [
    "....oooooo....",
    "...orrrrrro...",
    "..orRRRRRRro..",
    "..orRRRReRro..",
    ".orRRRRRcRRro.",
    ".orRRRRcCRRro.",
    ".orRRRRRcRRro.",
    ".orRRRRRRRRro.",
    "..orRRcgRRro..",
    "..orRRcRRRro..",
    "...orRRRRro...",
    "....orrrro....",
    ".....oooo.....",
    "..............",
]

# ── Build surfaces ────────────────────────────────────────────────
_frames_cache = None


def get_magma_golem_frames():
    """Return dict of {direction: [frame0, frame1]} for the magma golem."""
    global _frames_cache
    if _frames_cache is not None:
        return _frames_cache

    _frames_cache = {
        "down":  [surface_from_grid(g, _PAL, 2) for g in (_DOWN_0, _DOWN_1)],
        "up":    [surface_from_grid(g, _PAL, 2) for g in (_UP_0, _UP_1)],
        "left":  [surface_from_grid(g, _PAL, 2) for g in (_LEFT_0, _LEFT_1)],
        "right": [surface_from_grid(g, _PAL, 2) for g in (_RIGHT_0, _RIGHT_1)],
    }
    return _frames_cache


# ── Magma Projectile ──────────────────────────────────────────────
_PROJECTILE = [
    "..oooo..",
    ".oCCCCo.",
    "oCcccCCo",
    "oCccccCo",
    "oCccccCo",
    "oCCcccCo",
    ".oCCCCo.",
    "..oooo..",
]

_proj_cache = None


def get_magma_projectile_sprite():
    """Return a magma projectile sprite."""
    global _proj_cache
    if _proj_cache is not None:
        return _proj_cache

    _proj_cache = surface_from_grid(_PROJECTILE, _PAL, 1)
    return _proj_cache
