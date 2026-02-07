"""Pixel art sprites for Frost Golem (slow, tanky ice enemy)."""

from .pixel_art import surface_from_grid

# ── Palette ───────────────────────────────────────────────────────
_PAL = {
    'o': (15, 25, 40),        # dark outline/shadow
    'i': (90, 150, 210),      # ice body (medium blue)
    'I': (50, 90, 140),       # dark ice (deep blue)
    'L': (110, 170, 230),     # light ice (brighter)
    'c': (150, 210, 250),     # crystal highlight
    'C': (200, 240, 255),     # bright crystal/frost
    'W': (180, 220, 255),     # frost white
    'e': (255, 120, 40),      # glowing orange eyes
    'E': (220, 80, 20),       # eye core (darker)
    'g': (80, 180, 255),      # glowing blue (core)
    'G': (40, 140, 220),      # glowing blue (darker)
    'r': (50, 50, 60),        # rock dark
    'R': (70, 80, 90),        # rock medium
    'S': (90, 100, 110),      # stone/rock light
    's': (110, 120, 130),     # stone lighter
    'b': (30, 40, 50),        # rock shadow/crack
    '.': None,
}

# ── Down frames ───────────────────────────────────────────────────
_DOWN_0 = [
    "....oooooo....",
    "...oCWCCWCo...",
    "..oCLiiiiLCo..",
    "..oLiIbIbIiLo.",
    ".oCiiEeIEeiio.",
    ".oLiiIbbIIiio.",
    "oCiiiGggGiiio.",
    "oCiiIgGGgIiio.",
    "oSssiIIIIiiio.",
    "oSRRsIIIIrrbo.",
    "oSRRRRRRRrbbo.",
    ".oSRbRRbRrboo.",
    "..oRRRRRRroo..",
    "...oooooooo...",
]

_DOWN_1 = [
    "....oooooo....",
    "...oWCCCWCo...",
    "..oCLiiiiLCo..",
    "..oLiIbIbIiLo.",
    ".oCiiEeIEeiio.",
    ".oLiiIbbIIiio.",
    "oCiiiGggGiiio.",
    "oCiiIgGGgIiio.",
    ".oiiiIIIIisso.",
    ".obrrIIIIsSRo.",
    ".obbRRRRRRRSo.",
    "..oorRbRRbSo..",
    "..oorRRRRRo...",
    "...oooooooo...",
]

# ── Up frames ─────────────────────────────────────────────────────
_UP_0 = [
    "...oooooooo...",
    "..oorrRRrroo..",
    ".oRRbRRbRRbSo.",
    "oSRRRRRRRRRSo.",
    "oSRRsiIIIIsso.",
    "oCiiIIIIIiiio.",
    "oCiiIgGGgIiio.",
    "oCiiiGggGiiio.",
    ".oLiiIbbIIiio.",
    ".oCiiIbIbIiio.",
    "..oLiEeIEeiLo.",
    "..oCLiiiiLCo..",
    "...oCWCCWCo...",
    "....oooooo....",
]

_UP_1 = [
    "...oooooooo...",
    "..oorRRRRoo...",
    "..oSbRRbRroo..",
    ".oSRRRRRRRbbo.",
    ".osSRIIIIrrbo.",
    ".ossiIIIIiiio.",
    "oCiiIgGGgIiio.",
    "oCiiiGggGiiio.",
    ".oLiiIbbIIiio.",
    ".oCiiIbIbIiio.",
    "..oLiEeIEeiLo.",
    "..oCLiiiiLCo..",
    "...oWCCCWCo...",
    "....oooooo....",
]

# ── Left frames ───────────────────────────────────────────────────
_LEFT_0 = [
    "....oooooo....",
    "...oCWCCLo....",
    "..oCLiiiiCo...",
    "..oLiIbIIiLo..",
    ".oCiEeIbbiiCo.",
    ".oLiIIGggIiio.",
    "oCiiIgGGgiiCo.",
    "oCiiiIIIiisoo.",
    "oSssiIIIRRsSo.",
    "oSRRsIIRRRRSo.",
    "oSRRRbRRbRSoo.",
    ".oSRRRRRRroo..",
    "..oRRRRRroo...",
    "...ooooooo....",
]

_LEFT_1 = [
    "....oooooo....",
    "...oWCCCLo....",
    "..oCLiiiiCo...",
    "..oLiIbIIiLo..",
    ".oCiEeIbbiiCo.",
    ".oLiIIGggIiio.",
    "oCiiIgGGgiiCo.",
    ".ooCiiiIIiiso.",
    ".osSRIIIIisso.",
    ".oSRRRRRRRRSo.",
    "..ooSRbRRbRSo.",
    "...oorRRRRroo.",
    "....oorrRRoo..",
    "....ooooooo...",
]

# ── Right frames ──────────────────────────────────────────────────
_RIGHT_0 = [
    "....oooooo....",
    "....oLCCWCo...",
    "...oCiiiiLCo..",
    "..oLiIIbIiLo..",
    ".oCiibbIeEiCo.",
    ".oiiIgggGIiLo.",
    ".ooCiiGGggIiio",
    ".oosiIIIiiio..",
    ".oSRRIIIisSso.",
    ".oSRRRRIIsSRSo",
    ".ooSRbRRbRRRSo",
    "..oorRRRRRSo..",
    "...oorRRRRo...",
    "....ooooooo...",
]

_RIGHT_1 = [
    "....oooooo....",
    "....oLCCCWo...",
    "...oCiiiiLCo..",
    "..oLiIIbIiLo..",
    ".oCiibbIeEiCo.",
    ".oiiIgggGIiLo.",
    "oCiiIgGGgIiiCo",
    ".osiiIIiiCoo..",
    ".ossiIIIIRsSo.",
    "oSRRRRRRRRRSo.",
    "oSRbRRbRSoo...",
    ".oorRRRRroo...",
    "..ooRRrroo....",
    "...ooooooo....",
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
