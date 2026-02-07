"""Pixel art sprites for Fire Imp (fast melee enemy with fire trail)."""

from .pixel_art import surface_from_grid

# ── Palette ───────────────────────────────────────────────────────
_PAL = {
    'o': (20, 20, 20),        # dark outline
    'k': (40, 25, 25),        # charcoal/ash (dark body detail)
    'K': (60, 35, 30),        # lighter ash
    'r': (220, 80, 30),       # red body base
    'R': (180, 50, 20),       # darker red
    'd': (140, 30, 15),       # deep crimson (darkest red)
    'l': (255, 180, 60),      # lava glow (bright orange)
    'L': (255, 220, 100),     # lava highlight (yellow-orange)
    'w': (255, 255, 255),     # white-hot (eyes, flame core)
    'y': (255, 240, 150),     # bright yellow flame
    'Y': (255, 200, 80),      # yellow-orange flame
    'f': (255, 160, 50),      # orange flame
    'F': (255, 100, 30),      # deep orange flame
    'h': (200, 50, 20),       # hot red (flame edge)
    't': (120, 40, 20),       # dark red (flame trail end)
    'e': (10, 10, 10),        # eye pupils
    '.': None,
}

# ── Down frames ───────────────────────────────────────────────────
_DOWN_0 = [
    "......oo......",
    ".....oKKo.....",
    "....oKddKo....",
    "...odRRRRdo...",
    "..odRwewRdo...",
    "..odReeERdo...",
    ".odRRoooRRdo..",
    ".odRlLLlRdo...",
    ".odRRRRRRdo...",
    "..odRdRdRo....",
    "...oKdRdo.....",
    "....oooo......",
    "...oYfFho.....",
    "....oYto......",
]

_DOWN_1 = [
    "......oo......",
    ".....oKKo.....",
    "....oKddKo....",
    "...odRRRRdo...",
    "..odRwewRdo...",
    "..odReeERdo...",
    ".odRRoooRRdo..",
    ".odRlLLlRdo...",
    ".odRRRRRRdo...",
    "..odRdRdRo....",
    "....odRdo.....",
    "...ooKKoo.....",
    "..oyfFhto.....",
    "...oyto.......",
]

# ── Up frames ─────────────────────────────────────────────────────
_UP_0 = [
    "....oYto......",
    "...oYfFho.....",
    "....oooo......",
    "...oKdRdo.....",
    "..odRdRdRo....",
    ".odRRRRRRdo...",
    ".odRlLLlRdo...",
    ".odRRoooRRdo..",
    "..odReeERdo...",
    "..odRwewRdo...",
    "...odRRRRdo...",
    "....oKddKo....",
    ".....oKKo.....",
    "......oo......",
]

_UP_1 = [
    "...oyto.......",
    "..oyfFhto.....",
    "...ooKKoo.....",
    "....odRdo.....",
    "..odRdRdRo....",
    ".odRRRRRRdo...",
    ".odRlLLlRdo...",
    ".odRRoooRRdo..",
    "..odReeERdo...",
    "..odRwewRdo...",
    "...odRRRRdo...",
    "....oKddKo....",
    ".....oKKo.....",
    "......oo......",
]

# ── Left frames ───────────────────────────────────────────────────
_LEFT_0 = [
    "....oo........",
    "...oKKoo......",
    "..oKddKo......",
    ".odRRwRdo.....",
    ".odReRRdo.....",
    "odRRoRRRdo....",
    "odRlLoRRdoo...",
    "odRLlRRRdFo...",
    ".odRRRRRdho...",
    "..odRdRdoto...",
    "...ooKKoo.....",
    "....ooo.......",
    "...oyfFht.....",
    "....oYto......",
]

_LEFT_1 = [
    "....oo........",
    "...oKKoo......",
    "..oKddKo......",
    ".odRRwRdo.....",
    ".odReRRdo.....",
    "odRRoRRRdo....",
    "odRlLoRRdoo...",
    "odRLlRRRdFo...",
    ".odRRRRRdho...",
    "..odRdRdoto...",
    "....ooKoo.....",
    ".....oo.......",
    "...oYfFt......",
    "....oyt.......",
]

# ── Right frames ──────────────────────────────────────────────────
_RIGHT_0 = [
    "........oo....",
    "......ooKKo...",
    "......oKddKo..",
    ".....odRwRRdo.",
    ".....odRReRdo.",
    "....odRRRoRRdo",
    "...oodRRoLlRdo",
    "...oFdRRRlLRdo",
    "...ohdRRRRRdo.",
    "...otodRdRdo..",
    ".....ooKKoo...",
    ".......ooo....",
    ".....thFfyo...",
    "......otYo....",
]

_RIGHT_1 = [
    "........oo....",
    "......ooKKo...",
    "......oKddKo..",
    ".....odRwRRdo.",
    ".....odRReRdo.",
    "....odRRRoRRdo",
    "...oodRRoLlRdo",
    "...oFdRRRlLRdo",
    "...ohdRRRRRdo.",
    "...otodRdRdo..",
    ".....ooKoo....",
    ".......oo.....",
    "......tFfYo...",
    ".......tyo....",
]

# ── Build surfaces ────────────────────────────────────────────────
_frames_cache = None


def get_fire_imp_frames():
    """Return dict of {direction: [frame0, frame1]} for the fire imp."""
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
