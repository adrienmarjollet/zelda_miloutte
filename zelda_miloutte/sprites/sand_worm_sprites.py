"""Pixel art sprites for the Sand Worm boss (segmented worm, two phases)."""

from .pixel_art import surface_from_grid

# ── Phase 1 Palette (tan/sandy worm) ──────────────────────────────────
_PAL1 = {
    'o': (100, 70, 40),     # dark outline
    'w': (180, 150, 80),    # worm body main (sandy tan)
    'W': (200, 170, 100),   # worm body light/highlight
    's': (140, 110, 60),    # worm body shadow/segment
    'S': (160, 130, 70),    # segment highlight
    'e': (255, 100, 100),   # eyes/mouth red
    'E': (200, 60, 60),     # eye edge (darker red)
    't': (240, 230, 220),   # teeth white
    'T': (200, 190, 180),   # teeth shadow
    'm': (80, 50, 30),      # mouth interior
    '.': None,
}

# ── Phase 2 Palette (darker, redder, angrier) ─────────────────────────
_PAL2 = {
    'o': (80, 50, 30),      # dark outline
    'w': (160, 120, 70),    # worm body darker tan
    'W': (180, 140, 90),    # worm body light
    's': (120, 90, 50),     # worm body shadow
    'S': (140, 110, 60),    # segment highlight
    'e': (255, 80, 40),     # eyes/mouth bright red-orange
    'E': (220, 50, 30),     # eye edge (darker red)
    't': (220, 200, 180),   # teeth off-white
    'T': (180, 160, 140),   # teeth shadow
    'm': (60, 30, 20),      # mouth interior
    '.': None,
}

# ── Burrowed Palette (mostly transparent, just dust) ──────────────────
_PAL_BURROWED = {
    'o': (140, 110, 70),    # dust ring outline
    'd': (180, 150, 100),   # dust particles
    'D': (200, 170, 120),   # dust highlight
    '.': None,
}

# ── Surface frames (24x24 grid, scale=2 → 48x48px) ────────────────────
_SURFACE_DOWN_0 = [
    "........................",
    "........................",
    "........................",
    ".......oooooooooo.......",
    "......owWWWWWWWwo.......",
    ".....owWsssssssWwo......",
    ".....owWsSSSSSsWwo......",
    "....owWsSeEeEeSsWwo.....",
    "....owWsseeeeesWWwo.....",
    "....owWssoommossWwo.....",
    "....owWsomTTTmoWWwo.....",
    "....owWWomtttmoWWwo.....",
    ".....owWWommmoWWwo......",
    ".....owWWWWWWWWwo.......",
    "......owWsssssWwo.......",
    "......owWsSSSsWwo.......",
    ".......owWsssWwo........",
    "........owWsWwo.........",
    ".........owWwo..........",
    "..........owo...........",
    "..........owo...........",
    "...........o............",
    "........................",
    "........................",
]

_SURFACE_DOWN_1 = [
    "........................",
    "........................",
    "........................",
    ".......oooooooooo.......",
    "......owWWWWWWWwo.......",
    ".....owWsssssssWwo......",
    ".....owWsSSSSSsWwo......",
    "....owWsSeEeEeSsWwo.....",
    "....owWsseeeeesWWwo.....",
    "....owWssoommossWwo.....",
    "....owWsomTTTmoWWwo.....",
    "....owWWomtttmoWWwo.....",
    ".....owWWommmoWWwo......",
    ".....owWWWWWWWWwo.......",
    "......owWsssssWwo.......",
    "......owWsSSSsWwo.......",
    ".......owWsssWwo........",
    ".........owWsWwo........",
    "..........owWwo.........",
    "...........owo..........",
    "...........owo..........",
    "............o...........",
    "........................",
    "........................",
]

# ── Up frames (back view, less detail) ────────────────────────────────
_SURFACE_UP_0 = [
    "........................",
    "........................",
    "...........o............",
    "..........owo...........",
    "..........owo...........",
    ".........owWwo..........",
    "........owWsWwo.........",
    ".......owWsssWwo........",
    "......owWsSSSsWwo.......",
    "......owWsssssWwo.......",
    ".....owWWWWWWWWwo.......",
    ".....owWWWWWWWWwo.......",
    "....owWWWWWWWWWWwo......",
    "....owWsssssssssWwo.....",
    "....owWsSSSSSSSsWwo.....",
    ".....owWsssssssWwo......",
    ".....owWWWWWWWWwo.......",
    "......owWWWWWWwo........",
    ".......oooooooo.........",
    "........................",
    "........................",
    "........................",
    "........................",
    "........................",
]

