"""Pixel art sprites for archer enemies (hooded ranged attackers)."""

from .pixel_art import surface_from_grid

# ── Archer Palette ────────────────────────────────────────────────
_ARCHER_PAL = {
    'o': (15, 10, 20),      # dark outline
    'h': (25, 15, 45),      # hood dark
    'H': (40, 28, 70),      # hood lighter
    'r': (50, 35, 90),      # robe purple
    'R': (70, 50, 120),     # robe lighter
    'f': (200, 180, 160),   # face/hands skin
    'e': (180, 60, 60),     # eyes glowing red
    'E': (255, 100, 80),    # eye glow bright center
    'B': (100, 70, 35),     # bow wood
    'S': (180, 170, 150),   # bowstring
    'q': (90, 65, 30),      # quiver brown
    'a': (140, 110, 50),    # arrow tips in quiver
    'c': (60, 45, 100),     # cloak bottom/trim
    '.': None,
}

# ── Down frames ───────────────────────────────────────────────────
_DOWN_0 = [
    ".....ooo......",
    "....ohhho.....",
    "...ohHHHho....",
    "...oHHHHHo....",
    "..ohHHeEeHo...",
    "..oHHhehHHo...",
    "..ohHHfHHho...",
    "..oBSoRrooo...",
    "..oBorRRrqo...",
    "..oSrRRRRqo...",
    "..oorRrRrao...",
    "...orRRRrco...",
    "..ocrRRrcco...",
    "..occccccco...",
]

_DOWN_1 = [
    ".....ooo......",
    "....ohhho.....",
    "...ohHHHho....",
    "...oHHHHHo....",
    "..ohHHeEeHo...",
    "..oHHhehHHo...",
    "..ohHHfHHho...",
    "..oBSoRrooo...",
    "..oBorRRrqo...",
    "..oSrRRRRqo...",
    "..oorRrRrao...",
    "..ocrRRRrco...",
    "...ocRRRcco...",
    "...occcocco...",
]

# ── Up frames ─────────────────────────────────────────────────────
_UP_0 = [
    ".....ooo......",
    "....ohhho.....",
    "...ohHHHho....",
    "...oHHHHHo....",
    "..ohHHHHHho...",
    "..oqaaHHHHo...",
    "..oqqoHHHHo...",
    "..ooorRRrBo...",
    "...oorRRrSo...",
    "..oorRRRrSo...",
    "..oorRrRrBo...",
    "...orRRRrco...",
    "..ocrRRrcco...",
    "..occccccco...",
]

_UP_1 = [
    ".....ooo......",
    "....ohhho.....",
    "...ohHHHho....",
    "...oHHHHHo....",
    "..ohHHHHHho...",
    "..oqaaHHHHo...",
    "..oqqoHHHHo...",
    "..ooorRRrBo...",
    "..oorRRRrSo...",
    "...oorRRrSo...",
    "..oorRrRrBo...",
    "..ocrRRRrco...",
    "...ocRRRcco...",
    "...occcocco...",
]

# ── Left frames ───────────────────────────────────────────────────
_LEFT_0 = [
    "...ooo........",
    "..ohhho.......",
    ".ohHHHho......",
    ".oHHHHHo......",
    "ohHEeqao......",
    "oHHheqqqo.....",
    "ohHfHooo......",
    "ooRrRrfoo.....",
    ".orRRRRoo.....",
    ".orRRRRBSo....",
    ".orRrRrBSo....",
    ".ocRRRroBo....",
    "occrRRrccoo...",
    "ooccccccoo....",
]

_LEFT_1 = [
    "...ooo........",
    "..ohhho.......",
    ".ohHHHho......",
    ".oHHHHHo......",
    "ohHEeqao......",
    "oHHheqqqo.....",
    "ohHfHooo......",
    "ooRrRrfoo.....",
    ".orRRRRoo.....",
    ".orRRRRBSo....",
    ".ocrRrRBSo....",
    "..ocRRroBo....",
    "..occRrcco....",
    "...occocco....",
]

# ── Right frames ──────────────────────────────────────────────────
_RIGHT_0 = [
    "........ooo...",
    ".......ohhho..",
    "......ohHHHho.",
    "......oHHHHHo.",
    "......oaqeEHho",
    ".....oqqqehHHo",
    "......oooHfHho",
    ".....oofRrRoo.",
    ".....ooRRRRro.",
    "....oSBRRRRro.",
    "....oSBrRrRro.",
    "....oBorRRRco.",
    "...oocrRRrcco.",
    "....ooccccccoo",
]

_RIGHT_1 = [
    "........ooo...",
    ".......ohhho..",
    "......ohHHHho.",
    "......oHHHHHo.",
    "......oaqeEHho",
    ".....oqqqehHHo",
    "......oooHfHho",
    ".....oofRrRoo.",
    ".....ooRRRRro.",
    "....oSBRRRRro.",
    "....oSBrRrcoo.",
    "....oBoRRRco..",
    "....occrRcco..",
    "....occoccoo..",
]

# ── Build surfaces ────────────────────────────────────────────────
_archer_frames_cache = None


def get_archer_frames():
    """Return dict of {direction: [frame0, frame1]} for the archer."""
    global _archer_frames_cache
    if _archer_frames_cache is not None:
        return _archer_frames_cache

    _archer_frames_cache = {
        "down":  [surface_from_grid(g, _ARCHER_PAL, 2) for g in (_DOWN_0, _DOWN_1)],
        "up":    [surface_from_grid(g, _ARCHER_PAL, 2) for g in (_UP_0, _UP_1)],
        "left":  [surface_from_grid(g, _ARCHER_PAL, 2) for g in (_LEFT_0, _LEFT_1)],
        "right": [surface_from_grid(g, _ARCHER_PAL, 2) for g in (_RIGHT_0, _RIGHT_1)],
    }
    return _archer_frames_cache


# ── Projectile sprite ─────────────────────────────────────────────
_PROJECTILE_PAL = {
    'c': (200, 80, 200),    # core bright magenta
    'C': (255, 130, 255),   # core highlight
    'g': (140, 50, 160),    # glow edge
    'G': (100, 30, 120),    # outer glow
    't': (255, 200, 255),   # bright tip/center
    '.': None,
}

# 8x8 magical energy bolt sprite (pointing right by default, will be rotated)
_ARROW = [
    "........",
    "..ggtCc.",
    ".gctCCcg",
    "GgcCCcgg",
    "GgcCCcgg",
    ".gctCCcg",
    "..ggtCc.",
    "........",
]

_projectile_sprite_cache = None


def get_projectile_sprite():
    """Return the projectile (arrow) sprite surface."""
    global _projectile_sprite_cache
    if _projectile_sprite_cache is not None:
        return _projectile_sprite_cache

    _projectile_sprite_cache = surface_from_grid(_ARROW, _PROJECTILE_PAL, 1)
    return _projectile_sprite_cache
