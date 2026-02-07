"""Pixel art sprites for the boss (horned demon, two phases)."""

from .pixel_art import surface_from_grid

# ── Phase 1 Palette (purple demon) ───────────────────────────────────
_PAL1 = {
    'o': (15, 5, 25),       # dark outline
    'h': (80, 20, 100),     # horn base dark
    'H': (110, 40, 140),    # horn segments
    'G': (180, 70, 255),    # horn tip glow (bright purple)
    'g': (140, 50, 200),    # horn glow medium
    'b': (120, 40, 160),    # body main purple
    'B': (90, 25, 120),     # body dark/shadow
    'l': (150, 70, 190),    # body highlight (lighter purple)
    'L': (180, 100, 220),   # body brightest highlight
    's': (100, 30, 130),    # shoulder/muscle shadow
    'S': (130, 50, 170),    # shoulder highlight
    'e': (255, 80, 40),     # eyes bright core (glowing red-orange)
    'E': (255, 120, 80),    # eye outer glow
    'r': (180, 30, 20),     # eye ridge/brow
    'm': (40, 10, 50),      # mouth interior deep
    'M': (220, 200, 190),   # fangs (off-white)
    't': (190, 180, 170),   # teeth tips
    'a': (140, 60, 180),    # arm muscle light
    'A': (110, 40, 145),    # arm muscle dark
    'd': (100, 35, 130),    # arm shadow/claw base
    'D': (70, 20, 95),      # claw tips (dark sharp)
    'w': (70, 30, 90),      # wing membrane dark
    'W': (100, 50, 120),    # wing bone/edge
    'v': (50, 20, 70),      # wing shadow deep
    'V': (120, 60, 140),    # wing highlight
    'c': (255, 150, 255),   # chest rune core (bright glowing magenta)
    'C': (200, 100, 230),   # chest rune outer
    'k': (170, 80, 210),    # chest rune accent
    'p': (80, 30, 110),     # pants/legs main
    'P': (100, 40, 130),    # legs highlight
    'f': (50, 15, 70),      # feet/claws
    'F': (30, 8, 45),       # feet claw tips (darkest)
    'i': (60, 20, 85),      # tail base
    'I': (45, 12, 65),      # tail tip
    '.': None,
}

# ── Phase 2 Palette (crimson demon) ──────────────────────────────────
_PAL2 = {
    'o': (25, 5, 5),        # dark outline
    'h': (120, 20, 20),     # horn base dark
    'H': (180, 40, 30),     # horn segments
    'G': (255, 180, 100),   # horn tip glow (bright orange-yellow)
    'g': (240, 120, 60),    # horn glow medium
    'b': (200, 50, 50),     # body main crimson
    'B': (150, 30, 30),     # body dark/shadow
    'l': (240, 90, 80),     # body highlight (lighter crimson)
    'L': (255, 130, 110),   # body brightest highlight
    's': (160, 35, 35),     # shoulder/muscle shadow
    'S': (220, 70, 60),     # shoulder highlight
    'e': (255, 255, 80),    # eyes bright core (glowing yellow)
    'E': (255, 240, 140),   # eye outer glow
    'r': (140, 20, 10),     # eye ridge/brow
    'm': (80, 15, 15),      # mouth interior deep
    'M': (220, 200, 190),   # fangs (off-white)
    't': (190, 180, 170),   # teeth tips
    'a': (220, 80, 70),     # arm muscle light
    'A': (180, 50, 45),     # arm muscle dark
    'd': (160, 40, 35),     # arm shadow/claw base
    'D': (110, 25, 20),     # claw tips (dark sharp)
    'w': (130, 30, 25),     # wing membrane dark
    'W': (170, 50, 45),     # wing bone/edge
    'v': (100, 20, 18),     # wing shadow deep
    'V': (200, 70, 60),     # wing highlight
    'c': (255, 255, 150),   # chest rune core (bright glowing yellow)
    'C': (255, 220, 100),   # chest rune outer
    'k': (240, 180, 70),    # chest rune accent
    'p': (120, 25, 25),     # pants/legs main
    'P': (160, 40, 35),     # legs highlight
    'f': (80, 15, 15),      # feet/claws
    'F': (50, 10, 10),      # feet claw tips (darkest)
    'i': (90, 18, 18),      # tail base
    'I': (65, 12, 12),      # tail tip
    '.': None,
}

