import pygame
import math
from ..settings import TILE_SIZE


class Entity:
    def __init__(self, x, y, width, height, color):
        self.x = float(x)
        self.y = float(y)
        self.width = width
        self.height = height
        self.color = color
        self.vx = 0.0
        self.vy = 0.0
        self.alive = True
        self.facing = "down"

        # Knockback state
        self.knockback_vx = 0.0
        self.knockback_vy = 0.0
        self.knockback_timer = 0.0
        self.knockback_duration = 0.15

    @property
    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)

    @property
    def center_x(self):
        return self.x + self.width / 2

    @property
    def center_y(self):
        return self.y + self.height / 2

    @property
    def is_moving(self):
        return self.vx != 0.0 or self.vy != 0.0

    def apply_knockback(self, source_x, source_y, strength):
        """Apply knockback away from a source point."""
        dx = self.center_x - source_x
        dy = self.center_y - source_y
        dist = math.sqrt(dx * dx + dy * dy)

        if dist > 0:
            # Normalize and apply strength
            self.knockback_vx = (dx / dist) * strength
            self.knockback_vy = (dy / dist) * strength
        else:
            # If exactly on top, push in a default direction
            self.knockback_vx = strength
            self.knockback_vy = 0

        self.knockback_timer = self.knockback_duration

    def update_knockback(self, dt):
        """Update knockback state - call this in entity update methods."""
        if self.knockback_timer > 0:
            self.knockback_timer -= dt

            if self.knockback_timer <= 0:
                self.knockback_vx = 0
                self.knockback_vy = 0
                self.knockback_timer = 0
            else:
                # Decelerate knockback velocity over time
                # Use exponential decay for smooth deceleration
                decay = 0.85  # Per-frame decay factor
                self.knockback_vx *= decay
                self.knockback_vy *= decay

    def update(self, dt):
        pass

    def draw(self, surface, camera):
        r = self.rect.move(-camera.x, -camera.y)
        pygame.draw.rect(surface, self.color, r)

    def collides_with(self, other):
        return self.alive and other.alive and self.rect.colliderect(other.rect)
