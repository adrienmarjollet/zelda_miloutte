"""Treasure chest entity that can be opened to get items."""

import random
import pygame
from zelda_miloutte.entities.entity import Entity
from zelda_miloutte.settings import CHEST_SIZE, BROWN
from zelda_miloutte.sprites.chest_sprites import get_chest_closed, get_chest_open
from zelda_miloutte.sounds import get_sound_manager


class Chest(Entity):
    """A treasure chest that can be opened with the sword to get items."""

    def __init__(self, x, y, contents, gold_range=None):
        """
        Create a chest.

        Args:
            x: X position in pixels
            y: Y position in pixels
            contents: Item type string ("heart", "key", or "gold")
            gold_range: Optional (min, max) for gold amount. Defaults to (10, 50).
        """
        super().__init__(x, y, CHEST_SIZE, CHEST_SIZE, BROWN)
        self.contents = contents
        self.gold_range = gold_range or (10, 50)
        self.gold_amount = 0  # Set on open if contents == "gold"
        self.opened = False
        self._closed_sprite = get_chest_closed()
        self._open_sprite = get_chest_open()

    def open(self, player):
        """
        Open the chest and return the contained item.

        Args:
            player: The player entity

        Returns:
            Item type string to spawn, or None if already opened.
            For "gold" contents, the gold is added directly to the player
            and "gold" is returned as the type string.
        """
        if self.opened:
            return None

        self.opened = True
        get_sound_manager().play_chest_open()

        if self.contents == "gold":
            self.gold_amount = random.randint(self.gold_range[0], self.gold_range[1])
            player.gold += self.gold_amount
            get_sound_manager().play_gold_pickup()

        return self.contents

    def draw(self, surface, camera):
        """Draw the chest (closed or open)."""
        ox, oy = -camera.x, -camera.y
        r = self.rect.move(ox, oy)

        # Choose sprite based on opened state
        sprite = self._open_sprite if self.opened else self._closed_sprite
        surface.blit(sprite, (r.x, r.y))
