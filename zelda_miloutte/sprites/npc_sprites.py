"""Pixel art sprites for NPCs (Elder, Villager, Merchant, Guard)."""

from .pixel_art import surface_from_grid

# ══════════════════════════════════════════════════════════════════════
# ELDER - wise old figure with staff, white hair/beard, blue robes
# ══════════════════════════════════════════════════════════════════════

_ELDER_PAL = {
    'o': (20, 20, 20),       # dark outline
    's': (240, 220, 195),    # skin (pale)
    'S': (210, 190, 165),    # skin shadow
    'K': (185, 165, 140),    # skin deep shadow
    'w': (245, 245, 245),    # white hair/beard
    'W': (220, 220, 220),    # hair mid-tone
    'V': (190, 190, 190),    # hair shadow
    'e': (80, 120, 160),     # eye color (wise blue)
    'E': (40, 40, 40),       # eye pupil
    'Y': (100, 80, 60),      # eyebrow
    'b': (60, 90, 150),      # blue robe
    'B': (80, 110, 170),     # robe highlight
    'U': (70, 100, 160),     # robe mid-tone
    'd': (40, 60, 100),      # robe deep shadow
    'g': (180, 160, 80),     # gold trim
    'G': (220, 200, 100),    # gold highlight
    'h': (220, 190, 140),    # hand
    'H': (200, 170, 120),    # hand shadow
    'F': (140, 100, 60),     # staff wood
    'f': (110, 80, 50),      # staff shadow
    'j': (160, 220, 240),    # staff crystal
    'J': (120, 180, 200),    # crystal shadow
    '.': None,
}

# ── Elder Down frames ─────────────────────────────────────────────────
_ELDER_DOWN_0 = [
    "....owwwwo....",
    "...owWWWWwo...",
    "..owWWWWWWo...",
    "..osYsssYso...",
    ".osSeeSeSso...",
    ".osEeYSEeso...",
    ".osSSKSSSSo...",
    ".owWVWWWVWo...",
    "..oBBUBBBo....",
    ".oBgGBUBgGo...",
    ".oBBUdddUBo...",
    ".odbBBBBdbo...",
    ".odfo.ofdo....",
    "..ofo..oo.....",
]

_ELDER_DOWN_1 = [
    "....owwwwo....",
    "...owWWWWwo...",
    "..owWWWWWWo...",
    "..osYsssYso...",
    ".osSeeSeSso...",
    ".osEeYSEeso...",
    ".osSSKSSSSo...",
    ".owWVWWWVWo...",
    "..oBBUBBBo....",
    ".oBgGBUBgGo...",
    ".oBBUdddUBo...",
    ".odbBBBBdbo...",
    "..odfo.dbo....",
    "...ofo..oo....",
]

# ── Elder Up frames ───────────────────────────────────────────────────
_ELDER_UP_0 = [
    "....owwwwo....",
    "...owWWWWwo...",
    "..owWWWWWWo...",
    "..osYYYYYso...",
    ".osssssssso...",
    ".ossKSKSKso...",
    ".osSSKKSSSo...",
    ".owWVWWWVWo...",
    "..oBBUBBBo....",
    ".oBgGBUBgGo...",
    ".oBBUdddUBo...",
    ".odbBBBBdbo...",
    ".odfo.ofdo....",
    "..ofo..oo.....",
]

_ELDER_UP_1 = [
    "....owwwwo....",
    "...owWWWWwo...",
    "..owWWWWWWo...",
    "..osYYYYYso...",
    ".osssssssso...",
    ".ossKSKSKso...",
    ".osSSKKSSSo...",
    ".owWVWWWVWo...",
    "..oBBUBBBo....",
    ".oBgGBUBgGo...",
    ".oBBUdddUBo...",
    ".odbBBBBdbo...",
    "..odbo.fdo....",
    "...oo..ofo....",
]

