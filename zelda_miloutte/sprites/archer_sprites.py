"""Pixel art sprites for archer enemies (hooded ranged attackers)."""

from .pixel_art import surface_from_grid

# ── Archer Palette ────────────────────────────────────────────────
_ARCHER_PAL = {
    'o': (15, 10, 20),      # dark outline
    # Hood/Robe - richer purple tones
    'h': (20, 12, 35),      # hood deepest shadow
    'H': (35, 22, 60),      # hood dark
    'i': (50, 35, 85),      # hood mid-dark
    'I': (65, 45, 105),     # hood mid
    'P': (80, 55, 125),     # hood/robe lighter
    'r': (55, 40, 95),      # robe purple
    'R': (70, 50, 115),     # robe mid
    'T': (90, 65, 140),     # robe trim/highlight
    # Face/Skin
    'd': (40, 30, 50),      # dark shadowy face
    'f': (85, 70, 75),      # shadowy skin under hood
    'F': (120, 100, 105),   # lighter skin (hands)
    # Eyes - glowing with aura
    'e': (160, 50, 50),     # eye base red
    'E': (220, 70, 60),     # eye glow medium
    'G': (255, 120, 90),    # eye glow bright center
    'g': (120, 35, 50),     # eye glow outer aura
    # Bow - more detailed wood
    'b': (75, 55, 25),      # bow wood dark
    'B': (100, 75, 35),     # bow wood mid
    'W': (125, 95, 45),     # bow wood light/grain
    'S': (190, 180, 160),   # bowstring
    's': (150, 140, 120),   # bowstring shadow
    # Quiver & Arrows
    'q': (80, 60, 28),      # quiver brown dark
    'Q': (105, 80, 38),     # quiver brown mid
    'a': (150, 120, 55),    # arrow shaft
    'A': (180, 150, 70),    # arrow fletching
    't': (140, 140, 150),   # arrow tip metal
    # Cloak/Cape
    'c': (45, 32, 75),      # cloak dark purple
    'C': (60, 45, 95),      # cloak mid
    'L': (75, 55, 115),     # cloak flow highlight
    # Magical aura
    'm': (90, 50, 110),     # magic aura subtle
    'M': (120, 70, 140),    # magic aura glow
    '.': None,
}

# ── Down frames ───────────────────────────────────────────────────
_DOWN_0 = [
    ".....ooo......",
    "....ohHho.....",
    "...ohiIiho....",
    "..ohIIPPIho...",
    "..oIPgGgPIo...",
    ".oIIdEeEdIIo..",
    ".oIidffdiiPo..",
    ".oBWoRRroQqo..",
    "..BSoRRRrQao..",
    "..oSrRRRRtao..",
    "..oorRTRrao...",
    "..ocrRRRrcLo..",
    ".ocCrRRTrCLo..",
    ".oCCccccCCLo..",
]

_DOWN_1 = [
    ".....ooo......",
    "....ohHho.....",
    "...ohiIiho....",
    "..ohIIPPIho...",
    "..oIPgGgPIo...",
    ".oIIdEeEdIIo..",
    ".oIidffdiiPo..",
    ".oBWoRRroQqo..",
    "..BSoRRRrQao..",
    "..oSrRRRRtao..",
    "..oorRTRrao...",
    ".occrRRRrcLo..",
    "...oCRRTCLo...",
    "...oCCcoCLo...",
]

# ── Up frames ─────────────────────────────────────────────────────
_UP_0 = [
    ".....ooo......",
    "....ohHho.....",
    "...ohiIiho....",
    "..ohIIPPIho...",
    ".ohIPPPPPIo...",
    ".oQAatIIPIo...",
    ".oQqaoIPPIo...",
    ".oqoooRRrWBo..",
    "..ooorRRrWSo..",
    "..oorRRRrsSo..",
    "..oorRTRrWBo..",
    "..ocrRRRrcLo..",
    ".ocCrRRTrCLo..",
    ".oCCccccCCLo..",
]

_UP_1 = [
    ".....ooo......",
    "....ohHho.....",
    "...ohiIiho....",
    "..ohIIPPIho...",
    ".ohIPPPPPIo...",
    ".oQAatIIPIo...",
    ".oQqaoIPPIo...",
    ".oqoooRRrWBo..",
    "..oorRRRrWSo..",
    "..ooorRRrsSo..",
    "..oorRTRrWBo..",
    ".occrRRRrcLo..",
    "...oCRRTCLo...",
    "...oCCcoCLo...",
]

