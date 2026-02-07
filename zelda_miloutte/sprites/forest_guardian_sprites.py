"""Pixel art sprites for the Forest Guardian boss (tree creature, two phases)."""

from .pixel_art import surface_from_grid

# ── Phase 1 Palette (green/brown tree) ───────────────────────────────
_PAL1 = {
    'o': (20, 15, 10),      # dark outline
    't': (60, 40, 20),      # trunk dark brown
    'T': (90, 60, 30),      # trunk light brown
    'b': (45, 35, 20),      # branch dark
    'B': (70, 50, 25),      # branch light
    'l': (40, 120, 40),     # leaves dark green
    'L': (60, 160, 60),     # leaves bright green
    'g': (50, 140, 50),     # leaves mid green
    'e': (80, 255, 80),     # eyes glowing green
    'E': (40, 180, 40),     # eye edge (darker green)
    'm': (30, 20, 10),      # mouth interior
    'M': (220, 200, 180),   # mouth/teeth (light wood)
    'r': (100, 70, 40),     # roots dark
    'R': (130, 90, 50),     # roots light
    'k': (200, 160, 80),    # knot (wood knot)
    'f': (35, 110, 35),     # foliage shadow
    '.': None,
}

# ── Phase 2 Palette (darker, thorny, red eyes) ────────────────────────
_PAL2 = {
    'o': (30, 15, 10),      # dark outline
    't': (50, 30, 20),      # trunk darker brown
    'T': (70, 45, 25),      # trunk light brown
    'b': (40, 25, 15),      # branch dark
    'B': (60, 40, 20),      # branch light
    'l': (30, 80, 30),      # leaves darker green
    'L': (45, 110, 45),     # leaves mid green
    'g': (35, 90, 35),      # leaves dark green
    'e': (255, 80, 40),     # eyes glowing red-orange
    'E': (200, 40, 20),     # eye edge (darker red)
    'm': (40, 20, 10),      # mouth interior
    'M': (180, 140, 100),   # mouth/teeth (darker wood)
    'r': (90, 60, 35),      # roots dark
    'R': (110, 75, 40),     # roots light
    'k': (150, 100, 50),    # knot (wood knot)
    'f': (25, 70, 25),      # foliage shadow
    '.': None,
}

# ── Down frames (24x24 grid, scale=2 → 48x48px) ──────────────────────
_DOWN_0 = [
    "...oooooooooooooooo.....",
    "..olLLLLLLLLLLLLLLo.....",
    ".olLfLLLLLgLLLLLfLLo....",
    ".oLLLLgggggggggLLLLo....",
    "oLLLLggggllggggLLLLo....",
    "oLLLgglloEeoollggLLo....",
    "oLLLggloEeEeEolggLLo....",
    "oLLgggloeeeeeogggLLo....",
    "oLLggggoommogggggLLo....",
    "oLLoggoomMMmogggLLLo....",
    ".oLLooommmmooggLLLo.....",
    "..oTTTTTTTTTTTTo........",
    "..oTtTTTkkTTTtTo........",
    "..oTTtTTTTTTtTTo........",
    "..oBbTTTTTTTTBbo........",
    "oBbbBTTTTTTTBBbbBo......",
    "oBbbbBTTTTTBBbbbBo......",
    "..oBBbBTTTBBbBBo........",
    "....oRrRRRrRro..........",
    "....oRrRRRrRro..........",
    "...oRrRooRrRro..........",
    "...oRro..oRRro..........",
    "...oRo....oRRo..........",
    "......................",
]

_DOWN_1 = [
    "...oooooooooooooooo.....",
    "..olLLLLLLLLLLLLLLo.....",
    ".olLfLLLLLgLLLLLfLLo....",
    ".oLLLLgggggggggLLLLo....",
    "oLLLLggggllggggLLLLo....",
    "oLLLgglloEeoollggLLo....",
    "oLLLggloEeEeEolggLLo....",
    "oLLgggloeeeeeogggLLo....",
    "oLLggggoommogggggLLo....",
    "oLLLoggoomMmogggLLLo....",
    ".oLLLooommooggLLLo......",
    "..oTTTTTTTTTTTTo........",
    "..oTtTTTkkTTTtTo........",
    "..oTTtTTTTTTtTTo........",
    "..oBbTTTTTTTTBbo........",
    "oBbbBTTTTTTTTBbbBo......",
    "oBbbbBTTTTTTBbbbBo......",
    "..oBBbBTTTBBbBBo........",
    "....oRrRRRrRro..........",
    "....oRrRRRrRro..........",
    "...oRrRooRrRro..........",
    "...oRro..oRRro..........",
    "...oRo....oRRo..........",
    "......................",
]

