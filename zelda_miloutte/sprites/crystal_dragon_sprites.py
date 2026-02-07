"""Pixel art sprites for Crystal Dragon boss (large icy dragon, three phases)."""

from .pixel_art import surface_from_grid

# ── Phase 1 Palette (brilliant icy crystal dragon) ──────────────────
_PAL1 = {
    'o': (15, 25, 45),       # dark outline
    'd': (40, 80, 140),      # dark body base
    'D': (60, 110, 170),     # body mid tone
    'b': (80, 140, 200),     # body light
    'B': (100, 170, 230),    # body highlight
    'c': (140, 200, 250),    # crystal base
    'C': (180, 230, 255),    # crystal bright
    'S': (220, 245, 255),    # brilliant sapphire
    's': (200, 235, 255),    # sparkle/prismatic
    'e': (120, 220, 255),    # eye glow (ice blue)
    'E': (80, 180, 240),     # eye edge
    'w': (150, 195, 235),    # wing membrane light
    'W': (110, 160, 210),    # wing bone (darker crystal)
    'h': (230, 250, 255),    # horn/ice crown (brilliant)
    'H': (180, 220, 250),    # horn base
    't': (70, 130, 190),     # tail base
    'T': (50, 100, 160),     # tail dark
    'i': (190, 215, 245),    # ice shard/spike
    'f': (160, 210, 245),    # frost/mist effect
    'p': (120, 180, 230),    # crystal plate mid
    'P': (90, 150, 210),     # crystal plate dark
    '.': None,
}

# ── Phase 2 Palette (darker, aggressive, red eyes) ──────────────────
_PAL2 = {
    'o': (10, 15, 35),       # dark outline
    'd': (35, 65, 120),      # dark body base
    'D': (50, 95, 150),      # body mid tone
    'b': (70, 125, 180),     # body light
    'B': (90, 155, 210),     # body highlight
    'c': (120, 180, 230),    # crystal base (duller)
    'C': (160, 210, 245),    # crystal bright
    'S': (200, 230, 250),    # brilliant sapphire (muted)
    's': (180, 220, 245),    # sparkle/prismatic
    'e': (255, 100, 50),     # eye glow (fiery red-orange!)
    'E': (220, 70, 30),      # eye edge
    'w': (130, 175, 215),    # wing membrane light
    'W': (95, 145, 190),     # wing bone (darker crystal)
    'h': (210, 235, 250),    # horn/ice crown (brilliant)
    'H': (160, 200, 235),    # horn base
    't': (60, 115, 170),     # tail base
    'T': (40, 85, 140),      # tail dark
    'i': (170, 200, 230),    # ice shard/spike
    'f': (140, 190, 225),    # frost/mist effect
    'p': (100, 160, 210),    # crystal plate mid
    'P': (75, 135, 190),     # crystal plate dark
    '.': None,
}

# ── Down frames (24x24 grid, scale=2 -> 48x48px) ────────────────────
_DOWN_0 = [
    "......ooShhhhooo........",
    ".....oShHHHHHHhSo.......",
    "....oShHhsHsHhHhSo......",
    "...odDhHhiiiihHhDdo.....",
    "...odDDEebbbeEDDDdo.....",
    "..odDddbbbbbbbddDdo.....",
    "..odDbpfbbbbfpbDDdo.....",
    ".oodDbpcCCCCcpbDdoo.....",
    ".oWWdDbCsSsSsCbDdWWo....",
    "oWwwdDbcCCCCcbDdwwWo....",
    "oWwwodDpbBBbpDdowwWo....",
    ".oWwoodDpbbpDdoowWo.....",
    "..oWwoodDdDdoowWo.......",
    "...oWwoodddoowWo........",
    "....oWwoodddwWo.........",
    ".....oWoPPPPWo..........",
    "......ooTtiToo..........",
    ".......oTtitTo..........",
    ".......oTttTTo..........",
    "......oTtssTTo..........",
    "......oTTo.oTTo.........",
    ".....oTTo...oTTo........",
    ".....oTo.....oTo........",
    "......o.......o.........",
]

