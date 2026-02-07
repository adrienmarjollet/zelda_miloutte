"""Pixel art sprites for the Inferno Drake boss (dragon, two phases)."""

from .pixel_art import surface_from_grid

# ── Phase 1 Palette (red dragon) ──────────────────────────────────────
_PAL1 = {
    'o': (20, 10, 10),      # dark outline
    'r': (120, 25, 15),     # body dark red
    'R': (170, 40, 25),     # body mid red
    'S': (210, 55, 35),     # body bright red
    'd': (90, 20, 12),      # scales darkest
    'D': (140, 30, 20),     # scales dark
    'L': (180, 45, 28),     # scales light
    'w': (80, 18, 12),      # wing membrane dark
    'W': (110, 25, 18),     # wing membrane mid
    'M': (140, 35, 22),     # wing membrane light
    'n': (60, 15, 10),      # wing bone dark
    'N': (100, 22, 15),     # wing bone light
    'b': (200, 80, 30),     # belly/chest plate dark orange
    'B': (230, 100, 40),    # belly/chest plate mid orange
    'P': (250, 130, 55),    # belly/chest plate bright orange
    'e': (255, 220, 80),    # eyes glowing yellow
    'E': (200, 160, 50),    # eye edge (darker yellow)
    'h': (70, 50, 35),      # horn dark
    'H': (110, 85, 60),     # horn mid
    'I': (140, 110, 80),    # horn light
    't': (200, 200, 200),   # teeth/claws white
    'T': (150, 150, 150),   # teeth/claws gray
    'f': (255, 140, 40),    # fire bright orange
    'F': (220, 90, 25),     # fire dark orange
    'g': (255, 180, 60),    # fire yellow
    'G': (200, 120, 40),    # fire dark yellow
    's': (80, 60, 50),      # smoke/ash
    'k': (50, 40, 35),      # nostril/mouth dark
    'a': (100, 80, 70),     # ash/ember gray
    'A': (140, 100, 80),    # ash/ember light
    'c': (60, 50, 45),      # claw dark
    'C': (90, 70, 60),      # claw light
    'l': (180, 50, 30),     # tail flame base
    'x': (140, 35, 22),     # scales extra
    '.': None,
}

# ── Phase 2 Palette (wreathed in flame, brighter) ─────────────────────
_PAL2 = {
    'o': (40, 20, 15),      # dark outline (brighter)
    'r': (160, 45, 30),     # body dark red (brighter)
    'R': (210, 65, 40),     # body mid red (brighter)
    'S': (250, 85, 50),     # body bright red (brighter)
    'd': (120, 35, 22),     # scales darkest (brighter)
    'D': (180, 50, 35),     # scales dark (brighter)
    'L': (220, 70, 45),     # scales light (brighter)
    'w': (110, 30, 20),     # wing membrane dark (brighter)
    'W': (150, 45, 30),     # wing membrane mid (brighter)
    'M': (190, 60, 40),     # wing membrane light (brighter)
    'n': (90, 25, 18),      # wing bone dark (brighter)
    'N': (140, 40, 28),     # wing bone light (brighter)
    'b': (240, 110, 50),    # belly/chest plate dark orange (brighter)
    'B': (255, 140, 70),    # belly/chest plate mid orange (brighter)
    'P': (255, 170, 90),    # belly/chest plate bright orange (brighter)
    'e': (255, 250, 150),   # eyes glowing bright yellow
    'E': (255, 200, 100),   # eye edge (bright yellow)
    'h': (100, 75, 55),     # horn dark (brighter)
    'H': (150, 120, 90),    # horn mid (brighter)
    'I': (180, 150, 120),   # horn light (brighter)
    't': (255, 255, 255),   # teeth/claws white (brighter)
    'T': (200, 200, 200),   # teeth/claws gray (brighter)
    'f': (255, 180, 70),    # fire bright orange (more yellow)
    'F': (255, 140, 60),    # fire dark orange (brighter)
    'g': (255, 220, 120),   # fire yellow (brighter)
    'G': (255, 170, 90),    # fire dark yellow (brighter)
    's': (120, 90, 70),     # smoke/ash (brighter)
    'k': (70, 50, 40),      # nostril/mouth dark (brighter)
    'a': (150, 120, 100),   # ash/ember gray (brighter)
    'A': (190, 150, 120),   # ash/ember light (brighter)
    'c': (90, 70, 60),      # claw dark (brighter)
    'C': (130, 100, 85),    # claw light (brighter)
    'l': (230, 80, 45),     # tail flame base (brighter)
    'x': (190, 60, 40),     # scales extra (brighter)
    '.': None,
}

