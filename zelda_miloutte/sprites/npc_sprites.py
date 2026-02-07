"""Pixel art sprites for NPCs (Elder, Villager, Merchant, Guard)."""

from .pixel_art import surface_from_grid

# ══════════════════════════════════════════════════════════════════════
# ELDER - wise old figure, white hair/beard, blue robes
# ══════════════════════════════════════════════════════════════════════

_ELDER_PAL = {
    'o': (20, 20, 20),       # dark outline
    's': (240, 220, 195),    # skin (pale)
    'S': (210, 190, 165),    # skin shadow
    'w': (245, 245, 245),    # white hair/beard
    'W': (220, 220, 220),    # hair shadow
    'e': (80, 120, 160),     # eye color (wise blue)
    'E': (40, 40, 40),       # eye pupil
    'b': (60, 90, 150),      # blue robe
    'B': (80, 110, 170),     # robe highlight
    'd': (40, 60, 100),      # robe shadow
    'g': (180, 160, 80),     # gold trim
    'h': (220, 190, 140),    # hand
    '.': None,
}

# ── Elder Down frames ─────────────────────────────────────────────────
_ELDER_DOWN_0 = [
    "....owwwo.....",
    "...owWWWwo....",
    "..owWWWWWo....",
    "..osssssso....",
    ".osSeeSeSso...",
    ".osEeSSEeso...",
    ".osSSSSSSo....",
    ".owWWWWWWo....",
    "..oBBBBBo.....",
    ".oBgBBBgBo....",
    ".oBBdddBBo....",
    ".odBBBBBdo....",
    ".oddo.oddo....",
    "..oo...oo.....",
]

_ELDER_DOWN_1 = [
    "....owwwo.....",
    "...owWWWwo....",
    "..owWWWWWo....",
    "..osssssso....",
    ".osSeeSeSso...",
    ".osEeSSEeso...",
    ".osSSSSSSo....",
    ".owWWWWWWo....",
    "..oBBBBBo.....",
    ".oBgBBBgBo....",
    ".oBBdddBBo....",
    ".odBBBBBdo....",
    "..oddo.oo.....",
    "...oo...oo....",
]

# ── Elder Up frames ───────────────────────────────────────────────────
_ELDER_UP_0 = [
    "....owwwo.....",
    "...owWWWwo....",
    "..owWWWWWo....",
    "..osssssso....",
    ".osssssssso...",
    ".ossSSSSSso...",
    ".osSSSSSSo....",
    ".owWWWWWWo....",
    "..oBBBBBo.....",
    ".oBgBBBgBo....",
    ".oBBdddBBo....",
    ".odBBBBBdo....",
    ".oddo.oddo....",
    "..oo...oo.....",
]

_ELDER_UP_1 = [
    "....owwwo.....",
    "...owWWWwo....",
    "..owWWWWWo....",
    "..osssssso....",
    ".osssssssso...",
    ".ossSSSSSso...",
    ".osSSSSSSo....",
    ".owWWWWWWo....",
    "..oBBBBBo.....",
    ".oBgBBBgBo....",
    ".oBBdddBBo....",
    ".odBBBBBdo....",
    "..oddo.oo.....",
    "...oo...oo....",
]

# ── Elder Left frames ─────────────────────────────────────────────────
_ELDER_LEFT_0 = [
    "...owwwo......",
    "..owWWWwo.....",
    ".owWWWWWo.....",
    ".osssssso.....",
    "oseeSSsso.....",
    "osEeSSSSo.....",
    "osSSSSSSo.....",
    "owWWWWWWo.....",
    ".oBBBBBooooh..",
    "oBgBBBBBooh...",
    "oBBdddBBBoh...",
    "odBBBBBBdoh...",
    "oddo..oooo....",
    ".oo...........",
]

_ELDER_LEFT_1 = [
    "...owwwo......",
    "..owWWWwo.....",
    ".owWWWWWo.....",
    ".osssssso.....",
    "oseeSSsso.....",
    "osEeSSSSo.....",
    "osSSSSSSo.....",
    "owWWWWWWo.....",
    ".oBBBBBoh.....",
    "oBgBBBBoooh...",
    "oBBdddBBooh...",
    "odBBBBBdooh...",
    ".oddo.oooo....",
    "..oo..........",
]

