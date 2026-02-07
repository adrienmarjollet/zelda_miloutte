"""Pixel art sprites for companion entities (Cat, Fox, Fairy)."""

from zelda_miloutte.sprites.pixel_art import surface_from_grid

# ======================================================================
# CAT (Miloutte) - orange/brown tabby cat
# ======================================================================

_CAT_PAL = {
    'o': (20, 15, 10),       # dark outline
    'f': (220, 140, 50),     # orange fur
    'F': (190, 110, 35),     # darker fur / stripes
    'w': (255, 240, 220),    # white belly/chest
    'W': (240, 225, 205),    # white shadow
    'e': (80, 180, 80),      # green eyes
    'E': (30, 30, 20),       # eye pupil
    'n': (50, 30, 20),       # nose
    'p': (255, 160, 160),    # pink inner ear
    't': (190, 110, 35),     # tail (same as dark fur)
    '.': None,
}

# 12x12 cat sprites (idle frame 0 — sitting)
_CAT_DOWN_IDLE_0 = [
    ".ofo..ofo.",
    ".ofpo.opfo",
    "..ofFfFo..",
    ".oeEfEeo..",
    "..ofnfo...",
    "..owwwo...",
    ".oFfwfFo..",
    ".oFfffFo..",
    "..offfo...",
    "..ofofo...",
    "...o.o....",
]

_CAT_DOWN_IDLE_1 = [
    ".ofo..ofo.",
    ".ofpo.opfo",
    "..ofFfFo..",
    ".oeEfEeo..",
    "..ofnfo...",
    "..owwwo...",
    ".oFfwfFo..",
    ".oFfffFo..",
    "..offfo...",
    "..ofofo...",
    "..o...o...",
]

# Walk frames (slightly shifted legs)
_CAT_DOWN_WALK_0 = [
    ".ofo..ofo.",
    ".ofpo.opfo",
    "..ofFfFo..",
    ".oeEfEeo..",
    "..ofnfo...",
    "..owwwo...",
    ".oFfwfFo..",
    ".oFfffFo..",
    "..offfo...",
    ".ofo.ofo..",
    "..o...o...",
]

_CAT_DOWN_WALK_1 = [
    ".ofo..ofo.",
    ".ofpo.opfo",
    "..ofFfFo..",
    ".oeEfEeo..",
    "..ofnfo...",
    "..owwwo...",
    ".oFfwfFo..",
    ".oFfffFo..",
    "..offfo...",
    "..ofo.ofo.",
    "...o...o..",
]

# Happy frames (bounce up/down)
_CAT_DOWN_HAPPY_0 = [
    ".ofo..ofo.",
    ".ofpo.opfo",
    "..ofFfFo..",
    ".oeEfEeo..",
    "..ofnfo...",
    "..owwwo...",
    ".oFfwfFo..",
    ".oFfffFo..",
    "..offfo...",
    "..ofofo...",
    "...o.o....",
]

_CAT_DOWN_HAPPY_1 = [
    "..........",
    ".ofo..ofo.",
    ".ofpo.opfo",
    "..ofFfFo..",
    ".oeEfEeo..",
    "..ofnfo...",
    "..owwwo...",
    ".oFfwfFo..",
    ".oFfffFo..",
    "..offfo...",
    "..ofofo...",
]

# Up-facing cat
_CAT_UP_0 = [
    ".ofo..ofo.",
    ".ofFo.oFfo",
    "..ofFfFo..",
    "..offfff..",
    "..oFfFfo..",
    "..owwwo...",
    ".oFfwfFo..",
    ".oFfffFo..",
    "..offfo...",
    "..ofofo...",
    "...o.o....",
]

_CAT_UP_1 = [
    ".ofo..ofo.",
    ".ofFo.oFfo",
    "..ofFfFo..",
    "..offfff..",
    "..oFfFfo..",
    "..owwwo...",
    ".oFfwfFo..",
    ".oFfffFo..",
    "..offfo...",
    ".ofo.ofo..",
    "..o...o...",
]

# Left-facing cat
_CAT_LEFT_0 = [
    "ofo.......",
    "ofpo......",
    ".ofFffo...",
    "oeEfFfo...",
    ".ofnffo...",
    ".owwwfo...",
    ".oFwffo...",
    ".offfff..t",
    "..offfo..t",
    "..ofofo.t.",
    "...o.o....",
]

