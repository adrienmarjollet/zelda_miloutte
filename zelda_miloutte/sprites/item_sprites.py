"""Pixel art sprites for items (hearts, keys, and inventory items)."""

from zelda_miloutte.sprites.pixel_art import surface_from_grid

# ── Heart palette ─────────────────────────────────────────────────
_HEART_PAL = {
    'o': (100, 15, 15),     # dark red outline
    'r': (220, 40, 40),     # red
    'R': (170, 25, 25),     # dark red
    'l': (255, 90, 90),     # light red
    'p': (255, 160, 160),   # pink highlight
    '.': None,
}

# ── Key palette ───────────────────────────────────────────────────
_KEY_PAL = {
    'o': (120, 90, 10),     # dark gold outline
    'y': (255, 210, 60),    # gold
    'Y': (200, 160, 25),    # darker gold
    'l': (255, 240, 140),   # highlight
    'h': (170, 120, 15),    # handle/center dark
    '.': None,
}

# ── Heart frames (16x16, 2 frames for subtle bob) ────────────────
_HEART_0 = [
    "................",
    "..oooo..oooo....",
    ".opplr..rlppo...",
    ".olrrroorrrrro..",
    "orrrrrrrrrrrro..",
    "orrrrrrrrrrrrro.",
    ".orrrrrrrrrrrro.",
    "..orrrrrrrrrrr..",
    "..orrrrrrrrrro..",
    "...orrrrrrrro...",
    "....orrrrrrr....",
    ".....orrrRRo....",
    "......oRRRo.....",
    ".......oRo......",
    "........o.......",
    "................",
]

_HEART_1 = [
    "................",
    "................",
    "..oooo..oooo....",
    ".opplr..rlppo...",
    ".olrrroorrrrro..",
    "orrrrrrrrrrrro..",
    "orrrrrrrrrrrrro.",
    ".orrrrrrrrrrrro.",
    "..orrrrrrrrrrr..",
    "..orrrrrrrrrro..",
    "...orrrrrrrro...",
    "....orrrrrrr....",
    ".....orrrRRo....",
    "......oRRRo.....",
    ".......oRo......",
    "................",
]

# ── Key frames (16x16, 2 frames for subtle bob) ──────────────────
_KEY_0 = [
    "................",
    "....oooooo......",
    "...oyyllyo......",
    "...oylhhly......",
    "...oylhhly......",
    "...oyyllyo......",
    "....oooooo......",
    ".....oYYo.......",
    ".....oYYo.......",
    ".....oYYo.......",
    ".....oYYo.......",
    ".....oYYYo......",
    ".....oyYo.......",
    ".....oYYYo......",
    ".....oyYo.......",
    "................",
]

_KEY_1 = [
    "................",
    "................",
    "....oooooo......",
    "...oyyllyo......",
    "...oylhhly......",
    "...oylhhly......",
    "...oyyllyo......",
    "....oooooo......",
    ".....oYYo.......",
    ".....oYYo.......",
    ".....oYYo.......",
    ".....oYYo.......",
    ".....oYYYo......",
    ".....oyYo.......",
    ".....oYYYo......",
    "................",
]

# ── Build surfaces ────────────────────────────────────────────────
_heart_cache = None
_key_cache = None


def get_heart_frames():
    """Return [frame0, frame1] for heart item."""
    global _heart_cache
    if _heart_cache is not None:
        return _heart_cache
    _heart_cache = [surface_from_grid(g, _HEART_PAL, 1) for g in (_HEART_0, _HEART_1)]
    return _heart_cache


def get_key_frames():
    """Return [frame0, frame1] for key item."""
    global _key_cache
    if _key_cache is not None:
        return _key_cache
    _key_cache = [surface_from_grid(g, _KEY_PAL, 1) for g in (_KEY_0, _KEY_1)]
    return _key_cache


# ══════════════════════════════════════════════════════════════════
# Inventory item icons (16x16, single frame each)
# ══════════════════════════════════════════════════════════════════

