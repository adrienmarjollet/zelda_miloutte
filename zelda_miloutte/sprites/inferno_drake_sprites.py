"""Pixel art sprites for the Inferno Drake boss (dragon, two phases)."""

from zelda_miloutte.sprites.pixel_art import surface_from_grid

# ── Phase 1 Palette (red dragon) ──────────────────────────────────────
_PAL1 = {
    'o': (20, 10, 10),      # dark outline
    'r': (150, 30, 20),     # body dark red
    'R': (200, 50, 30),     # body bright red
    'd': (120, 25, 15),     # scales dark
    'D': (180, 40, 25),     # scales bright
    'w': (100, 20, 15),     # wing dark
    'W': (140, 30, 20),     # wing light
    'b': (200, 80, 30),     # belly orange
    'B': (230, 100, 40),    # belly bright orange
    'e': (255, 200, 50),    # eyes glowing yellow
    'E': (200, 150, 30),    # eye edge (darker yellow)
    'h': (80, 60, 40),      # horn dark
    'H': (120, 90, 60),     # horn light
    't': (100, 15, 10),     # teeth dark
    'T': (160, 25, 15),     # teeth light
    'f': (255, 120, 30),    # fire/flame bright
    'F': (200, 80, 20),     # fire/flame dark
    '.': None,
}

# ── Phase 2 Palette (wreathed in flame, brighter) ─────────────────────
_PAL2 = {
    'o': (30, 15, 10),      # dark outline
    'r': (180, 50, 30),     # body dark red (brighter)
    'R': (230, 70, 40),     # body bright red (brighter)
    'd': (150, 40, 25),     # scales dark (brighter)
    'D': (210, 60, 35),     # scales bright (brighter)
    'w': (130, 35, 20),     # wing dark (brighter)
    'W': (170, 50, 30),     # wing light (brighter)
    'b': (230, 100, 40),    # belly orange (brighter)
    'B': (255, 140, 60),    # belly bright orange (brighter)
    'e': (255, 230, 100),   # eyes glowing bright yellow
    'E': (230, 180, 60),    # eye edge (bright yellow)
    'h': (100, 80, 50),     # horn dark (brighter)
    'H': (150, 120, 80),    # horn light (brighter)
    't': (120, 20, 15),     # teeth dark (brighter)
    'T': (180, 35, 20),     # teeth light (brighter)
    'f': (255, 180, 60),    # fire/flame bright (more yellow)
    'F': (255, 120, 40),    # fire/flame dark (more orange)
    '.': None,
}

# ── Down frames (24x24 grid, scale=2 → 48x48px) ──────────────────────
_DOWN_0 = [
    "........................",
    "........oooooooo........",
    ".......oHhooooHho.......",
    "......ohooooooooho......",
    ".....ohhooooooooHHo.....",
    ".....oWWwwwwwwwwWWo.....",
    "....oWwwooooooooWWWo....",
    "....oWWooRRRRRRooWWo....",
    "...oWWooRRRRRRRRooWWo...",
    "...oWoooRdddddddRoooWo..",
    "..oWWooRRdDDDDDdRRooWWo.",
    "..oWooRRRdDbbbDdRRRooWo.",
    "..oooRRRddbbBbbddRRRooo.",
    "..ooRRRRdbbbBbbbdRRRRoo.",
    "..ooRRRRdbBBBBBdRRRRoo..",
    "..ooRRRRdbbBBbbdRRRRoo..",
    "...oRRRRddbbbbddRRRRo...",
    "...oRRRRRddddddRRRRRo...",
    "....oRRRRRRRRRRRRRRo....",
    "....ooRRRoEeoRRRRoo.....",
    ".....oRRRoeeoRRRRo......",
    "......oRRootTRRRo.......",
    ".......oRRRRRRRo........",
    "........oooooo..........",
]