# ── Left frames ───────────────────────────────────────────────────
_LEFT_0 = [
    "..mooo........",
    ".mohHho.......",
    "mohiIihom.....",
    "oIPgGeQAao....",
    "oIPEeQqato....",
    "oIidfQqqoo....",
    "oPiFooooo.....",
    "oorRRTFoo.....",
    "morRRRRoo.....",
    ".orRRRRbWSo...",
    ".orRTRrbWSo...",
    ".oCRRRrobBo...",
    "oCCrRRTcCLoo..",
    "ooCccccCLLo...",
]

_LEFT_1 = [
    "..mooo........",
    ".mohHho.......",
    "mohiIihom.....",
    "oIPgGeQAao....",
    "oIPEeQqato....",
    "oIidfQqqoo....",
    "oPiFooooo.....",
    "oorRRTFoo.....",
    "morRRRRoo.....",
    ".orRRRRbWSo...",
    ".oCrRTrbWSo...",
    "..oCRRrobBo...",
    "..oCcRTcCLo...",
    "...oCcoCLo....",
]

# ── Right frames ──────────────────────────────────────────────────
_RIGHT_0 = [
    "........ooom..",
    ".......ohHhom.",
    ".....moiIihom.",
    "....oAaQegPIo.",
    "...otaqQeEPIo.",
    "....ooqqqfdIo.",
    ".....oooooFiPo",
    ".....ooFTRRoo.",
    ".....ooRRRRrom",
    "...oSWbRRRRro.",
    "...oSWbrRTRro.",
    "...oBborRRRCo.",
    "..ooCLcTRRrCCo",
    "...oLLCccccooo",
]

_RIGHT_1 = [
    "........ooom..",
    ".......ohHhom.",
    ".....moiIihom.",
    "....oAaQegPIo.",
    "...otaqQeEPIo.",
    "....ooqqqfdIo.",
    ".....oooooFiPo",
    ".....ooFTRRoo.",
    ".....ooRRRRrom",
    "...oSWbRRRRro.",
    "...oSWbrTrCo..",
    "...oBborRRCo..",
    "...oLCcTRcCo..",
    "....oLCoCo....",
]

# ── Build surfaces ────────────────────────────────────────────────
_archer_frames_cache = None


def get_archer_frames():
    """Return dict of {direction: [frame0, frame1]} for the archer."""
    global _archer_frames_cache
    if _archer_frames_cache is not None:
        return _archer_frames_cache

    _archer_frames_cache = {
        "down":  [surface_from_grid(g, _ARCHER_PAL, 2) for g in (_DOWN_0, _DOWN_1)],
        "up":    [surface_from_grid(g, _ARCHER_PAL, 2) for g in (_UP_0, _UP_1)],
        "left":  [surface_from_grid(g, _ARCHER_PAL, 2) for g in (_LEFT_0, _LEFT_1)],
        "right": [surface_from_grid(g, _ARCHER_PAL, 2) for g in (_RIGHT_0, _RIGHT_1)],
    }
    return _archer_frames_cache


# ── Projectile sprite ─────────────────────────────────────────────
_PROJECTILE_PAL = {
    'c': (200, 80, 200),    # core bright magenta
    'C': (255, 130, 255),   # core highlight
    'g': (140, 50, 160),    # glow edge
    'G': (100, 30, 120),    # outer glow
    't': (255, 200, 255),   # bright tip/center
    '.': None,
}

# 8x8 magical energy bolt sprite (pointing right by default, will be rotated)
_ARROW = [
    "........",
    "..ggtCc.",
    ".gctCCcg",
    "GgcCCcgg",
    "GgcCCcgg",
    ".gctCCcg",
    "..ggtCc.",
    "........",
]

_projectile_sprite_cache = None


def get_projectile_sprite():
    """Return the projectile (arrow) sprite surface."""
    global _projectile_sprite_cache
    if _projectile_sprite_cache is not None:
        return _projectile_sprite_cache

    _projectile_sprite_cache = surface_from_grid(_ARROW, _PROJECTILE_PAL, 1)
    return _projectile_sprite_cache