_DOWN_1 = [
    "......ooShhhhSoo........",
    ".....oShHHHHHHhSo.......",
    "....oShHhiHiHhHhSo......",
    "...odDhHhsssshHhDdo.....",
    "...odDDEebbbeEDDDdo.....",
    "..odDddbbbbbbbddDdo.....",
    "..odDbpfbbbbfpbDDdo.....",
    ".oodDbpCcsCsCpbDdoo.....",
    ".oWWdDbcCCCCcbDdWWo.....",
    "oWwwdDbCsSsSCbDdwwWo....",
    "oWwwodDpbBBbpDdowwWo....",
    ".oWwoodDpbbpDdoowWo.....",
    "..oWwoodDdDdoowWo.......",
    "...oWwoodddoowWo........",
    "....oWwodddowWo.........",
    ".....oWoPPPPWo..........",
    "......ooTitToo..........",
    ".......oTttTTo..........",
    ".......oTtitTo..........",
    "......oTTssTTo..........",
    "......oTTo.oTTo.........",
    ".....oTTo...oTTo........",
    "......oTo....oTo........",
    "......o.......o.........",
]

# ── Up frames ────────────────────────────────────────────────────────
_UP_0 = [
    "......o.......o.........",
    ".....oTo.....oTo........",
    ".....oTTo...oTTo........",
    "......oTTo.oTTo.........",
    "......oTtssTTo..........",
    ".......oTttTTo..........",
    ".......oTtitTo..........",
    "......ooTtiToo..........",
    ".....oWoPPPPWo..........",
    "....oWwodddowWo.........",
    "...oWwoodddoowWo........",
    "..oWwoodDdDdoowWo.......",
    ".oWwoodDpbbpDdoowWo.....",
    "oWwwodDpbBBbpDdowwWo....",
    "oWwwdDbcCCCCcbDdwwWo....",
    ".oWWdDbCsSsSsCbDdWWo....",
    ".oodDbpcCCCCcpbDdoo.....",
    "..odDbpfbbbbfpbDDdo.....",
    "..odDddbbbbbbbddDdo.....",
    "...odDDdbbbbdDDDdo......",
    "...odDhHhiiiihHhDdo.....",
    "....oShHhsHsHhHhSo......",
    ".....oShHHHHHHhSo.......",
    "......ooShhhhooo........",
]

_UP_1 = [
    "......o.......o.........",
    "......oTo....oTo........",
    ".....oTTo...oTTo........",
    "......oTTo.oTTo.........",
    "......oTTssTTo..........",
    ".......oTtitTo..........",
    ".......oTttTTo..........",
    "......ooTitToo..........",
    ".....oWoPPPPWo..........",
    "....oWwodddowWo.........",
    "...oWwoodddoowWo........",
    "..oWwoodDdDdoowWo.......",
    ".oWwoodDpbbpDdoowWo.....",
    "oWwwodDpbBBbpDdowwWo....",
    "oWwwdDbCsSsSCbDdwwWo....",
    ".oWWdDbcCCCCcbDdWWo.....",
    ".oodDbpCcsCsCpbDdoo.....",
    "..odDbpfbbbbfpbDDdo.....",
    "..odDddbbbbbbbddDdo.....",
    "...odDDdbbbbdDDDdo......",
    "...odDhHhsssshHhDdo.....",
    "....oShHhiHiHhHhSo......",
    ".....oShHHHHHHhSo.......",
    "......ooShhhhSoo........",
]

