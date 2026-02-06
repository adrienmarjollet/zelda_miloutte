"""Pixel art sprites for enemies (goblin creatures)."""

from zelda_miloutte.sprites.pixel_art import surface_from_grid

# ── Palette ───────────────────────────────────────────────────────
_PAL = {
    'o': (20, 20, 20),      # dark outline
    'g': (85, 145, 70),     # goblin skin green
    'G': (60, 105, 50),     # darker skin shadow
    'l': (110, 175, 90),    # skin highlight (lighter green)
    'e': (255, 220, 60),    # eye color (bright yellow-red)
    'E': (40, 10, 10),      # eye pupil (very dark)
    't': (240, 235, 215),   # teeth/fangs (off-white)
    'h': (65, 55, 45),      # horns (dark brown/gray)
    'H': (95, 80, 65),      # horn highlight
    'a': (75, 80, 90),      # armor (dark metal gray-blue)
    'A': (105, 115, 125),   # armor highlight/rivet
    'b': (90, 65, 40),      # belt (brown)
    'p': (55, 45, 60),      # pants (dark cloth)
    'f': (70, 50, 35),      # feet/boots (dark brown)
    'c': (95, 155, 80),     # claw/hand color (slightly different from body)
    '.': None,
}

# ── Down frames ───────────────────────────────────────────────────
_DOWN_0 = [
    "...ohHHho.....",
    "..ohHHHHho....",
    "..olllllgo....",
    ".ogllgllggo...",
    ".ogeeGoeegg...",
    ".ogEeGGEeGo...",
    ".ogGttGttGo...",
    ".oGGGttGGGo...",
    ".ocaAaaAaco...",
    "ocaAaAaAaaco..",
    ".oaabbbbaaoo..",
    ".oopppppppo...",
    ".opp.oo.ppo...",
    ".off.oo.ffo...",
]

_DOWN_1 = [
    "...ohHHho.....",
    "..ohHHHHho....",
    "..olllllgo....",
    ".ogllgllggo...",
    ".ogeeGoeegg...",
    ".ogEeGGEeGo...",
    ".ogGttGttGo...",
    ".oGGGttGGGo...",
    "..caAaaAaco...",
    ".caAaAaAaacoo.",
    "..oaabbbbaaoo.",
    "..oopppppppo..",
    "..opp..ppoo...",
    "..off..ffo....",
]

# ── Up frames ─────────────────────────────────────────────────────
_UP_0 = [
    "...ohHHho.....",
    "..ohHHHHho....",
    "..olllllgo....",
    ".ogllgllggo...",
    ".ogGGGGGGgo...",
    ".oGGGGGGGGo...",
    ".oGGGGGGGGo...",
    ".oGGGGGGGGo...",
    ".ocaAaaAaco...",
    "ocaAaAaAaaco..",
    ".oaabbbbaaoo..",
    ".oopppppppo...",
    ".opp.oo.ppo...",
    ".off.oo.ffo...",
]

_UP_1 = [
    "...ohHHho.....",
    "..ohHHHHho....",
    "..olllllgo....",
    ".ogllgllggo...",
    ".ogGGGGGGgo...",
    ".oGGGGGGGGo...",
    ".oGGGGGGGGo...",
    ".oGGGGGGGGo...",
    "..caAaaAaco...",
    ".caAaAaAaacoo.",
    "..oaabbbbaaoo.",
    "..oopppppppo..",
    "..opp..ppoo...",
    "..off..ffo....",
]

# ── Left frames ───────────────────────────────────────────────────
_LEFT_0 = [
    "..ohhHo.......",
    ".ohHHHho......",
    ".ollllgo......",
    "ogllgllgo.....",
    "oeeGggggo.....",
    "oEeGGGGgo.....",
    "ogGttGGgo.....",
    "oGGGGGGGooo...",
    "oaAaaAacoocc..",
    "oaAaAaAacooc..",
    "ooaabbbaaooc..",
    ".oopppppppoo..",
    ".opp...oppoo..",
    ".off...offo...",
]

_LEFT_1 = [
    "..ohhHo.......",
    ".ohHHHho......",
    ".ollllgo......",
    "ogllgllgo.....",
    "oeeGggggo.....",
    "oEeGGGGgo.....",
    "ogGttGGgo.....",
    "..oGGGGGooocc.",
    ".oaAaaAacooc..",
    ".oaAaAaAacooc.",
    ".ooaabbbaaooc.",
    "..oopppppppoo.",
    "..opp..ppoo...",
    "..off..ffo....",
]

# ── Right frames ──────────────────────────────────────────────────
_RIGHT_0 = [
    ".......oHhho..",
    "......ohHHHho.",
    "......ogllllo.",
    ".....ogllgllo.",
    ".....oggggGee.",
    ".....ogGGGGEe.",
    ".....oggGGttg.",
    "...oooGGGGGGG.",
    "..ccoocaAaaAa.",
    "..cooaAaAaAaa.",
    "..cooaabbbaao.",
    "..oopppppppo..",
    "..ooppo...ppo.",
    "...offo...ffo.",
]

_RIGHT_1 = [
    ".......oHhho..",
    "......ohHHHho.",
    "......ogllllo.",
    ".....ogllgllo.",
    ".....oggggGee.",
    ".....ogGGGGEe.",
    ".....oggGGttg.",
    ".ccooGGGGGo...",
    "..coocaAaaAao.",
    ".coocaAaAaAao.",
    ".coooaabbbaao.",
    ".ooppppppppoo.",
    "...ooppo.ppo..",
    "....off.offo..",
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