# ── Sword palettes ───────────────────────────────────────────────
_WOOD_SWORD_PAL = {
    'o': (80, 50, 20),      # outline
    'b': (139, 90, 43),     # brown handle
    'B': (100, 65, 30),     # dark brown
    'g': (180, 180, 180),   # gray blade
    'G': (140, 140, 140),   # dark gray
    'l': (220, 220, 220),   # light highlight
    '.': None,
}

_IRON_SWORD_PAL = {
    'o': (60, 60, 70),      # outline
    'b': (139, 90, 43),     # brown handle
    'B': (100, 65, 30),     # dark brown
    'g': (200, 200, 210),   # steel blade
    'G': (150, 150, 165),   # dark steel
    'l': (235, 235, 245),   # highlight
    'y': (255, 210, 60),    # gold crossguard
    '.': None,
}

_FLAME_BLADE_PAL = {
    'o': (100, 20, 10),     # dark outline
    'b': (80, 40, 20),      # dark handle
    'B': (60, 30, 15),      # darker handle
    'r': (220, 60, 20),     # red blade
    'R': (180, 40, 15),     # dark red
    'f': (255, 140, 30),    # flame orange
    'F': (255, 200, 50),    # flame yellow
    'y': (255, 220, 80),    # bright yellow
    '.': None,
}

# ── Shield palettes ──────────────────────────────────────────────
_WOOD_SHIELD_PAL = {
    'o': (70, 45, 15),      # outline
    'b': (139, 100, 50),    # brown
    'B': (110, 75, 35),     # dark brown
    'l': (180, 140, 80),    # light wood
    'n': (100, 65, 25),     # nail/rim
    '.': None,
}

_GUARDIAN_SHIELD_PAL = {
    'o': (40, 50, 70),      # outline
    'b': (80, 120, 180),    # blue steel
    'B': (60, 90, 140),     # dark blue
    'l': (140, 180, 230),   # light blue
    'g': (255, 210, 60),    # gold trim
    'w': (240, 240, 250),   # white gem
    '.': None,
}

_MIRROR_SHIELD_PAL = {
    'o': (60, 60, 80),      # outline
    's': (220, 220, 240),   # silver
    'S': (180, 180, 200),   # dark silver
    'l': (245, 245, 255),   # highlight
    'g': (255, 210, 60),    # gold
    'c': (100, 200, 255),   # cyan gem
    'C': (60, 150, 220),    # dark cyan
    '.': None,
}

# ── Ring palettes ────────────────────────────────────────────────
_POWER_RING_PAL = {
    'o': (80, 40, 10),      # outline
    'g': (255, 210, 60),    # gold
    'G': (200, 160, 30),    # dark gold
    'r': (220, 40, 40),     # red gem
    'R': (160, 20, 20),     # dark red gem
    'l': (255, 240, 140),   # highlight
    '.': None,
}

_FIRE_RING_PAL = {
    'o': (100, 30, 10),     # outline
    'g': (255, 160, 30),    # orange gold
    'G': (200, 120, 20),    # dark orange
    'r': (255, 60, 20),     # fire red
    'R': (200, 30, 10),     # dark fire
    'f': (255, 220, 50),    # flame highlight
    '.': None,
}

_SAGE_RING_PAL = {
    'o': (20, 60, 40),      # outline
    'g': (60, 180, 100),    # green
    'G': (40, 130, 70),     # dark green
    'c': (120, 220, 255),   # cyan gem
    'C': (80, 170, 220),    # dark cyan
    'l': (180, 240, 200),   # highlight
    '.': None,
}

# ── Boots palettes ───────────────────────────────────────────────
_LEATHER_BOOTS_PAL = {
    'o': (70, 40, 15),      # outline
    'b': (150, 100, 50),    # leather
    'B': (120, 75, 35),     # dark leather
    'l': (190, 140, 80),    # highlight
    's': (100, 65, 25),     # sole
    '.': None,
}

_SWIFT_BOOTS_PAL = {
    'o': (30, 60, 80),      # outline
    'b': (80, 150, 200),    # blue leather
    'B': (50, 110, 160),    # dark blue
    'l': (140, 200, 240),   # highlight
    'w': (240, 240, 255),   # white wing
    's': (60, 80, 100),     # sole
    '.': None,
}