_CAT_LEFT_1 = [
    "ofo.......",
    "ofpo......",
    ".ofFffo...",
    "oeEfFfo...",
    ".ofnffo...",
    ".owwwfo...",
    ".oFwffo...",
    ".offfff..t",
    "..offfo..t",
    ".ofo.ofo..",
    "..o...o...",
]

# Right-facing cat
_CAT_RIGHT_0 = [
    ".......ofo",
    "......opfo",
    "...ofFffo.",
    "...oFfEEo.",
    "...offnfo.",
    "...ofwwwo.",
    "...offwFo.",
    "t..fffffo.",
    "t..offfo..",
    ".t.ofofo..",
    "....o.o...",
]

_CAT_RIGHT_1 = [
    ".......ofo",
    "......opfo",
    "...ofFffo.",
    "...oFfEEo.",
    "...offnfo.",
    "...ofwwwo.",
    "...offwFo.",
    "t..fffffo.",
    "t..offfo..",
    "..ofo.ofo.",
    "...o...o..",
]

# ======================================================================
# FOX (Rusty) - red/white fox
# ======================================================================

_FOX_PAL = {
    'o': (20, 15, 10),       # dark outline
    'f': (200, 70, 30),      # red-orange fur
    'F': (160, 50, 20),      # darker fur
    'w': (255, 245, 235),    # white fur (face/chest/tail tip)
    'W': (235, 225, 215),    # white shadow
    'e': (180, 120, 40),     # amber eyes
    'E': (30, 30, 20),       # eye pupil
    'n': (30, 20, 15),       # nose
    'p': (255, 160, 160),    # pink inner ear
    'k': (40, 30, 20),       # dark legs/feet
    't': (200, 70, 30),      # tail body
    'T': (255, 245, 235),    # tail tip (white)
    '.': None,
}

_FOX_DOWN_IDLE_0 = [
    ".ofo..ofo.",
    ".ofpo.opfo",
    "..offwfo..",
    ".oeEwEeo..",
    "..ownwo...",
    "..owwwo...",
    ".oFfwfFo..",
    ".oFfffFo..",
    "..okfko...",
    "..okooko..",
    "...o..o...",
]

_FOX_DOWN_IDLE_1 = [
    ".ofo..ofo.",
    ".ofpo.opfo",
    "..offwfo..",
    ".oeEwEeo..",
    "..ownwo...",
    "..owwwo...",
    ".oFfwfFo..",
    ".oFfffFo..",
    "..okfko...",
    ".oko..oko.",
    "..o....o..",
]

_FOX_DOWN_WALK_0 = [
    ".ofo..ofo.",
    ".ofpo.opfo",
    "..offwfo..",
    ".oeEwEeo..",
    "..ownwo...",
    "..owwwo...",
    ".oFfwfFo..",
    ".oFfffFo..",
    "..okfko...",
    ".oko.oko..",
    "..o...o...",
]

_FOX_DOWN_WALK_1 = [
    ".ofo..ofo.",
    ".ofpo.opfo",
    "..offwfo..",
    ".oeEwEeo..",
    "..ownwo...",
    "..owwwo...",
    ".oFfwfFo..",
    ".oFfffFo..",
    "..okfko...",
    "..oko.oko.",
    "...o...o..",
]

_FOX_DOWN_HAPPY_0 = [
    ".ofo..ofo.",
    ".ofpo.opfo",
    "..offwfo..",
    ".oeEwEeo..",
    "..ownwo...",
    "..owwwo...",
    ".oFfwfFo..",
    ".oFfffFo..",
    "..okfko...",
    "..okooko..",
    "...o..o...",
]

_FOX_DOWN_HAPPY_1 = [
    "..........",
    ".ofo..ofo.",
    ".ofpo.opfo",
    "..offwfo..",
    ".oeEwEeo..",
    "..ownwo...",
    "..owwwo...",
    ".oFfwfFo..",
    ".oFfffFo..",
    "..okfko...",
    "..okooko..",
]

_FOX_UP_0 = [
    ".ofo..ofo.",
    ".ofFo.oFfo",
    "..offffo..",
    "..oFffFo..",
    "..offffo..",
    "..owwwo...",
    ".oFfwfFo..",
    ".oFfffFo..",
    "..okfko...",
    "..okooko..",
    "...o..o...",
]