_DOWN_1 = [
    "........................",
    "........oooooooo........",
    ".......oHhooooHho.......",
    "......ohooooooooho......",
    ".....ohhooooooooHHo.....",
    ".....oWWwwwwwwwwWWo.....",
    "....oWwwooooooooWWWo....",
    "....oWWooRRRRRRooWWo....",
    "...oWWooRRRRRRRRooWWo...",
    "...oWoooRdddddddRoooWo..",
    "..oWWooRRdDDDDDdRRooWWo.",
    "..oWooRRRdDbbbDdRRRooWo.",
    "..oooRRRddbbBbbddRRRooo.",
    "..ooRRRRdbbbBbbbdRRRRoo.",
    "..ooRRRRdbBBBBBdRRRRoo..",
    "..ooRRRRdbbBBbbdRRRRoo..",
    "...oRRRRddbbbbddRRRRo...",
    "...oRRRRRddddddRRRRRo...",
    "....oRRRRRRRRRRRRRRo....",
    "....ooRRRoEeoRRRRoo.....",
    ".....oRRRoeeoRRRRo......",
    "......oRRotToRRRo.......",
    ".......oRRRRRRRo........",
    "........oooooo..........",
]

# ── Up frames ─────────────────────────────────────────────────────────
_UP_0 = [
    "........................",
    "........oooooooo........",
    ".......oHhooooHho.......",
    "......ohooooooooho......",
    ".....ohhooooooooHHo.....",
    ".....oWWwwwwwwwwWWo.....",
    "....oWwwooooooooWWWo....",
    "....oWWooRRRRRRooWWo....",
    "...oWWooRRRRRRRRooWWo...",
    "...oWoooRdddddddRoooWo..",
    "..oWWooRRdDDDDDdRRooWWo.",
    "..oWooRRRdDbbbDdRRRooWo.",
    "..oooRRRddbbBbbddRRRooo.",
    "..ooRRRRdbbbbbbbdRRRRoo.",
    "..ooRRRRdbbbbbbbdRRRRoo.",
    "..ooRRRRdbbbbbbbdRRRRoo.",
    "...oRRRRddbbbbbddRRRo...",
    "...oRRRRRddddddRRRRRo...",
    "....oRRRRRRRRRRRRRRo....",
    "....ooRRRRRRRRRRRoo.....",
    ".....oRRRRRRRRRRRo......",
    "......oRRRRRRRRRo.......",
    ".......oRRRRRRRo........",
    "........oooooo..........",
]

_UP_1 = [
    "........................",
    "........oooooooo........",
    ".......oHhooooHho.......",
    "......ohooooooooho......",
    ".....ohhooooooooHHo.....",
    ".....oWWwwwwwwwwWWo.....",
    "....oWwwooooooooWWWo....",
    "....oWWooRRRRRRooWWo....",
    "...oWWooRRRRRRRRooWWo...",
    "...oWoooRdddddddRoooWo..",
    "..oWWooRRdDDDDDdRRooWWo.",
    "..oWooRRRdDbbbDdRRRooWo.",
    "..oooRRRddbbBbbddRRRooo.",
    "..ooRRRRdbbbbbbbdRRRRoo.",
    "..ooRRRRdbbbbbbbdRRRRoo.",
    "..ooRRRRdbbbbbbbdRRRRoo.",
    "...oRRRRddbbbbddRRRRo...",
    "...oRRRRRddddddRRRRRo...",
    "....oRRRRRRRRRRRRRRo....",
    "....ooRRRRRRRRRRRoo.....",
    ".....oRRRRRRRRRRRo......",
    "......oRRRRRRRRRo.......",
    ".......oRRRRRRRo........",
    "........oooooo..........",
]

# ── Left frames ───────────────────────────────────────────────────────
_LEFT_0 = [
    "........................",
    "........oooooooo........",
    ".......ohHoooooo........",
    "......ohhoooooooo.......",
    ".....oHHooooooooo.......",
    ".....oWWWWwwwwwwo.......",
    "....oWWWWooooooo........",
    "....oWWooRRRRRRo........",
    "...oWWooRRRRRRRRo.......",
    "...oWoooRdddddddRo......",
    "..oWWooRRdDDDDDdRRo.....",
    "..oWooRRRdDbbbDdRRo.....",
    "..oooRRRddbbBbbddRRo....",
    "..ooRRRRdbbbBbbbdRRo....",
    "..ooRRRRdbBBBBBdRRRo....",
    "..ooRRRRdbbBBbbdRRRo....",
    "...oRRRRddbbbbddRRRo....",
    "...oRRRRRdddddRRRRRo....",
    "....oRRRRRRRRRRRRRRo....",
    "....ooRRRoEeoRRRRoo.....",
    ".....oRRRoeeoRRRRo......",
    "......oRRotToRRRo.......",
    ".......oRRRRRRRo........",
    "........oooooo..........",
]