_WINGED_BOOTS_PAL = {
    'o': (60, 40, 80),      # outline
    'b': (160, 120, 200),   # purple leather
    'B': (120, 80, 160),    # dark purple
    'l': (200, 170, 240),   # highlight
    'w': (255, 240, 200),   # golden wing
    'W': (255, 210, 140),   # dark golden wing
    's': (80, 50, 100),     # sole
    '.': None,
}

# ── Consumable palettes ─────────────────────────────────────────
_POTION_PAL = {
    'o': (40, 60, 40),      # outline
    'g': (120, 120, 140),   # glass
    'G': (100, 100, 120),   # dark glass
    'l': (160, 160, 180),   # glass highlight
    'p': (80, 200, 80),     # green potion
    'P': (50, 160, 50),     # dark green
    'h': (140, 240, 140),   # potion highlight
    'c': (160, 140, 100),   # cork
    '.': None,
}

_ELIXIR_PAL = {
    'o': (40, 30, 70),      # outline
    'g': (140, 130, 160),   # glass
    'G': (110, 100, 130),   # dark glass
    'l': (180, 170, 200),   # glass highlight
    'p': (180, 80, 220),    # purple elixir
    'P': (140, 50, 180),    # dark purple
    'h': (220, 140, 255),   # elixir highlight
    'c': (200, 180, 140),   # cork
    's': (255, 220, 100),   # sparkle
    '.': None,
}

_ANTIDOTE_PAL = {
    'o': (40, 50, 60),      # outline
    'g': (120, 130, 140),   # glass
    'G': (100, 110, 120),   # dark glass
    'l': (160, 170, 180),   # glass highlight
    'p': (255, 220, 80),    # yellow antidote
    'P': (220, 180, 40),    # dark yellow
    'h': (255, 240, 150),   # antidote highlight
    'c': (140, 120, 90),    # cork
    '.': None,
}

_BOMB_PAL = {
    'o': (30, 30, 30),      # outline
    'b': (60, 60, 70),      # bomb body
    'B': (40, 40, 50),      # dark body
    'l': (90, 90, 100),     # highlight
    'f': (255, 160, 30),    # fuse spark
    'F': (255, 100, 20),    # fuse fire
    'w': (180, 150, 100),   # fuse wick
    '.': None,
}

# ── Icon grids (16x16) ──────────────────────────────────────────

_WOODEN_SWORD_GRID = [
    "..............ol",
    ".............olg",
    "............olg.",
    "...........olg..",
    "..........olg...",
    ".........olg....",
    "........olg.....",
    ".......olg......",
    "......olg.......",
    ".....oBg........",
    "....oBb.........",
    "...oBb..........",
    "..oBb...........",
    ".oBb............",
    ".ob.............",
    ".o..............",
]

_IRON_SWORD_GRID = [
    "..............ol",
    ".............olg",
    "............olg.",
    "...........olg..",
    "..........olg...",
    ".........olg....",
    "........olg.....",
    ".......olg......",
    "......oyg.......",
    ".....oyGy.......",
    "......oBo.......",
    "......oBo.......",
    ".......Bb.......",
    ".......Bb.......",
    "........B.......",
    "................",
]

_FLAME_BLADE_GRID = [
    "..............Fy",
    ".............Ffr",
    "............ofr.",
    "...........ofr..",
    "..........ofr...",
    ".........ofr....",
    "........ofR.....",
    ".......oRR......",
    "......oRr.......",
    ".....oyR........",
    "....oyBy........",
    "......oBo.......",
    "......oBo.......",
    ".......Bb.......",
    ".......Bb.......",
    "........B.......",
]

_WOODEN_SHIELD_GRID = [
    "................",
    "....oooooo......",
    "...obbbbbo......",
    "..oblllllbo.....",
    "..obblbblbo.....",
    "..obbbbbBbo.....",
    "..obblbblbo.....",
    "..obbbbbBbo.....",
    "..obblbblbo.....",
    "..obbbbbBbo.....",
    "...obBBBbo......",
    "....oBBBo.......",
    ".....ooo........",
    "................",
    "................",
    "................",
]

