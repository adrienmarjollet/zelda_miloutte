import math
import random
import pygame
from .entity import Entity
from ..settings import (
    ENEMY_SIZE, ENEMY_SPEED, ENEMY_CHASE_SPEED, ENEMY_CHASE_RANGE,
    ENEMY_HP, ENEMY_DAMAGE, ENEMY_PATROL_PAUSE, RED, TILE_SIZE,
    ENEMY_TELEGRAPH_TIME, ENEMY_WINDUP_PULLBACK,
)
from ..sounds import get_sound_manager
from ..sprites import AnimatedSprite
from ..sprites.enemy_sprites import get_enemy_frames
from ..sprites.effects import flash_white, scale_shrink
from ..ai_state import EnemyAI


class Enemy(Entity, EnemyAI):
    def __init__(self, x, y, patrol_points=None):
        super().__init__(x, y, ENEMY_SIZE, ENEMY_SIZE, RED)
        self.hp = ENEMY_HP
        self.max_hp = ENEMY_HP
        self.damage = ENEMY_DAMAGE
        self.speed = ENEMY_SPEED
        self.chase_speed = ENEMY_CHASE_SPEED
        self.chase_range = ENEMY_CHASE_RANGE

        # Patrol
        if patrol_points and len(patrol_points) >= 2:
            self.patrol_points = [(p[0] * TILE_SIZE, p[1] * TILE_SIZE) for p in patrol_points]
        else:
            self.patrol_points = [(x, y)]
        self.patrol_index = 0
        self.patrol_pause = 0.0

        # Damage flash
        self.flash_timer = 0.0
        self.flash_duration = 0.15

        # Attack telegraph (wind-up before lunge)
        self.telegraph_timer = 0.0
        self.telegraphing = False
        self._telegraph_target_x = 0.0
        self._telegraph_target_y = 0.0
        self._lunge_timer = 0.0
        self._lunging = False

        # Death animation
        self.death_timer = 0.0
        self.death_duration = 0.3
        self.dying = False

        # XP value
        self.xp_value = 10

        # Drop system
        self.drop_chance = 0.3  # 30% chance to drop an item
        self.drop_table = [("heart", 3), ("key", 1)]  # hearts 3x more likely than keys

        # Gold drop
        self.gold_drop_chance = 0.6  # 60% chance to drop gold
        self.gold_drop_range = (1, 5)  # min/max gold amount

        # Sprites
        self.anim = AnimatedSprite(get_enemy_frames(), frame_duration=0.18)
        self._white_frames = {
            d: [flash_white(f) for f in frames]
            for d, frames in self.anim.frames.items()
        }

        # Initialize smart AI
        self.init_ai(
            detection_range=ENEMY_CHASE_RANGE,
            lose_range=ENEMY_CHASE_RANGE * 2.0,
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
        # Check if a drop happens
        if random.random() > self.drop_chance:
            return None

        # Use weighted random choice to pick which item
        items = [item_type for item_type, weight in self.drop_table]
        weights = [weight for item_type, weight in self.drop_table]
        return random.choices(items, weights=weights, k=1)[0]

    def get_gold_drop(self):
        """Determine if the enemy drops gold and how much.
        Returns gold amount (int) or 0.
        """
        if random.random() > self.gold_drop_chance:
            return 0
        return random.randint(self.gold_drop_range[0], self.gold_drop_range[1])

    def _distance_to(self, target):
        dx = target.center_x - self.center_x
        dy = target.center_y - self.center_y
        return math.sqrt(dx * dx + dy * dy)

    def _distance_to_point(self, tx, ty):
        dx = tx - self.center_x
        dy = ty - self.center_y
        return math.sqrt(dx * dx + dy * dy)

    def _move_toward(self, tx, ty, speed, dt=None):
        dx = tx - self.center_x
        dy = ty - self.center_y
        dist = math.sqrt(dx * dx + dy * dy)
        if dist < 2:
            self.vx = 0
            self.vy = 0
            return True  # Arrived
        self.vx = (dx / dist) * speed
        self.vy = (dy / dist) * speed
        return False

    def _update_facing_toward(self, tx, ty):
        """Update facing direction toward a target position."""
        dx = tx - self.center_x
        dy = ty - self.center_y
        if abs(dx) > abs(dy):
            self.facing = "right" if dx > 0 else "left"
        else:
            self.facing = "down" if dy > 0 else "up"

    def _do_patrol(self, dt):
        """Execute patrol behavior (idle state)."""
        if self.patrol_pause > 0:
            self.patrol_pause -= dt
            self.vx = 0
            self.vy = 0
        else:
            target = self.patrol_points[self.patrol_index]
            arrived = self._move_toward(target[0], target[1], self.speed)
            if arrived:
                self.patrol_index = (self.patrol_index + 1) % len(self.patrol_points)
                self.patrol_pause = ENEMY_PATROL_PAUSE

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

        # Stun timer (from parry)
        if not hasattr(self, 'stun_timer'):
            self.stun_timer = 0.0
        if self.stun_timer > 0:
            self.stun_timer -= dt
            self.vx = 0
            self.vy = 0
            # Move with collision (for knockback during stun)
            self.x += self.vx * dt
            tilemap.resolve_collision_x(self)
            self.y += self.vy * dt
            tilemap.resolve_collision_y(self)
            self.anim.update(dt, False)
            return

        # Skip AI during knockback
        if self.knockback_timer > 0:
            self.vx = self.knockback_vx
            self.vy = self.knockback_vy
        elif self._lunging:
            # Post-telegraph lunge: fast dash toward player
            self._lunge_timer -= dt
            if self._lunge_timer <= 0:
                self._lunging = False
                self.vx = 0
                self.vy = 0
        elif self.telegraphing:
            # Wind-up pause: enemy stops, pulls back slightly
            self.telegraph_timer -= dt
            self.vx = 0
            self.vy = 0
            if self.telegraph_timer <= 0:
                self.telegraphing = False
                # Lunge toward player
                self._lunging = True
                self._lunge_timer = 0.2
                dist = self._distance_to_point(self._telegraph_target_x, self._telegraph_target_y)
                if dist > 0:
                    dx = self._telegraph_target_x - self.center_x
                    dy = self._telegraph_target_y - self.center_y
                    lunge_speed = self.chase_speed * 2.5
                    self.vx = (dx / dist) * lunge_speed
                    self.vy = (dy / dist) * lunge_speed
        else:
            # Use smart AI state machine
            ai_result = self.update_ai(dt, player, tilemap)

            if ai_result is not None:
                target_x, target_y, speed = ai_result
                self._move_toward(target_x, target_y, speed)
                self._update_facing_toward(target_x, target_y)

                # Trigger telegraph when close enough and in ALERT state
                from ..ai_state import AlertState
                if (hasattr(self, 'ai_state') and self.ai_state == AlertState.ALERT
                        and self._distance_to(player) < 60
                        and not self.telegraphing and not self._lunging):
                    self.telegraphing = True
                    self.telegraph_timer = ENEMY_TELEGRAPH_TIME
                    self._telegraph_target_x = player.center_x
                    self._telegraph_target_y = player.center_y
                    self._update_facing_toward(player.center_x, player.center_y)
            else:
                # AI returned None -- do patrol
                self._do_patrol(dt)

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

        # Telegraph visual: red pulsing tint and pull-back offset
        if self.telegraphing:
            # Pulsing red overlay
            pulse = abs(math.sin(self.telegraph_timer * 12))
            tint_surf = frame.copy()
            red_overlay = pygame.Surface(tint_surf.get_size(), pygame.SRCALPHA)
            red_overlay.fill((255, 40, 40, int(80 * pulse)))
            tint_surf.blit(red_overlay, (0, 0))
            # Pull back slightly
            pb = ENEMY_WINDUP_PULLBACK * (self.telegraph_timer / ENEMY_TELEGRAPH_TIME)
            if self.facing == "up":
                fy += pb
            elif self.facing == "down":
                fy -= pb
            elif self.facing == "left":
                fx += pb
            elif self.facing == "right":
                fx -= pb
            surface.blit(tint_surf, (fx, fy))
        else:
            surface.blit(frame, (fx, fy))

        # Draw alert state icon
        self.draw_alert_icon(surface, camera)