# ── Elder Left frames ─────────────────────────────────────────────────
_ELDER_LEFT_0 = [
    "...owwwwo.....",
    "..owWWWWwo....",
    ".owWWWWWWo....",
    ".osYsssYso....",
    "osSeYSSsso....",
    "osEeKSSSSo....",
    "osSSKSKSSo....",
    "owWVWWWVWo....",
    ".oBBUBBBoooh..",
    "oBgGBUUBBooH..",
    "oBBUdddUBof...",
    "odbBBBBdboFjo.",
    "odfo..ooooJjo.",
    ".ofo..........",
]

_ELDER_LEFT_1 = [
    "...owwwwo.....",
    "..owWWWWwo....",
    ".owWWWWWWo....",
    ".osYsssYso....",
    "osSeYSSsso....",
    "osEeKSSSSo....",
    "osSSKSKSSo....",
    "owWVWWWVWo....",
    ".oBBUBBBoh....",
    "oBgGBUUBoooH..",
    "oBBUdddUBoH...",
    "odbBBBBdboFjo.",
    ".odfo.ooooJjo.",
    "..ofo.........",
]

# ── Elder Right frames ────────────────────────────────────────────────
_ELDER_RIGHT_0 = [
    ".....owwwwo...",
    "....owWWWWwo..",
    "....owWWWWWWo.",
    "....osYsssYso.",
    "....ossSeYSeo.",
    "....oSSSSKEeo.",
    "....oSSKSKSSo.",
    "....owWVWWWVo.",
    "..hoooBBBUBBo.",
    "..HoooBBUUBgo.",
    "...foBUdddUBo.",
    ".ojFobdBBBBdo.",
    ".ojJoooo.ofdo.",
    "..........ofo.",
]

_ELDER_RIGHT_1 = [
    ".....owwwwo...",
    "....owWWWWwo..",
    "....owWWWWWWo.",
    "....osYsssYso.",
    "....ossSeYSeo.",
    "....oSSSSKEeo.",
    "....oSSKSKSSo.",
    "....owWVWWWVo.",
    "....hoBBBUBBo.",
    "..HoooBoBUBgo.",
    "...HoBUdddUBo.",
    ".ojFobdBBBBdo.",
    ".ojJoooo.ofdo.",
    ".........ofo..",
]

# ══════════════════════════════════════════════════════════════════════
# VILLAGER - hardworking peasant with apron, brown hair, tools
# ══════════════════════════════════════════════════════════════════════

_VILLAGER_PAL = {
    'o': (20, 20, 20),       # dark outline
    's': (240, 210, 180),    # skin
    'S': (210, 180, 150),    # skin mid-shadow
    'K': (180, 150, 120),    # skin deep shadow
    'h': (90, 60, 40),       # brown hair
    'H': (110, 80, 55),      # hair highlight
    'V': (70, 45, 30),       # hair shadow
    'e': (100, 140, 180),    # eye color
    'E': (40, 40, 40),       # eye pupil
    'Y': (70, 50, 35),       # eyebrow
    't': (200, 170, 120),    # tan tunic
    'T': (220, 190, 140),    # tunic highlight
    'U': (180, 150, 100),    # tunic mid-tone
    'd': (140, 110, 75),     # tunic shadow
    'b': (100, 80, 60),      # brown belt/pants
    'B': (120, 95, 70),      # belt highlight
    'f': (80, 60, 45),       # feet
    'a': (210, 180, 140),    # arms
    'A': (180, 150, 110),    # arm shadow
    'p': (250, 245, 240),    # apron white
    'P': (220, 215, 210),    # apron shadow
    'r': (160, 130, 90),     # rope/tool handle
    '.': None,
}

# ── Villager Down frames ──────────────────────────────────────────────
_VILLAGER_DOWN_0 = [
    "....ohhho.....",
    "...ohHHHho....",
    "..ohHHHHVo....",
    "..osYsssYso...",
    ".osSeeSesSo...",
    ".osEeYSEeSo...",
    ".osSSKKSSSo...",
    "..oTTTTTTo....",
    "..oTUtUtTo....",
    ".oaTpppTao....",
    ".oaTpPpTao....",
    ".obBtUtbBo....",
    ".obBo.obBo....",
    "..ffo.offo....",
]

