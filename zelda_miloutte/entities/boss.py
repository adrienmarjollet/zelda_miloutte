import math
import pygame
from .enemy import Enemy
from ..settings import (
    BOSS_SIZE, BOSS_SPEED, BOSS_CHASE_SPEED, BOSS_CHARGE_SPEED,
    BOSS_HP, BOSS_DAMAGE, BOSS_CHARGE_DURATION, BOSS_CHARGE_COOLDOWN,
    BOSS_PHASE2_THRESHOLD, BOSS_PURPLE, TILE_SIZE,
)
from ..sounds import get_sound_manager
from ..sprites import AnimatedSprite
from ..sprites.boss_sprites import get_boss_frames_phase1, get_boss_frames_phase2
from ..sprites.effects import flash_white, scale_shrink


class Boss(Enemy):
    def __init__(self, x, y, hp=BOSS_HP, speed=BOSS_SPEED, chase_speed=BOSS_CHASE_SPEED,
                 charge_speed=BOSS_CHARGE_SPEED, damage=BOSS_DAMAGE,
                 frames_phase1_fn=None, frames_phase2_fn=None, color=BOSS_PURPLE):
        super().__init__(x, y, [])
        self.width = BOSS_SIZE
        self.height = BOSS_SIZE
        self.color = color
        self.hp = hp
        self.max_hp = hp
        self.damage = damage
        self.speed = speed
        self.chase_speed = chase_speed
        self.charge_speed = charge_speed

        # Charge attack
        self.charging = False
        self.charge_timer = 0.0
        self.charge_cooldown = 0.0
        self.charge_dx = 0.0
        self.charge_dy = 0.0

        # Phase
        self.phase = 1
        self.phase2_roar_played = False

        # Boss has shorter knockback duration
        self.knockback_duration = 0.08

        # XP value
        self.xp_value = 50

        # Boss always drops a heart (100% chance)
        self.drop_chance = 1.0
        self.drop_table = [("heart", 1)]

        # Sprites -- override the enemy's default anim
        # Use custom frame getters if provided, otherwise use default boss1 frames
        if frames_phase1_fn is None:
            frames_phase1_fn = get_boss_frames_phase1
        if frames_phase2_fn is None:
            frames_phase2_fn = get_boss_frames_phase2

        self.anim_p1 = AnimatedSprite(frames_phase1_fn(), frame_duration=0.20)
        self.anim_p2 = AnimatedSprite(frames_phase2_fn(), frame_duration=0.14)
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
        return self.hp <= self.max_hp * BOSS_PHASE2_THRESHOLD

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

        # Phase check
        if self.phase2 and self.phase == 1:
            self.phase = 2
            self.anim = self.anim_p2
            self._white_frames = self._white_p2
            if not self.phase2_roar_played:
                get_sound_manager().play_boss_roar()
                self.phase2_roar_played = True

        dist = self._distance_to(player)

        # Skip AI during knockback
        if self.knockback_timer > 0:
            self.vx = self.knockback_vx
            self.vy = self.knockback_vy
        elif self.charging:
            self.charge_timer -= dt
            self.vx = self.charge_dx * self.charge_speed
            self.vy = self.charge_dy * self.charge_speed
            if self.charge_timer <= 0:
                self.charging = False
                self.charge_cooldown = BOSS_CHARGE_COOLDOWN
                self.vx = 0
                self.vy = 0
        else:
            # Charge cooldown
            if self.charge_cooldown > 0:
                self.charge_cooldown -= dt

            # Phase 2: charge attack
            if self.phase == 2 and self.charge_cooldown <= 0 and dist < 200:
                self._start_charge(player)
            else:
                # Chase player
                self._move_toward(player.center_x, player.center_y,
                                  self.chase_speed, dt)

            # Update facing
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

    def _start_charge(self, player):
        dx = player.center_x - self.center_x
        dy = player.center_y - self.center_y
        dist = math.sqrt(dx * dx + dy * dy)
        if dist > 0:
            self.charge_dx = dx / dist
            self.charge_dy = dy / dist
        self.charging = True
        self.charge_timer = BOSS_CHARGE_DURATION

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
