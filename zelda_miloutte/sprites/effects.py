"""Visual effect helpers for sprites."""

import pygame


def flash_white(surface):
    """Return a copy of *surface* with all opaque pixels set to white."""
    white = surface.copy()
    white.fill((255, 255, 255, 0), special_flags=pygame.BLEND_RGBA_MAX)
    # Now set RGB to white while preserving alpha
    mask = pygame.mask.from_surface(surface)
    white_surf = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    for x in range(surface.get_width()):
        for y in range(surface.get_height()):
            if mask.get_at((x, y)):
                white_surf.set_at((x, y), (255, 255, 255, surface.get_at((x, y))[3]))
    return white_surf


def tint_surface(surface, tint_color):
    """Return a tinted copy (multiply blend) preserving alpha."""
    tinted = surface.copy()
    overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    overlay.fill((*tint_color[:3], 0))
    tinted.blit(overlay, (0, 0), special_flags=pygame.BLEND_RGB_MULT)
    return tinted


def scale_shrink(surface, progress):
    """Return *surface* scaled down by *progress* (0.0=full, 1.0=gone).

    Returns None if fully shrunk.
    """
    factor = max(0.0, 1.0 - progress)
    w = int(surface.get_width() * factor)
    h = int(surface.get_height() * factor)
    if w <= 0 or h <= 0:
        return None
    return pygame.transform.scale(surface, (w, h))
