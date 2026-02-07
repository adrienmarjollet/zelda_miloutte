"""Pixel art sprites for Mummy (slow tank enemy)."""

from .pixel_art import surface_from_grid

# ── Palette ───────────────────────────────────────────────────────
_PAL = {
    'o': (20, 20, 20),        # dark outline
    'w': (180, 170, 140),     # light wrapping
    'W': (140, 130, 100),     # darker wrapping
    'd': (100, 90, 70),       # dark shadow areas
    'D': (60, 50, 40),        # very dark shadow
    'e': (200, 200, 50),      # glowing yellow eyes
    'E': (150, 180, 60),      # green eye glow
    'b': (120, 110, 85),      # body base
    '.': None,
}

# ── Down frames ───────────────────────────────────────────────────
_DOWN_0 = [
    "....oooooo....",
    "...owwwwwwo...",
    "..owwwwwwwwo..",
    "..owWWWWWWwo..",
    ".owWWdddWWWwo.",
    ".owWWeooEWWwo.",
    ".owWWdooddWwo.",
    ".owWWWWWWWWwo.",
    ".owWWWWWWWWwo.",
    ".owWWWWWWWWwo.",
    "..owWWWWWWwo..",
    "..owWWWWWWwo..",
    "...oowoowoo...",
    ".....o..o.....",
]

_DOWN_1 = [
    "....oooooo....",
    "...owwwwwwo...",
    "..owwwwwwwwo..",
    "..owWWWWWWwo..",
    ".owWWdddWWWwo.",
    ".owWWeooEWWwo.",
    ".owWWdooddWwo.",
    ".owWWWWWWWWwo.",
    ".owWWWWWWWWwo.",
    ".owWWWWWWWWwo.",
    "..owWWWWWWwo..",
    "..owWWWWWWwo..",
    "...oowoowoo...",
    "....o....o....",
]

# ── Up frames ─────────────────────────────────────────────────────
_UP_0 = [
    ".....o..o.....",
    "...oowoowoo...",
    "..owWWWWWWwo..",
    "..owWWWWWWwo..",
    ".owWWWWWWWWwo.",
    ".owWWWWWWWWwo.",
    ".owWWWWWWWWwo.",
    ".owWWddddWWwo.",
    ".owWWWWWWWWwo.",
    ".owWWWWWWWWwo.",
    "..owWWWWWWwo..",
    "..owwwwwwwwo..",
    "...owwwwwwo...",
    "....oooooo....",
]

_UP_1 = [
    "....o....o....",
    "...oowoowoo...",
    "..owWWWWWWwo..",
    "..owWWWWWWwo..",
    ".owWWWWWWWWwo.",
    ".owWWWWWWWWwo.",
    ".owWWWWWWWWwo.",
    ".owWWddddWWwo.",
    ".owWWWWWWWWwo.",
    ".owWWWWWWWWwo.",
    "..owWWWWWWwo..",
    "..owwwwwwwwo..",
    "...owwwwwwo...",
    "....oooooo....",
]

# ── Left frames ───────────────────────────────────────────────────
_LEFT_0 = [
    "....oooooo....",
    "...owwwwwwo...",
    "..owwwwwwwwo..",
    "..owWWWWWWwo..",
    ".owWWWdWWWwo..",
    ".owWWeoWWWwo..",
    ".owWWWdWWWwo..",
    ".owWWWWWWWwo..",
    ".owWWWWWWWwo..",
    ".owWWWWWWWwo..",
    "..owWWWWWwo...",
    "..owWWWWWwo...",
    "...oowoowo....",
    ".....o..o.....",
]

_LEFT_1 = [
    "....oooooo....",
    "...owwwwwwo...",
    "..owwwwwwwwo..",
    "..owWWWWWWwo..",
    ".owWWWdWWWwo..",
    ".owWWeoWWWwo..",
    ".owWWWdWWWwo..",
    ".owWWWWWWWwo..",
    ".owWWWWWWWwo..",
    ".owWWWWWWWwo..",
    "..owWWWWWwo...",
    "..owWWWWWwo...",
    "...oowoowo....",
    "....o....o....",
]

# ── Right frames ──────────────────────────────────────────────────
_RIGHT_0 = [
    "....oooooo....",
    "...owwwwwwo...",
    "..owwwwwwwwo..",
    "..owWWWWWWwo..",
    "..owWWWdWWWwo.",
    "..owWWWoEWWwo.",
    "..owWWWdWWWwo.",
    "..owWWWWWWWwo.",
    "..owWWWWWWWwo.",
    "..owWWWWWWWwo.",
    "...owWWWWWwo..",
    "...owWWWWWwo..",
    "....owoowoo...",
    ".....o..o.....",
]

_RIGHT_1 = [
    "....oooooo....",
    "...owwwwwwo...",
    "..owwwwwwwwo..",
    "..owWWWWWWwo..",
    "..owWWWdWWWwo.",
    "..owWWWoEWWwo.",
    "..owWWWdWWWwo.",
    "..owWWWWWWWwo.",
    "..owWWWWWWWwo.",
    "..owWWWWWWWwo.",
    "...owWWWWWwo..",
    "...owWWWWWwo..",
    "....owoowoo...",
    "....o....o....",
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