# ── Left frames ──────────────────────────────────────────────────────
_LEFT_0 = [
    ".....ooShhhhooo.........",
    "....oShHHHHhSo..........",
    "...oShHhsHshSo..........",
    "..odDhHhiiihDo..........",
    "..odDDEebbeEDdoo........",
    ".odDddbbbbdddWWo........",
    ".odDbpfbbfpbdwwWo.......",
    "odDbpcCCCcpbdwwWo.......",
    "odDbCsSsSCbddwwWo.......",
    "odDbcCCCCcbddowWo.......",
    ".oddpbBBBbpddoowWo......",
    "..oddpbbpDdoowWo........",
    "...oddDdDdoowWo.........",
    "....oddddoowWo..........",
    ".....oddPoWWo...........",
    "......oPPPo.............",
    ".......oTitTo...........",
    "........oTtTo...........",
    "........oTtTo...........",
    ".......oTTsTTo..........",
    "......oTTo.oTTo.........",
    ".....oTTo...oTTo........",
    ".....oTo.....oTo........",
    "......o.......o.........",
]

_LEFT_1 = [
    ".....ooShhhhSoo.........",
    "....oShHHHHhSo..........",
    "...oShHhiHihSo..........",
    "..odDhHhssshDo..........",
    "..odDDEebbeEDdoo........",
    ".odDddbbbbdddWWo........",
    ".odDbpfbbfpbdwwWo.......",
    "odDbpCcsCcpbdwwWo.......",
    "odDbcCCCCcbddwwWo.......",
    "odDbCsSsSCbddowWo.......",
    ".oddpbBBBbpddoowWo......",
    "..oddpbbpDdoowWo........",
    "...oddDdDdoowWo.........",
    "....odddPoowWo..........",
    ".....oddoWWo............",
    "......oPPPo.............",
    ".......oTtTio...........",
    "........oTtTo...........",
    "........oTtTo...........",
    ".......oTsTTTo..........",
    "......oTTo.oTTo.........",
    ".....oTTo...oTTo........",
    "......oTo....oTo........",
    "......o.......o.........",
]

# ── Right frames ─────────────────────────────────────────────────────
_RIGHT_0 = [
    ".........oooShhhhooo....",
    "..........oShHHHHHhSo...",
    "..........oSshHshHhSo...",
    "..........oDhiiihHhDdo..",
    "........oodDEebbEEDDdo..",
    "........oWWdddbbbbdddDdo",
    ".......oWwwdbpfbbfpbDdo.",
    ".......oWwwdbpcCCCcpbDdo",
    ".......oWwwddbCsSsSCbDdo",
    ".......oWwoddcCCCCcbDdo.",
    "......oWwooddpbBBBbpddo.",
    "........oWwoodDpbbpddo..",
    ".........oWwoodDdDddo...",
    "..........oWwoodddddo...",
    "...........oWWoPodddo...",
    ".............oPPPo......",
    "...........oTitTo.......",
    "...........oTtTo........",
    "...........oTtTo........",
    "..........oTTsTTo.......",
    ".........oTTo.oTTo......",
    "........oTTo...oTTo.....",
    "........oTo.....oTo.....",
    ".........o.......o......",
]

_RIGHT_1 = [
    ".........ooShhhhSoo.....",
    "..........oShHHHHHhSo...",
    "..........oShiHiHhHhSo..",
    "..........odhsssHhHhDdo.",
    "........oodDEebbEEDDdo..",
    "........oWWdddbbbbdddDdo",
    ".......oWwwdbpfbbfpbDdo.",
    ".......oWwwdbpcCsCcpbDdo",
    ".......oWwwddbcCCCCcbDdo",
    ".......oWwoddCsSsSCbDdo.",
    "......oWwooddpbBBBbpddo.",
    "........oWwoodDpbbpddo..",
    ".........oWwoodDdDddo...",
    "..........oWwooPdddo....",
    "............oWWoddo.....",
    ".............oPPPo......",
    "...........oiTtTo.......",
    "...........oTtTo........",
    "...........oTtTo........",
    "..........oTTTsTo.......",
    ".........oTTo.oTTo......",
    "........oTTo...oTTo.....",
    "........oTo....oTo......",
    ".........o.......o......",
]

# ── Build surfaces ───────────────────────────────────────────────────
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