# ── Elder Right frames ────────────────────────────────────────────────
_ELDER_RIGHT_0 = [
    "......owwwo...",
    ".....owWWWwo..",
    ".....owWWWWWo.",
    ".....osssssso.",
    ".....ossSeeso.",
    ".....oSSSSEeo.",
    ".....oSSSSSSo.",
    ".....owWWWWWo.",
    "..hooooBBBBBo.",
    "...hooBBBBBgo.",
    "...hoBBBdddBo.",
    "...hododddddo.",
    "....ooooo.odo.",
    "...........oo.",
]

_ELDER_RIGHT_1 = [
    "......owwwo...",
    ".....owWWWwo..",
    ".....owWWWWWo.",
    ".....osssssso.",
    ".....ossSeeso.",
    ".....oSSSSEeo.",
    ".....oSSSSSSo.",
    ".....owWWWWWo.",
    ".....hoBBBBBo.",
    "...hoooBBBBgo.",
    "...hooBBdddBo.",
    "...hooBdBBBdo.",
    "....oooo.oddo.",
    "..........oo..",
]

# ══════════════════════════════════════════════════════════════════════
# VILLAGER - simple peasant, brown hair, tan clothes
# ══════════════════════════════════════════════════════════════════════

_VILLAGER_PAL = {
    'o': (20, 20, 20),       # dark outline
    's': (240, 210, 180),    # skin
    'S': (210, 180, 150),    # skin shadow
    'h': (90, 60, 40),       # brown hair
    'H': (110, 80, 55),      # hair highlight
    'e': (100, 140, 180),    # eye color
    'E': (40, 40, 40),       # eye pupil
    't': (200, 170, 120),    # tan tunic
    'T': (220, 190, 140),    # tunic highlight
    'd': (140, 110, 75),     # tunic shadow
    'b': (100, 80, 60),      # brown belt/pants
    'f': (80, 60, 45),       # feet
    'a': (210, 180, 140),    # arms
    '.': None,
}

# ── Villager Down frames ──────────────────────────────────────────────
_VILLAGER_DOWN_0 = [
    "....ohhho.....",
    "...ohHHHho....",
    "..ohHHHHHo....",
    "..osssssso....",
    ".osSeeSeSso...",
    ".osEeSSEeso...",
    ".osSSSSSSo....",
    "..oTTTTTo.....",
    "..oTtttTo.....",
    ".oaTTTTTao....",
    ".oaTdddTao....",
    ".obttttbbo....",
    ".obbo.obbo....",
    "..ffo.offo....",
]

_VILLAGER_DOWN_1 = [
    "....ohhho.....",
    "...ohHHHho....",
    "..ohHHHHHo....",
    "..osssssso....",
    ".osSeeSeSso...",
    ".osEeSSEeso...",
    ".osSSSSSSo....",
    "..oTTTTTo.....",
    "..oTtttTo.....",
    ".oaTTTTTao....",
    ".oaTdddTao....",
    ".obttttbbo....",
    "..obbo.bbo....",
    "...ffo.ffo....",
]

# ── Villager Up frames ────────────────────────────────────────────────
_VILLAGER_UP_0 = [
    "....ohhho.....",
    "...ohHHHho....",
    "..ohHHHHHo....",
    "..osssssso....",
    ".osssssssso...",
    ".ossSSSSSso...",
    ".osSSSSSSo....",
    "..oTTTTTo.....",
    "..oTtttTo.....",
    ".oaTTTTTao....",
    ".oaTdddTao....",
    ".obttttbbo....",
    ".obbo.obbo....",
    "..ffo.offo....",
]

_VILLAGER_UP_1 = [
    "....ohhho.....",
    "...ohHHHho....",
    "..ohHHHHHo....",
    "..osssssso....",
    ".osssssssso...",
    ".ossSSSSSso...",
    ".osSSSSSSo....",
    "..oTTTTTo.....",
    "..oTtttTo.....",
    ".oaTTTTTao....",
    ".oaTdddTao....",
    ".obttttbbo....",
    "..obbo.bbo....",
    "...ffo.ffo....",
]

