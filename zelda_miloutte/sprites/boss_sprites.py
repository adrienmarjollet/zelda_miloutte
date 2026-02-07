"""Pixel art sprites for the boss (horned demon, two phases)."""

from .pixel_art import surface_from_grid

# ── Phase 1 Palette (purple demon) ───────────────────────────────
_PAL1 = {
    'o': (15, 5, 25),       # dark outline
    'h': (80, 20, 100),     # horn dark
    'H': (110, 40, 140),    # horn light/tip
    'b': (120, 40, 160),    # body main purple
    'B': (90, 25, 120),     # body dark/shadow
    'l': (150, 70, 190),    # body highlight (lighter purple)
    'e': (255, 80, 40),     # eyes bright (glowing red-orange)
    'E': (180, 30, 20),     # eye edge (darker red)
    'm': (40, 10, 50),      # mouth interior
    'M': (220, 200, 190),   # mouth/fangs (off-white teeth)
    'a': (140, 60, 180),    # arm/claw (lighter purple)
    'A': (100, 35, 130),    # arm dark/claw tip
    'w': (70, 30, 90),      # wing/shoulder spike dark
    'W': (100, 50, 120),    # wing highlight
    'c': (255, 150, 255),   # chest rune (bright glowing)
    'p': (80, 30, 110),     # pants/legs
    'f': (50, 15, 70),      # feet/claws
    'F': (30, 8, 45),       # feet claw tips
    '.': None,
}

# ── Phase 2 Palette (crimson demon) ──────────────────────────────
_PAL2 = {
    'o': (25, 5, 5),        # dark outline
    'h': (120, 20, 20),     # horn dark
    'H': (180, 40, 30),     # horn light/tip
    'b': (200, 50, 50),     # body main crimson
    'B': (150, 30, 30),     # body dark/shadow
    'l': (240, 90, 80),     # body highlight (lighter crimson)
    'e': (255, 255, 80),    # eyes bright (glowing yellow)
    'E': (255, 200, 30),    # eye edge (darker yellow)
    'm': (80, 15, 15),      # mouth interior
    'M': (220, 200, 190),   # mouth/fangs (off-white teeth)
    'a': (220, 80, 70),     # arm/claw (lighter)
    'A': (160, 40, 35),     # arm dark/claw tip
    'w': (130, 30, 25),     # wing/shoulder spike dark
    'W': (170, 50, 45),     # wing highlight
    'c': (255, 255, 150),   # chest rune (bright glowing yellow)
    'p': (120, 25, 25),     # pants/legs
    'f': (80, 15, 15),      # feet/claws
    'F': (50, 10, 10),      # feet claw tips
    '.': None,
}

# ── Down frames (16x16) ──────────────────────────────────────────
_DOWN_0 = [
    "..oHHo....oHHo..",
    ".oHhhHo..oHhhHo.",
    ".ohhHHooooHHhho.",
    "oooBBBBBBBBBBoo.",
    "oBBlbbbbbbbblBo.",
    "oBeEebbbbbEeEBo.",
    "oBbbeebbbeebbBo.",
    "oBobbmmmmmbBoBo.",
    "WwoBlMMMMMlBowW",
    "WwoBbccccbBowW.",
    ".oaAlbbblbAaoo.",
    ".oaaabbbbaaBo...",
    ".ooppppppppo....",
    "..oppooopppo....",
    "..oFFo..oFFo....",
    "................",
]

_DOWN_1 = [
    "..oHHo....oHHo..",
    ".oHhhHo..oHhhHo.",
    ".ohhHHooooHHhho.",
    "oooBBBBBBBBBBoo.",
    "oBBlbbbbbbbblBo.",
    "oBeEebbbbbEeEBo.",
    "oBbbeebbbeebbBo.",
    "oBobbmmmmmboBBo.",
    "WwBBlMMMMMlBowW",
    "WwoBbccccbBBwW.",
    ".ooaAlbblbAaoo..",
    "..oaaabbbbaaBo..",
    "..ooppppppppo...",
    "...oppooopppo...",
    "...oFFo..oFFo...",
    "................",
]

# ── Up frames ─────────────────────────────────────────────────────
_UP_0 = [
    "..oHHo....oHHo..",
    ".oHhhHo..oHhhHo.",
    ".ohhHHooooHHhho.",
    "oooBBBBBBBBBBoo.",
    "oBlBBBBBBBBBBlBo",
    "oBBBBBBBBBBBBBBo",
    "oBlBBBBBBBBBBlBo",
    "oBlBBBBBBBBBBlBo",
    "WwBBBBBBBBBBBBwW",
    "WwBBlBBBBBlBBwW.",
    ".oaBBlBBBlBBaoo.",
    ".oaaaBBBBBaaBo..",
    ".ooppppppppo....",
    "..oppooopppo....",
    "..oFFo..oFFo....",
    "................",
]