_SURFACE_UP_1 = _SURFACE_UP_0  # Same frame for up

# ── Left frames ───────────────────────────────────────────────────────
_SURFACE_LEFT_0 = [
    "........................",
    "........................",
    "............o...........",
    "...........owo..........",
    "...........owo..........",
    "..........owWwo.........",
    ".........owWsWwo........",
    "........owWsssWwo.......",
    ".......owWsSSSsWwo......",
    "......owWsssssWWwo......",
    ".....owWWWWWWWWWwo......",
    "....omTTTWWWWWWWwo......",
    "....omtttssssssWwo......",
    "....ommmsSSSSSsWwo......",
    ".....oeeeSseEeSwo.......",
    ".....oEeEsseeewo........",
    "......oEEsssswo.........",
    ".......owWWWwo..........",
    "........oooooo..........",
    "........................",
    "........................",
    "........................",
    "........................",
    "........................",
]

_SURFACE_LEFT_1 = [
    "........................",
    "........................",
    "............o...........",
    "...........owo..........",
    "...........owo..........",
    "..........owWwo.........",
    ".........owWsWwo........",
    "........owWsssWwo.......",
    ".......owWsSSSsWwo......",
    "......owWsssssWWwo......",
    ".....owWWWWWWWWWwo......",
    "....omTTTWWWWWWWwo......",
    "....omtttssssssWwo......",
    "....ommmsSSSSSsWwo......",
    ".....oeeeSeEeSswo.......",
    ".....oEeEsseeeewo.......",
    "......oEEsssswo.........",
    ".......owWWWwo..........",
    "........oooooo..........",
    "........................",
    "........................",
    "........................",
    "........................",
    "........................",
]

# ── Right frames (mirror of left) ─────────────────────────────────────
_SURFACE_RIGHT_0 = [
    "........................",
    "........................",
    "...........o............",
    "..........owo...........",
    "..........owo...........",
    ".........owWwo..........",
    "........owWsWwo.........",
    ".......owWsssWwo........",
    "......owWsSSSsWwo.......",
    "......owWWsssssWwo......",
    "......owWWWWWWWWWwo.....",
    "......owWWWWWWWTTTmo....",
    "......owWssssssstttmo...",
    "......owWsSSSSSsmmmmo...",
    ".......owSeEeSseeeeo....",
    "........oweeeessEeEo....",
    ".........owssssEEo......",
    "..........owWWWwo.......",
    "..........oooooo........",
    "........................",
    "........................",
    "........................",
    "........................",
    "........................",
]

_SURFACE_RIGHT_1 = [
    "........................",
    "........................",
    "...........o............",
    "..........owo...........",
    "..........owo...........",
    ".........owWwo..........",
    "........owWsWwo.........",
    ".......owWsssWwo........",
    "......owWsSSSsWwo.......",
    "......owWWsssssWwo......",
    "......owWWWWWWWWWwo.....",
    "......owWWWWWWWTTTmo....",
    "......owWssssssstttmo...",
    "......owWsSSSSSsmmmmo...",
    ".......owsSeEeSeeeeo....",
    ".......oweeeessEeEo.....",
    ".........owssssEEo......",
    "..........owWWWwo.......",
    "..........oooooo........",
    "........................",
    "........................",
    "........................",
    "........................",
    "........................",
]

# ── Burrowed frames (small dust mound, 24x24 grid) ────────────────────
_BURROWED_0 = [
    "........................",
    "........................",
    "........................",
    "........................",
    "........................",
    "........................",
    "........................",
    "........................",
    "........................",
    "........................",
    ".........oooooo.........",
    "........odDDDDdo........",
    ".......odDdddDDdo.......",
    "......odDddddddDdo......",
    ".....odDdddddddddDo.....",
    ".....oddddddddddddo.....",
    "......odddddddddddo.....",
    ".......oooooooooo.......",
    "........................",
    "........................",
    "........................",
    "........................",
    "........................",
    "........................",
]

