"""Pixel art sprites for the Sand Worm boss (segmented worm, two phases)."""

from .pixel_art import surface_from_grid

# ── Phase 1 Palette (tan/sandy worm with armor plates) ────────────────
_PAL1 = {
    'o': (60, 40, 20),      # dark outline / deep shadows
    'w': (180, 150, 80),    # worm body main (sandy tan)
    'W': (210, 180, 110),   # worm body light/highlight
    's': (140, 110, 60),    # worm body shadow/segment
    'S': (160, 130, 70),    # segment highlight
    'a': (120, 95, 55),     # armor plate dark
    'A': (150, 120, 65),    # armor plate medium
    'B': (170, 140, 75),    # armor plate light
    'u': (200, 170, 100),   # underbelly soft
    'U': (220, 190, 120),   # underbelly highlight
    'e': (255, 60, 60),     # eyes bright red
    'E': (180, 40, 40),     # eye dark red
    't': (255, 245, 235),   # teeth bright white
    'T': (220, 210, 200),   # teeth mid
    'h': (180, 170, 160),   # teeth shadow
    'm': (40, 20, 10),      # mouth interior (gullet)
    'M': (60, 30, 15),      # mouth interior lighter
    'g': (80, 50, 30),      # gums/mouth edge
    'G': (100, 60, 35),     # gums lighter
    'l': (140, 180, 100),   # slime/drool green
    'L': (100, 140, 70),    # slime dark
    '.': None,
}

# ── Phase 2 Palette (darker, redder, angrier) ─────────────────────────
_PAL2 = {
    'o': (40, 25, 15),      # dark outline
    'w': (160, 120, 70),    # worm body darker tan
    'W': (190, 150, 90),    # worm body light
    's': (120, 90, 50),     # worm body shadow
    'S': (140, 110, 60),    # segment highlight
    'a': (100, 75, 45),     # armor plate dark
    'A': (130, 100, 55),    # armor plate medium
    'B': (150, 120, 65),    # armor plate light
    'u': (180, 140, 80),    # underbelly soft
    'U': (200, 160, 100),   # underbelly highlight
    'e': (255, 80, 40),     # eyes bright red-orange
    'E': (200, 50, 20),     # eye dark red
    't': (240, 220, 200),   # teeth off-white
    'T': (200, 180, 160),   # teeth mid
    'h': (160, 140, 120),   # teeth shadow
    'm': (30, 15, 10),      # mouth interior
    'M': (50, 25, 15),      # mouth interior lighter
    'g': (70, 40, 25),      # gums/mouth edge
    'G': (90, 50, 30),      # gums lighter
    'l': (120, 160, 80),    # slime/drool green
    'L': (80, 120, 50),     # slime dark
    '.': None,
}

# ── Burrowed Palette (dust cloud with ground cracks) ──────────────────
_PAL_BURROWED = {
    'o': (100, 80, 50),     # dust ring outline / cracks
    'O': (80, 60, 40),      # darker cracks
    'd': (180, 150, 100),   # dust particles
    'D': (210, 180, 130),   # dust highlight
    'p': (160, 130, 90),    # dust medium
    'P': (140, 110, 70),    # dust shadow
    'r': (120, 100, 60),    # ground ripples
    'R': (100, 80, 50),     # ripples dark
    '.': None,
}

# ── Surface frames (24x24 grid, scale=2 → 48x48px) ────────────────────
# DOWN frames: Massive circular mouth with rings of teeth, compound eyes, segmented body
_SURFACE_DOWN_0 = [
    "........................",
    "........................",
    "......oooooooooooo......",
    ".....oWWWWWWWWWWWWo.....",
    "....oWAAAaBBBaAAAAWo....",
    "....oWaeeoBBBoeeaAWo....",
    "...oWAeEeaBaBeaEeeAWo...",
    "...oWBeeoGggggGoeeBWo...",
    "..oWAaoGgtTtTtTtGaAAWo..",
    "..oWBaGgThhmMmhhTgGaBWo.",
    "..oWAaGthmmmmmmmhTGaAWo.",
    "..oWBaGthmLmmmLmhtGaBWo.",
    "..oWAaGthmmmmmmMhtGaAWo.",
    "..oWBaGgThhmmmhhTgGaBWo.",
    "..oWAaoGgtTthtTtGaaAWo..",
    "...oWBsaoGgglgGoasBWo...",
    "...oWAssaBaBaBaasAWo....",
    "....oWuUssBBBssuUWo.....",
    "....oWUuusBaBsuuUWo.....",
    ".....oWuUsaBasuUWo......",
    "......oWusaBsuWo........",
    ".......oWusuWo..........",
    "........oWUWo...........",
    ".........oo.............",
]

