"""Frost Golem enemy - slow tanky enemy with AoE ground slam attack."""

import math
import random
import pygame
from .entity import Entity
from ..settings import (
    FROST_GOLEM_SIZE, FROST_GOLEM_SPEED, FROST_GOLEM_HP,
    FROST_GOLEM_DAMAGE, FROST_GOLEM_CHASE_RANGE,
    FROST_GOLEM_SLAM_COOLDOWN, FROST_GOLEM_SLAM_RADIUS,
)
from ..sounds import get_sound_manager
from ..sprites import AnimatedSprite
from ..sprites.frost_golem_sprites import get_frost_golem_frames
from ..sprites.effects import flash_white, scale_shrink


class FrostGolem(Entity):
    """A slow, tanky ice enemy with an AoE ground slam attack."""

    def __init__(self, x, y):
        super().__init__(x, y, FROST_GOLEM_SIZE, FROST_GOLEM_SIZE, (80, 140, 200))
        self.hp = FROST_GOLEM_HP
        self.max_hp = FROST_GOLEM_HP
        self.damage = FROST_GOLEM_DAMAGE
        self.speed = FROST_GOLEM_SPEED
        self.chase_range = FROST_GOLEM_CHASE_RANGE

        # Ground slam AoE attack
        self.slam_cooldown = FROST_GOLEM_SLAM_COOLDOWN
        self.slam_timer = self.slam_cooldown
        self.slam_active = False
        self.slam_duration = 0.3
        self.slam_active_timer = 0.0
        self.slam_radius = FROST_GOLEM_SLAM_RADIUS

        # Damage flash
        self.flash_timer = 0.0
        self.flash_duration = 0.15

        # Death animation
        self.death_timer = 0.0
        self.death_duration = 0.3
        self.dying = False

        # XP value
        self.xp_value = 30

        # Status effect on contact
        self.applies_freeze = True

        # Drop system
        self.drop_chance = 0.35
        self.drop_table = [("heart", 3), ("key", 1)]

        # Sprites
        self.anim = AnimatedSprite(get_frost_golem_frames(), frame_duration=0.20)
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
        if random.random() > self.drop_chance:
            return None
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

        # Update slam
        if self.slam_active:
            self.slam_active_timer -= dt
            if self.slam_active_timer <= 0:
                self.slam_active = False
        else:
            self.slam_timer -= dt

        # Skip AI during knockback
        if self.knockback_timer > 0:
            self.vx = self.knockback_vx
            self.vy = self.knockback_vy
        else:
            dist = self._distance_to(player)
            if dist < self.chase_range:
                # Ground slam when close enough
                if dist < self.slam_radius and self.slam_timer <= 0:
                    self.slam_active = True
                    self.slam_active_timer = self.slam_duration
                    self.slam_timer = self.slam_cooldown
                    self.vx = 0
                    self.vy = 0
                    get_sound_manager().play_boss_roar()
                else:
                    # Chase player slowly
                    self._move_toward(player.center_x, player.center_y, self.speed)
                    # Update facing
                    dx = player.center_x - self.center_x
                    dy = player.center_y - self.center_y
                    if abs(dx) > abs(dy):
                        self.facing = "right" if dx > 0 else "left"
                    else:
                        self.facing = "down" if dy > 0 else "up"
            else:
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

        # Draw slam AoE indicator
        if self.slam_active:
            slam_surf = pygame.Surface((self.slam_radius * 2, self.slam_radius * 2), pygame.SRCALPHA)
            pulse = int(abs(self.slam_active_timer * 10 % 1.0 - 0.5) * 60) + 60
            pygame.draw.circle(slam_surf, (100, 180, 255, pulse),
                             (self.slam_radius, self.slam_radius), self.slam_radius, 3)
            sx = r.centerx - self.slam_radius
            sy = r.centery - self.slam_radius
            surface.blit(slam_surf, (sx, sy))