_UP_1 = [
    "..oHHo....oHHo..",
    ".oHhhHo..oHhhHo.",
    ".ohhHHooooHHhho.",
    "oooBBBBBBBBBBoo.",
    "oBlBBBBBBBBBBlBo",
    "oBBBBBBBBBBBBBBo",
    "oBlBBBBBBBBBBlBo",
    "oBlBBBBBBBBBBlBo",
    "WwBBBBBBBBBBBwWW",
    "WwBBlBBBBBlBBwW.",
    "..oaBBlBBlBBaoo.",
    "..oaaaBBBBaaBo..",
    "..ooppppppppo...",
    "...oppooopppo...",
    "...oFFo..oFFo...",
    "................",
]

# ── Left frames ───────────────────────────────────────────────────
_LEFT_0 = [
    ".oHHo...........",
    "oHhhHo..........",
    "ohhHHo..........",
    "ooBBBBBBBBoo....",
    "oBlbbbbbbblBo...",
    "oEeEbbbbbbBBo...",
    "oBeebbbbbbBBo...",
    "ommmbbbbbBBBo...",
    "WMMMMbbccbBBwW..",
    "WwBlbbbbbblBwW..",
    ".oAalbbbbbbaoo..",
    ".oaaaabbbbaBo...",
    ".oopppppppppo...",
    "..oppooopppo....",
    "..oFFo..oFFo....",
    "................",
]

_LEFT_1 = [
    ".oHHo...........",
    "oHhhHo..........",
    "ohhHHo..........",
    "ooBBBBBBBBoo....",
    "oBlbbbbbbblBo...",
    "oEeEbbbbbbBBo...",
    "oBeebbbbbbBBo...",
    "ommmbbbbBBBBo...",
    "WMMMMbbccbBBwW..",
    "WwBlbbbbbblBwW..",
    "..oAalbbbbbao...",
    "..oaaaabbbaBo...",
    "..oopppppppppo..",
    "...oppooopppo...",
    "...oFFo..oFFo...",
    "................",
]

# ── Right frames ──────────────────────────────────────────────────
_RIGHT_0 = [
    ".........oHHo...",
    "........oHhhHo..",
    "........oHHhho..",
    "....ooBBBBBBBoo.",
    "...oBlbbbbbbblBo",
    "...oBBbbbbbbEeEo",
    "...oBBbbbbbbeeEo",
    "...oBBBbbbbmmmo.",
    "..WwBBbccbbMMMMW",
    "..WwBlbbbbbblBwW",
    "..ooabbbbblaAo..",
    "...oBabbbaaaao..",
    "...opppppppppoo.",
    "....opppoopppo..",
    "....oFFo..oFFo..",
    "................",
]

_RIGHT_1 = [
    ".........oHHo...",
    "........oHhhHo..",
    "........oHHhho..",
    "....ooBBBBBBBoo.",
    "...oBlbbbbbbblBo",
    "...oBBbbbbbbEeEo",
    "...oBBbbbbbbeeEo",
    "...oBBBBbbmmmo..",
    "..WwBBbccbbMMMMW",
    "..WwBlbbbbbblBwW",
    "...oabbbblaAo...",
    "...oBabbaaaao...",
    "..opppppppppoo..",
    "...opppoopppo...",
    "...oFFo..oFFo...",
    "................",
]

# ── Build surfaces ────────────────────────────────────────────────
_cache_p1 = None
_cache_p2 = None


def get_boss_frames_phase1():
    """Return {direction: [frame0, frame1]} for boss phase 1 (purple)."""
    global _cache_p1
    if _cache_p1 is not None:
        return _cache_p1

    _cache_p1 = {
        "down":  [surface_from_grid(g, _PAL1, 3) for g in (_DOWN_0, _DOWN_1)],
        "up":    [surface_from_grid(g, _PAL1, 3) for g in (_UP_0, _UP_1)],
        "left":  [surface_from_grid(g, _PAL1, 3) for g in (_LEFT_0, _LEFT_1)],
        "right": [surface_from_grid(g, _PAL1, 3) for g in (_RIGHT_0, _RIGHT_1)],
    }
    return _cache_p1


