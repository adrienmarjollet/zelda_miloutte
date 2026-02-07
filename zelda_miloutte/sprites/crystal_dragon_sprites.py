"""Pixel art sprites for Crystal Dragon boss (large icy dragon, three phases)."""

from zelda_miloutte.sprites.pixel_art import surface_from_grid

# ── Phase 1 Palette (icy blue crystal dragon) ────────────────────
_PAL1 = {
    'o': (20, 30, 50),       # dark outline
    'd': (50, 90, 150),      # dark body
    'D': (70, 120, 180),     # body mid
    'b': (90, 160, 220),     # body light
    'B': (120, 190, 240),    # body highlight
    'c': (180, 220, 255),    # crystal
    'C': (200, 240, 255),    # crystal bright
    'e': (100, 200, 255),    # eye glow
    'E': (60, 160, 230),     # eye edge
    'w': (160, 200, 230),    # wing membrane
    'W': (130, 180, 220),    # wing dark
    'h': (220, 240, 255),    # horn/claw
    't': (80, 140, 200),     # tail
    'T': (60, 110, 170),     # tail dark
    '.': None,
}

# ── Phase 2 Palette (darker, more aggressive) ───────────────────
_PAL2 = {
    'o': (15, 20, 40),       # dark outline
    'd': (40, 70, 130),      # dark body
    'D': (60, 100, 160),     # body mid
    'b': (80, 140, 200),     # body light
    'B': (100, 170, 220),    # body highlight
    'c': (160, 200, 240),    # crystal (duller)
    'C': (180, 220, 250),    # crystal bright
    'e': (255, 120, 60),     # eye glow (now orange-red!)
    'E': (200, 80, 40),      # eye edge
    'w': (140, 180, 210),    # wing membrane
    'W': (110, 160, 200),    # wing dark
    'h': (200, 220, 240),    # horn/claw
    't': (60, 120, 180),     # tail
    'T': (40, 90, 150),      # tail dark
    '.': None,
}

# ── Down frames (24x24 grid, scale=2 -> 48x48px) ────────────────
_DOWN_0 = [
    "........oooooooo........",
    "......oocCCCCCcoo.......",
    ".....odDDbbBBBBDdo......",
    ".....odDbbBBBBBDdo......",
    "....odDdEebbEedDDdo.....",
    "....odDbbbbbbbdDDdo.....",
    "..oodDDbbccbbDDDdoo.....",
    ".oWwdDDbbbbbbDDdwWo.....",
    "oWwwdDDbBBBbDDdwwWo.....",
    "oWwwodDDbbbDDdowwWo.....",
    ".oWwoodDDDDDdoowWo......",
    "..oWwoodddddoowWo.......",
    "...oWwoddddddwWo........",
    "....oWoddddddWo.........",
    ".....ooTttttToo..........",
    "......oTtttTTo...........",
    "......oTtttTTo...........",
    ".....oTTtooTTTo..........",
    ".....oTTo..oTTo..........",
    ".....oTo....oTo..........",
    "......o......o...........",
    ".........................",
    ".........................",
    ".........................",
]

_DOWN_1 = [
    "........oooooooo........",
    "......oocCCCCCcoo.......",
    ".....odDDbbBBBBDdo......",
    ".....odDbbBBBBBDdo......",
    "....odDdEebbEedDDdo.....",
    "....odDbbbbbbbdDDdo.....",
    "..oodDDbbccbbDDDdoo.....",
    ".oWwdDDbbbbbbDDdwWo.....",
    "oWwwdDDbBBBbDDdwwWo.....",
    "oWwwodDDbbbDDdowwWo.....",
    ".oWwoodDDDDDdoowWo......",
    "..oWwoodddddoowWo.......",
    "...oWwoddddddwWo........",
    "....oWoddddddWo.........",
    ".....ooTttttToo..........",
    "......oTtttTTo...........",
    "......oTtttTTo...........",
    ".....oTTtooTTTo..........",
    ".....oTTo..oTTo..........",
    "......oTo...oTo..........",
    "......o......o...........",
    ".........................",
    ".........................",
    ".........................",
]

# ── Up frames ────────────────────────────────────────────────────
_UP_0 = [
    ".........................",
    ".........................",
    ".........................",
    "......o......o...........",
    ".....oTo....oTo..........",
    ".....oTTo..oTTo..........",
    ".....oTTtooTTTo..........",
    "......oTtttTTo...........",
    "......oTtttTTo...........",
    ".....ooTttttToo..........",
    "....oWoddddddWo.........",
    "...oWwoddddddwWo........",
    "..oWwoodddddoowWo.......",
    ".oWwoodDDDDDdoowWo......",
    "oWwwodDDbbbDDdowwWo.....",
    "oWwwdDDbBBBbDDdwwWo.....",
    ".oWwdDDbbbbbbDDdwWo.....",
    "..oodDDbbccbbDDDdoo.....",
    "....odDdddddddDDdo.....",
    "....odDbbbbbbdDDdo......",
    ".....odDDbbBBBBDdo......",
    ".....odDDbbBBBBDdo......",
    "......oocCCCCCcoo.......",
    "........oooooooo........",
]