_VILLAGER_DOWN_1 = [
    "....ohhho.....",
    "...ohHHHho....",
    "..ohHHHHVo....",
    "..osYsssYso...",
    ".osSeeSesSo...",
    ".osEeYSEeSo...",
    ".osSSKKSSSo...",
    "..oTTTTTTo....",
    "..oTUtUtTo....",
    ".oaTpppTao....",
    ".oaTpPpTao....",
    ".obBtUtbBo....",
    "..obBo.bBo....",
    "...ffo.ffo....",
]

# ── Villager Up frames ────────────────────────────────────────────────
_VILLAGER_UP_0 = [
    "....ohhho.....",
    "...ohHHHho....",
    "..ohHHHHVo....",
    "..osYYYYYso...",
    ".osssssssso...",
    ".ossKSKSKso...",
    ".osSSKKSSSo...",
    "..oTTTTTTo....",
    "..oTUtUtTo....",
    ".oaTpppTao....",
    ".oaTpPpTao....",
    ".obBtUtbBo....",
    ".obBo.obBo....",
    "..ffo.offo....",
]

_VILLAGER_UP_1 = [
    "....ohhho.....",
    "...ohHHHho....",
    "..ohHHHHVo....",
    "..osYYYYYso...",
    ".osssssssso...",
    ".ossKSKSKso...",
    ".osSSKKSSSo...",
    "..oTTTTTTo....",
    "..oTUtUtTo....",
    ".oaTpppTao....",
    ".oaTpPpTao....",
    ".obBtUtbBo....",
    "..obBo.bBo....",
    "...ffo.ffo....",
]

# ── Villager Left frames ──────────────────────────────────────────────
_VILLAGER_LEFT_0 = [
    "...ohhho......",
    "..ohHHHho.....",
    ".ohHHHHVo.....",
    ".osYsssYso....",
    "osSeYSKsso....",
    "osEeKSSSSo....",
    "osSSKKSSSo....",
    ".oTTTTTTo.....",
    ".oTUtUtTooooa.",
    "oaTpppTUTooa..",
    "oaTpPpUddToa..",
    "obBtUtUtbBoa..",
    "obBo..oooo....",
    ".ffo..........",
]

_VILLAGER_LEFT_1 = [
    "...ohhho......",
    "..ohHHHho.....",
    ".ohHHHHVo.....",
    ".osYsssYso....",
    "osSeYSKsso....",
    "osEeKSSSSo....",
    "osSSKKSSSo....",
    ".oTTTTTTo.....",
    ".oTUtUtToa....",
    "oaTpppTooooa..",
    "oaTpPpUTUooa..",
    "obBtUtbBbooa..",
    ".obBo.oooo....",
    "..ffo.........",
]

# ── Villager Right frames ─────────────────────────────────────────────
_VILLAGER_RIGHT_0 = [
    "......ohhho...",
    ".....ohHHHho..",
    ".....oVHHHHho.",
    "....osYsssYso.",
    "....ossKSYeSo.",
    "....oSSSSKEeo.",
    "....oSSKKSSo..",
    ".....oTTTTTTo.",
    ".aoooToTUtUTo.",
    "..aooTUTpppTa.",
    "..aoTddUpPpTa.",
    "..aoBbtUtUtBb.",
    "....oooo.obBo.",
    "..........off.",
]

_VILLAGER_RIGHT_1 = [
    "......ohhho...",
    ".....ohHHHho..",
    ".....oVHHHHho.",
    "....osYsssYso.",
    "....ossKSYeSo.",
    "....oSSSSKEeo.",
    "....oSSKKSSo..",
    ".....oTTTTTTo.",
    ".....aoTUtUTo.",
    "..aooooTpppTa.",
    "..aooUTUpPpTa.",
    "..aoobBbtUtBb.",
    "....oooo.obBo.",
    ".........off..",
]