_GUARDIAN_SHIELD_GRID = [
    "................",
    "....oooooo......",
    "...ogggggo......",
    "..oblllllbo.....",
    "..obblbblbo.....",
    "..obbwbbBbo.....",
    "..obblbblbo.....",
    "..obbbbbBbo.....",
    "..obblbblbo.....",
    "..obbbbbBbo.....",
    "...obBBBbo......",
    "....oBBBo.......",
    ".....ooo........",
    "................",
    "................",
    "................",
]

_MIRROR_SHIELD_GRID = [
    "................",
    "....oooooo......",
    "...ogggggo......",
    "..osllllsSo.....",
    "..oSslsslSo.....",
    "..oSscCsSSo.....",
    "..oSslsslSo.....",
    "..oSssssSso.....",
    "..oSslsslSo.....",
    "..oSssssSso.....",
    "...osSSSso......",
    "....oSSSo.......",
    ".....ooo........",
    "................",
    "................",
    "................",
]

_POWER_RING_GRID = [
    "................",
    "................",
    "................",
    "................",
    "......ooo.......",
    "....ooglgoo.....",
    "...ogGlllGgo....",
    "...oGg...gGo....",
    "...og.rRr.go....",
    "...oGg.R.gGo....",
    "...ogGgggGgo....",
    "....oogggoo.....",
    "......ooo.......",
    "................",
    "................",
    "................",
]

_FIRE_RING_GRID = [
    "................",
    "................",
    "................",
    "................",
    "......ooo.......",
    "....oogfgoo.....",
    "...ogGffrGgo....",
    "...oGg...gGo....",
    "...og.rRr.go....",
    "...oGg.R.gGo....",
    "...ogGgggGgo....",
    "....oogggoo.....",
    "......ooo.......",
    "................",
    "................",
    "................",
]

_SAGE_RING_GRID = [
    "................",
    "................",
    "................",
    "................",
    "......ooo.......",
    "....ooglgoo.....",
    "...ogGlllGgo....",
    "...oGg...gGo....",
    "...og.cCc.go....",
    "...oGg.C.gGo....",
    "...ogGgggGgo....",
    "....oogggoo.....",
    "......ooo.......",
    "................",
    "................",
    "................",
]

_LEATHER_BOOTS_GRID = [
    "................",
    "................",
    ".....oo..oo.....",
    "....ollo.llo....",
    "....obbo.bbo....",
    "....obbo.bbo....",
    "....obbo.bbo....",
    "....obbo.bbo....",
    "....obbo.bbo....",
    "...obbbo.bbbo...",
    "..obbBBo.bBBo..",
    "..ossssoosBss..",
    "..ossssoossss...",
    "...oooo..oooo...",
    "................",
    "................",
]

_SWIFT_BOOTS_GRID = [
    "................",
    ".......ww.......",
    ".....oow.ow.....",
    "....ollo.llo....",
    "....obbo.bbo....",
    "...wobbo.bbow...",
    "..w.obbo.bbo.w..",
    "....obbo.bbo....",
    "....obbo.bbo....",
    "...obbbo.bbbo...",
    "..obbBBo.bBBo..",
    "..ossssoossss...",
    "..ossssoossss...",
    "...oooo..oooo...",
    "................",
    "................",
]

_WINGED_BOOTS_GRID = [
    "................",
    "......wWww......",
    ".....oow.oW.....",
    "....ollo.llo....",
    "....obbo.bbo....",
    "..Wwobbo.bboWw..",
    ".W..obbo.bbo..W.",
    "....obbo.bbo....",
    "....obbo.bbo....",
    "...obbbo.bbbo...",
    "..obbBBo.bBBo..",
    "..ossssoossss...",
    "..ossssoossss...",
    "...oooo..oooo...",
    "................",
    "................",
]