# ── Down frames (20x16) ──────────────────────────────────────────────
_DOWN_0 = [
    "..oGgHho....ohhGgo..",  # horns with glowing tips, curved
    ".oGgHHhho..ohhHHgGo.",
    ".ogHHhhho..ohhhhHgo.",
    "..ohhhhhoooohhhho...",
    "oorrEeEoooooEeErroo.",  # fierce brow + glowing eyes
    "oBlllblbbbbblblllBo.",
    "oBlbMmMbbbbMmMblBBo.",  # snarling mouth with fangs
    "oBBbmmtMbbMtmmblBBo.",
    "VWwSsslllllssSSwWV..",  # massive wings + muscular shoulders
    "VWwBScCckcCcSBwWV...",  # elaborate chest rune
    ".oDAadbbbbdaADoo....",  # clawed arms extending
    "..oDdaabbaaDdo......",
    "..oopPppppPpo.......",  # muscular legs
    "...opPoooPpo........",
    "...oFFo.oFFo........",  # clawed feet
    "....oIIIo...........",  # tail
]

_DOWN_1 = [
    "..oGgHho....ohhGgo..",
    ".oGgHHhho..ohhHHgGo.",
    ".ogHHhhho..ohhhhHgo.",
    "..ohhhhhoooohhhho...",
    "oorEeEroooorEeErroo.",  # eyes slightly offset for animation
    "oBllblbbbbbblbllBBo.",
    "oBlbMmMbbbbMmMblBBo.",
    "oBBbmmtMbbMtmmblBBo.",
    ".VWwSslllllsSSwWV...",  # wings slightly raised
    ".VWwBScCckcCSBwWV...",
    "..oDAadbbbbdaADo....",
    "...oDdaabbaaDdo.....",
    "...oopPppppPpo......",
    "....opPoooPpo.......",
    "....oFFo.oFFo.......",
    ".....oIIIo..........",
]

# ── Up frames ─────────────────────────────────────────────────────────
_UP_0 = [
    "..oGgHho....ohhGgo..",
    ".oGgHHhho..ohhHHgGo.",
    ".ogHHhhho..ohhhhHgo.",
    "..ohhhhhoooohhhho...",
    "ooBBBBBBBBBBBBBBBoo.",  # back of head
    "oBlSsslllllsSsSlBo..",  # muscular back/shoulders
    "oBBslbbbbbbbblsBBo..",
    "oBlblbbbbbbbblblBo..",
    "VWwBbbbbbbbbbbBwWV..",  # wings spread wide
    "VWwBBlbbbbbblBBwWV..",
    ".oDAaabbbbbaaDDoo...",  # arms reaching up
    "..oDdaabbaaDdo......",
    "..oopPppppPpo.......",
    "...opPoooPpo........",
    "...oFFo.oFFo........",
    "....oIIIo...........",
]

_UP_1 = [
    "..oGgHho....ohhGgo..",
    ".oGgHHhho..ohhHHgGo.",
    ".ogHHhhho..ohhhhHgo.",
    "..ohhhhhoooohhhho...",
    "ooBBBBBBBBBBBBBBBoo.",
    "oBSlsSllllllsSSlBBo.",
    "oBBslbbbbbbbblsBBo..",
    "oBlblbbbbbbbblblBo..",
    ".VWwBbbbbbbbbbBwWV..",  # wings slightly different
    ".VWwBBlbbbblBBwWV...",
    "..oDAaabbbbbaaDDo...",
    "...oDdaabbaaDdo.....",
    "...oopPppppPpo......",
    "....opPoooPpo.......",
    "....oFFo.oFFo.......",
    ".....oIIIo..........",
]

# ── Left frames ───────────────────────────────────────────────────────
_LEFT_0 = [
    ".oGgHho.............",
    "oGgHHhho............",
    "ogHHhhhho...........",
    ".ohhhhho............",
    "oorEeErooo..........",  # fierce eye visible
    "oBlllblbBBo.........",
    "oBlbMmMbBBo.........",  # side view fangs
    "oBBbmmtblBBo........",
    "VWwSsslbbbBBwV......",  # wing + muscular arm
    "VWwBScCckbBBwV......",  # chest rune visible
    ".oDAadbbbbbaoo......",  # extended clawed arm
    "..oDdaabbbaBo.......",
    "..oopPppppPpo.......",
    "...opPoooPpo........",
    "...oFFo.oFFo........",
    "....oIIIo...........",
]

_LEFT_1 = [
    ".oGgHho.............",
    "oGgHHhho............",
    "ogHHhhhho...........",
    ".ohhhhho............",
    "oorEeEroo...........",
    "oBllblbBBo..........",
    "oBlbMmMbBBo.........",
    "oBBbmmtblBBo........",
    "VWwSslbbbBBwV.......",  # wing raised slightly
    "VWwBScCckbBBwV......",
    "..oDAadbbbbaoo......",  # arm reaching forward
    "...oDdaabbbaBo......",
    "...oopPppppPpo......",
    "....opPoooPpo.......",
    "....oFFo.oFFo.......",
    ".....oIIIo..........",
]