# ── Villager Left frames ──────────────────────────────────────────────
_VILLAGER_LEFT_0 = [
    "...ohhho......",
    "..ohHHHho.....",
    ".ohHHHHHo.....",
    ".osssssso.....",
    "oseeSSsso.....",
    "osEeSSSSo.....",
    "osSSSSSSo.....",
    ".oTTTTTo......",
    ".oTtttTooooa..",
    "oaTTTTTTooa...",
    "oaTdddTTToa...",
    "obttttttboa...",
    "obbo..oooo....",
    ".ffo..........",
]

_VILLAGER_LEFT_1 = [
    "...ohhho......",
    "..ohHHHho.....",
    ".ohHHHHHo.....",
    ".osssssso.....",
    "oseeSSsso.....",
    "osEeSSSSo.....",
    "osSSSSSSo.....",
    ".oTTTTTo......",
    ".oTtttToa.....",
    "oaTTTTToooa...",
    "oaTdddTTooa...",
    "obttttbbooa...",
    ".obbo.oooo....",
    "..ffo.........",
]

# ── Villager Right frames ─────────────────────────────────────────────
_VILLAGER_RIGHT_0 = [
    "......ohhho...",
    ".....ohHHHho..",
    ".....oHHHHHho.",
    ".....osssssso.",
    ".....ossSeeso.",
    ".....oSSSSEeo.",
    ".....oSSSSSSo.",
    "......oTTTTTo.",
    "..aooooTtttTo.",
    "...aooTTTTTTa.",
    "...aoTTTdddTa.",
    "...aobtttttbo.",
    "....oooo.obbo.",
    "..........off.",
]

_VILLAGER_RIGHT_1 = [
    "......ohhho...",
    ".....ohHHHho..",
    ".....oHHHHHho.",
    ".....osssssso.",
    ".....ossSeeso.",
    ".....oSSSSEeo.",
    ".....oSSSSSSo.",
    "......oTTTTTo.",
    ".....aoTtttTo.",
    "...aooooTTTTa.",
    "...aooTTdddTa.",
    "...aoobbtttbo.",
    "....oooo.obbo.",
    ".........off..",
]

# ══════════════════════════════════════════════════════════════════════
# MERCHANT - hooded figure, green cloak, gold accents
# ══════════════════════════════════════════════════════════════════════

_MERCHANT_PAL = {
    'o': (20, 20, 20),       # dark outline
    's': (220, 195, 165),    # skin (visible face)
    'S': (190, 165, 135),    # skin shadow
    'h': (40, 70, 50),       # hood dark
    'H': (55, 90, 65),       # hood medium
    'g': (70, 110, 75),      # green cloak
    'G': (90, 135, 95),      # cloak highlight
    'd': (50, 80, 55),       # cloak shadow
    'e': (90, 110, 80),      # eye color
    'E': (30, 30, 30),       # eye pupil
    'c': (210, 170, 60),     # gold coin/accent
    'C': (240, 200, 80),     # gold highlight
    'b': (90, 70, 50),       # belt/bag
    '.': None,
}

# ── Merchant Down frames ──────────────────────────────────────────────
_MERCHANT_DOWN_0 = [
    "...ohhhhho....",
    "..ohHHHHHho...",
    ".ohHHHHHHHo...",
    ".ohhosssohho..",
    ".ohoseeSsoho..",
    ".ohosEeEsoho..",
    ".ohosSSSsoho..",
    "..oGGGGGGGo...",
    "..oGggggGo....",
    ".oGcCgggCco...",
    ".oGggdddgGo...",
    ".odggggggdo...",
    ".oddo.oddo....",
    "..oo...oo.....",
]

_MERCHANT_DOWN_1 = [
    "...ohhhhho....",
    "..ohHHHHHho...",
    ".ohHHHHHHHo...",
    ".ohhosssohho..",
    ".ohoseeSsoho..",
    ".ohosEeEsoho..",
    ".ohosSSSsoho..",
    "..oGGGGGGGo...",
    "..oGggggGo....",
    ".oGcCgggCco...",
    ".oGggdddgGo...",
    ".odggggggdo...",
    "..oddo.ddo....",
    "...oo...oo....",
]

