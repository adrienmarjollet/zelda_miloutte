import math
import random
import pygame
from .entity import Entity
from ..settings import (
    SHADOW_STALKER_SIZE, SHADOW_STALKER_SPEED, SHADOW_STALKER_HP,
    SHADOW_STALKER_DAMAGE, SHADOW_STALKER_TELEPORT_COOLDOWN,
    SHADOW_STALKER_CHASE_RANGE, TILE_SIZE,
)
from ..sounds import get_sound_manager
from ..sprites import AnimatedSprite
from ..sprites.shadow_stalker_sprites import get_shadow_stalker_frames
from ..sprites.effects import flash_white, scale_shrink
from ..ai_state import EnemyAI, AlertState


class ShadowStalker(Entity, EnemyAI):
    """A teleporting melee enemy that chases the player and teleports periodically."""

    def __init__(self, x, y):
        super().__init__(x, y, SHADOW_STALKER_SIZE, SHADOW_STALKER_SIZE, (80, 40, 120))
        self.hp = SHADOW_STALKER_HP
        self.max_hp = SHADOW_STALKER_HP
        self.damage = SHADOW_STALKER_DAMAGE
        self.speed = SHADOW_STALKER_SPEED
        self.chase_speed = SHADOW_STALKER_SPEED
        self.chase_range = SHADOW_STALKER_CHASE_RANGE

        # Teleport behavior
        self.teleport_cooldown = SHADOW_STALKER_TELEPORT_COOLDOWN
        self.teleport_timer = self.teleport_cooldown

        # Particle emission flag for gameplay_state
        self.teleport_particles = False

        # Damage flash
        self.flash_timer = 0.0
        self.flash_duration = 0.15

        # Death animation
        self.death_timer = 0.0
        self.death_duration = 0.3
        self.dying = False

        # XP value
        self.xp_value = 15

        # Drop system
        self.drop_chance = 0.3
        self.drop_table = [("heart", 3), ("key", 1)]

        # Gold drop
        self.gold_drop_chance = 0.6
        self.gold_drop_range = (2, 8)

        # Sprites
        self.anim = AnimatedSprite(get_shadow_stalker_frames(), frame_duration=0.18)
        self._white_frames = {
            d: [flash_white(f) for f in frames]
            for d, frames in self.anim.frames.items()
        }

        # Initialize smart AI
        self.init_ai(
            detection_range=SHADOW_STALKER_CHASE_RANGE,
            lose_range=SHADOW_STALKER_CHASE_RANGE * 2.0,
            pathfind_interval=0.5,
            use_pathfinding=True,
        )

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
        if random.random() > self.drop_chance:
            return None
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

    def _move_toward(self, tx, ty, speed, dt=None):
        dx = tx - self.center_x
        dy = ty - self.center_y
        dist = math.sqrt(dx * dx + dy * dy)
        if dist < 2:
            self.vx = 0
            self.vy = 0
            return
        self.vx = (dx / dist) * speed
        self.vy = (dy / dist) * speed

    def _update_facing_toward(self, tx, ty):
        dx = tx - self.center_x
        dy = ty - self.center_y
        if abs(dx) > abs(dy):
            self.facing = "right" if dx > 0 else "left"
        else:
            self.facing = "down" if dy > 0 else "up"

    def _try_teleport(self, tilemap):
        """Attempt to teleport to a random position near current location."""
        min_range = 3
        max_range = 4
        attempts = 10

        for _ in range(attempts):
            offset_x = random.randint(-max_range, max_range)
            offset_y = random.randint(-max_range, max_range)

            if abs(offset_x) < min_range and abs(offset_y) < min_range:
                continue

            target_x = self.x + offset_x * TILE_SIZE
            target_y = self.y + offset_y * TILE_SIZE

            target_col = int(target_x) // TILE_SIZE
            target_row = int(target_y) // TILE_SIZE

            if not tilemap.is_solid(target_col, target_row):
                self.x = target_x
                self.y = target_y
                self.teleport_particles = True
                self.teleport_timer = self.teleport_cooldown
                return

        self.teleport_timer = self.teleport_cooldown

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

        # Update teleport timer
        self.teleport_timer -= dt
        if self.teleport_timer <= 0:
            self._try_teleport(tilemap)

        # Skip AI during knockback
        if self.knockback_timer > 0:
            self.vx = self.knockback_vx
            self.vy = self.knockback_vy
        else:
            # Use smart AI state machine
            ai_result = self.update_ai(dt, player, tilemap)

            if ai_result is not None:
                target_x, target_y, speed = ai_result
                self._move_toward(target_x, target_y, speed)
                self._update_facing_toward(target_x, target_y)
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

        # Draw alert state icon
        self.draw_alert_icon(surface, camera)
