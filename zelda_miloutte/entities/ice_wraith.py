"""Ice Wraith enemy - ghostly blue/white creature that phases through walls periodically."""

import math
import random
import pygame
from .entity import Entity
from ..settings import (
    ICE_WRAITH_SIZE, ICE_WRAITH_SPEED, ICE_WRAITH_HP,
    ICE_WRAITH_DAMAGE, ICE_WRAITH_CHASE_RANGE, ICE_WRAITH_PHASE_COOLDOWN,
)
from ..sounds import get_sound_manager
from ..sprites import AnimatedSprite
from ..sprites.ice_wraith_sprites import get_ice_wraith_frames
from ..sprites.effects import flash_white, scale_shrink


class IceWraith(Entity):
    """A ghostly ice enemy that chases the player and phases through walls periodically."""

    def __init__(self, x, y):
        super().__init__(x, y, ICE_WRAITH_SIZE, ICE_WRAITH_SIZE, (80, 160, 220))
        self.hp = ICE_WRAITH_HP
        self.max_hp = ICE_WRAITH_HP
        self.damage = ICE_WRAITH_DAMAGE
        self.speed = ICE_WRAITH_SPEED
        self.chase_range = ICE_WRAITH_CHASE_RANGE

        # Phasing behavior (ignore walls briefly)
        self.phase_cooldown = ICE_WRAITH_PHASE_COOLDOWN
        self.phase_timer = self.phase_cooldown
        self.phasing = False
        self.phase_duration = 2.0
        self.phase_active_timer = 0.0

        # Damage flash
        self.flash_timer = 0.0
        self.flash_duration = 0.15

        # Death animation
        self.death_timer = 0.0
        self.death_duration = 0.3
        self.dying = False

        # XP value
        self.xp_value = 20

        # Status effect on contact
        self.applies_freeze = True

        # Drop system
        self.drop_chance = 0.3
        self.drop_table = [("heart", 3), ("key", 1)]

        # Sprites
        self.anim = AnimatedSprite(get_ice_wraith_frames(), frame_duration=0.15)
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

        # Update phase timer
        if self.phasing:
            self.phase_active_timer -= dt
            if self.phase_active_timer <= 0:
                self.phasing = False
                self.phase_timer = self.phase_cooldown
        else:
            self.phase_timer -= dt
            if self.phase_timer <= 0:
                self.phasing = True
                self.phase_active_timer = self.phase_duration

        # Skip AI during knockback
        if self.knockback_timer > 0:
            self.vx = self.knockback_vx
            self.vy = self.knockback_vy
        else:
            # Check if player is in chase range
            dist = self._distance_to(player)
            if dist < self.chase_range:
                # Chase player
                self._move_toward(player.center_x, player.center_y, self.speed)
                # Update facing
                dx = player.center_x - self.center_x
                dy = player.center_y - self.center_y
                if abs(dx) > abs(dy):
                    self.facing = "right" if dx > 0 else "left"
                else:
                    self.facing = "down" if dy > 0 else "up"
            else:
                # Not in range, drift slowly in a random direction
                self.vx = 0
                self.vy = 0

        # Move - only resolve collisions when not phasing
        self.x += self.vx * dt
        if not self.phasing:
            tilemap.resolve_collision_x(self)
        self.y += self.vy * dt
        if not self.phasing:
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

        # Make semi-transparent when phasing
        if self.phasing:
            frame = frame.copy()
            frame.set_alpha(120)

        fx = r.centerx - frame.get_width() // 2
        fy = r.centery - frame.get_height() // 2
        surface.blit(frame, (fx, fy))