# ── Down frames (24x24 grid, scale=2 → 48x48px) ──────────────────────
# Down frame 0: Wings raised, mouth closed, tail visible
_DOWN_0 = [
    "..........fff...........",
    ".......ffooooooff.......",
    "......fIHhoooohHIf......",
    ".....fohHooooooHhof.....",
    "....fohhoooooooohhof....",
    "...foNNnoooooooonNNof...",
    "..foNWWnnoooooonnWWNo...",
    ".foNWMMWnoooooonWMMWNof.",
    ".fNWWMMWWnoooonWWMMWWNo.",
    "foNWMMWWnoRRRRonWWMMWNof",
    "oNWWMMWooRSSSSRooWMMWWNo",
    "oNWMMWooRdddddddRooWMMNo",
    "oNWMMWoRdDLLLLLDdRoWMMNo",
    "oNWWMWoRdLbbbbbbLoRMWWNo",
    "oNWWMWoRdLbBPPBbLoRMWWNo",
    "fNWWMWoRddbBPPBbdoRMWWNf",
    "fNWWMWoRRddbBBbdRoRMWWNf",
    ".oNWWWooRRddbbddRooWWNo.",
    ".foNWWoRRRddddRRRoWWNof.",
    "..foNooRRkeekRRooNof.l..",
    "...fooRRRoEEoRRRooff.l..",
    "....foRRoottoRRoffl.....",
    ".....foRRRttRRRoffl.....",
    "......fooooooooffl......",
]

# Down frame 1: Wings lowered, mouth slightly open, flame effect
_DOWN_1 = [
    "..........gfg...........",
    ".......gfooooof.........",
    "......goIHHoHHIog.......",
    ".....gohHooooooHhog.....",
    "....gohhooooooohhog.....",
    "...foNNnoooooooonNNof...",
    "..foWWWnnoooooonnWWWof..",
    ".foWMMWWnoooooonWWMMWof.",
    ".oNWWMWWnooooooonWWMWWNo",
    "foNWWMWnoRRRRRonWMWWNof.",
    "oNWWMWooRSSSSSRooWMWWNog",
    "oNWWMooRdddddddRooMWWNof",
    "oNWWMoRdDLLLLLLDdRoMWWNo",
    "oNWWMoRdLbbbbbbbbLoMWWNo",
    "oNWWMoRdLbBPPPBbdLoMWWNo",
    ".oNWMoRddbBPPBbddoRMWNo.",
    ".oNWWoRRddbBBbddRoRWWNo.",
    "..oNWooRRddbbddRooWNo...",
    "..foNooRRRddddRRooNof...",
    "...fooRRkTTTkRRoofg.l...",
    "....foRRooTToRRofgg.l...",
    ".....foRRoottoRoffl.....",
    "......foRRRRRRoffl......",
    ".......foooooofl........",
]