# ══════════════════════════════════════════════════════════════════════
# MERCHANT - hooded figure with coin pouches, green cloak, gold wares
# ══════════════════════════════════════════════════════════════════════

_MERCHANT_PAL = {
    'o': (20, 20, 20),       # dark outline
    's': (220, 195, 165),    # skin (visible face)
    'S': (190, 165, 135),    # skin shadow
    'K': (160, 135, 105),    # skin deep shadow
    'h': (40, 70, 50),       # hood dark
    'H': (55, 90, 65),       # hood medium
    'V': (65, 105, 75),      # hood highlight
    'g': (70, 110, 75),      # green cloak
    'G': (90, 135, 95),      # cloak highlight
    'U': (80, 120, 85),      # cloak mid-tone
    'd': (50, 80, 55),       # cloak shadow
    'e': (90, 110, 80),      # eye color
    'E': (30, 30, 30),       # eye pupil
    'Y': (50, 60, 45),       # eyebrow
    'c': (210, 170, 60),     # gold coin/accent
    'C': (240, 200, 80),     # gold highlight
    'z': (180, 145, 50),     # gold shadow
    'b': (90, 70, 50),       # belt/bag
    'B': (110, 85, 60),      # bag highlight
    'p': (140, 110, 80),     # pouch
    'P': (160, 125, 90),     # pouch highlight
    '.': None,
}

# ── Merchant Down frames ──────────────────────────────────────────────
_MERCHANT_DOWN_0 = [
    "...ohhhhho....",
    "..ohHHVHHho...",
    ".ohHHVVVHHo...",
    ".ohhosssohho..",
    ".ohosYeSYoho..",
    ".ohosEeEsoho..",
    ".ohosSKSsoho..",
    "..oGGUUGGGo...",
    "..oGgUgUGo....",
    ".oGcCgUgCzo...",
    ".oGgUdddgGo...",
    ".odgUpUpgdo...",
    ".odpbo.bpdo...",
    "..obo..obo....",
]

_MERCHANT_DOWN_1 = [
    "...ohhhhho....",
    "..ohHHVHHho...",
    ".ohHHVVVHHo...",
    ".ohhosssohho..",
    ".ohosYeSYoho..",
    ".ohosEeEsoho..",
    ".ohosSKSsoho..",
    "..oGGUUGGGo...",
    "..oGgUgUGo....",
    ".oGcCgUgCzo...",
    ".oGgUdddgGo...",
    ".odgUpUpgdo...",
    "..odpbo.pdo...",
    "...obo..obo...",
]

# ── Merchant Up frames ────────────────────────────────────────────────
_MERCHANT_UP_0 = [
    "...ohhhhho....",
    "..ohHHVHHho...",
    ".ohHHVVVHHo...",
    ".ohhhhhhhho...",
    ".ohhYYYYYhho..",
    ".ohhhhhhhho...",
    ".ohhhhhhho....",
    "..oGGUUGGGo...",
    "..oGgUgUGo....",
    ".oGcCgUgCzo...",
    ".oGgUdddgGo...",
    ".odgUpUpgdo...",
    ".odpbo.bpdo...",
    "..obo..obo....",
]

_MERCHANT_UP_1 = [
    "...ohhhhho....",
    "..ohHHVHHho...",
    ".ohHHVVVHHo...",
    ".ohhhhhhhho...",
    ".ohhYYYYYhho..",
    ".ohhhhhhhho...",
    ".ohhhhhhho....",
    "..oGGUUGGGo...",
    "..oGgUgUGo....",
    ".oGcCgUgCzo...",
    ".oGgUdddgGo...",
    ".odgUpUpgdo...",
    "..odpbo.pdo...",
    "...obo..obo...",
]