# ── Merchant Up frames ────────────────────────────────────────────────
_MERCHANT_UP_0 = [
    "...ohhhhho....",
    "..ohHHHHHho...",
    ".ohHHHHHHHo...",
    ".ohhhhhhhho...",
    ".ohhhhhhhhho..",
    ".ohhhhhhhho...",
    ".ohhhhhhho....",
    "..oGGGGGGGo...",
    "..oGggggGo....",
    ".oGcCgggCco...",
    ".oGggdddgGo...",
    ".odggggggdo...",
    ".oddo.oddo....",
    "..oo...oo.....",
]

_MERCHANT_UP_1 = [
    "...ohhhhho....",
    "..ohHHHHHho...",
    ".ohHHHHHHHo...",
    ".ohhhhhhhho...",
    ".ohhhhhhhhho..",
    ".ohhhhhhhho...",
    ".ohhhhhhho....",
    "..oGGGGGGGo...",
    "..oGggggGo....",
    ".oGcCgggCco...",
    ".oGggdddgGo...",
    ".odggggggdo...",
    "..oddo.ddo....",
    "...oo...oo....",
]

# ── Merchant Left frames ──────────────────────────────────────────────
_MERCHANT_LEFT_0 = [
    "..ohhhho......",
    ".ohHHHHho.....",
    "ohHHHHHHo.....",
    "ohhossoho.....",
    "ohoeesoho.....",
    "ohoEeSsho.....",
    "ohosSsho......",
    ".oGGGGGo......",
    ".oGggggooob...",
    "oGcCgggoob....",
    "oGggdddgob....",
    "odgggggdob....",
    "oddo..oooo....",
    ".oo...........",
]

_MERCHANT_LEFT_1 = [
    "..ohhhho......",
    ".ohHHHHho.....",
    "ohHHHHHHo.....",
    "ohhossoho.....",
    "ohoeesoho.....",
    "ohoEeSsho.....",
    "ohosSsho......",
    ".oGGGGGo......",
    ".oGggggob.....",
    "oGcCggooob....",
    "oGggdddoob....",
    "odgggdgoob....",
    ".oddo.oooo....",
    "..oo..........",
]

# ── Merchant Right frames ─────────────────────────────────────────────
_MERCHANT_RIGHT_0 = [
    "......ohhhho..",
    ".....ohHHHHho.",
    ".....oHHHHHHo.",
    ".....ohosshho.",
    ".....ohoeeho..",
    ".....ohsSeEho.",
    "......ohsSho..",
    "......oGGGGGo.",
    "...booooggggG.",
    "....booogCcGo.",
    "....bogdddgGo.",
    "....bododdgdo.",
    "....oooo.oddo.",
    "...........oo.",
]

_MERCHANT_RIGHT_1 = [
    "......ohhhho..",
    ".....ohHHHHho.",
    ".....oHHHHHHo.",
    ".....ohosshho.",
    ".....ohoeeho..",
    ".....ohsSeEho.",
    "......ohsSho..",
    "......oGGGGGo.",
    ".....boggggGo.",
    "....boooggCcG.",
    "....booodddgG.",
    "....boodgggdo.",
    "....oooo.oddo.",
    "..........oo..",
]

# ══════════════════════════════════════════════════════════════════════
# GUARD - armored figure, silver helmet, red cape
# ══════════════════════════════════════════════════════════════════════

_GUARD_PAL = {
    'o': (20, 20, 20),       # dark outline
    's': (220, 200, 175),    # skin
    'S': (190, 170, 145),    # skin shadow
    'm': (140, 145, 155),    # metal (silver)
    'M': (170, 175, 185),    # metal highlight
    'D': (90, 95, 105),      # metal dark
    'a': (120, 125, 135),    # armor body
    'A': (150, 155, 165),    # armor highlight
    'r': (160, 30, 30),      # red cape
    'R': (190, 50, 50),      # cape highlight
    'd': (110, 20, 20),      # cape shadow
    'e': (80, 110, 130),     # eye color
    'E': (30, 30, 30),       # eye pupil
    '.': None,
}

