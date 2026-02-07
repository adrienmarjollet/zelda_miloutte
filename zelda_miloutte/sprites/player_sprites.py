"""Pixel art sprites for the player character (Miloutte -- cat-eared adventurer)."""

from .pixel_art import surface_from_grid

# ── Palette ───────────────────────────────────────────────────────
_PAL = {
    'o': (20, 15, 10),      # dark outline
    'h': (255, 200, 50),    # hair / fur (gold)
    'H': (220, 170, 30),    # darker hair
    'k': (255, 170, 170),   # inner ear pink
    's': (240, 210, 180),   # skin (warmer tone)
    'S': (220, 190, 160),   # skin shadow
    'E': (30, 120, 60),     # eyes green (bright)
    'n': (40, 30, 20),      # nose/mouth
    'w': (255, 255, 255),   # eye whites/highlights
    'c': (60, 140, 60),     # tunic green
    'C': (45, 110, 45),     # tunic dark/fold
    'T': (90, 170, 90),     # tunic trim/collar (lighter green)
    'b': (110, 75, 40),     # belt brown
    'B': (140, 100, 50),    # belt buckle highlight
    'a': (240, 210, 180),   # arms (same as skin)
    'p': (80, 60, 45),      # pants
    'f': (65, 45, 30),      # boots
    'F': (85, 65, 45),      # boot highlight
    '.': None,              # transparent
}

_SHIELD_PAL = {
    'o': (20, 15, 10),      # outline
    'm': (120, 120, 140),   # metal body
    'M': (160, 160, 180),   # metal highlight
    'r': (60, 60, 80),      # metal dark/rivet
    'g': (160, 130, 40),    # gold trim
    'G': (200, 170, 60),    # gold highlight
    'e': (30, 120, 60),     # emblem green
    '.': None,
}

_SWORD_PAL = {
    'w': (210, 215, 230),   # blade main
    'W': (170, 175, 195),   # blade shadow/edge
    's': (240, 245, 255),   # blade shine/highlight (bright white-blue)
    'g': (160, 130, 40),    # guard gold
    'G': (200, 170, 60),    # guard highlight
    'h': (90, 55, 25),      # handle dark brown
    'H': (120, 80, 35),     # handle wrap lighter
    't': (230, 235, 245),   # blade tip (bright)
    '.': None,
}

# ── Down frames ───────────────────────────────────────────────────
_DOWN_0 = [
    "..ohhhohhho...",
    ".ohkhoohkho...",
    ".ohhHoohHho...",
    ".ohHhhhHhho...",
    ".osswsswsso...",
    ".osEwosEwso...",
    ".osssnsssso...",
    "..oTTTTTTo....",
    "..occccco.....",
    ".oaccccccao...",
    ".ooccbBcco....",
    "..occbbcco....",
    "..oppppppo....",
    "..offooFfo....",
]

_DOWN_1 = [
    "..ohhhohhho...",
    ".ohkhoohkho...",
    ".ohhHoohHho...",
    ".ohHhhhHhho...",
    ".osswsswsso...",
    ".osEwosEwso...",
    ".osssnsssso...",
    "..oTTTTTTo....",
    "..occccco.....",
    "..oaccccao....",
    "..oocbBco.....",
    "...occbco.....",
    "...oppoppo....",
    "...offoFfo....",
]

# ── Up frames ─────────────────────────────────────────────────────
_UP_0 = [
    "..ohhhohhho...",
    ".ohkhoohkho...",
    ".ohhHoohHho...",
    ".ohHhhhHhho...",
    "..ohhhhhho....",
    "..oHhhhHho....",
    "..ohHhHho.....",
    "..oCCCCCo.....",
    ".oCCCCCCCo....",
    ".oaCCbBCao....",
    "..oCCbbCo.....",
    "..oppppppo....",
    "..offooFfo....",
    "..offooFfo....",
]

_UP_1 = [
    "..ohhhohhho...",
    ".ohkhoohkho...",
    ".ohhHoohHho...",
    ".ohHhhhHhho...",
    "..ohhhhhho....",
    "..oHhhhHho....",
    "..ohHhHho.....",
    "..oCCCCCo.....",
    "..oCCCCCo.....",
    "..oaCCCao.....",
    "...oCbBo......",
    "...oppppo.....",
    "...offoFfo....",
    "...offoofo....",
]

# ── Left frames ───────────────────────────────────────────────────
_LEFT_0 = [
    "..ohhho.......",
    ".ohkHho.......",
    ".ohhHhho......",
    ".ohHhhhho.....",
    ".oSwsssso.....",
    ".osEwssso.....",
    ".ossnso.......",
    "..oTTTTo......",
    ".occcccco.....",
    "oaccccCCo.....",
    ".ocbBccco.....",
    ".oppppppo.....",
    ".offooFfo.....",
    ".offooFfo.....",
]

_LEFT_1 = [
    "..ohhho.......",
    ".ohkHho.......",
    ".ohhHhho......",
    ".ohHhhhho.....",
    ".oSwsssso.....",
    ".osEwssso.....",
    ".ossnso.......",
    "..oTTTTo......",
    "..occccco.....",
    ".oaccCCCo.....",
    "..ocbBcco.....",
    "..opppppo.....",
    "...offoFo.....",
    "...offoofo....",
]