# ── Merchant Left frames ──────────────────────────────────────────────
_MERCHANT_LEFT_0 = [
    "..ohhhhho.....",
    ".ohHHVHHho....",
    "ohHHVVVHHo....",
    "ohhosYsoho....",
    "ohoeeYsoho....",
    "ohoEeSKho.....",
    "ohosSKho......",
    ".oGGUGGGo.....",
    ".oGgUggoooob..",
    "oGcCgUgoobP...",
    "oGgUdddgopP...",
    "odgUpUpgobP...",
    "odpbo..ooobo..",
    ".obo..........",
]

_MERCHANT_LEFT_1 = [
    "..ohhhhho.....",
    ".ohHHVHHho....",
    "ohHHVVVHHo....",
    "ohhosYsoho....",
    "ohoeeYsoho....",
    "ohoEeSKho.....",
    "ohosSKho......",
    ".oGGUGGGo.....",
    ".oGgUggob.....",
    "oGcCgUoooobP..",
    "oGgUdddoobP...",
    "odgUpUgoobP...",
    ".odpbo.ooobo..",
    "..obo.........",
]

# ── Merchant Right frames ─────────────────────────────────────────────
_MERCHANT_RIGHT_0 = [
    ".....ohhhhho..",
    "....ohHHVHHho.",
    "....oHHVVVHHo.",
    "....ohosYshho.",
    "....ohoYeehho.",
    ".....ohKSEeho.",
    "......ohKssho.",
    ".....oGGGUGGo.",
    "..boooogUgGGo.",
    "...PboogoUgCc.",
    "...PpogdddUgG.",
    "...PbogpUpUgd.",
    "..obooo.obpdo.",
    "..........obo.",
]

_MERCHANT_RIGHT_1 = [
    ".....ohhhhho..",
    "....ohHHVHHho.",
    "....oHHVVVHHo.",
    "....ohosYshho.",
    "....ohoYeehho.",
    ".....ohKSEeho.",
    "......ohKssho.",
    ".....oGGGUGGo.",
    ".....boggUgGo.",
    "..Pboooogoggc.",
    "..PboodddUgGo.",
    "..PboogogUpgd.",
    "..obooo.obpdo.",
    ".........obo..",
]

# ══════════════════════════════════════════════════════════════════════
# GUARD - armored soldier with spear, silver helmet, red cape
# ══════════════════════════════════════════════════════════════════════

_GUARD_PAL = {
    'o': (20, 20, 20),       # dark outline
    's': (220, 200, 175),    # skin
    'S': (190, 170, 145),    # skin shadow
    'K': (160, 140, 115),    # skin deep shadow
    'm': (140, 145, 155),    # metal (silver)
    'M': (170, 175, 185),    # metal highlight
    'N': (155, 160, 170),    # metal mid-tone
    'D': (90, 95, 105),      # metal dark
    'V': (70, 75, 85),       # metal shadow
    'a': (120, 125, 135),    # armor body
    'A': (150, 155, 165),    # armor highlight
    'U': (135, 140, 150),    # armor mid-tone
    'r': (160, 30, 30),      # red cape
    'R': (190, 50, 50),      # cape highlight
    'W': (175, 40, 40),      # cape mid-tone
    'd': (110, 20, 20),      # cape shadow
    'e': (80, 110, 130),     # eye color
    'E': (30, 30, 30),       # eye pupil
    'p': (200, 190, 180),    # spear shaft
    'P': (180, 170, 160),    # spear shadow
    'j': (180, 185, 195),    # spear tip (metal)
    '.': None,
}

# ── Guard Down frames ─────────────────────────────────────────────────
_GUARD_DOWN_0 = [
    "...oMMMMMo....",
    "..oMMNmNMo....",
    ".oMmDDVDDmo...",
    ".omoosssoom...",
    ".omoseSeSom...",
    ".omosEeSEom...",
    ".omosSKSsom...",
    "..oAAUUAAo....",
    "..oAaUaUAo....",
    ".oRAaUaUARo...",
    ".oRWAddWRWo...",
    ".ordWRRWdro...",
    ".orpo.opro....",
    "..oPo..oPo....",
]

