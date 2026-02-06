"""Magma Golem enemy - slow tank that lobs magma projectiles."""

import math
import random
import pygame
from zelda_miloutte.entities.entity import Entity
from zelda_miloutte.entities.projectile import Projectile
from zelda_miloutte.settings import (
    MAGMA_GOLEM_SIZE, MAGMA_GOLEM_SPEED, MAGMA_GOLEM_HP,
    MAGMA_GOLEM_DAMAGE, MAGMA_GOLEM_CHASE_RANGE,
    MAGMA_GOLEM_SHOOT_COOLDOWN, MAGMA_GOLEM_PROJECTILE_SPEED,
)
from zelda_miloutte.sounds import get_sound_manager
from zelda_miloutte.sprites import AnimatedSprite
from zelda_miloutte.sprites.magma_golem_sprites import get_magma_golem_frames, get_magma_projectile_sprite
from zelda_miloutte.sprites.effects import flash_white, scale_shrink


class MagmaGolem(Entity):
    """A slow tank enemy that lobs magma projectiles."""

    def __init__(self, x, y):
        super().__init__(x, y, MAGMA_GOLEM_SIZE, MAGMA_GOLEM_SIZE, (100, 50, 30))
        self.hp = MAGMA_GOLEM_HP
        self.max_hp = MAGMA_GOLEM_HP
        self.damage = MAGMA_GOLEM_DAMAGE
        self.speed = MAGMA_GOLEM_SPEED
        self.chase_range = MAGMA_GOLEM_CHASE_RANGE

        # Shooting behavior
        self.shoot_cooldown = MAGMA_GOLEM_SHOOT_COOLDOWN
        self.shoot_timer = 0.0

        # Pending projectile to be added to game state
        self.pending_projectile = None

        # Damage flash
        self.flash_timer = 0.0
        self.flash_duration = 0.15

        # Death animation
        self.death_timer = 0.0
        self.death_duration = 0.3
        self.dying = False

        # XP value
        self.xp_value = 30

        # Drop system
        self.drop_chance = 0.3
        self.drop_table = [("heart", 3), ("key", 1)]

        # Sprites
        self.anim = AnimatedSprite(get_magma_golem_frames(), frame_duration=0.20)
        self._white_frames = {
            d: [flash_white(f) for f in frames]
            for d, frames in self.anim.frames.items()
        }

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

    def _distance_to(self, target):
        dx = target.center_x - self.center_x
        dy = target.center_y - self.center_y
        return math.sqrt(dx * dx + dy * dy)

    def _move_toward(self, tx, ty, speed):
        dx = tx - self.center_x
        dy = ty - self.center_y
        dist = math.sqrt(dx * dx + dy * dy)
        if dist < 2:
            self.vx = 0
            self.vy = 0
            return
        self.vx = (dx / dist) * speed
        self.vy = (dy / dist) * speed

    def _shoot(self, player):
        """Create a magma projectile aimed at the player."""
        if self.shoot_timer > 0:
            return None

        # Reset cooldown
        self.shoot_timer = self.shoot_cooldown

        # Create projectile from golem's center toward player's center
        sprite = get_magma_projectile_sprite()

        # Custom projectile with magma speed
        proj = Projectile(
            self.center_x, self.center_y,
            player.center_x, player.center_y,
            self.damage,
            sprite
        )
        # Override speed for magma projectile
        dx = player.center_x - self.center_x
        dy = player.center_y - self.center_y
        dist = math.sqrt(dx * dx + dy * dy)
        if dist > 0:
            proj.vx = (dx / dist) * MAGMA_GOLEM_PROJECTILE_SPEED
            proj.vy = (dy / dist) * MAGMA_GOLEM_PROJECTILE_SPEED

        return proj

    def update(self, dt, player, tilemap):
        if self.dying:
            self.death_timer -= dt
            if self.death_timer <= 0:
                self.alive = False
            return

        # Update knockback
        self.update_knockback(dt)

        if self.flash_timer > 0:
            self.flash_timer -= dt

        # Update shoot cooldown
        if self.shoot_timer > 0:
            self.shoot_timer -= dt

        # Clear pending projectile
        self.pending_projectile = None

        # Skip AI during knockback
        if self.knockback_timer > 0:
            self.vx = self.knockback_vx
            self.vy = self.knockback_vy
        else:
            # Check if player is in chase range
            dist = self._distance_to(player)
            if dist < self.chase_range:
                # Slowly chase player
                self._move_toward(player.center_x, player.center_y, self.speed)
                # Update facing
                dx = player.center_x - self.center_x
                dy = player.center_y - self.center_y
                if abs(dx) > abs(dy):
                    self.facing = "right" if dx > 0 else "left"
                else:
                    self.facing = "down" if dy > 0 else "up"

                # Shoot projectile if cooldown ready
                if self.shoot_timer <= 0:
                    self.pending_projectile = self._shoot(player)
            else:
                # Not in range, stop
                self.vx = 0
                self.vy = 0

        # Move with collision
        self.x += self.vx * dt
        tilemap.resolve_collision_x(self)
        self.y += self.vy * dt
        tilemap.resolve_collision_y(self)

        # Animation
        self.anim.update(dt, self.is_moving)

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
