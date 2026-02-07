"""Pixel art sprites for Scorpion (fast poison enemy)."""

from .pixel_art import surface_from_grid

# ── Palette ───────────────────────────────────────────────────────
_PAL = {
    'o': (20, 20, 20),        # dark outline
    'b': (160, 120, 40),      # brown/tan body
    'B': (140, 100, 30),      # darker brown
    'p': (100, 70, 20),       # dark brown pincers
    't': (180, 140, 60),      # tan tail
    's': (120, 90, 30),       # stinger base
    'S': (80, 50, 10),        # dark stinger tip
    'e': (60, 30, 10),        # very dark eyes
    '.': None,
}

# ── Down frames ───────────────────────────────────────────────────
_DOWN_0 = [
    ".....oooo.....",
    "....obbbo.....",
    "...obbbbbo....",
    "..obBBBBBbo...",
    "..obBeeeBbo...",
    ".obBBBBBBBbo..",
    ".obBBBBBBBbo..",
    ".obBBBBBBBbo..",
    "..obBBBBBbo...",
    "...obBBBbo....",
    "....otttoo....",
    "....ottsoo....",
    ".....oSo......",
    "......o.......",
]

_DOWN_1 = [
    ".....oooo.....",
    "....obbbo.....",
    "...obbbbbo....",
    "..obBBBBBbo...",
    "..obBeeeBbo...",
    ".obBBBBBBBbo..",
    ".obBBBBBBBbo..",
    ".obBBBBBBBbo..",
    "..obBBBBBbo...",
    "...obBBBbo....",
    "...ootttoo....",
    "....ottsoo....",
    ".....oSo......",
    "......o.......",
]

# ── Up frames ─────────────────────────────────────────────────────
_UP_0 = [
    "......o.......",
    ".....oSo......",
    "....ootsoo....",
    "....ootttoo...",
    "...obBBBbo....",
    "..obBBBBBbo...",
    ".obBBBBBBBbo..",
    ".obBBBBBBBbo..",
    ".obBBBBBBBbo..",
    "..obBeeeBbo...",
    "..obBBBBBbo...",
    "...obbbbbo....",
    "....obbbo.....",
    ".....oooo.....",
]

_UP_1 = [
    "......o.......",
    ".....oSo......",
    "....ootsoo....",
    "...ootttoo....",
    "...obBBBbo....",
    "..obBBBBBbo...",
    ".obBBBBBBBbo..",
    ".obBBBBBBBbo..",
    ".obBBBBBBBbo..",
    "..obBeeeBbo...",
    "..obBBBBBbo...",
    "...obbbbbo....",
    "....obbbo.....",
    ".....oooo.....",
]

# ── Left frames ───────────────────────────────────────────────────
_LEFT_0 = [
    "....oooo......",
    "...obbbo......",
    "..obbbbbooo...",
    ".obBBBBBopo...",
    ".obBeBBBBo....",
    "obBBBBBBBbo...",
    "obBBBBBBBbo...",
    "obBBBBBBbo....",
    ".obBBBBBo.....",
    "..obBBBo......",
    "...oottsoo....",
    "....ooSo......",
    "......o.......",
    "..............",
]

_LEFT_1 = [
    "....oooo......",
    "...obbbo......",
    "..obbbbbooo...",
    ".obBBBBBopo...",
    ".obBeBBBBo....",
    "obBBBBBBBbo...",
    "obBBBBBBBbo...",
    "obBBBBBBbo....",
    ".obBBBBBo.....",
    "..obBBBo......",
    "..oottsoo.....",
    "...ooSo.......",
    ".....o........",
    "..............",
]

# ── Right frames ──────────────────────────────────────────────────
_RIGHT_0 = [
    "......oooo....",
    "......obbbo...",
    "...ooobbbbbo..",
    "...opopBBBBbo.",
    "....obBBBeBbo.",
    "...obBBBBBBBbo",
    "...obBBBBBBBbo",
    "....obBBBBBBbo",
    ".....obBBBBbo.",
    "......obBBbo..",
    "....oosttoo...",
    "......oSoo....",
    ".......o......",
    "..............",
]

_RIGHT_1 = [
    "......oooo....",
    "......obbbo...",
    "...ooobbbbbo..",
    "...opopBBBBbo.",
    "....obBBBeBbo.",
    "...obBBBBBBBbo",
    "...obBBBBBBBbo",
    "....obBBBBBBbo",
    ".....obBBBBbo.",
    "......obBBbo..",
    ".....oosttoo..",
    ".......oSoo...",
    "........o.....",
    "..............",
]

# ── Build surfaces ────────────────────────────────────────────────
_frames_cache = None


def get_scorpion_frames():
    """Return dict of {direction: [frame0, frame1]} for the scorpion."""
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
