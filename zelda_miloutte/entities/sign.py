"""Sign entity that displays text when interacted with."""

import pygame
from .entity import Entity
from ..sprites.sign_sprites import get_sign_sprite
from ..settings import BROWN


class Sign(Entity):
    """A sign post that displays a message when the player interacts with it."""

    def __init__(self, x, y, text):
        """Initialize a sign at the given position with text to display.

        Args:
            x, y: Position in pixels
            text: The message to display when interacted with
        """
        # Signs are 24x24 but with a smaller footprint for collision (16x16 bottom part)
        super().__init__(x + 4, y + 8, 16, 16, BROWN)
        self.text = text
        self.sprite = get_sign_sprite()
        # Store the visual position (different from collision rect)
        self.visual_x = x
        self.visual_y = y

    def update(self, dt):
        """Signs are static and don't update."""
        pass

    def draw(self, surface, camera):
        """Draw the sign sprite."""
        ox, oy = -camera.x, -camera.y
        surface.blit(self.sprite, (self.visual_x + ox, self.visual_y + oy))