# ── Guard Down frames ─────────────────────────────────────────────────
_GUARD_DOWN_0 = [
    "...oMMMMMo....",
    "..oMMmmmMo....",
    ".oMmDDDDmo....",
    ".omossssom....",
    ".omoseeSom....",
    ".omosEeSom....",
    ".omosSssom....",
    "..oAAAAAo.....",
    "..oAaaaaAo....",
    ".oRAaAaARo....",
    ".oRAddddRo....",
    ".ordRRRdro....",
    ".ordo.odro....",
    "..oo...oo.....",
]

_GUARD_DOWN_1 = [
    "...oMMMMMo....",
    "..oMMmmmMo....",
    ".oMmDDDDmo....",
    ".omossssom....",
    ".omoseeSom....",
    ".omosEeSom....",
    ".omosSssom....",
    "..oAAAAAo.....",
    "..oAaaaaAo....",
    ".oRAaAaARo....",
    ".oRAddddRo....",
    ".ordRRRdro....",
    "..ordo.roo....",
    "...oo...oo....",
]

# ── Guard Up frames ───────────────────────────────────────────────────
_GUARD_UP_0 = [
    "...oMMMMMo....",
    "..oMMmmmMo....",
    ".oMmDDDDmo....",
    ".ommmmmmmm....",
    ".omDDDDDDo....",
    ".omDDDDDo.....",
    ".omooDDo......",
    "..oAAAAAo.....",
    "..oAaaaaAo....",
    ".oRAaAaARo....",
    ".oRAddddRo....",
    ".ordRRRdro....",
    ".ordo.odro....",
    "..oo...oo.....",
]

_GUARD_UP_1 = [
    "...oMMMMMo....",
    "..oMMmmmMo....",
    ".oMmDDDDmo....",
    ".ommmmmmmm....",
    ".omDDDDDDo....",
    ".omDDDDDo.....",
    ".omooDDo......",
    "..oAAAAAo.....",
    "..oAaaaaAo....",
    ".oRAaAaARo....",
    ".oRAddddRo....",
    ".ordRRRdro....",
    "..ordo.roo....",
    "...oo...oo....",
]

# ── Guard Left frames ─────────────────────────────────────────────────
_GUARD_LEFT_0 = [
    "..oMMMMMo.....",
    ".oMMmmmMo.....",
    "oMmDDDDmo.....",
    "omosssomo.....",
    "omoeeSomo.....",
    "omoEeSSmo.....",
    "omosSSSmo.....",
    ".oAAAAAo......",
    ".oAaaaaAooor..",
    "oRAaAaAAoor...",
    "oRAddddAor....",
    "ordRRRdroo....",
    "ordo..oooo....",
    ".oo...........",
]

_GUARD_LEFT_1 = [
    "..oMMMMMo.....",
    ".oMMmmmMo.....",
    "oMmDDDDmo.....",
    "omosssomo.....",
    "omoeeSomo.....",
    "omoEeSSmo.....",
    "omosSSSmo.....",
    ".oAAAAAo......",
    ".oAaaaaAor....",
    "oRAaAaAooor...",
    "oRAddddAoor...",
    "ordRRRdrooo...",
    ".ordo.oooo....",
    "..oo..........",
]

# ── Guard Right frames ────────────────────────────────────────────────
_GUARD_RIGHT_0 = [
    ".....oMMMMMo..",
    ".....oMmmmMMo.",
    ".....omDDDDmM.",
    ".....omosssmo.",
    ".....omoSeeo..",
    ".....omSSEeo..",
    ".....omSSSsmo.",
    "......oAAAAAo.",
    "..roooAaaaaAo.",
    "...rooAAaAaAR.",
    "....roAdddRAo.",
    "....oodrRRRdo.",
    "....oooo.odro.",
    "...........oo.",
]