def get_boss_frames_phase2():
    """Return {direction: [frame0, frame1]} for boss phase 2 (crimson)."""
    global _cache_p2
    if _cache_p2 is not None:
        return _cache_p2

    _cache_p2 = {
        "down":  [surface_from_grid(g, _PAL2, 3) for g in (_DOWN_0, _DOWN_1)],
        "up":    [surface_from_grid(g, _PAL2, 3) for g in (_UP_0, _UP_1)],
        "left":  [surface_from_grid(g, _PAL2, 3) for g in (_LEFT_0, _LEFT_1)],
        "right": [surface_from_grid(g, _PAL2, 3) for g in (_RIGHT_0, _RIGHT_1)],
    }
    return _cache_p2


# Boss 2 Phase 1 Palette (ice blue/cyan demon)
_BOSS2_PAL1 = {
    'o': (10, 20, 35),      # dark outline
    'h': (60, 120, 160),    # horn ice blue dark
    'H': (100, 170, 210),   # horn ice blue light
    'b': (90, 160, 200),    # body cyan
    'B': (60, 130, 170),    # body dark ice
    'l': (130, 200, 240),   # body highlight (lighter cyan)
    'e': (200, 250, 255),   # eyes bright cyan (glowing)
    'E': (130, 210, 245),   # eye edge (darker cyan)
    'm': (30, 60, 90),      # mouth interior
    'M': (220, 230, 240),   # mouth/fangs (icy white)
    'a': (120, 190, 230),   # arm/claw (lighter cyan)
    'A': (70, 140, 180),    # arm dark/claw tip
    'w': (50, 100, 140),    # wing/shoulder spike dark
    'W': (80, 140, 180),    # wing highlight
    'c': (180, 240, 255),   # chest marking (bright cyan glow)
    'p': (60, 110, 150),    # pants/legs
    'f': (40, 70, 100),     # feet/claws
    'F': (25, 45, 65),      # feet claw tips
    '.': None,
}

# Boss 2 Phase 2 Palette (dark blue/navy demon)
_BOSS2_PAL2 = {
    'o': (5, 10, 20),       # dark outline
    'h': (30, 50, 100),     # horn dark navy
    'H': (50, 80, 140),     # horn navy light
    'b': (40, 70, 130),     # body dark blue
    'B': (25, 45, 90),      # body very dark blue
    'l': (60, 100, 170),    # body highlight (lighter navy)
    'e': (255, 250, 120),   # eyes bright yellow (glowing)
    'E': (230, 210, 70),    # eye edge (darker yellow)
    'm': (15, 25, 50),      # mouth interior
    'M': (200, 190, 180),   # mouth/fangs (grayish white)
    'a': (60, 100, 160),    # arm/claw (lighter blue)
    'A': (35, 60, 110),     # arm dark/claw tip
    'w': (30, 50, 90),      # wing/shoulder spike dark
    'W': (45, 75, 120),     # wing highlight
    'c': (120, 180, 255),   # chest marking (bright blue glow)
    'p': (30, 50, 100),     # pants/legs
    'f': (20, 35, 70),      # feet/claws
    'F': (12, 20, 45),      # feet claw tips
    '.': None,
}

_cache_boss2_p1 = None
_cache_boss2_p2 = None


def get_boss2_frames_phase1():
    """Return {direction: [frame0, frame1]} for boss 2 phase 1 (ice blue/cyan)."""
    global _cache_boss2_p1
    if _cache_boss2_p1 is not None:
        return _cache_boss2_p1

    _cache_boss2_p1 = {
        "down":  [surface_from_grid(g, _BOSS2_PAL1, 3) for g in (_DOWN_0, _DOWN_1)],
        "up":    [surface_from_grid(g, _BOSS2_PAL1, 3) for g in (_UP_0, _UP_1)],
        "left":  [surface_from_grid(g, _BOSS2_PAL1, 3) for g in (_LEFT_0, _LEFT_1)],
        "right": [surface_from_grid(g, _BOSS2_PAL1, 3) for g in (_RIGHT_0, _RIGHT_1)],
    }
    return _cache_boss2_p1


def get_boss2_frames_phase2():
    """Return {direction: [frame0, frame1]} for boss 2 phase 2 (dark blue/navy)."""
    global _cache_boss2_p2
    if _cache_boss2_p2 is not None:
        return _cache_boss2_p2

    _cache_boss2_p2 = {
        "down":  [surface_from_grid(g, _BOSS2_PAL2, 3) for g in (_DOWN_0, _DOWN_1)],
        "up":    [surface_from_grid(g, _BOSS2_PAL2, 3) for g in (_UP_0, _UP_1)],
        "left":  [surface_from_grid(g, _BOSS2_PAL2, 3) for g in (_LEFT_0, _LEFT_1)],
        "right": [surface_from_grid(g, _BOSS2_PAL2, 3) for g in (_RIGHT_0, _RIGHT_1)],
    }
    return _cache_boss2_p2
