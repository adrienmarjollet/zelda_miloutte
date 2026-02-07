"""Pixel art sprites for the Forest Guardian boss (tree creature, two phases)."""

from .pixel_art import surface_from_grid

# ── Phase 1 Palette (green/brown tree) ───────────────────────────────
_PAL1 = {
    'o': (20, 15, 10),       # dark outline
    't': (60, 40, 20),       # trunk dark brown
    'T': (90, 60, 30),       # trunk light brown
    'u': (45, 25, 15),       # trunk very dark (shadow)
    'U': (110, 75, 40),      # trunk reddish-brown
    'b': (45, 35, 20),       # branch dark
    'B': (70, 50, 25),       # branch light
    'a': (55, 40, 22),       # bark texture mid
    'A': (80, 55, 28),       # bark texture light
    'l': (40, 120, 40),      # leaves dark green
    'L': (60, 160, 60),      # leaves bright green
    'g': (50, 140, 50),      # leaves mid green
    'G': (70, 180, 70),      # leaves yellow-green
    'j': (30, 100, 30),      # leaves forest dark
    'J': (45, 130, 45),      # leaves emerald
    'e': (80, 255, 80),      # eyes glowing green
    'E': (40, 180, 40),      # eye edge (darker green)
    'i': (20, 100, 20),      # eye socket shadow
    'm': (30, 20, 10),       # mouth interior
    'M': (220, 200, 180),    # mouth/teeth (light wood)
    'n': (50, 35, 20),       # mouth crack dark
    'r': (100, 70, 40),      # roots dark
    'R': (130, 90, 50),      # roots light
    'k': (200, 160, 80),     # knot (wood knot)
    'K': (180, 140, 70),     # knot darker
    'f': (35, 110, 35),      # foliage shadow
    's': (55, 180, 55),      # moss bright
    'S': (35, 120, 35),      # moss dark
    'h': (220, 180, 100),    # beehive/honey
    'H': (200, 150, 70),     # beehive dark
    'v': (100, 70, 50),      # vine brown
    'V': (80, 60, 40),       # vine dark
    'p': (255, 220, 180),    # flower petal light
    'P': (255, 180, 200),    # flower petal pink
    'c': (180, 140, 100),    # dirt/mud light
    'C': (120, 90, 60),      # dirt/mud dark
    'd': (140, 100, 70),     # dirt mid
    'w': (100, 80, 50),      # twig
    'W': (80, 60, 35),       # twig dark
    'z': (220, 200, 100),    # glowing sap
    'Z': (255, 240, 120),    # glowing sap bright
    'y': (200, 80, 60),      # mushroom cap
    'Y': (180, 60, 40),      # mushroom cap dark
    'x': (240, 230, 220),    # mushroom stem
    '.': None,
}

# ── Phase 2 Palette (darker, thorny, red eyes) ────────────────────────
_PAL2 = {
    'o': (30, 15, 10),       # dark outline
    't': (50, 30, 20),       # trunk darker brown
    'T': (70, 45, 25),       # trunk light brown
    'u': (35, 20, 12),       # trunk very dark (shadow)
    'U': (80, 50, 30),       # trunk reddish-brown
    'b': (40, 25, 15),       # branch dark
    'B': (60, 40, 20),       # branch light
    'a': (45, 30, 18),       # bark texture mid
    'A': (65, 45, 24),       # bark texture light
    'l': (30, 80, 30),       # leaves darker green (dying)
    'L': (45, 110, 45),      # leaves mid green (dying)
    'g': (35, 90, 35),       # leaves dark green
    'G': (50, 120, 50),      # leaves yellow-green (dying)
    'j': (20, 60, 20),       # leaves forest dark (dying)
    'J': (30, 80, 30),       # leaves emerald (dying)
    'e': (255, 80, 40),      # eyes glowing red-orange (angry)
    'E': (200, 40, 20),      # eye edge (darker red)
    'i': (60, 20, 10),       # eye socket shadow (reddish)
    'm': (40, 20, 10),       # mouth interior
    'M': (180, 140, 100),    # mouth/teeth (darker wood)
    'n': (50, 25, 15),       # mouth crack dark
    'r': (90, 60, 35),       # roots dark
    'R': (110, 75, 40),      # roots light
    'k': (150, 100, 50),     # knot (wood knot)
    'K': (130, 85, 45),      # knot darker
    'f': (25, 70, 25),       # foliage shadow
    's': (40, 100, 40),      # moss bright (dying)
    'S': (25, 70, 25),       # moss dark (dying)
    'h': (160, 120, 60),     # beehive/honey (dried)
    'H': (140, 100, 50),     # beehive dark
    'v': (80, 50, 35),       # vine brown (thorny)
    'V': (60, 40, 25),       # vine dark (thorny)
    'p': (180, 100, 80),     # thorn light
    'P': (160, 80, 60),      # thorn dark
    'c': (140, 100, 70),     # dirt/mud light
    'C': (100, 70, 50),      # dirt/mud dark
    'd': (120, 85, 60),      # dirt mid
    'w': (80, 60, 40),       # twig
    'W': (60, 45, 28),       # twig dark
    'z': (180, 120, 60),     # glowing sap (dimmer)
    'Z': (200, 150, 80),     # glowing sap bright (dimmer)
    'y': (140, 60, 50),      # mushroom cap (rotten)
    'Y': (120, 50, 40),      # mushroom cap dark (rotten)
    'x': (200, 190, 180),    # mushroom stem (pale)
    '.': None,
}