# ── Right frames ──────────────────────────────────────────────────────
_RIGHT_0 = [
    ".............ohhGgo.",
    "............ohhHHgGo",
    "...........ohhhhHgo.",
    "............ohhhhho.",
    "..........ooorEeEroo",  # fierce eye visible
    ".........oBBlblllBo.",
    ".........oBBbMmMblBo",  # side view fangs
    "........oBBlbmmtbBBo",
    "......VwBBbbbslsSWV.",  # wing + muscular arm
    "......VwBBbkcCcSBwWV",  # chest rune visible
    "......ooabbbbdaADo..",  # extended clawed arm
    ".......oBabbbaadDo..",
    ".......opPppppPpoo..",
    "........opPoooPpo...",
    "........oFFo.oFFo...",
    "...........oIIIo....",
]

_RIGHT_1 = [
    ".............ohhGgo.",
    "............ohhHHgGo",
    "...........ohhhhHgo.",
    "............ohhhhho.",
    "...........oorEeEroo",
    "..........oBblblBBo.",
    ".........oBBbMmMblBo",
    "........oBBlbmmtbBBo",
    ".......VwBBbbblsSwWV",  # wing raised slightly
    "......VwBBbkcCcSBwWV",
    "......ooabbbdaADo...",  # arm reaching forward
    "......oBabbbaaoDo...",
    "......opPppppPpoo...",
    ".......opPoooPpo....",
    ".......oFFo.oFFo....",
    "........oIIIo.......",
]

# ── Build surfaces ────────────────────────────────────────────────────
_cache_p1 = None
_cache_p2 = None


def get_boss_frames_phase1():
    """Return {direction: [frame0, frame1]} for boss phase 1 (purple)."""
    global _cache_p1
    if _cache_p1 is not None:
        return _cache_p1

    _cache_p1 = {
        "down":  [surface_from_grid(g, _PAL1, 3) for g in (_DOWN_0, _DOWN_1)],
        "up":    [surface_from_grid(g, _PAL1, 3) for g in (_UP_0, _UP_1)],
        "left":  [surface_from_grid(g, _PAL1, 3) for g in (_LEFT_0, _LEFT_1)],
        "right": [surface_from_grid(g, _PAL1, 3) for g in (_RIGHT_0, _RIGHT_1)],
    }
    return _cache_p1


def get_boss_frames_phase2():
    """Return {direction: [frame0, frame1]} for boss phase 2 (crimson)."""
    global _cache_p2
    if _cache_p2 is not None:
        return _cache_p2

    _cache_p2 = {
        "down":  [surface_from_grid(g, _PAL2, 3) for g in (_DOWN_0, _DOWN_1)],
        "up":    [surface_from_grid(g, _PAL2, 3) for g in (_UP_0, _UP_1)],
        "left":  [surface_from_grid(g, _PAL2, 3) for g in (_LEFT_0, _LEFT_1)],
        "right": [surface_from_grid(g, _PAL2, 3) for g in (_RIGHT_0, _RIGHT_1)],
    }
    return _cache_p2


# Boss 2 Phase 1 Palette (ice blue/cyan demon)
_BOSS2_PAL1 = {
    'o': (10, 20, 35),      # dark outline
    'h': (60, 120, 160),    # horn base dark
    'H': (100, 170, 210),   # horn segments
    'G': (200, 255, 255),   # horn tip glow (bright cyan-white)
    'g': (150, 220, 255),   # horn glow medium
    'b': (90, 160, 200),    # body main cyan
    'B': (60, 130, 170),    # body dark/shadow
    'l': (130, 200, 240),   # body highlight (lighter cyan)
    'L': (170, 230, 255),   # body brightest highlight
    's': (70, 140, 180),    # shoulder/muscle shadow
    'S': (110, 180, 220),   # shoulder highlight
    'e': (200, 250, 255),   # eyes bright core (glowing cyan-white)
    'E': (230, 255, 255),   # eye outer glow
    'r': (40, 90, 130),     # eye ridge/brow
    'm': (30, 60, 90),      # mouth interior deep
    'M': (220, 230, 240),   # fangs (icy white)
    't': (200, 215, 230),   # teeth tips
    'a': (120, 190, 230),   # arm muscle light
    'A': (90, 160, 200),    # arm muscle dark
    'd': (70, 140, 180),    # arm shadow/claw base
    'D': (50, 110, 150),    # claw tips (dark sharp)
    'w': (50, 100, 140),    # wing membrane dark
    'W': (80, 140, 180),    # wing bone/edge
    'v': (35, 70, 110),     # wing shadow deep
    'V': (100, 160, 200),   # wing highlight
    'c': (180, 240, 255),   # chest rune core (bright cyan glow)
    'C': (140, 210, 240),   # chest rune outer
    'k': (110, 190, 230),   # chest rune accent
    'p': (60, 110, 150),    # pants/legs main
    'P': (80, 140, 180),    # legs highlight
    'f': (40, 70, 100),     # feet/claws
    'F': (25, 45, 65),      # feet claw tips (darkest)
    'i': (50, 90, 130),     # tail base
    'I': (35, 65, 100),     # tail tip
    '.': None,
}

