"""Campfire rest spot entity -- interact to skip to dawn and restore HP."""

import math
import random
import pygame
from zelda_miloutte.entities.entity import Entity
from zelda_miloutte.sprites.pixel_art import surface_from_grid


# Campfire size in pixels
CAMPFIRE_SIZE = 24

_PAL = {
    'o': (60, 30, 10),       # dark wood outline
    'w': (110, 60, 20),      # wood
    'W': (90, 45, 15),       # wood shadow
    'f': (255, 160, 40),     # flame orange
    'F': (255, 220, 80),     # flame bright yellow
    'r': (220, 60, 20),      # flame red tip
    'R': (180, 40, 10),      # ember
    '.': None,
}

_CAMPFIRE_FRAME_0 = [
    "......FF......",
    ".....FfFf.....",
    "....FffrfF....",
    "...FffrrfFF...",
    "...frffrffF...",
    "..FffrRrffF...",
    "..fffRRRfff...",
    "...fRRRRf....",
    "..oWWwwWWo....",
    "..oWwwwwWo....",
    ".oowWWWwwoo...",
    ".oooooooooo...",
]

_CAMPFIRE_FRAME_1 = [
    ".....fF.......",
    "....FffF......",
    "...ffFrfF.....",
    "...FfrrrFF....",
    "..FfffrrfFf...",
    "..fffrRrfff...",
    "..fffRRRfff...",
    "...fRRRRf....",
    "..oWWwwWWo....",
    "..oWwwwwWo....",
    ".oowWWWwwoo...",
    ".oooooooooo...",
]

_cache = {}


def _get_campfire_frames():
    if "frames" not in _cache:
        _cache["frames"] = [
            surface_from_grid(_CAMPFIRE_FRAME_0, _PAL, 2),
            surface_from_grid(_CAMPFIRE_FRAME_1, _PAL, 2),
        ]
    return _cache["frames"]


class Campfire(Entity):
    """A rest spot. Interact to skip to dawn and restore HP."""

    def __init__(self, x, y):
        super().__init__(x, y, CAMPFIRE_SIZE, CAMPFIRE_SIZE, (255, 160, 40))
        self._frames = _get_campfire_frames()
        self._frame_index = 0
        self._anim_timer = 0.0
        self._anim_speed = 0.25  # seconds per frame
        self._glow_timer = 0.0

    def update(self, dt):
        self._anim_timer += dt
        if self._anim_timer >= self._anim_speed:
            self._anim_timer -= self._anim_speed
            self._frame_index = (self._frame_index + 1) % len(self._frames)
        self._glow_timer += dt

    def draw(self, surface, camera):
        if not self.alive:
            return
        ox, oy = -camera.x, -camera.y
        r = self.rect.move(ox, oy)

        # Draw warm glow circle behind the campfire
        glow_alpha = int(25 + 10 * math.sin(self._glow_timer * 3.0))
        glow_radius = 50 + int(5 * math.sin(self._glow_timer * 2.0))
        glow_surf = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(
            glow_surf, (255, 150, 50, glow_alpha),
            (glow_radius, glow_radius), glow_radius
        )
        surface.blit(
            glow_surf,
            (r.centerx - glow_radius, r.centery - glow_radius)
        )

        # Draw campfire sprite
        frame = self._frames[self._frame_index]
        fx = r.centerx - frame.get_width() // 2
        fy = r.centery - frame.get_height() // 2
        surface.blit(frame, (fx, fy))
