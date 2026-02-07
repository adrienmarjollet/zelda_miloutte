"""Pixel art sprites for Magma Golem (slow tank with lava cracks)."""

from .pixel_art import surface_from_grid

# ── Palette ───────────────────────────────────────────────────────
_PAL = {
    'o': (20, 20, 20),        # dark outline
    'b': (40, 40, 45),        # dark basalt
    'B': (55, 55, 60),        # medium basalt
    'r': (70, 50, 45),        # brown rock
    'R': (90, 65, 55),        # medium brown rock
    'g': (105, 85, 75),       # gray stone
    'G': (120, 100, 90),      # light gray stone
    'd': (150, 40, 20),       # deep red lava (cooling)
    'c': (200, 60, 20),       # dark red lava crack
    'C': (255, 100, 30),      # bright red-orange lava
    'l': (255, 150, 40),      # orange lava flow
    'L': (255, 200, 60),      # bright yellow lava
    'w': (255, 240, 200),     # white-hot lava core
    'y': (255, 220, 100),     # yellow glow
    'e': (255, 180, 80),      # eye glow orange
    '.': None,
}

# ── Down frames ───────────────────────────────────────────────────
_DOWN_0 = [
    "....oooooo....",
    "...ogyLygo....",
    "..ogGwLwGgo...",
    "..oGeyllyeGo..",
    ".ogGlLwLlGgo.",
    ".oRclLwLlcRo.",
    ".obdCLLCdboo.",
    ".obbcCCcbbbo.",
    ".oBrdccdrbBo.",
    "..orBdddBro..",
    "..oRbdcdbRo..",
    "...oRrcrRo...",
    "....ogbgo....",
    "....oooo.....",
]

_DOWN_1 = [
    "....oooooo....",
    "...ogyCygo....",
    "..ogGlClGgo...",
    "..oGeLllLeGo..",
    ".ogGCwLwCGgo.",
    ".oRcCwLwCcRo.",
    ".obdlwwldoo..",
    ".obbclclbbbo.",
    ".oBrdlldrbBo.",
    "..orBdcdBro..",
    "..oRbdldbRo..",
    "...oRrcrRo...",
    "....ogbgo....",
    "....oooo.....",
]

# ── Up frames ─────────────────────────────────────────────────────
_UP_0 = [
    "....oooo.....",
    "....ogbgo....",
    "...oRrcrRo...",
    "..oRbdcdbRo..",
    "..orBdddBro..",
    ".oBrdccdrbBo.",
    ".obbcCCcbbbo.",
    ".obdCLLCdboo.",
    ".oRclLwLlcRo.",
    ".ogGlLwLlGgo.",
    "..oGeyllyeGo..",
    "..ogGwLwGgo...",
    "...ogyLygo....",
    "....oooooo....",
]

_UP_1 = [
    "....oooo.....",
    "....ogbgo....",
    "...oRrcrRo...",
    "..oRbdldbRo..",
    "..orBdcdBro..",
    ".oBrdlldrbBo.",
    ".obbclclbbbo.",
    ".obdlwwldoo..",
    ".oRcCwLwCcRo.",
    ".ogGCwLwCGgo.",
    "..oGeLllLeGo..",
    "..ogGlClGgo...",
    "...ogyCygo....",
    "....oooooo....",
]

# ── Left frames ───────────────────────────────────────────────────
_LEFT_0 = [
    "...oooooo.....",
    "..ogyLyGo.....",
    ".ogGwLwGRo....",
    ".oGeyLcdbRo...",
    "ogGlwlCrbBo...",
    "oRcLwCdbBBoo..",
    "obdCLcdbbbbbo.",
    "obbcCcrbBBBBo.",
    "oBrdccdbBBoo..",
    ".orBdcdrbBo...",
    ".oRbdcdbRo....",
    "..oRrcRGo.....",
    "...ogbgo......",
    "....oooo......",
]

_LEFT_1 = [
    "...oooooo.....",
    "..ogyCyGo.....",
    ".ogGlClGRo....",
    ".oGeLlcdbRo...",
    "ogGCwCcrbBo...",
    "oRcCwldbBBoo..",
    "obdlwcdbbbbbo.",
    "obbclcrbBBBBo.",
    "oBrdlcdbBBoo..",
    ".orBdldrbBo...",
    ".oRbdldbRo....",
    "..oRrcRGo.....",
    "...ogbgo......",
    "....oooo......",
]

# ── Right frames ──────────────────────────────────────────────────
_RIGHT_0 = [
    ".....oooooo...",
    ".....oGyLygo..",
    "....oRGwLwGgo.",
    "...oRbdcLyeGo.",
    "...oBbrClwlGgo",
    "..ooBBbdCwLcRo",
    ".obbbbbdcLCdbo",
    ".oBBBBBrcCcbbo",
    "..ooBBbdccdrBo",
    "...oBbrdcdBro.",
    "....oRbdcdBRo.",
    ".....oGRcrRo..",
    "......ogbgo...",
    "......oooo....",
]

_RIGHT_1 = [
    ".....oooooo...",
    ".....oGyCygo..",
    "....oRGlClGgo.",
    "...oRbdcLlEGo.",
    "...oBbrcCwCGgo",
    "..ooBBbdlwCcRo",
    ".obbbbbdcwldbo",
    ".oBBBBBrclcbbo",
    "..ooBBbdcldrBo",
    "...oBbrdldBro.",
    "....oRbdldBRo.",
    ".....oGRcrRo..",
    "......ogbgo...",
    "......oooo....",
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
    ".owwwwo.",
    "owyyyLo",
    "owLLLCo",
    "oyCCCdo",
    "oLCcdco",
    ".odccdo.",
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
