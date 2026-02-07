"""Sand Worm boss - a worm that burrows underground and emerges to attack."""

import math
import random
import pygame
from .entity import Entity
from ..settings import (
    SAND_WORM_HP, SAND_WORM_SPEED, SAND_WORM_CHASE_SPEED,
    SAND_WORM_DAMAGE, SAND_WORM_SIZE, TILE_SIZE,
)
from ..sounds import get_sound_manager
from ..sprites import AnimatedSprite
from ..sprites.sand_worm_sprites import (
    get_sand_worm_frames_surface,
    get_sand_worm_frames_burrowed,
    get_sand_worm_frames_surface_p2,
    get_sand_worm_frames_burrowed_p2,
)
from ..sprites.effects import flash_white, scale_shrink


class SandWorm(Entity):
    """Sand Worm boss - burrows underground and emerges to attack."""

    def __init__(self, x, y):
        super().__init__(x, y, SAND_WORM_SIZE, SAND_WORM_SIZE, (180, 150, 80))
        self.hp = SAND_WORM_HP
        self.max_hp = SAND_WORM_HP
        self.damage = SAND_WORM_DAMAGE
        self.speed = SAND_WORM_SPEED
        self.chase_speed = SAND_WORM_CHASE_SPEED

        # State machine: "surface" or "burrowed"
        self.state = "surface"
        self.state_timer = 0.0
        self.surface_duration = 4.0  # Phase 1: 4 seconds on surface
        self.burrowed_duration = 2.0  # Phase 1: 2 seconds burrowed

        # Invulnerability when burrowed
        self.invulnerable = False

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
        self.xp_value = 100

        # Boss always drops a heart (100% chance)
        self.drop_chance = 1.0
        self.drop_table = [("heart", 1)]

        # AOE slam in phase 2
        self.emerge_slam_active = False
        self.emerge_slam_duration = 0.3
        self.emerge_slam_timer = 0.0

        # Flag for particle effects
        self.pending_sand_burst = False

        # Sprites
        self.anim_surface_p1 = AnimatedSprite(get_sand_worm_frames_surface(), frame_duration=0.20)
        self.anim_burrowed_p1 = AnimatedSprite(get_sand_worm_frames_burrowed(), frame_duration=0.20)
        self.anim_surface_p2 = AnimatedSprite(get_sand_worm_frames_surface_p2(), frame_duration=0.14)
        self.anim_burrowed_p2 = AnimatedSprite(get_sand_worm_frames_burrowed_p2(), frame_duration=0.14)

        self.anim_surface = self.anim_surface_p1
        self.anim_burrowed = self.anim_burrowed_p1
        self.anim = self.anim_surface

        # Pre-build white flash frames for both phases (surface only)
        self._white_surface_p1 = {
            d: [flash_white(f) for f in frames]
            for d, frames in self.anim_surface_p1.frames.items()
        }
        self._white_surface_p2 = {
            d: [flash_white(f) for f in frames]
            for d, frames in self.anim_surface_p2.frames.items()
        }
        self._white_frames = self._white_surface_p1

    @property
    def phase2(self):
        """Check if boss is in phase 2 (below 50% HP)."""
        return self.hp <= self.max_hp * 0.5

    def take_damage(self, amount):
        """Override to block damage when burrowed."""
        if self.dying or self.invulnerable:
            return False
        self.hp -= amount
        self.flash_timer = self.flash_duration
        get_sound_manager().play_enemy_hit()
        if self.hp <= 0:
            self.dying = True
            self.death_timer = self.death_duration
            get_sound_manager().play_boss_death()
        return True

    def apply_knockback(self, src_x, src_y, force):
        """Apply knockback only when on surface."""
        if self.state == "burrowed":
            return
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

    def _find_random_position(self, tilemap):
        """Find a random valid position in the arena (not on walls)."""
        # Try up to 20 times to find a valid position
        for _ in range(20):
            # Random position within the map bounds (avoiding edges)
            tile_x = random.randint(2, tilemap.width - 3)
            tile_y = random.randint(2, tilemap.height - 3)
            test_x = tile_x * TILE_SIZE + TILE_SIZE // 2
            test_y = tile_y * TILE_SIZE + TILE_SIZE // 2

            # Check if position is not on a solid tile
            tile = tilemap.get_tile_at(test_x, test_y)
            if tile is None or not tile.solid:
                return test_x, test_y

        # Fallback: return center of map
        return (tilemap.width * TILE_SIZE) // 2, (tilemap.height * TILE_SIZE) // 2

    def _burrow(self, tilemap):
        """Burrow underground and move to random position."""
        self.state = "burrowed"
        self.invulnerable = True
        self.state_timer = self.burrowed_duration
        self.pending_sand_burst = True

        # Move to random position
        new_x, new_y = self._find_random_position(tilemap)
        self.x = new_x - self.width // 2
        self.y = new_y - self.height // 2

        # Switch to burrowed animation
        self.anim = self.anim_burrowed

    def _emerge(self):
        """Emerge from underground."""
        self.state = "surface"
        self.invulnerable = False
        self.state_timer = self.surface_duration
        self.pending_sand_burst = True

        # Switch to surface animation
        self.anim = self.anim_surface

        # Phase 2: AOE slam on emerge
        if self.phase == 2:
            self.emerge_slam_active = True
            self.emerge_slam_timer = self.emerge_slam_duration
            get_sound_manager().play_boss_roar()

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

        # Update emerge slam timer
        if self.emerge_slam_active:
            self.emerge_slam_timer -= dt
            if self.emerge_slam_timer <= 0:
                self.emerge_slam_active = False

        # Phase check
        if self.phase2 and self.phase == 1:
            self.phase = 2
            self.surface_duration = 3.0  # Faster surface time
            self.burrowed_duration = 1.5  # Faster burrowed time
            self.anim_surface = self.anim_surface_p2
            self.anim_burrowed = self.anim_burrowed_p2
            self._white_frames = self._white_surface_p2
            if not self.phase2_roar_played:
                get_sound_manager().play_boss_roar()
                self.phase2_roar_played = True

        # State machine
        self.state_timer -= dt

        if self.state == "surface":
            # On surface: chase player
            if self.state_timer <= 0:
                self._burrow(tilemap)
            else:
                # Skip AI during knockback
                if self.knockback_timer > 0:
                    self.vx = self.knockback_vx
                    self.vy = self.knockback_vy
                else:
                    # Chase player
                    self._move_toward(player.center_x, player.center_y, self.chase_speed, dt)

                    # Update facing direction
                    dx = player.center_x - self.center_x
                    dy = player.center_y - self.center_y
                    if abs(dx) > abs(dy):
                        self.facing = "right" if dx > 0 else "left"
                    else:
                        self.facing = "down" if dy > 0 else "up"

                # Move with collision
                self.x += self.vx * dt
                tilemap.resolve_collision_x(self)
                self.y += self.vy * dt
                tilemap.resolve_collision_y(self)

        elif self.state == "burrowed":
            # Burrowed: invulnerable, waiting to emerge
            if self.state_timer <= 0:
                self._emerge()
            # No movement while burrowed (already repositioned)
            self.vx = 0
            self.vy = 0

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

        # Flash white on damage (only when on surface)
        if self.flash_timer > 0 and self.state == "surface":
            idx = self.anim._index % len(self._white_frames[self.facing])
            frame = self._white_frames[self.facing][idx]

        fx = r.centerx - frame.get_width() // 2
        fy = r.centery - frame.get_height() // 2
        surface.blit(frame, (fx, fy))