# ── Down frames (24x24 grid, scale=2 → 48x48px) ──────────────────────
_DOWN_0 = [
    "...ooooooooooooooooo....",
    "..oGLLLGLGLGLGLGLLGGo...",
    ".oGLfLlLjJjJjJjLlLfLGo..",
    ".oLLjJjJjlllllljJjJjLLo.",
    "oGLjJjlljjjjjjjjlljJjGLo",
    "oLjJjlljioEeEeiojlljJjLo",
    "oLjJjljoiEeeeeeEiojljJLo",
    "oLjjljjioEeeeeeEiojjljLo",
    "oLjjljjioeeeeeeoijjljjLo",
    "oLjjjjjioommmmmoijjjjjLo",
    "oLjjjjjnomMMMMmonnnnjjLo",
    "oLLoggnnmmnnnnmmngggLLLo",
    ".oLLooggnnnnnnnggggLLo..",
    "..oTTTTuTTTTTTuTTTTo....",
    "..oTtAaTkKTTKktAaTtTo...",
    "..oTTahTTTTTTTahaTTTo...",
    "..oBbaTTsSsTTsSaTTBbo...",
    ".oBbBaTTSsSTTSsTaTBbBo..",
    "oBwbBBaTTTTTTTaTBBbwBo..",
    ".oBWbBBaTTTaTBBbWBo.....",
    "..oRrRCRRRRRRRCrRro.....",
    "...oRrRCdRRRCdrRro......",
    "...oRrCo.oRoCrRro.......",
    "...oRCo...oCRro.........",
]

_DOWN_1 = [
    "...ooooooooooooooooo....",
    "..oGLGLGLGLGLGLGLGLGo...",
    ".oGLfLlLjJjJjJjLlLfLGo..",
    ".oLLjJjJjlllllljJjJjLLo.",
    "oGLjJjlljjjjjjjjlljJjGLo",
    "oLjJjlljioEeEeiojlljJjLo",
    "oLjJjljoiEeeeeeEiojljJLo",
    "oLjjljjioEeeeeeEiojjljLo",
    "oLjjljjioeeeeeeoijjljjLo",
    "oLjjjjjioommmmmoijjjjjLo",
    "oLjjjjjnomMMMmmonnnnjjLo",
    "oLLoggnnmmnnnnmmngggLLLo",
    ".oLLooggnnnnnnnggggLLo..",
    "..oTTTTuTTTTTTuTTTTo....",
    "..oTtAaTkKTTKktAaTtTo...",
    "..oTTahTTTTTTTahaTTTo...",
    "..oBbaTTsSsTTsSaTTBbo...",
    ".oBbBaTTSsSTTSsaTTBbBo..",
    "oBwbBBaTTTTTTaTTBBbwBo..",
    ".oBWbBBaTTaTTaBBbWBo....",
    "..oRrRCRRRRRRCRrRro.....",
    "...oRrRCdRRCdrRro.......",
    "...oRrCo.oRoCrRro.......",
    "...oRCo...oCRro.........",
]