_SURFACE_DOWN_1 = [
    "........................",
    "........................",
    "......oooooooooooo......",
    ".....oWWWWWWWWWWWWo.....",
    "....oWAAAaBBBaAAAAWo....",
    "....oWaeeoaBaoeeeAWo....",
    "...oWAeeEaBBBaEeeoAWo...",
    "...oWBseoGggggGoesBWo...",
    "..oWAAaGgtTtTtTtGaaAWo..",
    "..oWBaGgthhMmMhhTgGaBWo.",
    "..oWAaGthmmmmmmmhtGaAWo.",
    "..oWBaGthLmmmmmLhtGaBWo.",
    "..oWAaGthmMmMmmmhtGaAWo.",
    "..oWBaGgthhmmMhhTgGaBWo.",
    "..oWAaaGgtTthTtTGoaAWo..",
    "...oWBsaoGggllGoasBWo...",
    "...oWAassBaBaBassAWo....",
    "....oWuUusBBBsuUUWo.....",
    "....oWUuusaBasuuUWo.....",
    ".....oWuUsBaBsuUWo......",
    "......oWusaBsuWo........",
    ".......oWusuWo..........",
    "........oWUWo...........",
    ".........oo.............",
]

# UP frames: Back view showing armored segments tapering down
_SURFACE_UP_0 = [
    "........................",
    ".........oo.............",
    "........oWUWo...........",
    ".......oWusuWo..........",
    "......oWusaBsuWo........",
    ".....oWuUsaBasuUWo......",
    "....oWUuusBaBsuuUWo.....",
    "....oWuUssBBBssuUWo.....",
    "...oWAssaBaBaBassAWo....",
    "...oWBssBaBaBaBssBWo....",
    "..oWAaaBaBaBaBaBaaAWo...",
    "..oWBAABaBaBaBaBABBWo...",
    "..oWAAAaBaBaBaBaAAAWo...",
    "..oWWAAABaBaBaBAAAAWo...",
    "...oWWAAaBaBaBaAAWWo....",
    "...oWWWABaBaBaBAWWWo....",
    "....oWWWaBaBaBaWWWo.....",
    "....oWWWWBaBaBWWWWo.....",
    ".....oWWWWaBaWWWWo......",
    ".....oWWWWWBWWWWWo......",
    "......oWWWWWWWWWo.......",
    ".......oooooooo.........",
    "........................",
    "........................",
]

_SURFACE_UP_1 = _SURFACE_UP_0  # Same frame for up

# LEFT frames: Side view with mouth, eye cluster, undulating segments
_SURFACE_LEFT_0 = [
    "........................",
    "........................",
    "............oo..........",
    "...........oWWo.........",
    "..........oWuUWo........",
    ".........oWusUWo........",
    "........oWusaBWo........",
    ".......oWusBaBWo........",
    "......oWusBaBaWo........",
    ".....oWUsaBaBaWo........",
    "....oWusBaBaBAAo........",
    "...oGgtTBaBaBAAWo.......",
    "...oGthMaBaBaAAWo.......",
    "...oGthmaBaBAAAWWo......",
    "...oGthMmBasAAWWWo......",
    "...oGthmmaeeEeAWWo......",
    "...oGgtTaoEeeeAAWo......",
    "....oGgGaeEeeoAWo.......",
    ".....ooglLeeoAWo........",
    "......ooaoeoaWo.........",
    ".........oaoWo..........",
    "..........oWo...........",
    "...........o............",
    "........................",
]

_SURFACE_LEFT_1 = [
    "........................",
    "........................",
    "............oo..........",
    "...........oWWo.........",
    "..........oWUuWo........",
    ".........oWusuWo........",
    "........oWusBaWo........",
    ".......oWuaBaBWo........",
    "......oWusBaBaWo........",
    ".....oWusBaBaBWo........",
    "....oWUsaBaBaAAo........",
    "...oGgtTBaBaBAAWo.......",
    "...oGthmaBaBaAAWo.......",
    "...oGthMaBaBAAAWWo......",
    "...oGthmMBaaAAWWWo......",
    "...oGthmmaeEeeAWWo......",
    "...oGgtTaoeEeEAAWo......",
    "....oGgGaeeEeoAWo.......",
    ".....oogLleeaAWo........",
    "......ooaoeoaWo.........",
    ".........oaoWo..........",
    "..........oWo...........",
    "...........o............",
    "........................",
]