_FOX_UP_1 = [
    ".ofo..ofo.",
    ".ofFo.oFfo",
    "..offffo..",
    "..oFffFo..",
    "..offffo..",
    "..owwwo...",
    ".oFfwfFo..",
    ".oFfffFo..",
    "..okfko...",
    ".oko.oko..",
    "..o...o...",
]

_FOX_LEFT_0 = [
    "ofo.......",
    "ofpo......",
    ".ofwffo...",
    "oeEwffo...",
    ".ownffo...",
    ".owwwfo...",
    ".oFwffo...",
    ".offfff.tT",
    "..okfko.t.",
    "..okooko..",
    "...o..o...",
]

_FOX_LEFT_1 = [
    "ofo.......",
    "ofpo......",
    ".ofwffo...",
    "oeEwffo...",
    ".ownffo...",
    ".owwwfo...",
    ".oFwffo...",
    ".offfff.tT",
    "..okfko.t.",
    ".oko..oko.",
    "..o....o..",
]

_FOX_RIGHT_0 = [
    ".......ofo",
    "......opfo",
    "...offwfo.",
    "...offwEEo",
    "...offnwo.",
    "...ofwwwo.",
    "...offwFo.",
    "Tt.fffffo.",
    ".t.okfko..",
    "..okooko..",
    "...o..o...",
]

_FOX_RIGHT_1 = [
    ".......ofo",
    "......opfo",
    "...offwfo.",
    "...offwEEo",
    "...offnwo.",
    "...ofwwwo.",
    "...offwFo.",
    "Tt.fffffo.",
    ".t.okfko..",
    "..oko.oko.",
    "...o...o..",
]

# ======================================================================
# FAIRY (Lumina) - glowing blue/white fairy
# ======================================================================

_FAIRY_PAL = {
    'o': (30, 50, 80),       # outline (blue-tinted)
    'b': (100, 180, 255),    # blue glow body
    'B': (70, 140, 220),     # darker blue
    'w': (255, 255, 255),    # white core / glow
    'W': (220, 240, 255),    # light blue-white
    'g': (150, 220, 255),    # glow aura
    'G': (180, 240, 255),    # bright glow
    'e': (200, 230, 255),    # eyes
    'E': (50, 80, 120),      # eye pupil
    'k': (120, 200, 255),    # wing
    'K': (160, 220, 255),    # wing highlight
    '.': None,
}

_FAIRY_DOWN_IDLE_0 = [
    "....gGg...",
    "...gWwWg..",
    "..oWwwWo..",
    ".oeEwEeo..",
    "..oWwWo...",
    "k.obwbo..k",
    "K.oBbBo..K",
    "k..obo...k",
    "....o.....",
    "..........",
]

_FAIRY_DOWN_IDLE_1 = [
    "...gGGg...",
    "..gWwwWg..",
    "..oWwwWo..",
    ".oeEwEeo..",
    "..oWwWo...",
    ".kobwbok..",
    ".KoBbBoK..",
    ".k.obo.k..",
    "....o.....",
    "..........",
]

_FAIRY_DOWN_WALK_0 = [
    "....gGg...",
    "...gWwWg..",
    "..oWwwWo..",
    ".oeEwEeo..",
    "..oWwWo...",
    "k.obwbo..k",
    "K.oBbBo..K",
    "k..obo...k",
    "....o.....",
    "..........",
]

_FAIRY_DOWN_WALK_1 = [
    "...gGGg...",
    "..gWwwWg..",
    "..oWwwWo..",
    ".oeEwEeo..",
    "..oWwWo...",
    ".kobwbok..",
    ".KoBbBoK..",
    ".k.obo.k..",
    "....o.....",
    "..........",
]

_FAIRY_DOWN_HAPPY_0 = [
    "....gGg...",
    "...gWwWg..",
    "..oWwwWo..",
    ".oeEwEeo..",
    "..oWwWo...",
    "k.obwbo..k",
    "K.oBbBo..K",
    "k..obo...k",
    "....o.....",
    "..........",
]

_FAIRY_DOWN_HAPPY_1 = [
    "..........",
    "....gGg...",
    "...gWwWg..",
    "..oWwwWo..",
    ".oeEwEeo..",
    "..oWwWo...",
    "k.obwbo..k",
    "K.oBbBo..K",
    "k..obo...k",
    "....o.....",
]

_FAIRY_UP_0 = [
    "....gGg...",
    "...gWwWg..",
    "..oWwwWo..",
    "..oBbBo...",
    "..oWwWo...",
    "k.obwbo..k",
    "K.oBbBo..K",
    "k..obo...k",
    "....o.....",
    "..........",
]

