import math
import random
import pygame
from .enemy import Enemy
from ..settings import (
    BOSS_SIZE, BOSS_SPEED, BOSS_CHASE_SPEED, BOSS_CHARGE_SPEED,
    BOSS_HP, BOSS_DAMAGE, BOSS_CHARGE_DURATION, BOSS_CHARGE_COOLDOWN,
    BOSS_PHASE2_THRESHOLD, BOSS_PURPLE, TILE_SIZE,
    ENEMY_TELEGRAPH_TIME, PROJECTILE_SPEED,
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

        # Boss charge telegraph
        self.charge_telegraphing = False
        self.charge_telegraph_timer = 0.0
        self._charge_target_player = None

        # Slam attack (AoE shockwave)
        self.slamming = False
        self.slam_timer = 0.0
        self.slam_cooldown = 0.0
        self.slam_radius = 80
        self.slam_hit = False  # single-hit per slam
        self.pending_shockwave = None  # (cx, cy, radius) for gameplay_state

        # Projectile barrage
        self.barrage_cooldown = 0.0
        self.pending_projectiles = []  # collected by gameplay_state

        # Summon minions
        self.summon_cooldown = 0.0
        self.pending_summons = []  # (x, y) positions for gameplay_state to spawn

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

        # Update cooldowns
        if self.slam_cooldown > 0:
            self.slam_cooldown -= dt
        if self.barrage_cooldown > 0:
            self.barrage_cooldown -= dt
        if self.summon_cooldown > 0:
            self.summon_cooldown -= dt

        # Clear pending actions
        self.pending_shockwave = None
        self.pending_projectiles = []
        self.pending_summons = []

        # Skip AI during knockback
        if self.knockback_timer > 0:
            self.vx = self.knockback_vx
            self.vy = self.knockback_vy
        elif self.slamming:
            # Slam in progress: pause, then release shockwave
            self.slam_timer -= dt
            self.vx = 0
            self.vy = 0
            if self.slam_timer <= 0:
                self.slamming = False
                self.slam_cooldown = 4.0
                # Emit shockwave
                self.pending_shockwave = (self.center_x, self.center_y, self.slam_radius)
        elif self.charge_telegraphing:
            # Boss pauses before charge, shaking/pulsing
            self.charge_telegraph_timer -= dt
            self.vx = 0
            self.vy = 0
            if self.charge_telegraph_timer <= 0:
                self.charge_telegraphing = False
                if self._charge_target_player is not None:
                    self._start_charge(self._charge_target_player)
                    self._charge_target_player = None
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

            # Phase 2: choose attack pattern
            if self.phase == 2:
                attack_chosen = False

                # Slam attack when player is close
                if not attack_chosen and self.slam_cooldown <= 0 and dist < 70:
                    self._start_slam()
                    attack_chosen = True

                # Charge attack at medium range
                if not attack_chosen and self.charge_cooldown <= 0 and dist < 200:
                    self.charge_telegraphing = True
                    self.charge_telegraph_timer = ENEMY_TELEGRAPH_TIME * 0.8
                    self._charge_target_player = player
                    attack_chosen = True

                # Projectile barrage at range
                if not attack_chosen and self.barrage_cooldown <= 0 and dist > 100:
                    self._fire_barrage(player)
                    attack_chosen = True

                # Summon minions periodically
                if self.summon_cooldown <= 0 and dist > 60:
                    self._summon_minions()

                if not attack_chosen:
                    self._move_toward(player.center_x, player.center_y,
                                      self.chase_speed, dt)
            else:
                # Phase 1: just chase
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

    def _start_slam(self):
        """Start a ground slam (AoE shockwave)."""
        self.slamming = True
        self.slam_timer = 0.4  # wind-up before impact
        self.slam_hit = False

    def _fire_barrage(self, player):
        """Fire a spread of projectiles toward the player."""
        from .projectile import Projectile
        self.barrage_cooldown = 5.0
        num_shots = 5
        spread_angle = math.pi / 4  # 45 degree spread
        dx = player.center_x - self.center_x
        dy = player.center_y - self.center_y
        base_angle = math.atan2(dy, dx)

        for i in range(num_shots):
            angle = base_angle + spread_angle * (i / (num_shots - 1) - 0.5)
            target_x = self.center_x + math.cos(angle) * 200
            target_y = self.center_y + math.sin(angle) * 200
            proj = Projectile(
                self.center_x, self.center_y,
                target_x, target_y,
                self.damage, speed=PROJECTILE_SPEED * 0.8
            )
            self.pending_projectiles.append(proj)

    def _summon_minions(self):
        """Queue minion spawn positions around the boss."""
        self.summon_cooldown = 12.0
        num_minions = 2
        for i in range(num_minions):
            angle = random.uniform(0, 2 * math.pi)
            dist = random.randint(60, 100)
            sx = self.center_x + math.cos(angle) * dist
            sy = self.center_y + math.sin(angle) * dist
            self.pending_summons.append((sx, sy))

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

        # Slam telegraph visual: growing orange ring
        if self.slamming:
            progress = 1.0 - (self.slam_timer / 0.4)
            ring_r = int(self.slam_radius * progress)
            if ring_r > 4:
                ring_surf = pygame.Surface((ring_r * 2, ring_r * 2), pygame.SRCALPHA)
                alpha = int(150 * (1.0 - progress))
                pygame.draw.circle(ring_surf, (255, 150, 50, alpha), (ring_r, ring_r), ring_r, 3)
                surface.blit(ring_surf, (r.centerx - ring_r, r.centery - ring_r))

        # Boss charge telegraph visual: shake and red pulse
        if self.charge_telegraphing:
            import math as _math
            pulse = abs(_math.sin(self.charge_telegraph_timer * 15))
            tint_surf = frame.copy()
            red_overlay = pygame.Surface(tint_surf.get_size(), pygame.SRCALPHA)
            red_overlay.fill((255, 30, 30, int(100 * pulse)))
            tint_surf.blit(red_overlay, (0, 0))
            # Shake offset
            import random as _random
            shake_x = _random.randint(-3, 3)
            shake_y = _random.randint(-3, 3)
            surface.blit(tint_surf, (fx + shake_x, fy + shake_y))
        else:
            surface.blit(frame, (fx, fy))
