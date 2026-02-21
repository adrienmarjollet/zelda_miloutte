"""Shared fixtures and pygame initialization for tests."""

import os
import pytest

# Set SDL to use dummy video driver before importing pygame
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pygame

pygame.init()
# Create a small hidden display so Surface/Rect operations work
pygame.display.set_mode((1, 1))


@pytest.fixture
def simple_map_data():
    """A 5x5 map: walls on border, grass inside."""
    W = 1  # WALL
    G = 0  # GRASS
    return [
        [W, W, W, W, W],
        [W, G, G, G, W],
        [W, G, G, G, W],
        [W, G, G, G, W],
        [W, W, W, W, W],
    ]


@pytest.fixture
def open_map_data():
    """A 10x10 map: all grass (no walls)."""
    return [[0] * 10 for _ in range(10)]


@pytest.fixture
def corridor_map_data():
    """A map with a corridor that requires pathfinding around walls."""
    W = 1  # WALL
    G = 0  # GRASS
    return [
        [W, W, W, W, W, W, W],
        [W, G, G, W, G, G, W],
        [W, G, G, W, G, G, W],
        [W, G, G, G, G, G, W],
        [W, G, G, W, G, G, W],
        [W, G, G, W, G, G, W],
        [W, W, W, W, W, W, W],
    ]