# ── Right frames ──────────────────────────────────────────────────
_RIGHT_0 = [
    ".......ohhho..",
    ".......ohHkho.",
    "......ohhHhho.",
    ".....ohhhhHho.",
    ".....osssswSo.",
    ".....osssEwso.",
    ".......osnso..",
    "......oTTTTo..",
    ".....occccco..",
    ".....oCCcccca.",
    ".....occcBbco.",
    ".....opppppo..",
    ".....oFfooFfo.",
    ".....oFfooFfo.",
]

_RIGHT_1 = [
    ".......ohhho..",
    ".......ohHkho.",
    "......ohhHhho.",
    ".....ohhhhHho.",
    ".....osssswSo.",
    ".....osssEwso.",
    ".......osnso..",
    "......oTTTTo..",
    ".....occccco..",
    ".....oCCCcao..",
    ".....occBbco..",
    ".....oppppo...",
    ".....oFfofo...",
    "....ofoofffo..",
]

# ── Sword sprites (per direction) ────────────────────────────────
# Sword down: 10 wide x 18 tall  (SWORD_WIDTH=20 / scale2=10, SWORD_LENGTH=36 / scale2=18)
_SWORD_DOWN = [
    "....tt....",
    "...tswt...",
    "..tswwst..",
    ".tswWWwst.",
    "..gGGGg...",
    "...HhH....",
    "...hHh....",
    "...HhH....",
    "...sww....",
    "...sww....",
    "...sww....",
    "...sww....",
    "...sww....",
    "...sww....",
    "..Wswww...",
    "..Wswww...",
    "...Www....",
    "....w.....",
]

_SWORD_UP = [
    "....w.....",
    "...wwW....",
    "..wwwsW...",
    "..wwwsW...",
    "...wws....",
    "...wws....",
    "...wws....",
    "...wws....",
    "...wws....",
    "...wws....",
    "...HhH....",
    "...hHh....",
    "...HhH....",
    "..gGGGg...",
    ".tswWWwst.",
    "..tswwst..",
    "...tswt...",
    "....tt....",
]

_SWORD_LEFT = [
    ".........ttt......",
    "........tswwt.....",
    "ttwwwwwswWWGHhHg..",
    "WwwwwwwswWWGHhHg..",
    "........tswwt.....",
    ".........ttt......",
]

_SWORD_RIGHT = [
    "......ttt.........",
    ".....tswwt........",
    "..gHhHGWWwswwwwwtt",
    "..gHhHGWWwswwwwwWw",
    ".....tswwt........",
    "......ttt.........",
]

# ── Shield sprites (per direction) ──────────────────────────────
_SHIELD_DOWN = [
    "..ogGGgo..",
    ".omMMMMmo.",
    ".omMeeMmo.",
    ".omMeeMmo.",
    ".omMMMMmo.",
    ".orrrrro..",
    "..ommmo...",
]

_SHIELD_UP = [
    "...ommmo..",
    "..orrrrro.",
    ".omMMMMmo.",
    ".omMeeMmo.",
    ".omMeeMmo.",
    ".omMMMMmo.",
    "..ogGGgo..",
]

_SHIELD_LEFT = [
    "..oommo.",
    ".oMMMro.",
    "oGMeMro.",
    "oGMeMro.",
    ".oMMMro.",
    "..oommo.",
]

_SHIELD_RIGHT = [
    ".ommoo..",
    ".orMMMo.",
    ".orMeMGo",
    ".orMeMGo",
    ".orMMMo.",
    ".ommoo..",
]

# ── Build surfaces ────────────────────────────────────────────────
_frames_cache = None
_sword_cache = None
_shield_cache = None


def get_player_frames():
    """Return dict of {direction: [frame0, frame1]} for the player."""
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


def get_sword_surfaces():
    """Return dict of {direction: surface} for sword sprites."""
    global _sword_cache
    if _sword_cache is not None:
        return _sword_cache

    _sword_cache = {
        "down":  surface_from_grid(_SWORD_DOWN, _SWORD_PAL, 2),
        "up":    surface_from_grid(_SWORD_UP, _SWORD_PAL, 2),
        "left":  surface_from_grid(_SWORD_LEFT, _SWORD_PAL, 2),
        "right": surface_from_grid(_SWORD_RIGHT, _SWORD_PAL, 2),
    }
    return _sword_cache


def get_shield_surfaces():
    """Return dict of {direction: surface} for shield sprites."""
    global _shield_cache
    if _shield_cache is not None:
        return _shield_cache

    _shield_cache = {
        "down":  surface_from_grid(_SHIELD_DOWN, _SHIELD_PAL, 2),
        "up":    surface_from_grid(_SHIELD_UP, _SHIELD_PAL, 2),
        "left":  surface_from_grid(_SHIELD_LEFT, _SHIELD_PAL, 2),
        "right": surface_from_grid(_SHIELD_RIGHT, _SHIELD_PAL, 2),
    }
    return _shield_cache