_FAIRY_UP_1 = [
    "...gGGg...",
    "..gWwwWg..",
    "..oWwwWo..",
    "..oBbBo...",
    "..oWwWo...",
    ".kobwbok..",
    ".KoBbBoK..",
    ".k.obo.k..",
    "....o.....",
    "..........",
]

_FAIRY_LEFT_0 = [
    "...gGg....",
    "..gWwWg...",
    "..oWwWo...",
    ".oeEBo....",
    "..oWwo....",
    "..obwbo...",
    "..oBbBo.k.",
    "...obo..K.",
    "....o...k.",
    "..........",
]

_FAIRY_LEFT_1 = [
    "..gGGg....",
    "..gWwWg...",
    "..oWwWo...",
    ".oeEBo....",
    "..oWwo....",
    "..obwbo...",
    "..oBbBo.k.",
    "...obo..K.",
    "....o...k.",
    "..........",
]

_FAIRY_RIGHT_0 = [
    "....gGg...",
    "...gWwWg..",
    "...oWwWo..",
    "....oBEeo.",
    "....owWo..",
    "...obwbo..",
    ".k.oBbBo..",
    ".K..obo...",
    ".k...o....",
    "..........",
]

_FAIRY_RIGHT_1 = [
    "....gGGg..",
    "...gWwWg..",
    "...oWwWo..",
    "....oBEeo.",
    "....owWo..",
    "...obwbo..",
    ".k.oBbBo..",
    ".K..obo...",
    ".k...o....",
    "..........",
]

# Sniff/alert frame (same for all companions — slightly different color)
_CAT_SNIFF_0 = [
    ".ofo..ofo.",
    ".ofpo.opfo",
    "..ofFfFo..",
    ".oeEfEeo..",
    "..ofnfo...",
    "..owwwo...",
    ".oFfwfFo..",
    ".oFfffFo..",
    "..offfo...",
    "..ofofo...",
    "...o!o....",
]

# ======================================================================
# BUILD SURFACES
# ======================================================================

_cat_cache = None
_fox_cache = None
_fairy_cache = None


def get_cat_frames():
    """Return dict of animation sets for the Cat companion.

    Returns: {
        "idle":   {"down": [f0, f1], "up": [...], "left": [...], "right": [...]},
        "follow": {"down": [f0, f1], ...},
        "happy":  {"down": [f0, f1], ...},
    }
    """
    global _cat_cache
    if _cat_cache is not None:
        return _cat_cache

    _cat_cache = {
        "idle": {
            "down":  [surface_from_grid(g, _CAT_PAL, 2) for g in (_CAT_DOWN_IDLE_0, _CAT_DOWN_IDLE_1)],
            "up":    [surface_from_grid(g, _CAT_PAL, 2) for g in (_CAT_UP_0, _CAT_UP_1)],
            "left":  [surface_from_grid(g, _CAT_PAL, 2) for g in (_CAT_LEFT_0, _CAT_LEFT_1)],
            "right": [surface_from_grid(g, _CAT_PAL, 2) for g in (_CAT_RIGHT_0, _CAT_RIGHT_1)],
        },
        "follow": {
            "down":  [surface_from_grid(g, _CAT_PAL, 2) for g in (_CAT_DOWN_WALK_0, _CAT_DOWN_WALK_1)],
            "up":    [surface_from_grid(g, _CAT_PAL, 2) for g in (_CAT_UP_0, _CAT_UP_1)],
            "left":  [surface_from_grid(g, _CAT_PAL, 2) for g in (_CAT_LEFT_0, _CAT_LEFT_1)],
            "right": [surface_from_grid(g, _CAT_PAL, 2) for g in (_CAT_RIGHT_0, _CAT_RIGHT_1)],
        },
        "happy": {
            "down":  [surface_from_grid(g, _CAT_PAL, 2) for g in (_CAT_DOWN_HAPPY_0, _CAT_DOWN_HAPPY_1)],
            "up":    [surface_from_grid(g, _CAT_PAL, 2) for g in (_CAT_UP_0, _CAT_UP_1)],
            "left":  [surface_from_grid(g, _CAT_PAL, 2) for g in (_CAT_LEFT_0, _CAT_LEFT_1)],
            "right": [surface_from_grid(g, _CAT_PAL, 2) for g in (_CAT_RIGHT_0, _CAT_RIGHT_1)],
        },
    }
    return _cat_cache


