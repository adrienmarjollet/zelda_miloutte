import math
import pygame
from zelda_miloutte.entities.entity import Entity
from zelda_miloutte.settings import PROJECTILE_SIZE, PROJECTILE_SPEED, TILE_SIZE


class Projectile(Entity):
    """Arrow or magic bolt shot by ranged enemies."""

    def __init__(self, x, y, target_x, target_y, damage, sprite=None):
        super().__init__(x, y, PROJECTILE_SIZE, PROJECTILE_SIZE, (255, 100, 100))
        self.damage = damage
        self.lifetime = 3.0  # Disappears after 3 seconds
        self.sprite = sprite

        # Calculate velocity toward target
        dx = target_x - x
        dy = target_y - y
        dist = math.sqrt(dx * dx + dy * dy)
        if dist > 0:
            self.vx = (dx / dist) * PROJECTILE_SPEED
            self.vy = (dy / dist) * PROJECTILE_SPEED
        else:
            self.vx = PROJECTILE_SPEED
            self.vy = 0

        # Calculate angle for sprite rotation (in degrees)
        self.angle = math.degrees(math.atan2(dy, dx))

    def update(self, dt, tilemap):
        """Update projectile position and lifetime."""
        if not self.alive:
            return

        # Update lifetime
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.alive = False
            return

        # Move
        self.x += self.vx * dt
        self.y += self.vy * dt

        # Check wall collision by converting pixel coords to tile coords
        col = int(self.center_x) // TILE_SIZE
        row = int(self.center_y) // TILE_SIZE
        if tilemap.is_solid(col, row):
            self.alive = False

    def draw(self, surface, camera):
        """Draw the projectile sprite."""
        if not self.alive:
            return

        ox, oy = -camera.x, -camera.y
        r = self.rect.move(ox, oy)

        if self.sprite:
            # Rotate the sprite to face movement direction
            rotated = pygame.transform.rotate(self.sprite, -self.angle)
            rx = r.centerx - rotated.get_width() // 2
            ry = r.centery - rotated.get_height() // 2
            surface.blit(rotated, (rx, ry))
        else:
            # Fallback to simple rectangle
            pygame.draw.rect(surface, self.color, r)
