"""Pixel art sprites for Scorpion (fast poison enemy)."""

from .pixel_art import surface_from_grid

# ── Palette ───────────────────────────────────────────────────────
_PAL = {
    'o': (20, 20, 20),        # dark outline
    'b': (160, 120, 40),      # tan body
    'B': (140, 100, 30),      # medium brown body
    'D': (100, 70, 20),       # dark brown segments
    'y': (200, 180, 60),      # yellow/gold highlights
    'p': (120, 80, 30),       # pincers base
    'P': (160, 110, 40),      # pincers tips
    't': (110, 80, 35),       # tail segments
    'T': (90, 60, 25),        # dark tail
    'v': (180, 60, 30),       # red-orange venom
    'V': (220, 80, 40),       # bright venom tip
    'g': (100, 180, 70),      # poison green glow
    'G': (80, 140, 50),       # darker poison
    'e': (255, 0, 0),         # red eyes
    'l': (80, 60, 20),        # legs
    '.': None,
}

# ── Down frames ───────────────────────────────────────────────────
_DOWN_0 = [
    "...oo....oo...",
    "..oPoooooPos..",
    "..oPooooooP...",
    ".obbyBBBByo...",
    ".obBeeBByo....",
    "lobBBDBBbol...",
    "lobBBDBBbol...",
    ".obBBDBBbo....",
    "..obBDBbo.....",
    "...obTbo......",
    "....oTo.......",
    "...ooToo......",
    "...ovVgo......",
    "....oGo.......",
]

_DOWN_1 = [
    "...oo....oo...",
    "..oPoooooPo...",
    "..oPoooooPos..",
    "..obbyBBByos..",
    "...obBeeBBo...",
    ".lobBBDBBbol..",
    ".lobBBDBBbol..",
    "..obBBDBBbo...",
    "...obBDBbo....",
    "....obTbo.....",
    ".....oTo......",
    "....ooToo.....",
    "....ovVgo.....",
    ".....oGo......",
]

# ── Up frames ─────────────────────────────────────────────────────
_UP_0 = [
    ".....oGo......",
    "....ovVgo.....",
    "....ooToo.....",
    ".....oTo......",
    "....obTbo.....",
    "...obBDBbo....",
    "..obBBDBBbo...",
    ".lobBBDBBbol..",
    ".lobBBDBBbol..",
    "...obBeeBBo...",
    "..obbyBBByos..",
    "..oPoooooPos..",
    "..oPoooooPo...",
    "...oo....oo...",
]

_UP_1 = [
    "....oGo.......",
    "...ovVgo......",
    "...ooToo......",
    "....oTo.......",
    "...obTbo......",
    "..obBDBbo.....",
    ".obBBDBBbo....",
    "lobBBDBBbol...",
    "lobBBDBBbol...",
    ".obBeeBByo....",
    ".obbyBBBByo...",
    "..oPooooooP...",
    "..oPoooooPos..",
    "...oo....oo...",
]

# ── Left frames ───────────────────────────────────────────────────
_LEFT_0 = [
    "..............",
    "...oooooo.....",
    "..oPooobyo....",
    "..oPobBeBo....",
    ".obBBBBDBol...",
    ".obBBBBDBoloo.",
    "obBBBBDBol.oo.",
    "obBBBBBol..ovV",
    ".obBBBol..ooTG",
    "..obBol...oTo.",
    "...obo....oo..",
    "....o.........",
    "..............",
    "..............",
]

_LEFT_1 = [
    "..............",
    "...oooooo.....",
    "..oPoobyo.....",
    "..oPooBeBo....",
    ".obBBBBDBol...",
    ".obBBBBDBoloo.",
    "obBBBBDBool.oo",
    "obBBBBBol..ovV",
    ".obBBBol...oTG",
    "..obBol....oo.",
    "...obol.......",
    "....o.........",
    "..............",
    "..............",
]

# ── Right frames ──────────────────────────────────────────────────
_RIGHT_0 = [
    "..............",
    ".....oooooo...",
    "....oyboooPo..",
    "....oBeBboPo..",
    "...loBDBBBBbo.",
    ".oolobDBBBBbo.",
    ".oo.loBDBBBBbo",
    "Vvo..loBBBBBbo",
    "GToo..loBBBbo.",
    ".oTo...loBbo..",
    "..oo....obo...",
    ".........o....",
    "..............",
    "..............",
]

_RIGHT_1 = [
    "..............",
    ".....oooooo...",
    ".....oyboooPo.",
    "....oBeBooP...",
    "...loBDBBBBbo.",
    ".oolobDBBBBbo.",
    "oo.looBDBBBBbo",
    "Vvo..loBBBBBbo",
    "GTo...loBBBbo.",
    ".oo....loBbo..",
    ".......lobo...",
    ".........o....",
    "..............",
    "..............",
]

# ── Build surfaces ────────────────────────────────────────────────
_frames_cache = None


def get_scorpion_frames():
    """Return dict of {direction: [frame0, frame1]} for the scorpion."""
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