_GUARD_DOWN_1 = [
    "...oMMMMMo....",
    "..oMMNmNMo....",
    ".oMmDDVDDmo...",
    ".omoosssoom...",
    ".omoseSeSom...",
    ".omosEeSEom...",
    ".omosSKSsom...",
    "..oAAUUAAo....",
    "..oAaUaUAo....",
    ".oRAaUaUARo...",
    ".oRWAddWRWo...",
    ".ordWRRWdro...",
    "..orpo.pro....",
    "...oPo.oPo....",
]

# ── Guard Up frames ───────────────────────────────────────────────────
_GUARD_UP_0 = [
    "...oMMMMMo....",
    "..oMMNmNMo....",
    ".oMmDDVDDmo...",
    ".ommmmmmmm....",
    ".omDVDDVDo....",
    ".omDVVDDo.....",
    ".omooVDo......",
    "..oAAUUAAo....",
    "..oAaUaUAo....",
    ".oRAaUaUARo...",
    ".oRWAddWRWo...",
    ".ordWRRWdro...",
    ".orpo.opro....",
    "..oPo..oPo....",
]

_GUARD_UP_1 = [
    "...oMMMMMo....",
    "..oMMNmNMo....",
    ".oMmDDVDDmo...",
    ".ommmmmmmm....",
    ".omDVDDVDo....",
    ".omDVVDDo.....",
    ".omooVDo......",
    "..oAAUUAAo....",
    "..oAaUaUAo....",
    ".oRAaUaUARo...",
    ".oRWAddWRWo...",
    ".ordWRRWdro...",
    "..orpo.pro....",
    "...oPo.oPo....",
]

# ── Guard Left frames ─────────────────────────────────────────────────
_GUARD_LEFT_0 = [
    "..oMMMMMo.....",
    ".oMMNmNMo.....",
    "oMmDDVDDmo....",
    "omooossoomo...",
    "omoeSeSomo....",
    "omoEeSKNmo....",
    "omosSKSNmo....",
    ".oAAUUAAo.....",
    ".oAaUaUAooorj.",
    "oRAaUaUAAoorj.",
    "oRWAddddAoPP..",
    "ordWRRWdroP...",
    "orpo..oooo....",
    ".oPo..........",
]

_GUARD_LEFT_1 = [
    "..oMMMMMo.....",
    ".oMMNmNMo.....",
    "oMmDDVDDmo....",
    "omooossoomo...",
    "omoeSeSomo....",
    "omoEeSKNmo....",
    "omosSKSNmo....",
    ".oAAUUAAo.....",
    ".oAaUaUAorj...",
    "oRAaUaUAoorj..",
    "oRWAddddAoPP..",
    "ordWRRWdrooP..",
    ".orpo.oooo....",
    "..oPo.........",
]

# ── Guard Right frames ────────────────────────────────────────────────
_GUARD_RIGHT_0 = [
    ".....oMMMMMo..",
    ".....oMNmNMMo.",
    "....omDDVDDmM.",
    "...omooossoom.",
    "....omoSeSemo.",
    "....omNKSEEmo.",
    "....omNSKSsmo.",
    ".....oAAUUAAo.",
    ".jroooAaUaUAo.",
    ".jrooAAaUaUAR.",
    "..PPoPAdddWRo.",
    "...PordWRRWdo.",
    "....oooo.opro.",
    "..........oPo.",
]

_GUARD_RIGHT_1 = [
    ".....oMMMMMo..",
    ".....oMNmNMMo.",
    "....omDDVDDmM.",
    "...omooossoom.",
    "....omoSeSemo.",
    "....omNKSEEmo.",
    "....omNSKSsmo.",
    ".....oAAUUAAo.",
    "...jroAaUaUAo.",
    "..jrooAAaUaAR.",
    "..PPoPAdddWRo.",
    "..Pooodrdwrdo.",
    "....oooo.opro.",
    "..........oPo.",
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
