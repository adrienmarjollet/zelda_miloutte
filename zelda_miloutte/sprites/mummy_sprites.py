"""Pixel art sprites for Mummy (slow tank enemy)."""

from .pixel_art import surface_from_grid

# ── Palette ───────────────────────────────────────────────────────
_PAL = {
    'o': (20, 20, 20),        # dark outline
    'w': (200, 190, 150),     # light wrapping (aged linen)
    'W': (160, 150, 115),     # medium wrapping
    'x': (120, 110, 85),      # dark wrapping (stained)
    'X': (90, 80, 60),        # very dark wrapping (dirty)
    'f': (60, 50, 35),        # rotting flesh (exposed)
    'F': (40, 30, 20),        # very dark rotted flesh
    'b': (80, 70, 50),        # bone showing through
    'e': (220, 255, 80),      # glowing yellow eyes
    'E': (100, 180, 70),      # eerie green eye glow
    'g': (180, 140, 50),      # golden hieroglyph
    'G': (140, 100, 30),      # dark hieroglyph
    's': (50, 45, 35),        # deep shadow
    't': (140, 130, 100),     # trailing bandage
    '.': None,
}

# ── Down frames ───────────────────────────────────────────────────
_DOWN_0 = [
    "....oooooo....",
    "...owwXwwwo...",
    "..owxWfFwWxo..",
    "..oxWeooEwxo..",
    ".oxWxFffFxWxo.",
    ".owXwbFFbwXwo.",
    ".owWxgGGxWWwo.",
    ".owWWxXxWWWwo.",
    "oowWWWWWWWWoo.",
    "oxWWWxoxWWWxo.",
    ".oxWWxfxWWxo..",
    "..owWxXxWwo...",
    "..oowooowoo...",
    "....ot..to....",
]

_DOWN_1 = [
    "....oooooo....",
    "...owwXwwwo...",
    "..owxWfFwWxo..",
    "..oxWeooEwxo..",
    ".oxWxFffFxWxo.",
    ".owXwbFFbwXwo.",
    ".owWxgGGxWWwo.",
    ".owWWxXxWWWwo.",
    ".oowWWWWWWoo..",
    ".oxWWWxoxWWxo.",
    "..oxWWxfxWxo..",
    "...owWxXxwo...",
    "...oowooowo...",
    ".....ot..to...",
]

# ── Up frames ─────────────────────────────────────────────────────
_UP_0 = [
    "....ot..to....",
    "..oowooowoo...",
    "..owWxXxWwo...",
    ".oxWWxfxWWxo..",
    "oxWWWxoxWWWxo.",
    "oowWWWWWWWWoo.",
    ".owWWWxXxWWwo.",
    ".owWWxXXxWWwo.",
    ".owXwsFsFwXwo.",
    ".oxWxFffFxWxo.",
    "..oxWxssxWxo..",
    "..owxWfFwWxo..",
    "...owwXwwwo...",
    "....oooooo....",
]

_UP_1 = [
    ".....ot..to...",
    "...oowooowo...",
    "...owWxXxwo...",
    "..oxWWxfxWxo..",
    ".oxWWWxoxWWxo.",
    ".oowWWWWWWoo..",
    ".owWWWxXxWWwo.",
    ".owWWxXXxWWwo.",
    ".owXwsFsFwXwo.",
    ".oxWxFffFxWxo.",
    "..oxWxssxWxo..",
    "..owxWfFwWxo..",
    "...owwXwwwo...",
    "....oooooo....",
]

# ── Left frames ───────────────────────────────────────────────────
_LEFT_0 = [
    "....oooooo....",
    "...owwXwwwo...",
    "..owxWfFwWxo..",
    "..oxWeosxWxo..",
    "ooxWxFfxWWxo..",
    "oxXwbFxgGxwo..",
    "owWxXxWWWWwo..",
    "owWWWWWWWWwo..",
    "owWWWWWWWWwo..",
    ".oxWWxoxWWxo..",
    "..oxWxfxWxo...",
    "...owWxXwo....",
    "...oowoooo....",
    ".....ot.......",
]

_LEFT_1 = [
    "....oooooo....",
    "...owwXwwwo...",
    "..owxWfFwWxo..",
    "..oxWeosxWxo..",
    ".ooxWxFfxWWxo.",
    ".oxXwbFxgGxwo.",
    ".owWxXxWWWWwo.",
    ".owWWWWWWWWwo.",
    ".owWWWWWWWWwo.",
    "..oxWWxoxWWxo.",
    "...oxWxfxWxo..",
    "....owWxXwo...",
    "....oowoooo...",
    "......ot......",
]

# ── Right frames ──────────────────────────────────────────────────
_RIGHT_0 = [
    "....oooooo....",
    "...owwXwwwo...",
    "..oxWfFwWxwo..",
    "..oxWxsoEwxo..",
    "..oxWWxfFxWxoo",
    "..owxGGgxFbwXo",
    "..owWWWWxXxWwo",
    "..owWWWWWWWWwo",
    "..owWWWWWWWWwo",
    "..oxWWxoxWWxo.",
    "...oxWxfxWxo..",
    "....owXxWwo...",
    "....oooowoo...",
    ".......to.....",
]

_RIGHT_1 = [
    "....oooooo....",
    "...owwXwwwo...",
    "..oxWfFwWxwo..",
    "..oxWxsoEwxo..",
    ".oxWWxfFxWxoo.",
    ".owxGGgxFbwXo.",
    ".owWWWWxXxWwo.",
    ".owWWWWWWWWwo.",
    ".owWWWWWWWWwo.",
    ".oxWWxoxWWxo..",
    "..oxWxfxWxo...",
    "...owXxWwo....",
    "...oooowoo....",
    "......to......",
]

# ── Build surfaces ────────────────────────────────────────────────
_frames_cache = None


def get_mummy_frames():
    """Return dict of {direction: [frame0, frame1]} for the mummy."""
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