_POTION_GRID = [
    "................",
    "................",
    "......ooo.......",
    ".....occco......",
    "......ooo.......",
    ".....ogGo.......",
    "....ogllGo......",
    "...oghhppGo.....",
    "...oppppppo.....",
    "...opphppPo.....",
    "...oppppppo.....",
    "...oPPpPPPo.....",
    "....oPPPPo......",
    ".....oooo.......",
    "................",
    "................",
]

_ELIXIR_GRID = [
    "................",
    ".......s........",
    "......ooo.......",
    ".....occco......",
    "......ooo.......",
    ".....ogGo.......",
    "....ogllGo......",
    "...oghhppGo.....",
    "...opppsppo.....",
    "...opphppPo.....",
    "...opsppppo.....",
    "...oPPpPPPo.....",
    "....oPPPPo......",
    ".....oooo.......",
    "................",
    "................",
]

_ANTIDOTE_GRID = [
    "................",
    "................",
    "......ooo.......",
    ".....occco......",
    "......ooo.......",
    ".....ogGo.......",
    "....ogllGo......",
    "...oghhppGo.....",
    "...oppppppo.....",
    "...opphppPo.....",
    "...oppppppo.....",
    "...oPPpPPPo.....",
    "....oPPPPo......",
    ".....oooo.......",
    "................",
    "................",
]

_BOMB_GRID = [
    "................",
    ".......fF.......",
    "......fw........",
    "......w.........",
    ".....ooo........",
    "....oblbo.......",
    "...obbbBbo......",
    "...obbBBbo......",
    "...obbBBbo......",
    "...obbbBbo......",
    "....obBbo.......",
    ".....ooo........",
    "................",
    "................",
    "................",
    "................",
]

# ── Icon cache and accessor ──────────────────────────────────────
_icon_cache = {}

_ICON_DEFS = {
    "wooden_sword":   (_WOODEN_SWORD_GRID,   _WOOD_SWORD_PAL),
    "iron_sword":     (_IRON_SWORD_GRID,     _IRON_SWORD_PAL),
    "flame_blade":    (_FLAME_BLADE_GRID,    _FLAME_BLADE_PAL),
    "wooden_shield":  (_WOODEN_SHIELD_GRID,  _WOOD_SHIELD_PAL),
    "guardian_shield": (_GUARDIAN_SHIELD_GRID, _GUARDIAN_SHIELD_PAL),
    "mirror_shield":  (_MIRROR_SHIELD_GRID,  _MIRROR_SHIELD_PAL),
    "power_ring":     (_POWER_RING_GRID,     _POWER_RING_PAL),
    "fire_ring":      (_FIRE_RING_GRID,      _FIRE_RING_PAL),
    "sage_ring":      (_SAGE_RING_GRID,      _SAGE_RING_PAL),
    "leather_boots":  (_LEATHER_BOOTS_GRID,  _LEATHER_BOOTS_PAL),
    "swift_boots":    (_SWIFT_BOOTS_GRID,    _SWIFT_BOOTS_PAL),
    "winged_boots":   (_WINGED_BOOTS_GRID,   _WINGED_BOOTS_PAL),
    "potion":         (_POTION_GRID,         _POTION_PAL),
    "elixir":         (_ELIXIR_GRID,         _ELIXIR_PAL),
    "antidote":       (_ANTIDOTE_GRID,       _ANTIDOTE_PAL),
    "bomb":           (_BOMB_GRID,           _BOMB_PAL),
}


def get_inventory_icon(icon_id):
    """Return a 16x16 Surface for the given inventory item icon_id."""
    if icon_id in _icon_cache:
        return _icon_cache[icon_id]
    defn = _ICON_DEFS.get(icon_id)
    if defn is None:
        # Return a magenta placeholder
        import pygame
        surf = pygame.Surface((16, 16), pygame.SRCALPHA)
        surf.fill((255, 0, 255))
        _icon_cache[icon_id] = surf
        return surf
    grid, palette = defn
    surf = surface_from_grid(grid, palette, 1)
    _icon_cache[icon_id] = surf
    return surf
