"""Pixel art sprites for enemies (goblin creatures)."""

from .pixel_art import surface_from_grid

# ── Palette ───────────────────────────────────────────────────────
_PAL = {
    'o': (20, 20, 20),      # dark outline
    'g': (85, 145, 70),     # goblin skin green (base)
    'G': (60, 105, 50),     # darker skin shadow
    'm': (75, 125, 60),     # mid-tone green (new - for shading)
    'l': (110, 175, 90),    # skin highlight (lighter green)
    'L': (130, 195, 110),   # bright highlight (new - for volume)
    'e': (255, 90, 50),     # eye glow (fierce red-orange)
    'E': (180, 40, 20),     # eye inner glow (darker red)
    'y': (255, 220, 60),    # eye reflection (yellow)
    't': (240, 235, 215),   # teeth/fangs (off-white)
    'T': (200, 195, 185),   # fang shadow (new)
    'h': (65, 55, 45),      # horns (dark brown/gray)
    'H': (95, 80, 65),      # horn highlight
    'R': (115, 100, 80),    # horn ridges (new - brighter)
    'a': (75, 80, 90),      # armor (dark metal gray-blue)
    'A': (105, 115, 125),   # armor highlight
    'S': (125, 135, 145),   # armor shine (new - brightest metal)
    'V': (55, 60, 70),      # armor rivet/detail (new - darker metal)
    'b': (90, 65, 40),      # belt (brown)
    'B': (110, 85, 55),     # belt buckle/highlight (new)
    'p': (55, 45, 60),      # pants (dark cloth)
    'f': (70, 50, 35),      # feet/boots (dark brown)
    'F': (90, 70, 50),      # boot highlight (new)
    'c': (95, 155, 80),     # claw/hand color (slightly different from body)
    'C': (75, 125, 65),     # claw shadow (new)
    'w': (140, 120, 90),    # weapon handle (wood)
    'W': (160, 140, 110),   # weapon handle highlight (new)
    'd': (90, 90, 85),      # weapon blade/club (dark iron)
    'D': (120, 120, 115),   # weapon metal highlight (new)
    'x': (70, 70, 65),      # weapon shadow (new)
    '.': None,
}

# ── Down frames ───────────────────────────────────────────────────
_DOWN_0 = [
    "...ohRHRho.....",
    "..ohRHHHRho...",
    "..oLlllllmo...",
    ".omllmllmgo...",
    ".omeyEeeyEm...",
    ".ogEeGGEeGo...",
    ".ogGtTGTtGo...",
    ".oGGtTTTtGo...",
    ".ocVASSAVco...",
    "ocaVASASAaco..",
    ".oaaBbBbaaoo..",
    ".oopppppppo...",
    ".opf.oo.pfo...",
    ".off.oo.Ffo...",
]

_DOWN_1 = [
    "...ohRHRho.....",
    "..ohRHHHRho...",
    "..oLlllllmo...",
    ".omllmllmgo...",
    ".omeyEeeyEm...",
    ".ogEeGGEeGo...",
    ".ogGtTGTtGo...",
    ".oGGtTTTtGo...",
    "..cVASSAVco...",
    ".caVASASAacoo.",
    "..oaaBbBbaaoo.",
    "..oopppppppo..",
    "..opf..pFo....",
    "..off..ffo....",
]

# ── Up frames ─────────────────────────────────────────────────────
_UP_0 = [
    "...ohRHRho.....",
    "..ohRHHHRho...",
    "..oLlllllmo...",
    ".omllmllmgo...",
    ".omGGGGGGGo...",
    ".oGGGmGmGGo...",
    ".oGGGGGGGGo...",
    ".oGGmGGmGGo...",
    ".ocVASSAVco...",
    "ocaVASASAaco..",
    ".oaaBbBbaaoo..",
    ".oopppppppo...",
    ".opf.oo.pfo...",
    ".off.oo.Ffo...",
]

_UP_1 = [
    "...ohRHRho.....",
    "..ohRHHHRho...",
    "..oLlllllmo...",
    ".omllmllmgo...",
    ".omGGGGGGGo...",
    ".oGGGmGmGGo...",
    ".oGGGGGGGGo...",
    ".oGGmGGmGGo...",
    "..cVASSAVco...",
    ".caVASASAacoo.",
    "..oaaBbBbaaoo.",
    "..oopppppppo..",
    "..opf..pFo....",
    "..off..ffo....",
]

# ── Left frames ───────────────────────────────────────────────────
_LEFT_0 = [
    "..ohhRo.......",
    ".ohRHHRho.....",
    ".oLllllmo.....",
    "omllmllgo.....",
    "oyeEmmmmo.....",
    "oEeGGGGmo.....",
    "omGtTGGgo.....",
    "oGGtTGGGooooxd",
    "oVASSAVcooCxdd",
    "oaVASASacooCdd",
    "ooaaBbBaaoocWw",
    ".oopppppppooWw",
    ".opf...opfoo..",
    ".off...oFfo...",
]

_LEFT_1 = [
    "..ohhRo.......",
    ".ohRHHRho.....",
    ".oLllllmo.....",
    "omllmllgo.....",
    "oyeEmmmmo.....",
    "oEeGGGGmo.....",
    "omGtTGGgo.....",
    "..oGGtTGooodxd",
    ".oVASSAacooxDd",
    ".oaVASASacoocd",
    ".ooaaBbBaaooWw",
    "..oopppppppoWw",
    "..opf..pfo....",
    "..off..Ffo....",
]

# ── Right frames ──────────────────────────────────────────────────
_RIGHT_0 = [
    ".......oRhho..",
    ".....ohRHHRho.",
    ".....omlllllo.",
    ".....ogllmllo.",
    ".....ommmmEey.",
    ".....omGGGGEe.",
    ".....oggGGtTm.",
    "dxoooGGGtTGGG.",
    "ddxCoocVASSAV.",
    "ddCooocaSASAa.",
    "wWcoooaaBbBao.",
    "wWoopppppppo..",
    "..oopfpo...pf.",
    "...oFfo...off.",
]

_RIGHT_1 = [
    ".......oRhho..",
    ".....ohRHHRho.",
    ".....omlllllo.",
    ".....ogllmllo.",
    ".....ommmmEey.",
    ".....omGGGGEe.",
    ".....oggGGtTm.",
    "dxdoooGtTGGo..",
    "dDxoocaASSAVo.",
    "dcooocaSASAao.",
    "wWooooaaBbBao.",
    "wWopppppppoo..",
    "....ofp.ofpo..",
    "....oFf.offo..",
]

# ── Build surfaces ────────────────────────────────────────────────
_frames_cache = None


def get_enemy_frames():
    """Return dict of {direction: [frame0, frame1]} for the enemy."""
    global _frames_cache
    if _frames_cache is not None:
        return _frames_cache

    _frames_cache = {
        "down":  [surface_from_grid(g, _PAL, 2) for g in (_DOWN_0, _DOWN_1)],
        "up":    [surface_from_grid(g, _PAL, 2) for g in (_UP_0, _UP_1)],
        "left":  [surface_from_grid(g, _PAL, 2) for g in (_LEFT_0, _LEFT_1)],
        "right": [surface_from_grid(g, _PAL, 2) for g in (_RIGHT_0, _RIGHT_1)],
    }
    return _frames_cache
