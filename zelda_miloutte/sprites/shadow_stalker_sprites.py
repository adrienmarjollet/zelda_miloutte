"""Pixel art sprites for Shadow Stalker (teleporting enemy)."""

from .pixel_art import surface_from_grid

# ── Palette ───────────────────────────────────────────────────────────
_PAL = {
    # Outline and structure
    'o': (15, 10, 20),         # deep void outline
    'O': (30, 15, 35),         # lighter outline edge

    # Hood and cloak body gradients
    'h': (45, 25, 65),         # hood shadow
    'H': (60, 35, 85),         # hood edge
    'c': (40, 20, 60),         # cloak dark
    'C': (55, 30, 75),         # cloak medium

    # Shadow body core
    's': (70, 40, 100),        # shadow body
    'S': (50, 25, 70),         # darker shadow core
    'd': (25, 15, 35),         # deep void darkness
    'D': (35, 18, 50),         # void medium

    # Purple highlights and wisps
    'p': (95, 50, 130),        # purple highlight
    'P': (110, 65, 150),       # bright purple
    'w': (85, 45, 120),        # wispy edge
    'W': (100, 55, 140),       # bright wisp

    # Ethereal glow
    'g': (140, 100, 180),      # pale lavender glow
    'G': (160, 120, 200),      # bright lavender aura

    # Eyes - piercing magenta/pink with glow
    'e': (200, 40, 180),       # eye base magenta
    'E': (255, 80, 240),       # bright eye highlight
    'a': (180, 70, 160),       # eye aura/glow
    'A': (220, 100, 200),      # bright aura

    # Shadow tendrils
    't': (45, 20, 60),         # dark tendril
    'T': (60, 30, 80),         # lighter tendril

    # Void runes and energy
    'v': (80, 20, 100),        # void purple rune
    'V': (100, 30, 130),       # bright void rune

    '.': None,  # transparent
}

# ── Down frames ───────────────────────────────────────────────────────
_DOWN_0 = [
    "......oooo....",
    ".....oHHHHo...",
    "....oHppPHHo..",
    "...oHpgGgpHo..",
    "..oHpSSdDSPho.",
    "..ohAEedEeAho.",
    "..ohaeedeaaho.",
    "..ohsSdvDssho.",
    ".owhsSdDdSswo.",
    ".owsCSDDScTwo.",
    "..oTsSsDsTto..",
    "...otSdStto...",
    "....ottotto...",
    "......ttt.....",
]

_DOWN_1 = [
    "......oooo....",
    ".....oHHHHo...",
    "....oHPpPHHo..",
    "...oHpgGgPHo..",
    "..oHPSSdDSsho.",
    "..ohaEedEeAho.",
    "..ohaeedeeaho.",
    "..ohsSvdDssho.",
    ".owhsSDdDSswo.",
    ".oTwCsddScwTo.",
    "..ottsSdSto...",
    "....otSdSto...",
    "....otttto....",
    ".....t.t......",
]

# ── Up frames ─────────────────────────────────────────────────────────
_UP_0 = [
    "......oooo....",
    ".....oHHHHo...",
    "....oHppPHHo..",
    "...oHpwWwpHo..",
    "..oHpSSdDSPho.",
    "..ohsSDvDssho.",
    "..ohsSdDdSsho.",
    "..ohsSdDdssho.",
    ".owhsSDDdSswo.",
    ".owsCSDDScTwo.",
    "..oTsSsDsTto..",
    "...otSdStto...",
    "....ottotto...",
    "......ttt.....",
]

_UP_1 = [
    "......oooo....",
    ".....oHHHHo...",
    "....oHPppHHo..",
    "...oHpwWWPHo..",
    "..oHPSSdDSsho.",
    "..ohsSDDvssho.",
    "..ohsSvdDssho.",
    "..ohsSDdDssho.",
    ".owhsSdDdSswo.",
    ".oTwCsddScwTo.",
    "..ottsSdSto...",
    "....otSdSto...",
    "....otttto....",
    ".....t.t......",
]

# ── Left frames ───────────────────────────────────────────────────────
_LEFT_0 = [
    ".....oooo.....",
    "....oHHHHo....",
    "...oHppPHHo...",
    "..oHpwWwpHo...",
    ".oHpSSdDSpho..",
    ".ohaEeSdssho..",
    ".ohaeeDvdsho..",
    ".ohsSdDdssTo..",
    ".otsCDdDSswo..",
    "otwsSSdDScwo..",
    "otTsSdDdSso...",
    ".otSdvdSsto...",
    "..otSdStto....",
    "...otttto.....",
]

_LEFT_1 = [
    ".....oooo.....",
    "....oHHHHo....",
    "...oHPppHHo...",
    "..oHpWwwPHo...",
    ".oHPSdDDsho...",
    ".ohaEedSssho..",
    ".ohaeedvssTho.",
    ".ohsSDdDsswTo.",
    ".oTsCdDdScwo..",
    ".otTsSDdDswo..",
    "..ottSdDsso...",
    "...otSvdSto...",
    "....otstto....",
    ".....tt.t.....",
]

# ── Right frames ──────────────────────────────────────────────────────
_RIGHT_0 = [
    ".....oooo.....",
    "....oHHHHo....",
    "...oHHPpPHo...",
    "...oHpwWwpHo..",
    "..ohpSdDSsPHo.",
    "..ohssdSeEaho.",
    "..ohsdvDeeaho.",
    "..oTssdDdSsho.",
    "..owsSdDdCsto.",
    "..owcSDdDSswto",
    "...osSdDdSsTto",
    "...otsSDvdSto.",
    "....ottdSto...",
    ".....otttto...",
]

_RIGHT_1 = [
    ".....oooo.....",
    "....oHHHHo....",
    "...oHHppPHo...",
    "..oHPwwWpHo...",
    "...ohsDDdSPHo.",
    "..ohsssSdeEho.",
    ".ohTssvdeeaho.",
    ".oTwssDdDSsho.",
    "..owcSDdDcsToo",
    "..owsDdDSsTto.",
    "...ossdDdSto..",
    "...otSdvSto...",
    "....ottsto....",
    ".....t.tt.....",
]

# ── Build surfaces ────────────────────────────────────────────────────
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
