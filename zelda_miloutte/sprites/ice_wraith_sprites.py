"""Pixel art sprites for Ice Wraith (ghostly blue/white enemy)."""

from .pixel_art import surface_from_grid

# ── Palette ───────────────────────────────────────────────────────────
_PAL = {
    # Ice outline and structure
    'o': (15, 25, 45),         # deep frostbite outline
    'O': (25, 40, 60),         # lighter ice outline

    # Ice body gradients - crystalline blues
    'i': (100, 180, 230),      # ice body light
    'I': (70, 150, 210),       # ice body medium
    'c': (50, 120, 180),       # cold ice dark
    'C': (40, 90, 150),        # deep ice core

    # Brilliant white highlights - ice crystals
    'w': (240, 250, 255),      # brilliant white crystal
    'W': (200, 230, 250),      # white ice highlight
    'x': (220, 240, 255),      # crystal shimmer
    'X': (180, 220, 245),      # crystal medium

    # Pale cyan/frost tones
    'f': (150, 210, 240),      # frost light
    'F': (120, 190, 230),      # frost medium
    't': (90, 170, 220),       # frost trail
    'T': (60, 140, 200),       # frost trail dark

    # Pale violet - cold aura
    'v': (160, 170, 230),      # violet aura light
    'V': (130, 140, 210),      # violet aura medium
    'a': (100, 110, 190),      # cold aura dark

    # Icy blue eyes with white-hot centers
    'e': (200, 240, 255),      # eye glow white-blue
    'E': (150, 220, 255),      # eye bright cyan
    'y': (100, 200, 255),      # eye icy blue
    'Y': (60, 160, 230),       # eye deep ice

    # Ice crystal/snowflake details
    's': (230, 245, 255),      # sparkle crystal
    'S': (190, 220, 245),      # crystal edge

    # Icicle spikes - sharp and dangerous
    'k': (180, 210, 240),      # icicle light
    'K': (140, 180, 220),      # icicle medium
    'p': (100, 150, 200),      # icicle sharp point

    # Frost mist particles
    'm': (170, 200, 235),      # mist light
    'M': (140, 180, 220),      # mist medium
    'd': (110, 160, 210),      # dissolving frost
    'D': (80, 140, 190),       # deep mist

    '.': None,  # transparent
}

# ── Down frames ───────────────────────────────────────────────────────
_DOWN_0 = [
    "....oooooo....",
    "...owxwxwxo...",
    "..oWxIiiIxWo..",
    "..oXeyseysXo..",
    ".oIiYyCCYyiIo.",
    ".oIiCCwwCCiIo.",
    "kpoiCCssCCiopk",
    ".koIiCCCCiIok.",
    "..oXfiiiiifXo.",
    "...omfttfmo...",
    "....odtddo....",
    ".....mdtm.....",
    "......dd......",
    "..............",
]

_DOWN_1 = [
    "....oooooo....",
    "...osxwxwso...",
    "..oWxIiiIxWo..",
    "..oXeysyesXo..",
    ".oIiyYCCYyiIo.",
    ".oIiCCswCCiIo.",
    "pkoiCCssCCiokp",
    ".koIiCCCCiIok.",
    "...oXfiiiXo...",
    "....omfftmo...",
    "...odtddtdo...",
    "....mdtdm.....",
    ".....dd.dd....",
    "..............",
]

# ── Up frames ─────────────────────────────────────────────────────────
_UP_0 = [
    "......dd......",
    ".....mdtm.....",
    "....odtddo....",
    "...omfttfmo...",
    "..oXfiiiiifXo.",
    ".koIiCCCCiIok.",
    "kpoiCCssCCiopk",
    ".oIiCCwwCCiIo.",
    ".oIiyYCCYyiIo.",
    "..oXiCwwCiXo..",
    "..oWxIiiIxWo..",
    "...owxsxwxo...",
    "....oooooo....",
    "..............",
]

_UP_1 = [
    ".....dd.dd....",
    "....mdtdm.....",
    "...odtddtdo...",
    "....omfftmo...",
    "...oXfiiiXo...",
    ".koIiCCCCiIok.",
    "pkoiCCssCCiokp",
    ".oIiCCswCCiIo.",
    ".oIiyYCCYyiIo.",
    "..oXiCswCiXo..",
    "..oWxIiiIxWo..",
    "...oswxwxso...",
    "....oooooo....",
    "..............",
]

# ── Left frames ───────────────────────────────────────────────────────
_LEFT_0 = [
    "....oooo......",
    "...owxwxo.....",
    "..oWxIiixo....",
    "..oXeysIiWok..",
    ".oIiYyCCiiXop.",
    ".oIiCCwCCCfmo.",
    ".oIiCCssCCfmo.",
    "koIiCCCCiiXok.",
    "..oXfiiiiifXo.",
    "...omfttfmo...",
    "....odttdo....",
    ".....mdtm.....",
    "......dd......",
    "..............",
]

_LEFT_1 = [
    "....oooo......",
    "...oswxwo.....",
    "..oWxIiixo....",
    "..oXeysIiWokp.",
    ".oIiyYCCiiXok.",
    ".oIiCCsCCCfmo.",
    ".oIiCCswCCfmo.",
    "koIiCCCCiiXo..",
    "...oXfiiiXo...",
    "....omfftmo...",
    "...odttddo....",
    "....mddtm.....",
    ".....dd.......",
    "..............",
]

# ── Right frames ──────────────────────────────────────────────────────
_RIGHT_0 = [
    "......oooo....",
    ".....oxwxwo...",
    "....oxxiIxWo..",
    "..koWiIsyeXo..",
    ".poXiiCCyYiIo.",
    ".omfCCCwCCiIo.",
    ".omfCCssCCiIo.",
    ".koXiiCCCCiIok",
    "..oXfiiiiifXo.",
    "...omfttfmo...",
    "....odttdo....",
    ".....mdtm.....",
    "......dd......",
    "..............",
]

_RIGHT_1 = [
    "......oooo....",
    ".....owxwso...",
    "....oxxiIxWo..",
    ".pkoWiIsyeXo..",
    ".koXiiCCYyiIo.",
    ".omfCCCsCCiIo.",
    ".omfCCwsCCiIo.",
    "..oXiiCCCCiIok",
    "...oXiiiXo....",
    "...omtffmo....",
    "....oddttdo...",
    ".....mdtddm...",
    ".......dd.....",
    "..............",
]

# ── Build surfaces ────────────────────────────────────────────────────
_frames_cache = None


def get_ice_wraith_frames():
    """Return dict of {direction: [frame0, frame1]} for the ice wraith."""
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
