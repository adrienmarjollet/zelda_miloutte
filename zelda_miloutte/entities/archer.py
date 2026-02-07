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
from zelda_miloutte.ai_state import AlertState
from zelda_miloutte.pathfinding import find_path, find_cover_position, has_line_of_sight, can_pathfind


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

        # Optimal range: archers try to stay at this distance
        self.optimal_range = ARCHER_SHOOT_RANGE * 0.7

        # Strafing behavior
        self._strafe_dir = 1  # 1 or -1
        self._strafe_timer = 0.0
        self._strafe_interval = 1.5  # Switch strafe direction every 1.5s

        # Cover-seeking behavior
        self._cover_pos = None
        self._cover_timer = 0.0
        self._cover_interval = 3.0  # Re-evaluate cover every 3s

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

        # Gold drop
        self.gold_drop_chance = 0.6
        self.gold_drop_range = (1, 5)

        # Sprites (archer-specific)
        self.anim = AnimatedSprite(get_archer_frames(), frame_duration=0.18)
        self._white_frames = {
            d: [flash_white(f) for f in frames]
            for d, frames in self.anim.frames.items()
        }

        # Pending projectile to be added to game state
        self.pending_projectile = None

        # Initialize smart AI with archer-specific settings
        self.init_ai(
            detection_range=ARCHER_SHOOT_RANGE,
            lose_range=ARCHER_SHOOT_RANGE * 2.5,
            pathfind_interval=0.8,
            use_pathfinding=True,
        )

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

    def _get_strafe_velocity(self, player, speed):
        """Calculate velocity for strafing sideways relative to player direction."""
        dx = player.center_x - self.center_x
        dy = player.center_y - self.center_y
        dist = math.sqrt(dx * dx + dy * dy)
        if dist < 1:
            return 0, 0
        # Perpendicular direction for strafing
        perp_x = -dy / dist * self._strafe_dir
        perp_y = dx / dist * self._strafe_dir
        return perp_x * speed, perp_y * speed

    def update(self, dt, player, tilemap):
        """Update archer with improved ranged AI behavior."""
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

        # Update strafe timer
        self._strafe_timer += dt
        if self._strafe_timer >= self._strafe_interval:
            self._strafe_timer = 0.0
            self._strafe_dir *= -1

        # Clear pending projectile
        self.pending_projectile = None

        # Skip AI during knockback
        if self.knockback_timer > 0:
            self.vx = self.knockback_vx
            self.vy = self.knockback_vy
        else:
            # Use smart AI state machine for detection
            ai_result = self.update_ai(dt, player, tilemap)

            if ai_result is not None and self.ai_state in (AlertState.ALERT, AlertState.SUSPICIOUS):
                # Archer-specific combat AI
                dist = self._distance_to(player)
                has_los = has_line_of_sight(
                    tilemap, self.center_x, self.center_y,
                    player.center_x, player.center_y
                )

                # Face the player
                self._update_facing_toward(player.center_x, player.center_y)

                if dist < self.flee_range:
                    # Too close -- flee away from player
                    dx = self.center_x - player.center_x
                    dy = self.center_y - player.center_y
                    flee_dist = math.sqrt(dx * dx + dy * dy)
                    if flee_dist > 0:
                        self.vx = (dx / flee_dist) * self.speed
                        self.vy = (dy / flee_dist) * self.speed
                elif not has_los and self.ai_state == AlertState.ALERT:
                    # No line of sight -- try to find a position with LOS
                    # Use pathfinding to reach a better position
                    self._cover_timer -= dt
                    if self._cover_timer <= 0:
                        self._cover_timer = self._cover_interval
                        self._cover_pos = None  # Reset cover, find shooting position

                    # Move toward player to re-establish LOS
                    target_x, target_y, speed = ai_result
                    self._move_toward(target_x, target_y, speed)
                elif dist < self.shoot_range and has_los:
                    # In shooting range with LOS -- strafe and shoot
                    strafe_vx, strafe_vy = self._get_strafe_velocity(player, self.speed * 0.7)

                    # Also add range-maintaining component
                    dx = self.center_x - player.center_x
                    dy = self.center_y - player.center_y
                    range_dist = math.sqrt(dx * dx + dy * dy)
                    if range_dist > 0:
                        # Push toward optimal range
                        range_factor = (dist - self.optimal_range) / self.optimal_range
                        range_factor = max(-1.0, min(1.0, range_factor))
                        # Negative range_factor = too close, positive = too far
                        range_vx = -(dx / range_dist) * self.speed * 0.3 * range_factor
                        range_vy = -(dy / range_dist) * self.speed * 0.3 * range_factor
                    else:
                        range_vx, range_vy = 0, 0

                    self.vx = strafe_vx + range_vx
                    self.vy = strafe_vy + range_vy

                    # Shoot if cooldown ready
                    if self.shoot_timer <= 0:
                        self.pending_projectile = self.shoot(player)
                else:
                    # Out of shoot range -- approach using pathfinding
                    target_x, target_y, speed = ai_result
                    self._move_toward(target_x, target_y, speed)
            elif ai_result is not None:
                # LOST state -- move toward last known position
                target_x, target_y, speed = ai_result
                self._move_toward(target_x, target_y, speed)
                self._update_facing_toward(target_x, target_y)
            else:
                # IDLE state -- stay still (archers don't patrol actively)
                self.vx = 0
                self.vy = 0

        # Move with collision
        self.x += self.vx * dt
        tilemap.resolve_collision_x(self)
        self.y += self.vy * dt
        tilemap.resolve_collision_y(self)

        # Animation
        self.anim.update(dt, self.is_moving)