_BURROWED_1 = [
    "........................",
    "........................",
    "........................",
    "........................",
    "........................",
    "........................",
    "........................",
    "........................",
    "........................",
    "........................",
    ".........oooooo.........",
    "........odDDDDdo........",
    ".......odDddDDDdo.......",
    "......odDdddddddDo......",
    ".....odDddddddddDdo.....",
    ".....odddddddddddddo....",
    "......odddddddddddo.....",
    ".......oooooooooo.......",
    "........................",
    "........................",
    "........................",
    "........................",
    "........................",
    "........................",
]

# ── Build surfaces ────────────────────────────────────────────────────
_cache_surface_p1 = None
_cache_burrowed_p1 = None
_cache_surface_p2 = None
_cache_burrowed_p2 = None


def get_sand_worm_frames_surface():
    """Return {direction: [frame0, frame1]} for Sand Worm phase 1 surface."""
    global _cache_surface_p1
    if _cache_surface_p1 is not None:
        return _cache_surface_p1

    _cache_surface_p1 = {
        "down":  [surface_from_grid(g, _PAL1, 2) for g in (_SURFACE_DOWN_0, _SURFACE_DOWN_1)],
        "up":    [surface_from_grid(g, _PAL1, 2) for g in (_SURFACE_UP_0, _SURFACE_UP_1)],
        "left":  [surface_from_grid(g, _PAL1, 2) for g in (_SURFACE_LEFT_0, _SURFACE_LEFT_1)],
        "right": [surface_from_grid(g, _PAL1, 2) for g in (_SURFACE_RIGHT_0, _SURFACE_RIGHT_1)],
    }
    return _cache_surface_p1


def get_sand_worm_frames_burrowed():
    """Return {direction: [frame0, frame1]} for Sand Worm phase 1 burrowed."""
    global _cache_burrowed_p1
    if _cache_burrowed_p1 is not None:
        return _cache_burrowed_p1

    _cache_burrowed_p1 = {
        "down":  [surface_from_grid(g, _PAL_BURROWED, 2) for g in (_BURROWED_0, _BURROWED_1)],
        "up":    [surface_from_grid(g, _PAL_BURROWED, 2) for g in (_BURROWED_0, _BURROWED_1)],
        "left":  [surface_from_grid(g, _PAL_BURROWED, 2) for g in (_BURROWED_0, _BURROWED_1)],
        "right": [surface_from_grid(g, _PAL_BURROWED, 2) for g in (_BURROWED_0, _BURROWED_1)],
    }
    return _cache_burrowed_p1


def get_sand_worm_frames_surface_p2():
    """Return {direction: [frame0, frame1]} for Sand Worm phase 2 surface."""
    global _cache_surface_p2
    if _cache_surface_p2 is not None:
        return _cache_surface_p2

    _cache_surface_p2 = {
        "down":  [surface_from_grid(g, _PAL2, 2) for g in (_SURFACE_DOWN_0, _SURFACE_DOWN_1)],
        "up":    [surface_from_grid(g, _PAL2, 2) for g in (_SURFACE_UP_0, _SURFACE_UP_1)],
        "left":  [surface_from_grid(g, _PAL2, 2) for g in (_SURFACE_LEFT_0, _SURFACE_LEFT_1)],
        "right": [surface_from_grid(g, _PAL2, 2) for g in (_SURFACE_RIGHT_0, _SURFACE_RIGHT_1)],
    }
    return _cache_surface_p2


def get_sand_worm_frames_burrowed_p2():
    """Return {direction: [frame0, frame1]} for Sand Worm phase 2 burrowed."""
    global _cache_burrowed_p2
    if _cache_burrowed_p2 is not None:
        return _cache_burrowed_p2

    _cache_burrowed_p2 = {
        "down":  [surface_from_grid(g, _PAL_BURROWED, 2) for g in (_BURROWED_0, _BURROWED_1)],
        "up":    [surface_from_grid(g, _PAL_BURROWED, 2) for g in (_BURROWED_0, _BURROWED_1)],
        "left":  [surface_from_grid(g, _PAL_BURROWED, 2) for g in (_BURROWED_0, _BURROWED_1)],
        "right": [surface_from_grid(g, _PAL_BURROWED, 2) for g in (_BURROWED_0, _BURROWED_1)],
    }
    return _cache_burrowed_p2
