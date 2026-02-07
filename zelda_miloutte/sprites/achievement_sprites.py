"""16x16 icon sprites for achievements using surface_from_grid()."""

from zelda_miloutte.sprites.pixel_art import surface_from_grid

# ── Palettes ─────────────────────────────────────────────────────

_TROPHY_PAL = {
    'g': (255, 200, 50),   # gold
    'G': (210, 160, 30),   # dark gold
    'l': (255, 235, 130),  # gold highlight
    'b': (139, 90, 43),    # brown base
    'B': (100, 65, 30),    # dark brown
    '.': None,
}

_SWORD_PAL = {
    's': (180, 190, 200),  # steel
    'S': (140, 150, 160),  # dark steel
    'l': (220, 225, 230),  # steel highlight
    'h': (139, 90, 43),    # hilt brown
    'H': (100, 65, 30),    # dark hilt
    'g': (255, 200, 50),   # gold guard
    'r': (200, 50, 50),    # ruby pommel
    '.': None,
}

_CHEST_PAL = {
    'b': (139, 90, 43),    # brown
    'B': (100, 65, 30),    # dark brown
    'l': (180, 130, 70),   # light brown
    'g': (255, 200, 50),   # gold lock
    'G': (210, 160, 30),   # dark gold
    'k': (60, 60, 60),     # keyhole
    '.': None,
}

_CLOCK_PAL = {
    'c': (200, 200, 210),  # clock face
    'C': (160, 160, 170),  # clock shadow
    'r': (80, 80, 90),     # rim
    'R': (60, 60, 70),     # dark rim
    'h': (40, 40, 50),     # hands
    'd': (200, 50, 50),    # center dot
    '.': None,
}

_SHIELD_PAL = {
    's': (80, 120, 200),   # shield blue
    'S': (50, 80, 150),    # dark blue
    'l': (120, 160, 230),  # highlight
    'g': (255, 200, 50),   # gold trim
    'G': (210, 160, 30),   # dark gold
    'w': (220, 220, 230),  # white emblem
    '.': None,
}

_STAR_PAL = {
    'y': (255, 220, 60),   # yellow
    'Y': (220, 180, 30),   # dark yellow
    'l': (255, 245, 150),  # highlight
    '.': None,
}

_COMPASS_PAL = {
    'c': (200, 190, 170),  # compass body
    'C': (160, 150, 130),  # shadow
    'r': (200, 50, 50),    # red needle
    'b': (80, 80, 200),    # blue needle
    'g': (255, 200, 50),   # gold rim
    'G': (210, 160, 30),   # dark gold
    'w': (230, 230, 230),  # white face
    '.': None,
}

_SCROLL_PAL = {
    'p': (230, 215, 180),  # parchment
    'P': (200, 185, 150),  # dark parchment
    'r': (139, 90, 43),    # roll
    'R': (100, 65, 30),    # dark roll
    't': (80, 60, 40),     # text lines
    'x': (200, 50, 50),    # wax seal
    '.': None,
}

# ── Grids (8x8, rendered at scale=2 for 16x16 pixels) ───────────

_TROPHY_GRID = [
    "..lggl..",
    ".gGggGg.",
    "ggGggGgg",
    "ggGggGgg",
    ".gGGGGg.",
    "..gGGg..",
    "..bGGb..",
    ".bBBBBb.",
]

_SWORD_GRID = [
    "......sl",
    ".....slS",
    "....slS.",
    "...slS..",
    "..slS...",
    ".gsSg...",
    ".hHg....",
    ".rH.....",
]

_CHEST_GRID = [
    "........",
    ".bBBBBb.",
    "bllllllb",
    "bBgGgBBb",
    "bBGkGBBb",
    "bBBBBBBb",
    "bBlllBBb",
    ".bBBBBb.",
]

_CLOCK_GRID = [
    "..rRRr..",
    ".RccccR.",
    "Rcc.hccR",
    "Rc..hccR",
    "RccdcccR",
    "Rc...ccR",
    ".RccccR.",
    "..rRRr..",
]

_SHIELD_GRID = [
    ".gGGGGg.",
    "gSlllllg",
    "gSswwSsg",
    "gSswwSsg",
    "gSslllsg",
    ".gSSSSg.",
    "..gSSg..",
    "...gg...",
]

_STAR_GRID = [
    "...yY...",
    "...yY...",
    ".ylYYly.",
    "YYYlYYYY",
    ".YYlYYy.",
    "..YlYy..",
    ".Yy.yYy.",
    ".Y....Y.",
]

_COMPASS_GRID = [
    "..gGGg..",
    ".GwwwwG.",
    "GwwrwwwG",
    "GwwrwwwG",
    "GwwwwwwG",
    "GwwbwwwG",
    ".GwwwwG.",
    "..gGGg..",
]

_SCROLL_GRID = [
    ".rRRRRr.",
    "rpPPPPpr",
    ".ptPtPp.",
    ".ptPtPp.",
    ".pPPPPp.",
    ".ptPtPp.",
    "rpPPPPpr",
    ".rRxRRr.",
]

# ── Build surfaces ───────────────────────────────────────────────
_cache = {}

_ICON_MAP = {
    "trophy": (_TROPHY_GRID, _TROPHY_PAL),
    "sword": (_SWORD_GRID, _SWORD_PAL),
    "chest": (_CHEST_GRID, _CHEST_PAL),
    "clock": (_CLOCK_GRID, _CLOCK_PAL),
    "shield": (_SHIELD_GRID, _SHIELD_PAL),
    "star": (_STAR_GRID, _STAR_PAL),
    "compass": (_COMPASS_GRID, _COMPASS_PAL),
    "scroll": (_SCROLL_GRID, _SCROLL_PAL),
}


def get_achievement_icon(icon_id):
    """Return a 16x16 Surface for the given achievement icon id."""
    if icon_id not in _cache:
        if icon_id in _ICON_MAP:
            grid, pal = _ICON_MAP[icon_id]
            _cache[icon_id] = surface_from_grid(grid, pal, 2)
        else:
            # Fallback: return trophy icon
            grid, pal = _ICON_MAP["trophy"]
            _cache[icon_id] = surface_from_grid(grid, pal, 2)
    return _cache[icon_id]


def get_locked_icon(icon_id):
    """Return a greyed-out version of the achievement icon."""
    key = f"{icon_id}_locked"
    if key not in _cache:
        import pygame
        original = get_achievement_icon(icon_id)
        locked = original.copy()
        # Convert to greyscale by averaging colors
        w, h = locked.get_size()
        for x in range(w):
            for y in range(h):
                r, g, b, a = locked.get_at((x, y))
                if a > 0:
                    grey = (r + g + b) // 3
                    # Darken it further
                    grey = grey // 2
                    locked.set_at((x, y), (grey, grey, grey, a))
        _cache[key] = locked
    return _cache[key]