# ── Up frames ─────────────────────────────────────────────────────────
_UP_0 = [
    "...oooooooooooooooo.....",
    "..olLLLLLLLLLLLLLLo.....",
    ".olLfLLLLLgLLLLLfLLo....",
    ".oLLLLgggggggggLLLLo....",
    "oLLLLggggllggggLLLLo....",
    "oLLLggllgggllggLLLo.....",
    "oLLLggllgggllggLLLo.....",
    "oLLgggllgggllgggLLo.....",
    "oLLgggggggggggggLLo.....",
    "oLLLggggggggggggLLLo....",
    ".oLLLggggggggggLLLo.....",
    "..oTTTTTTTTTTTTo........",
    "..oTtTTTkkTTTtTo........",
    "..oTTtTTTTTTtTTo........",
    "..oBbTTTTTTTTBbo........",
    "oBbbBTTTTTTTBBbbBo......",
    "oBbbbBTTTTTBBbbbBo......",
    "..oBBbBTTTBBbBBo........",
    "....oRrRRRrRro..........",
    "....oRrRRRrRro..........",
    "...oRrRooRrRro..........",
    "...oRro..oRRro..........",
    "...oRo....oRRo..........",
    "......................",
]

_UP_1 = [
    "...oooooooooooooooo.....",
    "..olLLLLLLLLLLLLLLo.....",
    ".olLfLLLLLgLLLLLfLLo....",
    ".oLLLLgggggggggLLLLo....",
    "oLLLLggggllggggLLLLo....",
    "oLLLggllgggllggLLLo.....",
    "oLLLggllgggllggLLLo.....",
    "oLLgggllgggllgggLLo.....",
    "oLLgggggggggggggLLo.....",
    "oLLLoggggggggggLLLo.....",
    ".oLLLggggggggggLLLo.....",
    "..oTTTTTTTTTTTTo........",
    "..oTtTTTkkTTTtTo........",
    "..oTTtTTTTTTtTTo........",
    "..oBbTTTTTTTTBbo........",
    "oBbbBTTTTTTTTBbbBo......",
    "oBbbbBTTTTTTBbbbBo......",
    "..oBBbBTTTBBbBBo........",
    "....oRrRRRrRro..........",
    "....oRrRRRrRro..........",
    "...oRrRooRrRro..........",
    "...oRro..oRRro..........",
    "...oRo....oRRo..........",
    "......................",
]

# ── Left frames ───────────────────────────────────────────────────────
_LEFT_0 = [
    ".....oooooooooooo.......",
    "....olLLLLLLLLLLo.......",
    "...olLfLLLgLLfLLo.......",
    "...oLLLgggggggLLLo......",
    "..oLLLggllllggLLLo......",
    "..oLLggloEeolggLLo......",
    "..oLLggloeEeogggLLo.....",
    "..oLLggloeeeoggggLLo....",
    "oBboLggoomoggggggLLo....",
    "oBBboLggomMogggggLLo....",
    "..obbBooommogggLLLo.....",
    "...oTTTTTTTTTTTo........",
    "...oTtTTkkTTTto.........",
    "...oTTtTTTTtTTo.........",
    "...oBbTTTTTTBbo.........",
    "...oBbBTTTTBbBo.........",
    "...oBbbBTTBbBo..........",
    "....oBBbBBbBo...........",
    "....oRrRRrRRo...........",
    "....oRRrRrRRo...........",
    "...oRrRoRrRo............",
    "...oRro.oRRo............",
    "...oRo...oRo............",
    "........................",
]

_LEFT_1 = [
    ".....oooooooooooo.......",
    "....olLLLLLLLLLLo.......",
    "...olLfLLLgLLfLLo.......",
    "...oLLLgggggggLLLo......",
    "..oLLLggllllggLLLo......",
    "..oLLggloEeolggLLo......",
    "..oLLggloeEeogggLLo.....",
    "..oLLggloeeeoggggLLo....",
    "oBboLggoommogggggLLo....",
    "oBBboLggomMogggggLLo....",
    "..obbBooommogggLLLo.....",
    "...oTTTTTTTTTTTo........",
    "...oTtTTkkTTTto.........",
    "...oTTtTTTTtTTo.........",
    "...oBbTTTTTTBbo.........",
    "...oBbBTTTTBbbBo........",
    "...oBbbBTTBbbbBo........",
    "....oBBbBBbBBo..........",
    "....oRrRRrRRo...........",
    "....oRRrRrRRo...........",
    "...oRrRoRrRo............",
    "...oRro.oRRo............",
    "...oRo...oRo............",
    "........................",
]

