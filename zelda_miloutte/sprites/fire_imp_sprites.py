"""Pixel art sprites for Fire Imp (fast melee enemy with fire trail)."""

from .pixel_art import surface_from_grid

# ── Palette ───────────────────────────────────────────────────────
_PAL = {
    'o': (20, 20, 20),        # dark outline
    'r': (220, 80, 30),       # red body
    'R': (180, 50, 20),       # darker red
    'f': (255, 200, 50),      # yellow flame
    'F': (255, 120, 30),      # orange flame
    'e': (10, 10, 10),        # eyes
    'h': (255, 100, 20),      # hot spots
    '.': None,
}

# ── Down frames ───────────────────────────────────────────────────
_DOWN_0 = [
    "....oooooo....",
    "...orrrrrro...",
    "..orrRRRRrro..",
    "..orReeeeRro..",
    ".orrRRRRRRrro.",
    ".orrRRhhRRrro.",
    ".orrRRRRRRrro.",
    "..orrRRRRrro..",
    "..oFrrrrrFo...",
    "...oFfffFo....",
    "....offfoo....",
    ".....oFo......",
    "......o.......",
    "..............",
]

_DOWN_1 = [
    "....oooooo....",
    "...orrrrrro...",
    "..orrRRRRrro..",
    "..orReeeeRro..",
    ".orrRRRRRRrro.",
    ".orrRRhhRRrro.",
    ".orrRRRRRRrro.",
    "..orrRRRRrro..",
    "...oFrrrFo....",
    "....oFfFo.....",
    "...oofffoo....",
    "....oFo.......",
    ".....o........",
    "..............",
]

# ── Up frames ─────────────────────────────────────────────────────
_UP_0 = [
    "......o.......",
    ".....oFo......",
    "....offfoo....",
    "...oFfffFo....",
    "..oFrrrrrFo...",
    "..orrRRRRrro..",
    ".orrRRRRRRrro.",
    ".orrRRhhRRrro.",
    ".orrRRRRRRrro.",
    "..orReeeeRro..",
    "..orrRRRRrro..",
    "...orrrrrro...",
    "....oooooo....",
    "..............",
]

_UP_1 = [
    ".....o........",
    "....oFo.......",
    "...oofffoo....",
    "....oFfFo.....",
    "...oFrrrFo....",
    "..orrRRRRrro..",
    ".orrRRRRRRrro.",
    ".orrRRhhRRrro.",
    ".orrRRRRRRrro.",
    "..orReeeeRro..",
    "..orrRRRRrro..",
    "...orrrrrro...",
    "....oooooo....",
    "..............",
]

# ── Left frames ───────────────────────────────────────────────────
_LEFT_0 = [
    "....oooo......",
    "...orrrro.....",
    "..orrRRRrro...",
    "..orReReRroo..",
    ".orrRRRRRRrFo.",
    ".orrRhRRhhRfo.",
    ".orrRRRRRRrFo.",
    "..orrRRRRrroo.",
    "..oFrrrrrrFo..",
    "...oFffffFo...",
    "....offffoo...",
    ".....oFFo.....",
    "......oo......",
    "..............",
]

_LEFT_1 = [
    "....oooo......",
    "...orrrro.....",
    "..orrRRRrro...",
    "..orReReRroo..",
    ".orrRRRRRRrFo.",
    ".orrRhRRhhRfo.",
    ".orrRRRRRRrFo.",
    "..orrRRRRrroo.",
    "...oFrrrrFo...",
    "....oFffFo....",
    "...ooffffoo...",
    "....oFFo......",
    ".....oo.......",
    "..............",
]

# ── Right frames ──────────────────────────────────────────────────
_RIGHT_0 = [
    "......oooo....",
    ".....orrrro...",
    "...orrRRRrro..",
    "..oorReReRro..",
    ".oFrRRRRRRrro.",
    ".ofRhhRRhRrro.",
    ".oFrRRRRRRrro.",
    ".oorrRRRRrro..",
    "..oFrrrrrrFo..",
    "...oFffffFo...",
    "...ooffffoo...",
    ".....oFFo.....",
    "......oo......",
    "..............",
]

_RIGHT_1 = [
    "......oooo....",
    ".....orrrro...",
    "...orrRRRrro..",
    "..oorReReRro..",
    ".oFrRRRRRRrro.",
    ".ofRhhRRhRrro.",
    ".oFrRRRRRRrro.",
    ".oorrRRRRrro..",
    "...oFrrrrFo...",
    "....oFffFo....",
    "..ooffffoo....",
    "......oFFo....",
    ".......oo.....",
    "..............",
]

# ── Build surfaces ────────────────────────────────────────────────
_frames_cache = None


def get_fire_imp_frames():
    """Return dict of {direction: [frame0, frame1]} for the fire imp."""
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
