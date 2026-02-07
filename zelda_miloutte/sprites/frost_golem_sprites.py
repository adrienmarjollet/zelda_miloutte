"""Pixel art sprites for Frost Golem (slow, tanky ice enemy)."""

from .pixel_art import surface_from_grid

# ── Palette ───────────────────────────────────────────────────────
_PAL = {
    'o': (20, 30, 50),        # dark outline
    'i': (80, 140, 200),      # ice body
    'I': (50, 100, 160),      # dark ice
    'c': (140, 200, 240),     # crystal highlight
    'C': (180, 230, 255),     # bright crystal
    'e': (255, 100, 60),      # glowing orange eyes
    'E': (200, 60, 30),       # eye edge
    'r': (60, 110, 170),      # rock/core dark
    'R': (90, 150, 200),      # rock lighter
    '.': None,
}

# ── Down frames ───────────────────────────────────────────────────
_DOWN_0 = [
    "....oooooo....",
    "...oiiiiiio...",
    "..oiiIIIIiio..",
    "..oiEeiiEeio..",
    ".oiiiIIIIiiio.",
    ".oiiicIIciIio.",
    ".oiiiIIIIiiio.",
    "..oiiIIIIiio..",
    "..orrRRRRrro..",
    ".orrRRRRRRrro.",
    ".orrRRIIRRrro.",
    ".orrRRRRRRrro.",
    "..orrRRRRrro..",
    "...oooooooo...",
]

_DOWN_1 = [
    "....oooooo....",
    "...oiiiiiio...",
    "..oiiIIIIiio..",
    "..oiEeiiEeio..",
    ".oiiiIIIIiiio.",
    ".oiiicIIciIio.",
    ".oiiiIIIIiiio.",
    "..oiiIIIIiio..",
    "..orrRRRRrro..",
    ".orrRRRRRRrro.",
    ".orrRIIIRRrro.",
    ".orrRRRRRRrro.",
    "..orrRRRRrro..",
    "...oooooooo...",
]

# ── Up frames ─────────────────────────────────────────────────────
_UP_0 = [
    "...oooooooo...",
    "..orrRRRRrro..",
    ".orrRRRRRRrro.",
    ".orrRRIIRRrro.",
    ".orrRRRRRRrro.",
    "..orrRRRRrro..",
    "..oiiIIIIiio..",
    ".oiiiIIIIiiio.",
    ".oiiicIIciIio.",
    ".oiiiIIIIiiio.",
    "..oiiiiiiiio..",
    "..oiiIIIIiio..",
    "...oiiiiiio...",
    "....oooooo....",
]

_UP_1 = [
    "...oooooooo...",
    "..orrRRRRrro..",
    ".orrRRRRRRrro.",
    ".orrRIIIRRrro.",
    ".orrRRRRRRrro.",
    "..orrRRRRrro..",
    "..oiiIIIIiio..",
    ".oiiiIIIIiiio.",
    ".oiiicIIciIio.",
    ".oiiiIIIIiiio.",
    "..oiiiiiiiio..",
    "..oiiIIIIiio..",
    "...oiiiiiio...",
    "....oooooo....",
]

# ── Left frames ───────────────────────────────────────────────────
_LEFT_0 = [
    "....oooo......",
    "...oiiiio.....",
    "..oiiIIiio....",
    "..oiEeIeiioo..",
    ".oiiicIIiiRro.",
    ".oiiiIIiirRro.",
    ".oiiicIIiiRro.",
    "..oiiIIIiiroo.",
    "..orrRRRRrro..",
    ".orrRRRRRrro..",
    ".orrRIIRRrro..",
    ".orrRRRRRrro..",
    "..orrRRRrro...",
    "...oooooooo...",
]

_LEFT_1 = [
    "....oooo......",
    "...oiiiio.....",
    "..oiiIIiio....",
    "..oiEeIeiioo..",
    ".oiiicIIiiRro.",
    ".oiiiIIiirRro.",
    ".oiiicIIiiRro.",
    "..oiiIIIiiroo.",
    "..orrRRRRrro..",
    ".orrRRRRRrro..",
    ".orrRRIRRrro..",
    ".orrRRRRRrro..",
    "..orrRRRrro...",
    "...oooooooo...",
]

# ── Right frames ──────────────────────────────────────────────────
_RIGHT_0 = [
    "......oooo....",
    ".....oiiiio...",
    "....oiiIIiio..",
    "..ooiieIeEio..",
    ".orRiiIIciiio.",
    ".orRriiIIiiio.",
    ".orRiiIIciiio.",
    "..ooriIIIiio..",
    "..orrRRRRrro..",
    "..orrRRRRRrro.",
    "..orrRRIIRrro.",
    "..orrRRRRRrro.",
    "...orrRRRrro..",
    "...oooooooo...",
]

_RIGHT_1 = [
    "......oooo....",
    ".....oiiiio...",
    "....oiiIIiio..",
    "..ooiieIeEio..",
    ".orRiiIIciiio.",
    ".orRriiIIiiio.",
    ".orRiiIIciiio.",
    "..ooriIIIiio..",
    "..orrRRRRrro..",
    "..orrRRRRRrro.",
    "..orrRRRIRrro.",
    "..orrRRRRRrro.",
    "...orrRRRrro..",
    "...oooooooo...",
]

# ── Build surfaces ────────────────────────────────────────────────
_frames_cache = None


def get_frost_golem_frames():
    """Return dict of {direction: [frame0, frame1]} for the frost golem."""
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