# ── Up frames ─────────────────────────────────────────────────────────
_UP_0 = [
    "...ooooooooooooooooo....",
    "..oGLLLGLGLGLGLGLLGGo...",
    ".oGLfLlLjJjJjJjLlLfLGo..",
    ".oLLjJjJjlllllljJjJjLLo.",
    "oGLjJjlljjjjjjjjlljJjGLo",
    "oLjJjlljjjjjjjjjjlljJjLo",
    "oLjJjljoggggggggojljJLo.",
    "oLjjljjoggggggggoojjljLo",
    "oLjjljjogggggggggjjljjLo",
    "oLjjjjjjgggggggggjjjjjLo",
    "oLjjjjjjgggggggggjjjjjLo",
    "oLLoggggggggggggggggLLLo",
    ".oLLooggggggggggggLLLo..",
    "..oTTTTuTTTTTTuTTTTo....",
    "..oTtAaTkKTTKktAaTtTo...",
    "..oTTahTTTTTTTahaTTTo...",
    "..oBbaTTsSsTTsSaTTBbo...",
    ".oBbBaTTSsSTTSsTaTBbBo..",
    "oBwbBBaTTTTTTTaTBBbwBo..",
    ".oBWbBBaTTTaTBBbWBo.....",
    "..oRrRCRRRRRRRCrRro.....",
    "...oRrRCdRRRCdrRro......",
    "...oRrCo.oRoCrRro.......",
    "...oRCo...oCRro.........",
]

_UP_1 = [
    "...ooooooooooooooooo....",
    "..oGLGLGLGLGLGLGLGLGo...",
    ".oGLfLlLjJjJjJjLlLfLGo..",
    ".oLLjJjJjlllllljJjJjLLo.",
    "oGLjJjlljjjjjjjjlljJjGLo",
    "oLjJjlljjjjjjjjjjlljJjLo",
    "oLjJjljoggggggggojljJLo.",
    "oLjjljjoggggggggoojjljLo",
    "oLjjljjogggggggggjjljjLo",
    "oLjjjjjjgggggggggjjjjjLo",
    "oLjjjjjjgggggggggjjjjjLo",
    "oLLoggggggggggggggggLLLo",
    ".oLLooggggggggggggLLLo..",
    "..oTTTTuTTTTTTuTTTTo....",
    "..oTtAaTkKTTKktAaTtTo...",
    "..oTTahTTTTTTTahaTTTo...",
    "..oBbaTTsSsTTsSaTTBbo...",
    ".oBbBaTTSsSTTSsaTTBbBo..",
    "oBwbBBaTTTTTTaTTBBbwBo..",
    ".oBWbBBaTTaTTaBBbWBo....",
    "..oRrRCRRRRRRCRrRro.....",
    "...oRrRCdRRCdrRro.......",
    "...oRrCo.oRoCrRro.......",
    "...oRCo...oCRro.........",
]

# ── Left frames ───────────────────────────────────────────────────────
_LEFT_0 = [
    ".....ooooooooooooooo....",
    "....oGLLGLGLGLGLGLGo....",
    "...oGLfLjJjJjJjLfLGo....",
    "...oLLjJjlllllljJjLLo...",
    "..oGLjJjjjjjjjjjjJjGLo..",
    "..oLjJjljioEeEiojjJjLo..",
    "..oLjJjljiEeeeEiojljJLo.",
    "..oLjjljjioEeEeoijjljLo.",
    ".oWboLjljjioeeoijjjjLo..",
    "oWwBoLjjjjiomoijjjjjLo..",
    "oBbBoLjjjnomMmnnjjjLLo..",
    "..obbBggnnmmnngggLLLo...",
    "...oTTTuTTTTTTTTTo......",
    "...oTtAaTkKTTKkaTto.....",
    "...oTTahTTTTTTahTTo.....",
    "...oBbaTTsSsTTsaBbo.....",
    "...oBbBaTTSsTTaBbBo.....",
    "...oBwbBaTTTTaBbwBo.....",
    "....oBWbBaTaBbWBo.......",
    "....oRrRCRRRCrRRo.......",
    "....oRRrRCdCrRRo........",
    "...oRrRCo.oCrRo.........",
    "...oRrCo...oCRo.........",
    "...oRCo.....oCo.........",
]