def get_fox_frames():
    """Return dict of animation sets for the Fox companion."""
    global _fox_cache
    if _fox_cache is not None:
        return _fox_cache

    _fox_cache = {
        "idle": {
            "down":  [surface_from_grid(g, _FOX_PAL, 2) for g in (_FOX_DOWN_IDLE_0, _FOX_DOWN_IDLE_1)],
            "up":    [surface_from_grid(g, _FOX_PAL, 2) for g in (_FOX_UP_0, _FOX_UP_1)],
            "left":  [surface_from_grid(g, _FOX_PAL, 2) for g in (_FOX_LEFT_0, _FOX_LEFT_1)],
            "right": [surface_from_grid(g, _FOX_PAL, 2) for g in (_FOX_RIGHT_0, _FOX_RIGHT_1)],
        },
        "follow": {
            "down":  [surface_from_grid(g, _FOX_PAL, 2) for g in (_FOX_DOWN_WALK_0, _FOX_DOWN_WALK_1)],
            "up":    [surface_from_grid(g, _FOX_PAL, 2) for g in (_FOX_UP_0, _FOX_UP_1)],
            "left":  [surface_from_grid(g, _FOX_PAL, 2) for g in (_FOX_LEFT_0, _FOX_LEFT_1)],
            "right": [surface_from_grid(g, _FOX_PAL, 2) for g in (_FOX_RIGHT_0, _FOX_RIGHT_1)],
        },
        "happy": {
            "down":  [surface_from_grid(g, _FOX_PAL, 2) for g in (_FOX_DOWN_HAPPY_0, _FOX_DOWN_HAPPY_1)],
            "up":    [surface_from_grid(g, _FOX_PAL, 2) for g in (_FOX_UP_0, _FOX_UP_1)],
            "left":  [surface_from_grid(g, _FOX_PAL, 2) for g in (_FOX_LEFT_0, _FOX_LEFT_1)],
            "right": [surface_from_grid(g, _FOX_PAL, 2) for g in (_FOX_RIGHT_0, _FOX_RIGHT_1)],
        },
    }
    return _fox_cache


def get_fairy_frames():
    """Return dict of animation sets for the Fairy companion."""
    global _fairy_cache
    if _fairy_cache is not None:
        return _fairy_cache

    _fairy_cache = {
        "idle": {
            "down":  [surface_from_grid(g, _FAIRY_PAL, 2) for g in (_FAIRY_DOWN_IDLE_0, _FAIRY_DOWN_IDLE_1)],
            "up":    [surface_from_grid(g, _FAIRY_PAL, 2) for g in (_FAIRY_UP_0, _FAIRY_UP_1)],
            "left":  [surface_from_grid(g, _FAIRY_PAL, 2) for g in (_FAIRY_LEFT_0, _FAIRY_LEFT_1)],
            "right": [surface_from_grid(g, _FAIRY_PAL, 2) for g in (_FAIRY_RIGHT_0, _FAIRY_RIGHT_1)],
        },
        "follow": {
            "down":  [surface_from_grid(g, _FAIRY_PAL, 2) for g in (_FAIRY_DOWN_WALK_0, _FAIRY_DOWN_WALK_1)],
            "up":    [surface_from_grid(g, _FAIRY_PAL, 2) for g in (_FAIRY_UP_0, _FAIRY_UP_1)],
            "left":  [surface_from_grid(g, _FAIRY_PAL, 2) for g in (_FAIRY_LEFT_0, _FAIRY_LEFT_1)],
            "right": [surface_from_grid(g, _FAIRY_PAL, 2) for g in (_FAIRY_RIGHT_0, _FAIRY_RIGHT_1)],
        },
        "happy": {
            "down":  [surface_from_grid(g, _FAIRY_PAL, 2) for g in (_FAIRY_DOWN_HAPPY_0, _FAIRY_DOWN_HAPPY_1)],
            "up":    [surface_from_grid(g, _FAIRY_PAL, 2) for g in (_FAIRY_UP_0, _FAIRY_UP_1)],
            "left":  [surface_from_grid(g, _FAIRY_PAL, 2) for g in (_FAIRY_LEFT_0, _FAIRY_LEFT_1)],
            "right": [surface_from_grid(g, _FAIRY_PAL, 2) for g in (_FAIRY_RIGHT_0, _FAIRY_RIGHT_1)],
        },
    }
    return _fairy_cache