# ── Up frames ─────────────────────────────────────────────────────────
# Up frame 0: Wings spread wide, view from back, tail curving
_UP_0 = [
    "........................",
    "....ll.........ll.......",
    "...llffoooooofflll......",
    "..llfIHhoooohHIffl......",
    "..llohhoooooohholl......",
    ".lfoNNnoooooonNNofll....",
    ".lfoWWnnoooonnWWNofl....",
    "lloNWWWnoooonWWWNofll...",
    "loNWWMWnooooonWMWWNofl..",
    "foNWWMWooRRRRooWMWWNof..",
    "oNWWMMooRSSSSSRooMMWWNo.",
    "oNWWMooRdddddddRooMWWNo.",
    "oNWWMoRdDLLLLLLDdRoMWWNo",
    "oNWWMoRdLbbbbbbbbLoMWWNo",
    "oNWWMoRdLbbbbbbbdLoMWWNo",
    ".oNWMoRddbbbbbbbdoRMWNo.",
    ".oNWWoRRddbbbbddRoRWWNo.",
    "..oNWooRRddddddRooWNo...",
    "..foNooRRRRRRRRooNof....",
    "...fooRRRRRRRRRooff.....",
    "....foRRRRRRRRRof.......",
    ".....foRRRRRRRof........",
    "......fooooooof.........",
    ".......fffffff..........",
]

# Up frame 1: Wings slightly different position, tail sway
_UP_1 = [
    "........................",
    ".....ll........ll.......",
    "....llffoooooofflll.....",
    "...llfoHHoooHHofll......",
    "...llohhooooohhofl......",
    "..lfoNNnoooooonNNofl....",
    "..lfoWWnnoooonnWWNofll..",
    ".lloNWWWnoooonWWWNofl...",
    ".loNWWMWnooooonWMWWNofl.",
    ".foNWWMWooRRRRooWMWWNof.",
    ".oNWWMMooRSSSSSRooMMWWNo",
    ".oNWWMooRdddddddRooMWWNo",
    "oNWWWMoRdDLLLLLLDdRoMWNo",
    "oNWWWMoRdLbbbbbbbbLoMWNo",
    "oNWWWMoRdLbbbbbbbdLoMWNo",
    ".oNWWMoRddbbbbbbbdoRMNo.",
    "..oNWWoRRddbbbbddRoRWNo.",
    "...oNWooRRddddddRooWof..",
    "...foNooRRRRRRRRooNof...",
    "....fooRRRRRRRRRooff....",
    ".....foRRRRRRRRRof......",
    "......foRRRRRRRof.......",
    ".......fooooooof........",
    "........ffffff..........",
]

# ── Left frames ───────────────────────────────────────────────────────
# Left frame 0: Dragon facing left with prominent snout, visible legs
_LEFT_0 = [
    "........................",
    ".........fffgg..........",
    "......ggfooooogg........",
    ".....gfohHIoooff........",
    "....gfohhoookTof........",
    "...gfohhoookTTTog.......",
    "..gfoNNnoooooEEof.......",
    ".gfoNWWnnoooooEef.......",
    ".goNWWMWnooooooof.......",
    "goNWWMMWooRRRRoof.......",
    "fNWWMMMooRSSSRRooc......",
    "oNWWMMooRdddddRRooCc....",
    "oNWWMooRdDLLLDdRRooc....",
    "oNWWMoRdLbbbbbbdRRo.....",
    "oNWWMoRdLbBPPBbdRRRo....",
    "fNWWMoRddbBPPBbddRRo....",
    "fNWWWoRRddbBBbddRRRo....",
    ".oNWWooRRddbbddRRRRo....",
    ".foNWoRRRddddddRRRRo....",
    "..foooRRRRRRRRRRRRRo....",
    "...ffoRRRRRRRRRRRoof....",
    "....ffoRRRRRRRRRooff....",
    ".....lffooooooooffl.....",
    "......llfffffffll.......",
]

