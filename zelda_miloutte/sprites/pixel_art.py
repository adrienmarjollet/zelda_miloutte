"""Utility to convert ASCII grids into pygame surfaces."""

import pygame


def surface_from_grid(grid, palette, scale=1):
    """Convert an ASCII art grid to a pygame Surface.

    Args:
        grid: list of strings, each string is a row of characters.
        palette: dict mapping character -> (r, g, b) or (r, g, b, a).
                 Characters not in palette (or mapped to None) are transparent.
        scale: integer pixel size for each grid cell.

    Returns:
        pygame.Surface with per-pixel alpha.
    """
    h = len(grid)
    w = max(len(row) for row in grid) if h else 0
    surf = pygame.Surface((w * scale, h * scale), pygame.SRCALPHA)
    for ry, row in enumerate(grid):
        for rx, ch in enumerate(row):
            color = palette.get(ch)
            if color is None:
                continue
            surf.fill(color, (rx * scale, ry * scale, scale, scale))
    return surf