_GUARD_RIGHT_1 = [
    ".....oMMMMMo..",
    ".....oMmmmMMo.",
    ".....omDDDDmM.",
    ".....omosssmo.",
    ".....omoSeeo..",
    ".....omSSEeo..",
    ".....omSSSsmo.",
    "......oAAAAAo.",
    "...roAaaaaAo..",
    "...roooAaAaAR.",
    "...rooAdddRAo.",
    "...ooordRRRdo.",
    "....oooo.odro.",
    "..........oo..",
]

# ══════════════════════════════════════════════════════════════════════
# BUILD SURFACES
# ══════════════════════════════════════════════════════════════════════

_elder_cache = None
_villager_cache = None
_merchant_cache = None
_guard_cache = None


def get_elder_frames():
    """Return dict of {direction: [frame0, frame1]} for the Elder NPC."""
    global _elder_cache
    if _elder_cache is not None:
        return _elder_cache

    _elder_cache = {
        "down":  [surface_from_grid(g, _ELDER_PAL, 2) for g in (_ELDER_DOWN_0, _ELDER_DOWN_1)],
        "up":    [surface_from_grid(g, _ELDER_PAL, 2) for g in (_ELDER_UP_0, _ELDER_UP_1)],
        "left":  [surface_from_grid(g, _ELDER_PAL, 2) for g in (_ELDER_LEFT_0, _ELDER_LEFT_1)],
        "right": [surface_from_grid(g, _ELDER_PAL, 2) for g in (_ELDER_RIGHT_0, _ELDER_RIGHT_1)],
    }
    return _elder_cache


def get_villager_frames():
    """Return dict of {direction: [frame0, frame1]} for the Villager NPC."""
    global _villager_cache
    if _villager_cache is not None:
        return _villager_cache

    _villager_cache = {
        "down":  [surface_from_grid(g, _VILLAGER_PAL, 2) for g in (_VILLAGER_DOWN_0, _VILLAGER_DOWN_1)],
        "up":    [surface_from_grid(g, _VILLAGER_PAL, 2) for g in (_VILLAGER_UP_0, _VILLAGER_UP_1)],
        "left":  [surface_from_grid(g, _VILLAGER_PAL, 2) for g in (_VILLAGER_LEFT_0, _VILLAGER_LEFT_1)],
        "right": [surface_from_grid(g, _VILLAGER_PAL, 2) for g in (_VILLAGER_RIGHT_0, _VILLAGER_RIGHT_1)],
    }
    return _villager_cache


def get_merchant_frames():
    """Return dict of {direction: [frame0, frame1]} for the Merchant NPC."""
    global _merchant_cache
    if _merchant_cache is not None:
        return _merchant_cache

    _merchant_cache = {
        "down":  [surface_from_grid(g, _MERCHANT_PAL, 2) for g in (_MERCHANT_DOWN_0, _MERCHANT_DOWN_1)],
        "up":    [surface_from_grid(g, _MERCHANT_PAL, 2) for g in (_MERCHANT_UP_0, _MERCHANT_UP_1)],
        "left":  [surface_from_grid(g, _MERCHANT_PAL, 2) for g in (_MERCHANT_LEFT_0, _MERCHANT_LEFT_1)],
        "right": [surface_from_grid(g, _MERCHANT_PAL, 2) for g in (_MERCHANT_RIGHT_0, _MERCHANT_RIGHT_1)],
    }
    return _merchant_cache


def get_guard_frames():
    """Return dict of {direction: [frame0, frame1]} for the Guard NPC."""
    global _guard_cache
    if _guard_cache is not None:
        return _guard_cache

    _guard_cache = {
        "down":  [surface_from_grid(g, _GUARD_PAL, 2) for g in (_GUARD_DOWN_0, _GUARD_DOWN_1)],
        "up":    [surface_from_grid(g, _GUARD_PAL, 2) for g in (_GUARD_UP_0, _GUARD_UP_1)],
        "left":  [surface_from_grid(g, _GUARD_PAL, 2) for g in (_GUARD_LEFT_0, _GUARD_LEFT_1)],
        "right": [surface_from_grid(g, _GUARD_PAL, 2) for g in (_GUARD_RIGHT_0, _GUARD_RIGHT_1)],
    }
    return _guard_cache
