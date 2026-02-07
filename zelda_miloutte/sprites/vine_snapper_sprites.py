"""Pixel art sprites for Vine Snapper (stationary plant enemy)."""

from .pixel_art import surface_from_grid

# ── Palette ───────────────────────────────────────────────────────
_PAL = {
    'o': (20, 20, 20),        # dark outline
    'g': (30, 130, 30),       # green body
    'G': (20, 90, 20),        # darker green
    'l': (50, 170, 50),       # light green highlight
    'r': (180, 30, 30),       # red thorns/mouth
    'R': (220, 60, 60),       # bright red
    'd': (40, 60, 30),        # dark green base
    'D': (25, 40, 20),        # very dark green
    '.': None,
}

# Vine Snapper is stationary, so we just need "down" direction with 2 frames for idle animation
# Frame 0: Closed/neutral
_DOWN_0 = [
    "......oo......",
    ".....ollo.....",
    "....ollllo....",
    "...olllgllo...",
    "..ollggggllo..",
    "..olggggglo...",
    "..olrrrrrglo..",
    "..olRrrrrRlo..",
    "..olggggglo...",
    "..olggggglo...",
    "..odgggggdo...",
    "..oddggdddo...",
    "..odDDDDDdo...",
    "...oooooo.....",
]

# Frame 1: Slightly open/menacing
_DOWN_1 = [
    "......oo......",
    ".....ollo.....",
    "....ollllo....",
    "...olllgllo...",
    "..ollggggllo..",
    "..olggggglo...",
    "..olRrrrrRlo..",
    "..olrrrrrrlo..",
    "..olRrrrrRlo..",
    "..olggggglo...",
    "..odgggggdo...",
    "..oddggdddo...",
    "..odDDDDDdo...",
    "...oooooo.....",
]

# Thorn projectile sprite (small, simple)
_THORN = [
    "...oro...",
    "..orRro..",
    ".orRRRro.",
    "orRRRRRro",
    ".orRRRro.",
    "..orRro..",
    "...oro...",
]

_THORN_PAL = {
    'o': (20, 20, 20),
    'r': (180, 30, 30),
    'R': (220, 60, 60),
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
