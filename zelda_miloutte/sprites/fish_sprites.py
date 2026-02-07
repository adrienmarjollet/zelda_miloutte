"""Procedural pixel art sprites for fish (16x16 each)."""

from .pixel_art import surface_from_grid

# ── Palettes ──────────────────────────────────────────────────────

_BASS_PAL = {
    'o': (40, 60, 30),
    'b': (80, 130, 60),
    'B': (60, 100, 45),
    'l': (120, 170, 90),
    'e': (20, 20, 20),
    'w': (200, 200, 180),
    '.': None,
}

_TROUT_PAL = {
    'o': (60, 50, 40),
    'b': (160, 120, 80),
    'B': (130, 95, 60),
    'l': (200, 160, 110),
    'r': (180, 60, 50),
    'e': (20, 20, 20),
    'w': (200, 200, 180),
    '.': None,
}

_GOLDEN_CARP_PAL = {
    'o': (140, 100, 20),
    'b': (255, 210, 60),
    'B': (220, 170, 30),
    'l': (255, 240, 140),
    'e': (20, 20, 20),
    'w': (255, 255, 220),
    's': (255, 255, 180),
    '.': None,
}

_MOSSY_PIKE_PAL = {
    'o': (30, 50, 25),
    'b': (60, 100, 50),
    'B': (45, 75, 35),
    'l': (90, 140, 70),
    'm': (80, 120, 40),
    'e': (20, 20, 20),
    'w': (180, 200, 160),
    '.': None,
}

_MAGIC_CARP_PAL = {
    'o': (60, 30, 100),
    'b': (140, 80, 200),
    'B': (100, 50, 160),
    'l': (180, 130, 240),
    's': (255, 200, 255),
    'e': (40, 20, 60),
    'w': (220, 200, 255),
    '.': None,
}

_SAND_EEL_PAL = {
    'o': (120, 90, 40),
    'b': (210, 180, 120),
    'B': (170, 140, 90),
    'l': (240, 210, 150),
    'e': (40, 30, 10),
    'w': (230, 220, 190),
    '.': None,
}

_OASIS_PERCH_PAL = {
    'o': (30, 80, 100),
    'b': (60, 160, 180),
    'B': (40, 120, 140),
    'l': (100, 200, 220),
    'e': (20, 30, 30),
    'w': (180, 220, 230),
    '.': None,
}

_ANCIENT_FISH_PAL = {
    'o': (60, 50, 30),
    'b': (140, 120, 80),
    'B': (100, 85, 55),
    'l': (180, 160, 110),
    'g': (200, 180, 60),
    'e': (30, 20, 10),
    'w': (220, 210, 180),
    's': (255, 230, 100),
    '.': None,
}

_LAVA_TROUT_PAL = {
    'o': (120, 30, 10),
    'b': (220, 80, 30),
    'B': (180, 50, 15),
    'l': (255, 140, 50),
    'f': (255, 200, 50),
    'e': (60, 10, 5),
    'w': (255, 180, 100),
    '.': None,
}

_MAGMA_FISH_PAL = {
    'o': (100, 20, 10),
    'b': (200, 50, 20),
    'B': (160, 35, 15),
    'l': (255, 100, 30),
    'f': (255, 200, 50),
    'F': (255, 240, 100),
    'e': (50, 10, 5),
    'w': (255, 150, 80),
    '.': None,
}

# ── Grids (16x16) ────────────────────────────────────────────────

_BASS_GRID = [
    "................",
    "................",
    "................",
    ".......oo.......",
    "......oblb......",
    ".oo..obbbbo.....",
    "obboobbbbbo.....",
    "obbbbbbbbbeo....",
    "oBbbbbBbbbweo...",
    "obbbobbbbo......",
    ".oo..obBbo......",
    "......oBb.......",
    ".......oo.......",
    "................",
    "................",
    "................",
]

_TROUT_GRID = [
    "................",
    "................",
    "................",
    ".......oo.......",
    "......olll......",
    ".oo..oblbbo.....",
    "obboobbbbbo.....",
    "oBbbbbrrrbeoo...",
    "obbbbbrrrbweo...",
    "oBbbobbbbo.oo...",
    ".oo..obBbo......",
    "......oBb.......",
    ".......oo.......",
    "................",
    "................",
    "................",
]

_GOLDEN_CARP_GRID = [
    "................",
    "................",
    "......ooo.......",
    ".....oblbo......",
    "....obllbo......",
    ".oo.obbbbbo.....",
    "obboobbbbbo.....",
    "oBbbbbbbbbeo....",
    "obbbbbBbbbweo...",
    "oBbbobbbbo......",
    ".oo.obBbbo......",
    ".....oBBb.......",
    "......ooo.......",
    "................",
    "................",
    "................",
]