_LEFT_1 = [
    ".....ooooooooooooooo....",
    "....oGLGLGLGLGLGLGLo....",
    "...oGLfLjJjJjJjLfLGo....",
    "...oLLjJjlllllljJjLLo...",
    "..oGLjJjjjjjjjjjjJjGLo..",
    "..oLjJjljioEeEiojjJjLo..",
    "..oLjJjljiEeeeEiojljJLo.",
    "..oLjjljjioEeEeoijjljLo.",
    ".oWboLjljjioeeioijjjLo..",
    "oWwBoLjjjjiomoijjjjjLo..",
    "oBbBoLjjjnomMmnnjjjLLo..",
    "..obbBggnnmmnngggLLLo...",
    "...oTTTuTTTTTTTTTo......",
    "...oTtAaTkKTTKkaTto.....",
    "...oTTahTTTTTTahTTo.....",
    "...oBbaTTsSsTTsaBbo.....",
    "...oBbBaTTSsTaTBbBo.....",
    "...oBwbBaTTTaTBbwBo.....",
    "....oBWbBaTaTbWBo.......",
    "....oRrRCRRRCrRRo.......",
    "....oRRrRCdCrRRo........",
    "...oRrRCo.oCrRo.........",
    "...oRrCo...oCRo.........",
    "...oRCo.....oCo.........",
]

# ── Right frames ──────────────────────────────────────────────────────
_RIGHT_0 = [
    "....ooooooooooooooo.....",
    "....oGLGLGLGLGLGLLGo....",
    "....oGLfLjJjJjJjLfLGo...",
    "...oLLjJjlllllljJjLLo...",
    "..oLGjJjjjjjjjjjjjJjGLo.",
    "..oLjJjjoiEeEioijljJjLo.",
    ".oLjJjloiEeeeeiijljJjLo.",
    ".oLjljjioeeEeEioijjljLo.",
    "..oLjjjjioeeoijjljjLobWo",
    "..oLjjjjjiomoijjjjjLoBwWo",
    "..oLLjjjnnmMMmonnjjjLoBbBo",
    "...oLLLgggnnmmnnggBbbo..",
    "......oTTTTTTTTTuTTTo...",
    ".....ottaTkKTTkKtAaTTo..",
    ".....oTThaThTTTThaTTTo..",
    ".....obBasTTsSsTTaTbBo..",
    ".....oBbBaTTsSttaTBbBo..",
    ".....oBwbBaTTTTaBbwBo...",
    ".......oBWbBaTaBbWBo....",
    ".......oRRrCRRRCRrRo....",
    "........oRRrCdCrRRo.....",
    ".........oRrCo.oCrRRo...",
    ".........oRCo...oCrRo...",
    ".........oCo.....oCRo...",
]

_RIGHT_1 = [
    "....ooooooooooooooo.....",
    "....oLGLGLGLGLGLGLGo....",
    "....oGLfLjJjJjJjLfLGo...",
    "...oLLjJjlllllljJjLLo...",
    "..oLGjJjjjjjjjjjjjJjGLo.",
    "..oLjJjjoiEeEioijljJjLo.",
    ".oLjJjloiEeeeeiijljJjLo.",
    ".oLjljjioeeEeEioijjljLo.",
    "..oLjjjjioeeioijjljjLobWo",
    "..oLjjjjjiomoijjjjjLoBwWo",
    "..oLLjjjnnmMMmonnjjjLoBbBo",
    "...oLLLgggnnmmnnggBbbo..",
    "......oTTTTTTTTTuTTTo...",
    ".....ottaTkKTTkKtAaTTo..",
    ".....oTThaThTTTThaTTTo..",
    ".....obBasTTsSsTTaTbBo..",
    ".....oBbBaTaTsSttaTBbBo.",
    ".....oBwbBaTaTTTaBbwBo..",
    ".......oBWbaTaBbWBo.....",
    ".......oRRrCRRRCRrRo....",
    "........oRRrCdCrRRo.....",
    ".........oRrCo.oCrRRo...",
    ".........oRCo...oCrRo...",
    ".........oCo.....oCRo...",
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