_LEFT_1 = [
    "........................",
    "........oooooooo........",
    ".......ohHoooooo........",
    "......ohhoooooooo.......",
    ".....oHHooooooooo.......",
    ".....oWWWWwwwwwwo.......",
    "....oWWWWooooooo........",
    "....oWWooRRRRRRo........",
    "...oWWooRRRRRRRRo.......",
    "...oWoooRdddddddRo......",
    "..oWWooRRdDDDDDdRRo.....",
    "..oWooRRRdDbbbDdRRo.....",
    "..oooRRRddbbBbbddRRo....",
    "..ooRRRRdbbbBbbbdRRo....",
    "..ooRRRRdbBBBBBdRRRo....",
    "..ooRRRRdbbBBbbdRRRo....",
    "...oRRRRddbbbbddRRRo....",
    "...oRRRRRdddddRRRRRo....",
    "....oRRRRRRRRRRRRRRo....",
    "....ooRRRoEeoRRRRoo.....",
    ".....oRRRoeeoRRRRo......",
    "......oRRootTRRRo.......",
    ".......oRRRRRRRo........",
    "........oooooo..........",
]

# ── Right frames ──────────────────────────────────────────────────────
_RIGHT_0 = [
    "........................",
    "........oooooooo........",
    "........ooooooHho.......",
    ".......ooooooooHHo......",
    ".......oooooooooHHo.....",
    ".......owwwwwwWWWWo.....",
    "........oooooooWWWWo....",
    "........oRRRRRRooWWo....",
    ".......oRRRRRRRRooWWo...",
    "......oRdddddddRoooWo...",
    ".....oRRdDDDDDdRRooWWo..",
    ".....oRRdDbbbDdRRRooWo..",
    "....oRRddbbBbbddRRRooo..",
    "....oRRdbbbBbbbdRRRRoo..",
    "....oRRRdBBBBBBdRRRRoo..",
    "....oRRRdbbBBbbdRRRRoo..",
    "....oRRRddbbbbddRRRRo...",
    "....oRRRRRdddddRRRRRo...",
    "....oRRRRRRRRRRRRRRRo...",
    ".....ooRRRRoEeoRRRoo....",
    "......oRRRRoeeoRRRo.....",
    ".......oRRRotToRRo......",
    "........oRRRRRRRo.......",
    "..........oooooo........",
]

_RIGHT_1 = [
    "........................",
    "........oooooooo........",
    "........ooooooHho.......",
    ".......ooooooooHHo......",
    ".......oooooooooHHo.....",
    ".......owwwwwwWWWWo.....",
    "........oooooooWWWWo....",
    "........oRRRRRRooWWo....",
    ".......oRRRRRRRRooWWo...",
    "......oRdddddddRoooWo...",
    ".....oRRdDDDDDdRRooWWo..",
    ".....oRRdDbbbDdRRRooWo..",
    "....oRRddbbBbbddRRRooo..",
    "....oRRdbbbBbbbdRRRRoo..",
    "....oRRRdBBBBBBdRRRRoo..",
    "....oRRRdbbBBbbdRRRRoo..",
    "....oRRRddbbbbddRRRRo...",
    "....oRRRRRdddddRRRRRo...",
    "....oRRRRRRRRRRRRRRRo...",
    ".....ooRRRRoEeoRRRoo....",
    "......oRRRRoeeoRRRo.....",
    ".......oRRRootTRo.......",
    "........oRRRRRRRo.......",
    "..........oooooo........",
]

# ── Build surfaces ────────────────────────────────────────────────────
_cache_p1 = None
_cache_p2 = None


def get_inferno_drake_frames_phase1():
    """Return {direction: [frame0, frame1]} for Inferno Drake phase 1 (red dragon)."""
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


def get_inferno_drake_frames_phase2():
    """Return {direction: [frame0, frame1]} for Inferno Drake phase 2 (wreathed in flame)."""
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
