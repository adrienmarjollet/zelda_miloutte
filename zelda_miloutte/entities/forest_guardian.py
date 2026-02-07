"""Forest Guardian boss - a tree entity that summons vines."""

import math
import random
import pygame
from .entity import Entity
from ..settings import (
    FOREST_GUARDIAN_HP, FOREST_GUARDIAN_SPEED, FOREST_GUARDIAN_CHASE_SPEED,
    FOREST_GUARDIAN_DAMAGE, FOREST_GUARDIAN_SIZE, TILE_SIZE,
)
from ..sounds import get_sound_manager
from ..sprites import AnimatedSprite
from ..sprites.forest_guardian_sprites import (
    get_forest_guardian_frames_phase1,
    get_forest_guardian_frames_phase2,
)
from ..sprites.effects import flash_white, scale_shrink


class ForestGuardian(Entity):
    """Forest Guardian boss - a tree that roots and summons vines."""

    def __init__(self, x, y):
        super().__init__(x, y, FOREST_GUARDIAN_SIZE, FOREST_GUARDIAN_SIZE, (30, 100, 30))
        self.hp = FOREST_GUARDIAN_HP
        self.max_hp = FOREST_GUARDIAN_HP
        self.damage = FOREST_GUARDIAN_DAMAGE
        self.speed = FOREST_GUARDIAN_SPEED
        self.chase_speed = FOREST_GUARDIAN_CHASE_SPEED

        # Root slam attack
        self.root_slam_timer = 0.0
        self.root_slam_cooldown = 3.0  # Phase 1: every 3s
        self.root_slam_active = False
        self.root_slam_duration = 0.3

        # Vine summon (phase 2 only)
        self.vine_summon_timer = 0.0
        self.vine_summon_cooldown = 8.0  # Every 8s
        self.pending_summons = []  # List of {"x": x, "y": y} dicts

        # Phase
        self.phase = 1
        self.phase2_roar_played = False

        # Boss has shorter knockback duration
        self.knockback_duration = 0.08

        # Damage flash
        self.flash_timer = 0.0
        self.flash_duration = 0.15

        # Death animation
        self.death_timer = 0.0
        self.death_duration = 0.5
        self.dying = False

        # XP value
        self.xp_value = 75

        # Boss always drops a heart (100% chance)
        self.drop_chance = 1.0
        self.drop_table = [("heart", 1)]

        # Sprites
        self.anim_p1 = AnimatedSprite(get_forest_guardian_frames_phase1(), frame_duration=0.20)
        self.anim_p2 = AnimatedSprite(get_forest_guardian_frames_phase2(), frame_duration=0.14)
        self.anim = self.anim_p1

        # Pre-build white flash frames for both phases
        self._white_p1 = {
            d: [flash_white(f) for f in frames]
            for d, frames in self.anim_p1.frames.items()
        }
        self._white_p2 = {
            d: [flash_white(f) for f in frames]
            for d, frames in self.anim_p2.frames.items()
        }
        self._white_frames = self._white_p1

    @property
    def phase2(self):
        """Check if boss is in phase 2 (below 50% HP)."""
        return self.hp <= self.max_hp * 0.5

    def take_damage(self, amount):
        """Override to play boss-specific death sound."""
        if self.dying:
            return
        self.hp -= amount
        self.flash_timer = self.flash_duration
        get_sound_manager().play_enemy_hit()
        if self.hp <= 0:
            self.dying = True
            self.death_timer = self.death_duration
            get_sound_manager().play_boss_death()

    def apply_knockback(self, src_x, src_y, force):
        """Apply knockback with reduced effect (boss is heavy)."""
        dx = self.center_x - src_x
        dy = self.center_y - src_y
        dist = math.sqrt(dx * dx + dy * dy)
        if dist > 0:
            # Reduced knockback for boss
            self.knockback_vx = (dx / dist) * force * 0.3
            self.knockback_vy = (dy / dist) * force * 0.3
            self.knockback_timer = self.knockback_duration

    def get_drop(self):
        """Return item drop. Boss always drops a heart."""
        if random.random() > self.drop_chance:
            return None
        items = [item_type for item_type, weight in self.drop_table]
        weights = [weight for item_type, weight in self.drop_table]
        return random.choices(items, weights=weights, k=1)[0]

    def _distance_to(self, target):
        """Calculate distance to target entity."""
        dx = target.center_x - self.center_x
        dy = target.center_y - self.center_y
        return math.sqrt(dx * dx + dy * dy)

    def _move_toward(self, target_x, target_y, speed, dt):
        """Move toward a target position."""
        dx = target_x - self.center_x
        dy = target_y - self.center_y
        dist = math.sqrt(dx * dx + dy * dy)
        if dist > 0:
            self.vx = (dx / dist) * speed
            self.vy = (dy / dist) * speed

    def _perform_root_slam(self):
        """Trigger root slam attack."""
        self.root_slam_active = True
        self.root_slam_timer = self.root_slam_duration
        get_sound_manager().play_boss_roar()  # Use existing sound for slam

    def _summon_vines(self):
        """Summon 2 VineSnapper enemies near the boss."""
        self.pending_summons = []
        for _ in range(2):
            # Spawn offset in random direction, ~3 tiles away
            angle = random.uniform(0, 2 * math.pi)
            offset_x = math.cos(angle) * TILE_SIZE * 3
            offset_y = math.sin(angle) * TILE_SIZE * 3
            spawn_x = self.center_x + offset_x
            spawn_y = self.center_y + offset_y
            self.pending_summons.append({"x": spawn_x, "y": spawn_y})

    def update(self, dt, player, tilemap):
        """Update boss AI and movement."""
        if self.dying:
            self.death_timer -= dt
            if self.death_timer <= 0:
                self.alive = False
            return

        # Update knockback
        self.update_knockback(dt)

        if self.flash_timer > 0:
            self.flash_timer -= dt

        # Update root slam timer
        if self.root_slam_active:
            self.root_slam_timer -= dt
            if self.root_slam_timer <= 0:
                self.root_slam_active = False

        # Phase check
        if self.phase2 and self.phase == 1:
            self.phase = 2
            self.anim = self.anim_p2
            self._white_frames = self._white_p2
            self.root_slam_cooldown = 2.0  # Faster slams in phase 2
            if not self.phase2_roar_played:
                get_sound_manager().play_boss_roar()
                self.phase2_roar_played = True

        dist = self._distance_to(player)

        # Skip AI during knockback
        if self.knockback_timer > 0:
            self.vx = self.knockback_vx
            self.vy = self.knockback_vy
        else:
            # Root slam attack logic
            if dist < 100 and self.root_slam_timer <= 0:
                self._perform_root_slam()
                self.root_slam_timer = self.root_slam_cooldown
                # Pause briefly during slam
                self.vx = 0
                self.vy = 0
            else:
                # Chase player
                speed = self.chase_speed if self.phase == 2 else self.speed
                self._move_toward(player.center_x, player.center_y, speed, dt)

            # Update facing direction
            dx = player.center_x - self.center_x
            dy = player.center_y - self.center_y
            if abs(dx) > abs(dy):
                self.facing = "right" if dx > 0 else "left"
            else:
                self.facing = "down" if dy > 0 else "up"

        # Phase 2: Vine summon
        if self.phase == 2:
            self.vine_summon_timer += dt
            if self.vine_summon_timer >= self.vine_summon_cooldown:
                self._summon_vines()
                self.vine_summon_timer = 0.0

        # Move with collision
        self.x += self.vx * dt
        tilemap.resolve_collision_x(self)
        self.y += self.vy * dt
        tilemap.resolve_collision_y(self)

        # Update animation
        self.anim.update(dt, self.vx != 0 or self.vy != 0)

    def draw(self, surface, camera):
        """Draw the boss sprite."""
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
