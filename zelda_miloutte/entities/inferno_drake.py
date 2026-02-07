"""Inferno Drake boss - a dragon with fire breath and meteor attacks."""

import math
import random
import pygame
from .entity import Entity
from ..settings import (
    INFERNO_DRAKE_HP, INFERNO_DRAKE_SPEED, INFERNO_DRAKE_CHASE_SPEED,
    INFERNO_DRAKE_DAMAGE, INFERNO_DRAKE_SIZE, TILE_SIZE,
)
from ..sounds import get_sound_manager
from ..sprites import AnimatedSprite
from ..sprites.inferno_drake_sprites import (
    get_inferno_drake_frames_phase1,
    get_inferno_drake_frames_phase2,
)
from ..sprites.effects import flash_white, scale_shrink


class InfernoDrake(Entity):
    """Inferno Drake boss - the final boss with fire breath and meteor attacks."""

    def __init__(self, x, y):
        super().__init__(x, y, INFERNO_DRAKE_SIZE, INFERNO_DRAKE_SIZE, (200, 50, 20))
        self.hp = INFERNO_DRAKE_HP
        self.max_hp = INFERNO_DRAKE_HP
        self.damage = INFERNO_DRAKE_DAMAGE
        self.speed = INFERNO_DRAKE_SPEED
        self.chase_speed = INFERNO_DRAKE_CHASE_SPEED

        # Fire breath attack
        self.fire_breath_timer = 0.0
        self.fire_breath_cooldown = 4.0  # Phase 1: every 4s
        self.fire_breath_active = False
        self.fire_breath_duration = 0.8
        self.fire_breath_rect = None

        # Meteor attack (phase 2 only)
        self.meteor_timer = 0.0
        self.meteor_cooldown = 8.0  # Every 8s
        self.pending_meteors = []  # List of {"x": x, "y": y, "timer": 1.5, "exploded": False}

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
        self.xp_value = 150

        # Boss always drops a heart (100% chance)
        self.drop_chance = 1.0
        self.drop_table = [("heart", 1)]

        # Sprites
        self.anim_p1 = AnimatedSprite(get_inferno_drake_frames_phase1(), frame_duration=0.20)
        self.anim_p2 = AnimatedSprite(get_inferno_drake_frames_phase2(), frame_duration=0.14)
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

    def _perform_fire_breath(self):
        """Trigger fire breath attack."""
        self.fire_breath_active = True
        self.fire_breath_timer = self.fire_breath_duration
        get_sound_manager().play_boss_roar()  # Use existing sound for fire breath

        # Create damage zone in front of boss based on facing direction
        breath_length = 80
        breath_width = 60

        if self.facing == "right":
            self.fire_breath_rect = pygame.Rect(
                self.rect.right, self.center_y - breath_width // 2,
                breath_length, breath_width
            )
        elif self.facing == "left":
            self.fire_breath_rect = pygame.Rect(
                self.rect.left - breath_length, self.center_y - breath_width // 2,
                breath_length, breath_width
            )
        elif self.facing == "down":
            self.fire_breath_rect = pygame.Rect(
                self.center_x - breath_width // 2, self.rect.bottom,
                breath_width, breath_length
            )
        else:  # up
            self.fire_breath_rect = pygame.Rect(
                self.center_x - breath_width // 2, self.rect.top - breath_length,
                breath_width, breath_length
            )

    def _summon_meteors(self, tilemap):
        """Summon 3 meteors at random positions."""
        self.pending_meteors = []
        for _ in range(3):
            # Random position within the map bounds (avoiding edges)
            tile_x = random.randint(2, tilemap.cols - 3)
            tile_y = random.randint(2, tilemap.rows - 3)
            meteor_x = tile_x * TILE_SIZE + TILE_SIZE // 2
            meteor_y = tile_y * TILE_SIZE + TILE_SIZE // 2

            # Check if position is not on a solid tile
            tile = tilemap.get_tile_at(meteor_x, meteor_y)
            if tile is None or not tile.solid:
                self.pending_meteors.append({
                    "x": meteor_x,
                    "y": meteor_y,
                    "timer": 1.5,
                    "exploded": False
                })

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

        # Update fire breath timer
        if self.fire_breath_active:
            self.fire_breath_timer -= dt
            if self.fire_breath_timer <= 0:
                self.fire_breath_active = False
                self.fire_breath_rect = None

        # Phase check
        if self.phase2 and self.phase == 1:
            self.phase = 2
            self.anim = self.anim_p2
            self._white_frames = self._white_p2
            self.fire_breath_cooldown = 3.0  # Faster fire breath in phase 2
            if not self.phase2_roar_played:
                get_sound_manager().play_boss_roar()
                self.phase2_roar_played = True

        dist = self._distance_to(player)

        # Skip AI during knockback
        if self.knockback_timer > 0:
            self.vx = self.knockback_vx
            self.vy = self.knockback_vy
        else:
            # Fire breath attack logic
            self.fire_breath_timer += dt
            if self.fire_breath_timer >= self.fire_breath_cooldown:
                self._perform_fire_breath()
                self.fire_breath_timer = 0.0
                # Pause briefly during breath
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

        # Phase 2: Meteor summon
        if self.phase == 2:
            self.meteor_timer += dt
            if self.meteor_timer >= self.meteor_cooldown:
                self._summon_meteors(tilemap)
                self.meteor_timer = 0.0

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
