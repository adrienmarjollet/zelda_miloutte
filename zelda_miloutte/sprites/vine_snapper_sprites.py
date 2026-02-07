"""Pixel art sprites for Vine Snapper (stationary plant enemy)."""

from .pixel_art import surface_from_grid

# ── Palette ───────────────────────────────────────────────────────
_PAL = {
    'o': (20, 20, 20),        # dark outline
    'g': (30, 130, 30),       # medium green body
    'G': (20, 90, 20),        # darker green
    'l': (50, 170, 50),       # light green highlight
    'L': (80, 200, 80),       # lime green
    'f': (15, 70, 15),        # forest dark green
    'e': (40, 150, 60),       # emerald green
    'r': (180, 30, 30),       # red thorns
    'R': (220, 60, 60),       # bright red
    'p': (220, 100, 120),     # pink mouth interior
    'P': (255, 140, 160),     # light pink flesh
    'w': (240, 240, 240),     # white teeth
    'W': (200, 200, 200),     # off-white teeth shadow
    'y': (230, 220, 80),      # yellow pollen
    'b': (90, 60, 30),        # brown stem
    'B': (70, 45, 20),        # dark brown
    'd': (40, 60, 30),        # dark green base
    'D': (25, 40, 20),        # very dark green
    's': (80, 50, 20),        # soil brown
    '.': None,
}

# Vine Snapper is stationary, so we just need "down" direction with 2 frames for snap animation
# Frame 0: Mouth slightly open, idle/waiting
_DOWN_0 = [
    ".....owwwo....",
    "....owPPPwo...",
    "...owPppPwo...",
    "..owPprrrPwo..",
    ".owLggpggLwo..",
    ".oLlggggglLo..",
    "oelegggggleo..",
    "oleggggggleo..",
    ".oeggggggeo...",
    ".obgggggbo....",
    ".obbbgbbo.....",
    "..obBbBo......",
    "..osssso......",
    "...oooo.......",
]

# Frame 1: Mouth WIDE open, snapping with teeth visible
_DOWN_1 = [
    "...owwwwwwo...",
    "..owWwwwWwo...",
    ".owPPppppPwo..",
    ".owPprrrpPwo..",
    "owLggrrrggLwo.",
    "oLlggrrrggleo.",
    "oelggpppggleo.",
    "oeggggpggggeo.",
    ".oeggggggeo...",
    ".obgggggbo....",
    ".obbbgbbo.....",
    "..obBbBo......",
    "..osssso......",
    "...oooo.......",
]

# Thorn projectile sprite (sharp barbed spine with trailing vine)
_THORN = [
    "...owo...",
    "..owWo...",
    ".owWWo...",
    "owRRRoo..",
    ".orRRgo..",
    "..orReo..",
    "...orgo..",
    "....oo...",
]

_THORN_PAL = {
    'o': (20, 20, 20),        # dark outline
    'w': (240, 240, 240),     # white sharp tip
    'W': (200, 200, 200),     # off-white
    'r': (180, 30, 30),       # red thorn body
    'R': (220, 60, 60),       # bright red
    'g': (30, 130, 30),       # green vine trail
    'e': (40, 150, 60),       # emerald green
    '.': None,
}

# ── Build surfaces ────────────────────────────────────────────────
_frames_cache = None
_thorn_cache = None


def get_vine_snapper_frames():
    """Return dict of {direction: [frame0, frame1]} for the vine snapper."""
    global _frames_cache
    if _frames_cache is not None:
        return _frames_cache

    # Vine Snapper only has "down" facing (it's a plant)
    frames = [surface_from_grid(g, _PAL, 2) for g in (_DOWN_0, _DOWN_1)]
    _frames_cache = {
        "down": frames,
        "up": frames,     # Use same frames for all directions
        "left": frames,
        "right": frames,
    }
    return _frames_cache


def get_thorn_sprite():
    """Return the thorn projectile sprite."""
    global _thorn_cache
    if _thorn_cache is not None:
        return _thorn_cache

    _thorn_cache = surface_from_grid(_THORN, _THORN_PAL, 2)
    return _thorn_cache
