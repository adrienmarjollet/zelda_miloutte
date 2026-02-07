"""Pixel art sprites for Ice Wraith (ghostly blue/white enemy)."""

from zelda_miloutte.sprites.pixel_art import surface_from_grid

# ── Palette ───────────────────────────────────────────────────────
_PAL = {
    'o': (30, 50, 80),        # dark outline
    'b': (80, 160, 220),      # blue body
    'B': (60, 120, 190),      # darker blue
    'w': (200, 220, 245),     # white highlight
    'W': (170, 200, 235),     # light blue-white
    'e': (180, 230, 255),     # glowing eyes
    'E': (100, 200, 255),     # eye center
    'g': (120, 180, 230),     # ghost trail
    '.': None,
}

# ── Down frames ───────────────────────────────────────────────────
_DOWN_0 = [
    "....oooooo....",
    "...obbbbBBo...",
    "..obBBBBBBBo..",
    "..obEewwEeBo..",
    ".obbBBBBBBbbo.",
    ".obbBBwwBBbbo.",
    ".obbBBBBBBbbo.",
    "..obbBBBBbbo..",
    "..oWbbbbbbWo..",
    "...oWggggWo...",
    "....oggggoo...",
    ".....oggo.....",
    "......oo......",
    "..............",
]

_DOWN_1 = [
    "....oooooo....",
    "...obbbbBBo...",
    "..obBBBBBBBo..",
    "..obEewwEeBo..",
    ".obbBBBBBBbbo.",
    ".obbBBwwBBbbo.",
    ".obbBBBBBBbbo.",
    "..obbBBBBbbo..",
    "...oWbbbbWo...",
    "....oWggWo....",
    "...ooggggoo...",
    "....oggo......",
    ".....oo.......",
    "..............",
]

# ── Up frames ─────────────────────────────────────────────────────
_UP_0 = [
    "......oo......",
    ".....oggo.....",
    "....oggggoo...",
    "...oWggggWo...",
    "..oWbbbbbbWo..",
    "..obbBBBBbbo..",
    ".obbBBBBBBbbo.",
    ".obbBBwwBBbbo.",
    ".obbBBBBBBbbo.",
    "..obBBwwBBBo..",
    "..obBBBBBBBo..",
    "...obbbbBBo...",
    "....oooooo....",
    "..............",
]

_UP_1 = [
    ".....oo.......",
    "....oggo......",
    "...ooggggoo...",
    "....oWggWo....",
    "...oWbbbbWo...",
    "..obbBBBBbbo..",
    ".obbBBBBBBbbo.",
    ".obbBBwwBBbbo.",
    ".obbBBBBBBbbo.",
    "..obBBwwBBBo..",
    "..obBBBBBBBo..",
    "...obbbbBBo...",
    "....oooooo....",
    "..............",
]

# ── Left frames ───────────────────────────────────────────────────
_LEFT_0 = [
    "....oooo......",
    "...obbbbo.....",
    "..obBBBBbbo...",
    "..obEeBeBboo..",
    ".obbBBBBBBbWo.",
    ".obbBwBBwwBgo.",
    ".obbBBBBBBbWo.",
    "..obbBBBBbboo.",
    "..oWbbbbbbWo..",
    "...oWggggWo...",
    "....oggggoo...",
    ".....ogWo.....",
    "......oo......",
    "..............",
]

_LEFT_1 = [
    "....oooo......",
    "...obbbbo.....",
    "..obBBBBbbo...",
    "..obEeBeBboo..",
    ".obbBBBBBBbWo.",
    ".obbBwBBwwBgo.",
    ".obbBBBBBBbWo.",
    "..obbBBBBbboo.",
    "...oWbbbbWo...",
    "....oWggWo....",
    "...ooggggoo...",
    "....ogWo......",
    ".....oo.......",
    "..............",
]

# ── Right frames ──────────────────────────────────────────────────
_RIGHT_0 = [
    "......oooo....",
    ".....obbbbo...",
    "...obbBBBBbo..",
    "..oobBeBEeBo..",
    ".oWbBBBBBBbbo.",
    ".ogBwwBBwBbbo.",
    ".oWbBBBBBBbbo.",
    "..oobbBBBBbbo.",
    "..oWbbbbbbWo..",
    "...oWggggWo...",
    "...ooggggoo...",
    ".....oWgo.....",
    "......oo......",
    "..............",
]

_RIGHT_1 = [
    "......oooo....",
    ".....obbbbo...",
    "...obbBBBBbo..",
    "..oobBeBEeBo..",
    ".oWbBBBBBBbbo.",
    ".ogBwwBBwBbbo.",
    ".oWbBBBBBBbbo.",
    "..oobbBBBBbbo.",
    "...oWbbbbWo...",
    "....oWggWo....",
    "..ooggggoo....",
    "......oWgo....",
    ".......oo.....",
    "..............",
]

# ── Build surfaces ────────────────────────────────────────────────
_frames_cache = None


def get_ice_wraith_frames():
    """Return dict of {direction: [frame0, frame1]} for the ice wraith."""
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
