"""Procedural pixel art sprites for ability icons and effects."""

import pygame
import math
from zelda_miloutte.sprites.pixel_art import surface_from_grid


# ── Palette for ability icons ────────────────────────────────────────
_ICON_PAL = {
    'o': (20, 15, 10),       # outline
    '.': None,                # transparent
    # Spin Attack colors
    'S': (200, 220, 240),     # blade silver
    's': (160, 175, 200),     # blade shadow
    'g': (180, 150, 40),      # gold guard
    'w': (255, 255, 220),     # white flash
    # Dash colors
    'B': (60, 160, 255),      # bright blue
    'b': (30, 100, 200),      # dark blue
    'c': (120, 200, 255),     # cyan highlight
    # Fire Blast colors
    'R': (255, 80, 20),       # bright red-orange
    'r': (200, 50, 10),       # dark red
    'Y': (255, 200, 50),      # yellow flame
    'y': (255, 150, 30),      # orange flame
    # Shield Barrier colors
    'G': (80, 220, 120),      # green glow
    'e': (40, 180, 80),       # dark green
    'L': (160, 255, 180),     # light green
    # Mana colors
    'M': (60, 120, 255),      # mana blue
    'm': (30, 80, 200),       # dark mana blue
}

# ── Spin Attack icon (16x16 grid) ───────────────────────────────────
_SPIN_ICON = [
    "....oooo....",
    "..oowSSoo...",
    ".oowSSSsoo..",
    "ooSSSSssoo..",
    "oSSSgssooo..",
    "oSSggsoo....",
    "osSgso......",
    "oossoo..oo..",
    ".oooo..owoo.",
    "......owSSo.",
    "....oosSSSo.",
    "..ooossSSoo.",
    ".ooSSSSSoo..",
    ".oowSSSoo...",
    "..oowSoo....",
    "...oooo.....",
]

# ── Dash icon (16x16 grid) ──────────────────────────────────────────
_DASH_ICON = [
    "............",
    "..oo........",
    ".oBBoo......",
    ".oBBBBoo....",
    "ooBBBBBBoo..",
    "..ooBBBBBBo.",
    "....oocBBBo.",
    "......oocBo.",
    ".....oocBo..",
    "...oocBBo...",
    "..oBBBBoo...",
    ".oBBBBoo....",
    ".oBBoo......",
    "..oo........",
    "............",
    "............",
]

# ── Fire Blast icon (16x16 grid) ────────────────────────────────────
_FIRE_ICON = [
    "............",
    "......oo....",
    ".....oYo....",
    "....oYYoo...",
    "...oYYRoo...",
    "..ooYRRoo...",
    ".oyYYRRoo...",
    ".oYYRRRoo...",
    "oYYYRRRoo...",
    "oYYRRRroo...",
    "oYRRRrroo...",
    ".oRRrroo....",
    ".ooRrroo....",
    "..oorroo....",
    "...oooo.....",
    "............",
]

# ── Shield Barrier icon (16x16 grid) ────────────────────────────────
_SHIELD_ICON = [
    "............",
    "...oooooo...",
    "..oLLLLLLo..",
    ".oLGGGGGGo..",
    ".oGGeeGGGo..",
    "oGGeeeeeGo..",
    "oGeeeeeeGo..",
    "oGeeeeeeGo..",
    "oGeeeeeeGo..",
    "oGGeeeeeGo..",
    ".oGGeeGGo...",
    ".oGGGGGGo...",
    "..oGGGGo....",
    "...oGGo.....",
    "....oo......",
    "............",
]

# ── Caches ───────────────────────────────────────────────────────────
_icon_cache = {}
_effect_cache = {}


def get_ability_icon(ability_name):
    """Return a 24x24 (or similar) surface for the ability HUD icon."""
    if ability_name in _icon_cache:
        return _icon_cache[ability_name]

    grids = {
        "spin_attack": _SPIN_ICON,
        "dash": _DASH_ICON,
        "fire_blast": _FIRE_ICON,
        "shield_barrier": _SHIELD_ICON,
    }

    grid = grids.get(ability_name)
    if grid is None:
        # Fallback: small colored square
        surf = pygame.Surface((24, 24), pygame.SRCALPHA)
        surf.fill((100, 100, 100, 180))
        _icon_cache[ability_name] = surf
        return surf

    surf = surface_from_grid(grid, _ICON_PAL, 2)
    _icon_cache[ability_name] = surf
    return surf


def create_spin_arc_surface():
    """Create a spin arc effect surface (circular slash trail)."""
    if "spin_arc" in _effect_cache:
        return _effect_cache["spin_arc"]

    size = 96
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    center = size // 2
    # Draw a bright arc
    for angle_deg in range(0, 360, 5):
        angle = math.radians(angle_deg)
        for r in range(30, 44):
            x = int(center + math.cos(angle) * r)
            y = int(center + math.sin(angle) * r)
            if 0 <= x < size and 0 <= y < size:
                alpha = max(0, 220 - abs(r - 37) * 30)
                surf.set_at((x, y), (220, 230, 255, alpha))

    _effect_cache["spin_arc"] = surf
    return surf


def create_dash_afterimage(player_frame, alpha=100):
    """Create a semi-transparent blue-tinted copy of a player frame for dash trail."""
    if player_frame is None:
        return None
    copy = player_frame.copy()
    # Tint blue
    tint = pygame.Surface(copy.get_size(), pygame.SRCALPHA)
    tint.fill((60, 140, 255, alpha))
    copy.blit(tint, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    return copy


def create_fireball_surface():
    """Create a fireball projectile surface."""
    if "fireball" in _effect_cache:
        return _effect_cache["fireball"]

    grid = [
        "...oo...",
        "..oYYo..",
        ".oYYRRo.",
        "oYYRRRo.",
        "oYRRrro.",
        ".oRrroo.",
        "..oroo..",
        "...oo...",
    ]
    surf = surface_from_grid(grid, _ICON_PAL, 2)
    _effect_cache["fireball"] = surf
    return surf


def create_shield_bubble_surface():
    """Create a shield bubble overlay surface."""
    if "shield_bubble" in _effect_cache:
        return _effect_cache["shield_bubble"]

    size = 48
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    center = size // 2
    # Draw concentric circles with decreasing alpha
    for r in range(center, center - 6, -1):
        alpha = max(0, 60 - (center - r) * 12)
        pygame.draw.circle(surf, (80, 220, 120, alpha), (center, center), r, 1)
    # Bright inner highlight
    pygame.draw.circle(surf, (160, 255, 180, 40), (center, center), center - 6)

    _effect_cache["shield_bubble"] = surf
    return surf
