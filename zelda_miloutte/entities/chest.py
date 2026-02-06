"""Treasure chest entity that can be opened to get items."""

import pygame
from zelda_miloutte.entities.entity import Entity
from zelda_miloutte.settings import CHEST_SIZE, BROWN
from zelda_miloutte.sprites.chest_sprites import get_chest_closed, get_chest_open
from zelda_miloutte.sounds import get_sound_manager


class Chest(Entity):
    """A treasure chest that can be opened with the sword to get items."""

    def __init__(self, x, y, contents):
        """
        Create a chest.

        Args:
            x: X position in pixels
            y: Y position in pixels
            contents: Item type string ("heart" or "key")
        """
        super().__init__(x, y, CHEST_SIZE, CHEST_SIZE, BROWN)
        self.contents = contents
        self.opened = False
        self._closed_sprite = get_chest_closed()
        self._open_sprite = get_chest_open()

    def open(self, player):
        """
        Open the chest and return the contained item.

        Args:
            player: The player entity (not currently used but for future expansion)

        Returns:
            Item type string to spawn, or None if already opened
        """
        if self.opened:
            return None

        self.opened = True
        get_sound_manager().play_chest_open()
        return self.contents

    def draw(self, surface, camera):
        """Draw the chest (closed or open)."""
        ox, oy = -camera.x, -camera.y
        r = self.rect.move(ox, oy)

        # Choose sprite based on opened state
        sprite = self._open_sprite if self.opened else self._closed_sprite
        surface.blit(sprite, (r.x, r.y))
