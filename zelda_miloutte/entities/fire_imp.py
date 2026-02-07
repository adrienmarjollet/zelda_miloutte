"""Fire Imp enemy - fast melee attacker that leaves fire trail hazards."""

import math
import random
import pygame
from .entity import Entity
from ..settings import (
    FIRE_IMP_SIZE, FIRE_IMP_SPEED, FIRE_IMP_HP,
    FIRE_IMP_DAMAGE, FIRE_IMP_CHASE_RANGE,
)
from ..sounds import get_sound_manager
from ..sprites import AnimatedSprite
from ..sprites.fire_imp_sprites import get_fire_imp_frames
from ..sprites.effects import flash_white, scale_shrink
from ..ai_state import EnemyAI, AlertState


class FireImp(Entity, EnemyAI):
    """A fast melee enemy that leaves fire trail hazards."""

    def __init__(self, x, y):
        super().__init__(x, y, FIRE_IMP_SIZE, FIRE_IMP_SIZE, (220, 80, 30))
        self.hp = FIRE_IMP_HP
        self.max_hp = FIRE_IMP_HP
        self.damage = FIRE_IMP_DAMAGE
        self.speed = FIRE_IMP_SPEED
        self.chase_speed = FIRE_IMP_SPEED
        self.chase_range = FIRE_IMP_CHASE_RANGE

        # Fire trail behavior
        self.fire_trail_cooldown = 0.8
        self.fire_trail_timer = self.fire_trail_cooldown
        self.pending_fire_trails = []

        # Damage flash
        self.flash_timer = 0.0
        self.flash_duration = 0.15

        # Death animation
        self.death_timer = 0.0
        self.death_duration = 0.3
        self.dying = False

        # XP value
        self.xp_value = 25

        # Status effect on contact
        self.applies_burn = True

        # Drop system
        self.drop_chance = 0.3
        self.drop_table = [("heart", 3), ("key", 1)]

        # Gold drop
        self.gold_drop_chance = 0.6
        self.gold_drop_range = (2, 8)

        # Sprites
        self.anim = AnimatedSprite(get_fire_imp_frames(), frame_duration=0.15)
        self._white_frames = {
            d: [flash_white(f) for f in frames]
            for d, frames in self.anim.frames.items()
        }

        # Initialize smart AI -- fire imp is aggressive and fast
        self.init_ai(
            detection_range=FIRE_IMP_CHASE_RANGE,
            lose_range=FIRE_IMP_CHASE_RANGE * 2.0,
            pathfind_interval=0.4,
            use_pathfinding=True,
            suspicious_duration=0.5,  # Quick to react
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

        # Update fire trail timer
        self.fire_trail_timer -= dt

        # Clear pending fire trails
        self.pending_fire_trails = []

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

        # Create fire trail if moving and timer ready
        if self.is_moving and self.fire_trail_timer <= 0:
            self.fire_trail_timer = self.fire_trail_cooldown
            self.pending_fire_trails.append({
                "x": self.center_x,
                "y": self.center_y,
                "timer": 3.0
            })

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
