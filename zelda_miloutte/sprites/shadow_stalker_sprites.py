"""Pixel art sprites for Shadow Stalker (teleporting enemy)."""

from zelda_miloutte.sprites.pixel_art import surface_from_grid

# ── Palette ───────────────────────────────────────────────────────
_PAL = {
    'o': (20, 20, 20),        # dark outline
    's': (80, 40, 120),       # shadow purple body
    'S': (50, 25, 80),        # darker shadow
    'p': (120, 60, 160),      # lighter purple highlight
    'e': (200, 50, 200),      # glowing magenta eyes
    'E': (255, 100, 255),     # bright eye highlight
    'd': (40, 20, 60),        # very dark shadow
    'w': (100, 50, 140),      # wispy effect
    '.': None,
}

# ── Down frames ───────────────────────────────────────────────────
_DOWN_0 = [
    "......oo......",
    ".....owwo.....",
    "....owwwwo....",
    "...owwswwwo...",
    "..owwssswwwo..",
    "..oswsssswo...",
    "..osEeoEeos...",
    "..oseeoees....",
    "..osssssso....",
    ".owsssssswo...",
    ".owssssssswo..",
    ".ossssssssso..",
    "..ooosssoo....",
    ".....ooo......",
]

_DOWN_1 = [
    "......oo......",
    ".....owwo.....",
    "....owwwwo....",
    "...owwswwwo...",
    "..owwssswwwo..",
    "..oswsssswo...",
    "..osEeoEeos...",
    "..oseeoees....",
    "..osssssso....",
    ".owsssssswo...",
    "..ossssssso...",
    "..osssssssoo..",
    "...ooossoo....",
    "......oo......",
]

# ── Up frames ─────────────────────────────────────────────────────
_UP_0 = [
    "......oo......",
    ".....owwo.....",
    "....owwwwo....",
    "...owwswwwo...",
    "..owwssswwwo..",
    "..oswsssswo...",
    "..osssssso....",
    "..osssssso....",
    "..osssssso....",
    ".owsssssswo...",
    ".owssssssswo..",
    ".ossssssssso..",
    "..ooosssoo....",
    ".....ooo......",
]

_UP_1 = [
    "......oo......",
    ".....owwo.....",
    "....owwwwo....",
    "...owwswwwo...",
    "..owwssswwwo..",
    "..oswsssswo...",
    "..osssssso....",
    "..osssssso....",
    "..osssssso....",
    ".owsssssswo...",
    "..ossssssso...",
    "..osssssssoo..",
    "...ooossoo....",
    "......oo......",
]

# ── Left frames ───────────────────────────────────────────────────
_LEFT_0 = [
    ".....oo.......",
    "....owwo......",
    "...owwwwo.....",
    "..owwswwwo....",
    ".owwsssswwo...",
    ".oswssssswo...",
    ".osEosssso....",
    ".oseoossso....",
    ".ossssssswo...",
    "owssssssswo...",
    "owssssssso....",
    "oossssssso....",
    "..oossso......",
    "....oo........",
]

_LEFT_1 = [
    ".....oo.......",
    "....owwo......",
    "...owwwwo.....",
    "..owwswwwo....",
    ".owwsssswwo...",
    ".oswssssswo...",
    ".osEosssso....",
    ".oseoossso....",
    ".ossssssswo...",
    ".owssssssswo..",
    "..osssssssso..",
    "..osssssssoo..",
    "...oossso.....",
    ".....oo.......",
]

# ── Right frames ──────────────────────────────────────────────────
_RIGHT_0 = [
    ".......oo.....",
    "......owwo....",
    ".....owwwwo...",
    "....owwswwwo..",
    "...owwsssswwo.",
    "...owssssswo..",
    "....ossssoEso.",
    "....osssooeso.",
    "...owsssssso..",
    "...owssssssswo",
    "....ossssssswo",
    "....osssssssoo",
    "......osssoo..",
    "........oo....",
]

_RIGHT_1 = [
    ".......oo.....",
    "......owwo....",
    ".....owwwwo...",
    "....owwswwwo..",
    "...owwsssswwo.",
    "...owssssswo..",
    "....ossssoEso.",
    "....osssooeso.",
    "...owsssssso..",
    "..owssssssswo.",
    "..osssssssso..",
    "..oossssssso..",
    ".....ossoo....",
    ".......oo.....",
]

# ── Build surfaces ────────────────────────────────────────────────
_frames_cache = None


def get_shadow_stalker_frames():
    """Return dict of {direction: [frame0, frame1]} for the shadow stalker."""
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
