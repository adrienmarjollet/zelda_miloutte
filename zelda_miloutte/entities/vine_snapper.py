import math
import random
import pygame
from zelda_miloutte.entities.entity import Entity
from zelda_miloutte.entities.projectile import Projectile
from zelda_miloutte.settings import (
    VINE_SNAPPER_SIZE, VINE_SNAPPER_HP, VINE_SNAPPER_DAMAGE,
    VINE_SNAPPER_SHOOT_RANGE, VINE_SNAPPER_SHOOT_COOLDOWN,
    VINE_SNAPPER_PROJECTILE_SPEED,
)
from zelda_miloutte.sounds import get_sound_manager
from zelda_miloutte.sprites import AnimatedSprite
from zelda_miloutte.sprites.vine_snapper_sprites import get_vine_snapper_frames, get_thorn_sprite
from zelda_miloutte.sprites.effects import flash_white, scale_shrink
from zelda_miloutte.pathfinding import has_line_of_sight


class VineSnapper(Entity):
    """A stationary plant enemy that shoots thorn projectiles at the player."""

    def __init__(self, x, y):
        super().__init__(x, y, VINE_SNAPPER_SIZE, VINE_SNAPPER_SIZE, (30, 130, 30))
        self.hp = VINE_SNAPPER_HP
        self.max_hp = VINE_SNAPPER_HP
        self.damage = VINE_SNAPPER_DAMAGE
        self.speed = 0  # Stationary
        self.shoot_range = VINE_SNAPPER_SHOOT_RANGE
        self.shoot_cooldown = VINE_SNAPPER_SHOOT_COOLDOWN
        self.shoot_timer = 0.0

        # Damage flash
        self.flash_timer = 0.0
        self.flash_duration = 0.15

        # Death animation
        self.death_timer = 0.0
        self.death_duration = 0.3
        self.dying = False

        # XP value
        self.xp_value = 12

        # Drop system
        self.drop_chance = 0.3
        self.drop_table = [("heart", 3), ("key", 1)]

        # Gold drop
        self.gold_drop_chance = 0.6
        self.gold_drop_range = (1, 5)

        # Sprites
        self.anim = AnimatedSprite(get_vine_snapper_frames(), frame_duration=0.25)
        self._white_frames = {
            d: [flash_white(f) for f in frames]
            for d, frames in self.anim.frames.items()
        }

        # Pending projectile to be added to game state
        self.pending_projectile = None

        # Always face down (since it's a plant)
        self.facing = "down"

    def take_damage(self, amount):
        if self.dying:
            return
        self.hp -= amount
        self.flash_timer = self.flash_duration
        get_sound_manager().play_enemy_hit()
        if self.hp <= 0:
            self.dying = True
            self.death_timer = self.death_duration
            get_sound_manager().play_enemy_death()

    def get_drop(self):
        """Determine if the enemy drops an item and which one.
        Returns the item_type string ("heart" or "key") or None.
        """
        # Check if a drop happens
        if random.random() > self.drop_chance:
            return None

        # Use weighted random choice to pick which item
        items = [item_type for item_type, weight in self.drop_table]
        weights = [weight for item_type, weight in self.drop_table]
        return random.choices(items, weights=weights, k=1)[0]

    def get_gold_drop(self):
        if random.random() > self.gold_drop_chance:
            return 0
        return random.randint(self.gold_drop_range[0], self.gold_drop_range[1])

    def _distance_to(self, target):
        dx = target.center_x - self.center_x
        dy = target.center_y - self.center_y
        return math.sqrt(dx * dx + dy * dy)

    def shoot(self, player):
        """Create a projectile aimed at the player's current position."""
        if self.shoot_timer > 0:
            return None

        # Reset cooldown
        self.shoot_timer = self.shoot_cooldown

        # Create projectile from vine snapper's center toward player's center
        sprite = get_thorn_sprite()
        projectile = Projectile(
            self.center_x, self.center_y,
            player.center_x, player.center_y,
            self.damage,
            sprite
        )
        # Override projectile speed with vine snapper's specific speed
        dx = player.center_x - self.center_x
        dy = player.center_y - self.center_y
        dist = math.sqrt(dx * dx + dy * dy)
        if dist > 0:
            projectile.vx = (dx / dist) * VINE_SNAPPER_PROJECTILE_SPEED
            projectile.vy = (dy / dist) * VINE_SNAPPER_PROJECTILE_SPEED
        return projectile

    def update(self, dt, player, tilemap):
        if self.dying:
            self.death_timer -= dt
            if self.death_timer <= 0:
                self.alive = False
            return

        # Update knockback (minimal effect since stationary)
        self.update_knockback(dt)

        if self.flash_timer > 0:
            self.flash_timer -= dt

        # Update shoot cooldown
        if self.shoot_timer > 0:
            self.shoot_timer -= dt

        # Clear pending projectile
        self.pending_projectile = None

        # Stationary AI: only shoot if player is in range AND has line of sight
        dist = self._distance_to(player)
        if dist < self.shoot_range and self.shoot_timer <= 0:
            if has_line_of_sight(tilemap, self.center_x, self.center_y,
                                player.center_x, player.center_y):
                self.pending_projectile = self.shoot(player)

        # Vine Snapper doesn't move (stationary)
        self.vx = 0
        self.vy = 0

        # Animation (always plays idle animation)
        self.anim.update(dt, True)  # Always animate

    def draw(self, surface, camera):
        if not self.alive:
            return
        ox, oy = -camera.x, -camera.y
        r = self.rect.move(ox, oy)

        frame = self.anim.get_frame(self.facing)

        if self.dying:
            progress = 1.0 - (self.death_timer / self.death_duration)
            shrunk = scale_shrink(frame, progress)
            if shrunk is not None:
                sx = r.centerx - shrunk.get_width() // 2
                sy = r.centery - shrunk.get_height() // 2
                surface.blit(shrunk, (sx, sy))
            return

        # Flash white on damage
        if self.flash_timer > 0:
            idx = self.anim._index % len(self._white_frames[self.facing])
            frame = self._white_frames[self.facing][idx]

        fx = r.centerx - frame.get_width() // 2
        fy = r.centery - frame.get_height() // 2
        surface.blit(frame, (fx, fy))