# RIGHT frames: Mirror of left
_SURFACE_RIGHT_0 = [
    "........................",
    "........................",
    "..........oo............",
    ".........oWWo...........",
    "........oWUuWo..........",
    "........oWUsuo..........",
    "........oWaBsuo.........",
    "........oWaBaBsuo.......",
    "........oWaBaBsuo.......",
    "........oWaBaBasUWo.....",
    "........oAABaBaBsuWo....",
    ".......oWAABaBaBTtGGo...",
    ".......oWAAaBaBaMhtGo...",
    "......oWWAAABaBamhtGo...",
    "......oWWWAAsaBMmhtGo...",
    "......oWWeEeeamhtGo.....",
    "......oWAAeeeEoaTtGGo...",
    ".......oWAoeeEeaGgGo....",
    "........oWAoeeLlgoo.....",
    ".........oWaoeoaoo......",
    "..........oWoao.........",
    "...........oWo..........",
    "............o...........",
    "........................",
]

_SURFACE_RIGHT_1 = [
    "........................",
    "........................",
    "..........oo............",
    ".........oWWo...........",
    "........oWuUWo..........",
    "........oWusuo..........",
    "........oWaBsuo.........",
    "........oWaBaBuo........",
    "........oWaBaBsuo.......",
    "........oWaBaBsBuWo.....",
    "........oAAaBaBsUWo.....",
    ".......oWAABaBaBTtGGo...",
    ".......oWAAaBaBamhtGo...",
    "......oWWAAABaBaMhtGo...",
    "......oWWWAAaaBMmhtGo...",
    "......oWWAeeEeamhtGo....",
    "......oWAAEeEeoaTtGGo...",
    ".......oWAoeeEeaGgGo....",
    "........oWAaeeLlgoo.....",
    ".........oWaoeoaoo......",
    "..........oWoao.........",
    "...........oWo..........",
    "............o...........",
    "........................",
]

# ── Burrowed frames (dust cloud with ground cracks, radial spray) ──────
_BURROWED_0 = [
    "........................",
    "........................",
    "............d...........",
    "........d...............",
    "...........D...........d",
    "........................",
    "..d........OOOOo........",
    ".......OOOorrrrrOOOo....",
    "......OrrrRRRRRRrrrO....",
    ".....OrRRoooooooooRrO...",
    "....OrRoDDdddddddDDoRO..",
    "....OrRodDpppppppDdoRo..",
    "...OrRodDpPPPPPPPPdDoRo.",
    "...oRRodpPPdddddPPpoRRo.",
    "...oRRodpPdddddddPpoRRo.",
    "...OrRodDPddddddDPdoRro.",
    "....OroodDpPPPPpDdooRo..",
    "....OrRoddDDDDDDdooRro..",
    ".....OrrooooooooooRro...",
    "......OrrrRRRRRRrrrO....",
    ".......OOOorrrrrOOo.....",
    "..........oOOOOo........",
    ".......d................",
    "..d.............D.......",
]

_BURROWED_1 = [
    "........................",
    ".........D..............",
    "........................",
    "......d................d",
    "..d.....................",
    "............OOOo........",
    ".......OOOorrrrrOOo.....",
    "......OrrrRRRRRRrrrO....",
    ".....OrRRoooooooooRRo...",
    "....OrRoDdddddddddDoRo..",
    "...OrRodDpppppppppDdoRo.",
    "...oRRodDPPPPPPPPPDdoRRo",
    "...oRRodpPPdddddPPpoRRo.",
    "...oRRodpPddddddPPpoRRo.",
    "...OrRodDPPddddDPPdoRro.",
    "....OroodDpPPPPPDdooRo..",
    "....OrRoodDDDDDddooRro..",
    ".....OrrRooooooooRRro...",
    "......OrrrrRRRRrrrro....",
    ".......OOOorrrrrOOo.....",
    "..........oOOOoo........",
    "........d...............",
    "...............D........",
    "..D.....................",
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