_UP_1 = [
    ".........................",
    ".........................",
    ".........................",
    "......o......o...........",
    "......oTo...oTo..........",
    ".....oTTo..oTTo..........",
    ".....oTTtooTTTo..........",
    "......oTtttTTo...........",
    "......oTtttTTo...........",
    ".....ooTttttToo..........",
    "....oWoddddddWo.........",
    "...oWwoddddddwWo........",
    "..oWwoodddddoowWo.......",
    ".oWwoodDDDDDdoowWo......",
    "oWwwodDDbbbDDdowwWo.....",
    "oWwwdDDbBBBbDDdwwWo.....",
    ".oWwdDDbbbbbbDDdwWo.....",
    "..oodDDbbccbbDDDdoo.....",
    "....odDdddddddDDdo.....",
    "....odDbbbbbbdDDdo......",
    ".....odDDbbBBBBDdo......",
    ".....odDDbbBBBBDdo......",
    "......oocCCCCCcoo.......",
    "........oooooooo........",
]

# ── Left frames ──────────────────────────────────────────────────
_LEFT_0 = [
    "......oooooooo..........",
    "....oocCCCCcoo..........",
    "...odDDbbBBDdo..........",
    "...odDEebeEDdo..........",
    "..odDDbbbbDDdoo.........",
    "..odDbbccbDDdwWo........",
    ".odDDbbbbDDdwwWo........",
    ".odDDbBBbDDdwwWo........",
    "odDDDbbbDDddwwWo........",
    "odDDDDDDDddowWo.........",
    ".oddddddddoowWo.........",
    "..oTtttttdwWo...........",
    "...oTtttTTo.............",
    "....oTtTTo..............",
    ".....oTTo...............",
    "......oo................",
    "........................",
    "........................",
    "........................",
    "........................",
    "........................",
    "........................",
    "........................",
    "........................",
]

_LEFT_1 = [
    "......oooooooo..........",
    "....oocCCCCcoo..........",
    "...odDDbbBBDdo..........",
    "...odDEebeEDdo..........",
    "..odDDbbbbDDdoo.........",
    "..odDbbccbDDdwWo........",
    ".odDDbbbbDDdwwWo........",
    ".odDDbBBbDDdwwWo........",
    "odDDDbbbDDddwwWo........",
    "odDDDDDDDddowWo.........",
    ".oddddddddoowWo.........",
    "..oTtttttdwWo...........",
    "...oTtttTTo.............",
    "....oTtTTo..............",
    ".....oTTo...............",
    "......oo................",
    "........................",
    "........................",
    "........................",
    "........................",
    "........................",
    "........................",
    "........................",
    "........................",
]

# ── Right frames ─────────────────────────────────────────────────
_RIGHT_0 = [
    "..........oooooooo......",
    "..........oocCCCCcoo....",
    "..........odDBBbbDDdo...",
    "..........odDEebeEDdo...",
    ".........oodDDbbbbDDdo..",
    "........oWwdDDbbccbDdo..",
    "........oWwwdDDbbbbDDdo.",
    "........oWwwdDDbBBbDDdo.",
    "........oWwwddDDbbDDDdo.",
    ".........oWwodddDDDDDdo.",
    ".........oWwooddddddddo.",
    "...........oWwdtttttTo..",
    ".............oTtttTTo...",
    "..............oTTtTo....",
    "...............oTTo.....",
    "................oo......",
    "........................",
    "........................",
    "........................",
    "........................",
    "........................",
    "........................",
    "........................",
    "........................",
]

_RIGHT_1 = [
    "..........oooooooo......",
    "..........oocCCCCcoo....",
    "..........odDBBbbDDdo...",
    "..........odDEebeEDdo...",
    ".........oodDDbbbbDDdo..",
    "........oWwdDDbbccbDdo..",
    "........oWwwdDDbbbbDDdo.",
    "........oWwwdDDbBBbDDdo.",
    "........oWwwddDDbbDDDdo.",
    ".........oWwodddDDDDDdo.",
    ".........oWwooddddddddo.",
    "...........oWwdtttttTo..",
    ".............oTtttTTo...",
    "..............oTTtTo....",
    "...............oTTo.....",
    "................oo......",
    "........................",
    "........................",
    "........................",
    "........................",
    "........................",
    "........................",
    "........................",
    "........................",
]

# ── Build surfaces ───────────────────────────────────────────────
_cache_p1 = None
_cache_p2 = None


def get_crystal_dragon_frames_phase1():
    """Return {direction: [frame0, frame1]} for Crystal Dragon phase 1."""
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


def get_crystal_dragon_frames_phase2():
    """Return {direction: [frame0, frame1]} for Crystal Dragon phase 2 (darker, red eyes)."""
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