# ── Right frames ──────────────────────────────────────────────────────
_RIGHT_0 = [
    ".......oooooooooooo.....",
    ".......olLLLLLLLLLo.....",
    ".......olLfLLgLLfLLo....",
    "......oLLLgggggggLLLo...",
    "......oLLLggllllggLLLo..",
    "......oLLggloEeolggLLo..",
    ".....oLLgggoeEeolgggLo..",
    "....oLLggggoeeeolggLLo..",
    "....oLLggggggoomggLobBo.",
    "....oLLggggggoMmogLobbBo",
    ".....oLLLgggommoogLBbo..",
    "........oTTTTTTTTTTTo...",
    ".........otTTTkkTTtTo...",
    ".........oTTtTTTTtTTo...",
    ".........obBTTTTTTbBo...",
    ".........oBbBTTTTBbBo...",
    "..........oBbBTTBbbBo...",
    "...........oBbBBbBBo....",
    "...........oRRrRRrRo....",
    "...........oRRrRrRRo....",
    "............oRrRoRrRo...",
    "............oRRo.oRRo...",
    "............oRo...oRo...",
    "........................",
]

_RIGHT_1 = [
    ".......oooooooooooo.....",
    ".......olLLLLLLLLLo.....",
    ".......olLfLLgLLfLLo....",
    "......oLLLgggggggLLLo...",
    "......oLLLggllllggLLLo..",
    "......oLLggloEeolggLLo..",
    ".....oLLgggoeEeolgggLo..",
    "....oLLggggoeeeolggLLo..",
    "....oLLggggggoommggLobBo",
    "....oLLggggggoMmogLobbBo",
    ".....oLLLgggommoogLBbo..",
    "........oTTTTTTTTTTTo...",
    ".........otTTTkkTTtTo...",
    ".........oTTtTTTTtTTo...",
    ".........obBTTTTTTbBo...",
    "........oBbbBTTTTBbBo...",
    "........oBbbbBTTBbbBo...",
    ".........oBBbBBbBBo.....",
    "...........oRRrRRrRo....",
    "...........oRRrRrRRo....",
    "............oRrRoRrRo...",
    "............oRRo.oRRo...",
    "............oRo...oRo...",
    "........................",
]

# ── Build surfaces ────────────────────────────────────────────────────
_cache_p1 = None
_cache_p2 = None


def get_forest_guardian_frames_phase1():
    """Return {direction: [frame0, frame1]} for Forest Guardian phase 1 (green tree)."""
    global _cache_p1
    if _cache_p1 is not None:
        return _cache_p1

    _cache_p1 = {
        "down":  [surface_from_grid(g, _PAL1, 2) for g in (_DOWN_0, _DOWN_1)],
        "up":    [surface_from_grid(g, _PAL1, 2) for g in (_UP_0, _UP_1)],
        "left":  [surface_from_grid(g, _PAL1, 2) for g in (_LEFT_0, _LEFT_1)],
        "right": [surface_from_grid(g, _PAL1, 2) for g in (_RIGHT_0, _RIGHT_1)],
    }
    return _cache_p1


def get_forest_guardian_frames_phase2():
    """Return {direction: [frame0, frame1]} for Forest Guardian phase 2 (dark thorny tree)."""
    global _cache_p2
    if _cache_p2 is not None:
        return _cache_p2

    _cache_p2 = {
        "down":  [surface_from_grid(g, _PAL2, 2) for g in (_DOWN_0, _DOWN_1)],
        "up":    [surface_from_grid(g, _PAL2, 2) for g in (_UP_0, _UP_1)],
        "left":  [surface_from_grid(g, _PAL2, 2) for g in (_LEFT_0, _LEFT_1)],
        "right": [surface_from_grid(g, _PAL2, 2) for g in (_RIGHT_0, _RIGHT_1)],
    }
    return _cache_p2
