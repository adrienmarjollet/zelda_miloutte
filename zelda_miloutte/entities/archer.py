import math
import pygame
from zelda_miloutte.entities.enemy import Enemy
from zelda_miloutte.entities.projectile import Projectile
from zelda_miloutte.settings import (
    ARCHER_SIZE, ARCHER_SPEED, ARCHER_HP, ARCHER_DAMAGE,
    ARCHER_SHOOT_RANGE, ARCHER_SHOOT_COOLDOWN, ARCHER_FLEE_RANGE,
    RED, TILE_SIZE,
)
from zelda_miloutte.sprites import AnimatedSprite
from zelda_miloutte.sprites.archer_sprites import get_archer_frames, get_projectile_sprite
from zelda_miloutte.sprites.effects import flash_white


class Archer(Enemy):
    """Ranged enemy that shoots projectiles at the player."""

    def __init__(self, x, y, patrol_points=None):
        # Call Entity.__init__ directly to avoid Enemy's __init__
        from zelda_miloutte.entities.entity import Entity
        Entity.__init__(self, x, y, ARCHER_SIZE, ARCHER_SIZE, RED)

        self.hp = ARCHER_HP
        self.max_hp = ARCHER_HP
        self.damage = ARCHER_DAMAGE
        self.speed = ARCHER_SPEED
        self.chase_speed = ARCHER_SPEED  # Archers don't chase, they maintain distance
        self.chase_range = ARCHER_SHOOT_RANGE  # Detection range
        self.shoot_range = ARCHER_SHOOT_RANGE
        self.flee_range = ARCHER_FLEE_RANGE
        self.shoot_cooldown = ARCHER_SHOOT_COOLDOWN
        self.shoot_timer = 0.0

        # Patrol (archers stay put by default)
        if patrol_points and len(patrol_points) >= 2:
            self.patrol_points = [(p[0] * TILE_SIZE, p[1] * TILE_SIZE) for p in patrol_points]
        else:
            self.patrol_points = [(x, y)]
        self.patrol_index = 0
        self.patrol_pause = 0.0

        # Damage flash
        self.flash_timer = 0.0
        self.flash_duration = 0.15

        # Death animation
        self.death_timer = 0.0
        self.death_duration = 0.3
        self.dying = False

        # XP value
        self.xp_value = 15

        # Drop system (same as base enemy)
        self.drop_chance = 0.3
        self.drop_table = [("heart", 3), ("key", 1)]

        # Sprites (archer-specific)
        self.anim = AnimatedSprite(get_archer_frames(), frame_duration=0.18)
        self._white_frames = {
            d: [flash_white(f) for f in frames]
            for d, frames in self.anim.frames.items()
        }

        # Pending projectile to be added to game state
        self.pending_projectile = None

    def shoot(self, player):
        """Create a projectile aimed at the player's current position."""
        if self.shoot_timer > 0:
            return None

        # Reset cooldown
        self.shoot_timer = self.shoot_cooldown

        # Create projectile from archer's center toward player's center
        sprite = get_projectile_sprite()
        projectile = Projectile(
            self.center_x, self.center_y,
            player.center_x, player.center_y,
            self.damage,
            sprite
        )
        return projectile

    def update(self, dt, player, tilemap):
        """Update archer with ranged AI behavior."""
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
            # Ranged AI behavior
            dist = self._distance_to(player)

            # Face the player if in range
            if dist < self.shoot_range:
                dx = player.center_x - self.center_x
                dy = player.center_y - self.center_y
                if abs(dx) > abs(dy):
                    self.facing = "right" if dx > 0 else "left"
                else:
                    self.facing = "down" if dy > 0 else "up"

            # Flee if player is too close
            if dist < self.flee_range:
                # Move away from player
                dx = self.center_x - player.center_x
                dy = self.center_y - player.center_y
                flee_dist = math.sqrt(dx * dx + dy * dy)
                if flee_dist > 0:
                    self.vx = (dx / flee_dist) * self.speed
                    self.vy = (dy / flee_dist) * self.speed
            # Shoot if in range and cooldown ready
            elif dist < self.shoot_range:
                # Stop moving and shoot
                self.vx = 0
                self.vy = 0
                if self.shoot_timer <= 0:
                    self.pending_projectile = self.shoot(player)
            else:
                # No player in range, stay still (archers don't patrol actively)
                self.vx = 0
                self.vy = 0

        # Move with collision
        self.x += self.vx * dt
        tilemap.resolve_collision_x(self)
        self.y += self.vy * dt
        tilemap.resolve_collision_y(self)

        # Animation
        self.anim.update(dt, self.is_moving)