# Left frame 1: Wings flap, mouth open with flame
_LEFT_1 = [
    "..........gfgg..........",
    "........gffooogg........",
    ".......gfohIIooffg......",
    "......gfohhoookTofg.....",
    ".....gfohhoookTtTog.....",
    "....gfoNNnoooooEEofg....",
    "...gfoWWWnnoooooEef.....",
    "..gfoNWWMWnooooooof.....",
    "..goNWWMMWooRRRRoof.....",
    ".goNWWMMMooRSSSRRooc....",
    ".fNWWMMooRdddddRRooCc...",
    ".oNWWMooRdDLLLDdRRooc...",
    "oNWWWMoRdLbbbbbbdRRo....",
    "oNWWWMoRdLbBPPBbdRRRo...",
    "oNWWWMoRddbBPPBbddRRo...",
    ".oNWWMoRRddbBBbddRRRo...",
    ".oNWWWooRRddbbddRRRRo...",
    "..oNWWoRRRddddddRRRRo...",
    "..foNooRRRRRRRRRRRRRo...",
    "...ffoRRRRRRRRRRRRoof...",
    "....ffoRRRRRRRRRooff....",
    ".....lffoooooooofl......",
    "......llfffffffll.......",
    ".......llllllll.........",
]

# ── Right frames ──────────────────────────────────────────────────────
# Right frame 0: Dragon facing right, mirror of left
_RIGHT_0 = [
    "........................",
    "..........ggfff.........",
    "........ggoooooofgg.....",
    "........ffooIHhofg......",
    "........foTkooohofg.....",
    ".......goTTTkooohhofg...",
    ".......foEEooooonNNofg..",
    ".......feEooooonnWWNofg.",
    ".......foooooonWMWWNog..",
    ".......fooRRRRooWMMWWNog",
    "......cooRRSSSRooMMMWWNf",
    "...cCoooRRdddddRooMMWWNo",
    "...cooRRdDLLLLDdRooMWWNo",
    ".....oRRdbbbbbbLdRoMWWNo",
    "....oRRRdBPPBbLdRoMWWNo.",
    "....oRRddBPPBbddRoMWWNf.",
    "....oRRRddbBBbddRooWWNf.",
    "....oRRRRddbbddRRooWWNo.",
    "....oRRRRddddddRRRoWNof.",
    "....oRRRRRRRRRRRRRooof..",
    "....fooRRRRRRRRRRRoff...",
    "....ffooRRRRRRRRRoff....",
    ".....llffooooooooffll...",
    ".......llfffffffll......",
]

# Right frame 1: Wings flap, mouth with flame
_RIGHT_1 = [
    "..........ggfg..........",
    "........ggooofg.........",
    "......gffooIIhofg.......",
    ".....gfoTkooohhofg......",
    ".....goTtTkooohhofg.....",
    "....gfoEEooooonNNofg....",
    ".....feEooooonnWWWofg...",
    ".....foooooonWMWWNofog..",
    ".....fooRRRRooWMMWWNog..",
    "....cooRRSSSRooMMMWWNog.",
    "...cCoooRRdddddRooMMWWNf",
    "...cooRRdDLLLLDdRooMWWNo",
    "....oRRdbbbbbbLdRoMWWWNo",
    "...oRRRdBPPBbLdRoMWWWNo.",
    "...oRRddBPPBbddRoMWWWNo.",
    "...oRRRddbBBbddRRoMWWNo.",
    "...oRRRRddbbddRRooWWWNo.",
    "...oRRRRddddddRRRoWWNo..",
    "...oRRRRRRRRRRRRRooNof..",
    "...fooRRRRRRRRRRRRoff...",
    "....ffooRRRRRRRRRoff....",
    "......lfoooooooooffll...",
    ".......llfffffffll......",
    ".........llllllll.......",
]

# ── Build surfaces ────────────────────────────────────────────────────
_cache_p1 = None
_cache_p2 = None


def get_inferno_drake_frames_phase1():
    """Return {direction: [frame0, frame1]} for Inferno Drake phase 1 (red dragon)."""
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


def get_inferno_drake_frames_phase2():
    """Return {direction: [frame0, frame1]} for Inferno Drake phase 2 (wreathed in flame)."""
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