# Boss 2 Phase 2 Palette (dark blue/navy demon)
_BOSS2_PAL2 = {
    'o': (5, 10, 20),       # dark outline
    'h': (30, 50, 100),     # horn base dark
    'H': (50, 80, 140),     # horn segments
    'G': (180, 200, 255),   # horn tip glow (bright blue-white)
    'g': (120, 150, 230),   # horn glow medium
    'b': (40, 70, 130),     # body main dark blue
    'B': (25, 45, 90),      # body very dark blue
    'l': (60, 100, 170),    # body highlight (lighter navy)
    'L': (80, 130, 200),    # body brightest highlight
    's': (30, 55, 105),     # shoulder/muscle shadow
    'S': (50, 85, 150),     # shoulder highlight
    'e': (255, 250, 120),   # eyes bright core (glowing yellow)
    'E': (255, 255, 180),   # eye outer glow
    'r': (20, 35, 70),      # eye ridge/brow
    'm': (15, 25, 50),      # mouth interior deep
    'M': (200, 190, 180),   # fangs (grayish white)
    't': (180, 170, 160),   # teeth tips
    'a': (60, 100, 160),    # arm muscle light
    'A': (45, 75, 130),     # arm muscle dark
    'd': (35, 60, 110),     # arm shadow/claw base
    'D': (25, 45, 85),      # claw tips (dark sharp)
    'w': (30, 50, 90),      # wing membrane dark
    'W': (45, 75, 120),     # wing bone/edge
    'v': (20, 35, 65),      # wing shadow deep
    'V': (55, 90, 140),     # wing highlight
    'c': (120, 180, 255),   # chest rune core (bright blue glow)
    'C': (80, 140, 220),    # chest rune outer
    'k': (60, 110, 190),    # chest rune accent
    'p': (30, 50, 100),     # pants/legs main
    'P': (45, 70, 130),     # legs highlight
    'f': (20, 35, 70),      # feet/claws
    'F': (12, 20, 45),      # feet claw tips (darkest)
    'i': (25, 40, 80),      # tail base
    'I': (18, 28, 60),      # tail tip
    '.': None,
}

_cache_boss2_p1 = None
_cache_boss2_p2 = None


def get_boss2_frames_phase1():
    """Return {direction: [frame0, frame1]} for boss 2 phase 1 (ice blue/cyan)."""
    global _cache_boss2_p1
    if _cache_boss2_p1 is not None:
        return _cache_boss2_p1

    _cache_boss2_p1 = {
        "down":  [surface_from_grid(g, _BOSS2_PAL1, 3) for g in (_DOWN_0, _DOWN_1)],
        "up":    [surface_from_grid(g, _BOSS2_PAL1, 3) for g in (_UP_0, _UP_1)],
        "left":  [surface_from_grid(g, _BOSS2_PAL1, 3) for g in (_LEFT_0, _LEFT_1)],
        "right": [surface_from_grid(g, _BOSS2_PAL1, 3) for g in (_RIGHT_0, _RIGHT_1)],
    }
    return _cache_boss2_p1


def get_boss2_frames_phase2():
    """Return {direction: [frame0, frame1]} for boss 2 phase 2 (dark blue/navy)."""
    global _cache_boss2_p2
    if _cache_boss2_p2 is not None:
        return _cache_boss2_p2

    _cache_boss2_p2 = {
        "down":  [surface_from_grid(g, _BOSS2_PAL2, 3) for g in (_DOWN_0, _DOWN_1)],
        "up":    [surface_from_grid(g, _BOSS2_PAL2, 3) for g in (_UP_0, _UP_1)],
        "left":  [surface_from_grid(g, _BOSS2_PAL2, 3) for g in (_LEFT_0, _LEFT_1)],
        "right": [surface_from_grid(g, _BOSS2_PAL2, 3) for g in (_RIGHT_0, _RIGHT_1)],
    }
    return _cache_boss2_p2