_MOSSY_PIKE_GRID = [
    "................",
    "................",
    "................",
    "..........oo....",
    ".........oblb...",
    "........obbbeo..",
    ".oo...obbbbweo..",
    "omboobbbbbbo....",
    "oBbbbbBbbbo.....",
    ".obbobbBbo......",
    "..oo.obbo.......",
    "......oo........",
    "................",
    "................",
    "................",
    "................",
]

_MAGIC_CARP_GRID = [
    "................",
    "................",
    "......ooo.......",
    ".....oblso......",
    "....obllbo......",
    ".oo.obbbbbo.....",
    "osboobbsbbo.....",
    "oBbbbbbbbbeo....",
    "obbbsbBbbbweo...",
    "oBbbobbbbo......",
    ".oo.obBbbo......",
    ".....oBBb.......",
    "......ooo.......",
    "................",
    "................",
    "................",
]

_SAND_EEL_GRID = [
    "................",
    "................",
    "................",
    "................",
    "...........oo...",
    "..........olbeo.",
    ".........oblweo.",
    "........obbbo...",
    ".......obbbo....",
    "...oooobBbo.....",
    "..oBBBBBbo......",
    "..obbbbbo.......",
    "...ooo..........",
    "................",
    "................",
    "................",
]

_OASIS_PERCH_GRID = [
    "................",
    "................",
    "................",
    ".......oo.......",
    "......oblb......",
    ".oo..obllbo.....",
    "obboobbbbbo.....",
    "oBbbbbbbbbeoo...",
    "obbbbbBbbbweo...",
    "obbbobbbbo.oo...",
    ".oo..obBbo......",
    "......oBb.......",
    ".......oo.......",
    "................",
    "................",
    "................",
]

_ANCIENT_FISH_GRID = [
    "................",
    "................",
    ".....oooo.......",
    "....ogblso......",
    "...ogbllbo......",
    ".oo.obbbbbo.....",
    "osboobbsbbo.....",
    "oBbbbbbbbbeo....",
    "obbgsbBgbbweo...",
    "oBbbobbbbo......",
    ".oo.obBbbo......",
    ".....oBBb.......",
    "......ooo.......",
    "................",
    "................",
    "................",
]

_LAVA_TROUT_GRID = [
    "................",
    "................",
    "................",
    ".......oo.......",
    "......olfl......",
    ".oo..oblbbo.....",
    "obboobbfbbo.....",
    "oBbbbbbbbbeo....",
    "obbfbbBbbbweo...",
    "oBbbobbbbo......",
    ".oo..obBbo......",
    "......oBb.......",
    ".......oo.......",
    "................",
    "................",
    "................",
]

_MAGMA_FISH_GRID = [
    "................",
    "................",
    ".....oooo.......",
    "....oFblFo......",
    "...ofbllbo......",
    ".oo.obbfbbo.....",
    "ofboobbbbbo.....",
    "oBbbfbbbbbeoo...",
    "obbbbbBfbbweo...",
    "oBbbobbbbo.oo...",
    ".oo.obBfbo......",
    ".....oBBb.......",
    "......ooo.......",
    "................",
    "................",
    "................",
]

# ── Build and cache ──────────────────────────────────────────────

_FISH_DEFS = {
    "bass":         (_BASS_GRID,         _BASS_PAL),
    "trout":        (_TROUT_GRID,        _TROUT_PAL),
    "golden_carp":  (_GOLDEN_CARP_GRID,  _GOLDEN_CARP_PAL),
    "mossy_pike":   (_MOSSY_PIKE_GRID,   _MOSSY_PIKE_PAL),
    "magic_carp":   (_MAGIC_CARP_GRID,   _MAGIC_CARP_PAL),
    "sand_eel":     (_SAND_EEL_GRID,     _SAND_EEL_PAL),
    "oasis_perch":  (_OASIS_PERCH_GRID,  _OASIS_PERCH_PAL),
    "ancient_fish": (_ANCIENT_FISH_GRID, _ANCIENT_FISH_PAL),
    "lava_trout":   (_LAVA_TROUT_GRID,   _LAVA_TROUT_PAL),
    "magma_fish":   (_MAGMA_FISH_GRID,   _MAGMA_FISH_PAL),
}

_fish_cache = {}


def get_fish_sprite(fish_id):
    """Return a 16x16 Surface for the given fish sprite_id."""
    if fish_id in _fish_cache:
        return _fish_cache[fish_id]
    defn = _FISH_DEFS.get(fish_id)
    if defn is None:
        # Magenta placeholder
        import pygame
        surf = pygame.Surface((16, 16), pygame.SRCALPHA)
        surf.fill((255, 0, 255))
        _fish_cache[fish_id] = surf
        return surf
    grid, palette = defn
    surf = surface_from_grid(grid, palette, 1)
    _fish_cache[fish_id] = surf
    return surf
