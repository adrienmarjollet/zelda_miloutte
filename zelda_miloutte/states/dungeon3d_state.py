"""First-person 3D dungeon state using raycasting (Wolfenstein 3D style)."""

import math
import random
import pygame
from .state import State
from ..raycaster import Raycaster, FOV
from ..settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, RED, GOLD, BLACK,
    HEART_RED, KEY_YELLOW,
)
from ..sounds import get_sound_manager


# ── 3D Dungeon Map ──────────────────────────────────────────────────
# 0 = floor, 1 = stone wall, 2 = mossy wall, 3 = brick wall,
# 4 = boss door (purple), 5 = dark red stone
# fmt: off
DUNGEON_3D_MAP = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 2, 2, 0, 0, 2, 2, 0, 0, 0, 1, 0, 0, 3, 3, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 3, 3, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 3, 3, 0, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 2, 2, 0, 0, 2, 2, 0, 0, 0, 1, 0, 0, 3, 3, 0, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]
# fmt: on

# Player start position (tile coords, float)
PLAYER_START = (2.5, 2.5)
PLAYER_START_ANGLE = 0.0

# Exit position (tile coords) - step here to leave
EXIT_POS = (1.5, 7.5)

# Enemy definitions for the 3D dungeon
ENEMY_DEFS = [
    {"x": 10.5, "y": 5.5, "hp": 4, "damage": 1, "speed": 1.8, "color": (180, 60, 60), "size": 0.6, "xp": 15},
    {"x": 14.5, "y": 2.5, "hp": 3, "damage": 1, "speed": 2.0, "color": (60, 150, 60), "size": 0.5, "xp": 12},
    {"x": 5.5, "y": 15.5, "hp": 4, "damage": 1, "speed": 1.8, "color": (180, 60, 60), "size": 0.6, "xp": 15},
    {"x": 14.5, "y": 17.5, "hp": 3, "damage": 1, "speed": 2.0, "color": (60, 150, 60), "size": 0.5, "xp": 12},
    {"x": 21.5, "y": 5.5, "hp": 5, "damage": 2, "speed": 1.5, "color": (100, 80, 160), "size": 0.7, "xp": 20},
    {"x": 21.5, "y": 14.5, "hp": 5, "damage": 2, "speed": 1.5, "color": (100, 80, 160), "size": 0.7, "xp": 20},
]

# Boss definition
BOSS_DEF = {
    "x": 10.0, "y": 10.0, "hp": 20, "damage": 3, "speed": 1.5,
    "color": (200, 50, 200), "size": 1.0, "xp": 100,
    "charge_speed": 4.0, "charge_cooldown": 3.0,
}

# Item pickups
ITEM_DEFS = [
    {"x": 2.5, "y": 15.5, "type": "heart"},
    {"x": 21.5, "y": 1.5, "type": "heart"},
    {"x": 21.5, "y": 18.5, "type": "key"},
    {"x": 10.5, "y": 1.5, "type": "heart"},
]


class Enemy3D:
    """A simple enemy for the 3D dungeon."""

    def __init__(self, x, y, hp, damage, speed, color, size, xp):
        self.x = float(x)
        self.y = float(y)
        self.hp = hp
        self.max_hp = hp
        self.damage = damage
        self.speed = speed
        self.color = color
        self.size = size
        self.xp = xp
        self.alive = True
        self.flash_timer = 0.0
        self.attack_cooldown = 0.0
        self.state = "idle"  # idle, chase, attack
        self.detection_range = 8.0
        self.attack_range = 0.8

    def update(self, dt, px, py, map_data):
        if not self.alive:
            return

        self.flash_timer = max(0, self.flash_timer - dt)
        self.attack_cooldown = max(0, self.attack_cooldown - dt)

        # Distance to player
        dx = px - self.x
        dy = py - self.y
        dist = math.sqrt(dx * dx + dy * dy)

        if dist < self.detection_range:
            self.state = "chase"
        else:
            self.state = "idle"

        if self.state == "chase" and dist > self.attack_range:
            # Move toward player
            if dist > 0:
                move_x = (dx / dist) * self.speed * dt
                move_y = (dy / dist) * self.speed * dt

                # Check wall collision for x
                new_x = self.x + move_x
                margin = 0.2
                if not _is_wall(map_data, new_x + margin, self.y) and \
                   not _is_wall(map_data, new_x - margin, self.y):
                    self.x = new_x

                # Check wall collision for y
                new_y = self.y + move_y
                if not _is_wall(map_data, self.x, new_y + margin) and \
                   not _is_wall(map_data, self.x, new_y - margin):
                    self.y = new_y

    def take_damage(self, amount):
        self.hp -= amount
        self.flash_timer = 0.15
        if self.hp <= 0:
            self.alive = False

    def get_render_color(self):
        if self.flash_timer > 0:
            return (255, 255, 255)
        return self.color


class Boss3D(Enemy3D):
    """Boss enemy with charge attack for the 3D dungeon."""

    def __init__(self, x, y, hp, damage, speed, color, size, xp,
                 charge_speed=4.0, charge_cooldown=3.0):
        super().__init__(x, y, hp, damage, speed, color, size, xp)
        self.charge_speed = charge_speed
        self.charge_cooldown_max = charge_cooldown
        self.charge_timer = 0.0
        self.charging = False
        self.charge_dir_x = 0
        self.charge_dir_y = 0
        self.charge_duration = 0.5
        self.charge_duration_timer = 0.0
        self.detection_range = 15.0
        self.phase = 1
        self.telegraph_timer = 0.0
        self.telegraphing = False

    def update(self, dt, px, py, map_data):
        if not self.alive:
            return

        self.flash_timer = max(0, self.flash_timer - dt)
        self.attack_cooldown = max(0, self.attack_cooldown - dt)
        self.charge_timer = max(0, self.charge_timer - dt)

        # Phase 2 at half health
        if self.hp <= self.max_hp // 2 and self.phase == 1:
            self.phase = 2
            self.speed *= 1.3
            self.charge_speed *= 1.3
            self.charge_cooldown_max *= 0.7

        dx = px - self.x
        dy = py - self.y
        dist = math.sqrt(dx * dx + dy * dy)

        if self.charging:
            # Execute charge
            self.charge_duration_timer -= dt
            move_x = self.charge_dir_x * self.charge_speed * dt
            move_y = self.charge_dir_y * self.charge_speed * dt

            new_x = self.x + move_x
            new_y = self.y + move_y
            margin = 0.3

            hit_wall = False
            if _is_wall(map_data, new_x + margin, self.y) or \
               _is_wall(map_data, new_x - margin, self.y):
                hit_wall = True
            else:
                self.x = new_x

            if _is_wall(map_data, self.x, new_y + margin) or \
               _is_wall(map_data, self.x, new_y - margin):
                hit_wall = True
            else:
                self.y = new_y

            if self.charge_duration_timer <= 0 or hit_wall:
                self.charging = False
                self.charge_timer = self.charge_cooldown_max

        elif self.telegraphing:
            self.telegraph_timer -= dt
            if self.telegraph_timer <= 0:
                self.telegraphing = False
                self.charging = True
                self.charge_duration_timer = self.charge_duration
                if dist > 0:
                    self.charge_dir_x = dx / dist
                    self.charge_dir_y = dy / dist

        elif dist < self.detection_range:
            # Try to initiate charge
            if self.charge_timer <= 0 and dist > 2.0:
                self.telegraphing = True
                self.telegraph_timer = 0.6
            elif dist > self.attack_range:
                # Normal chase
                if dist > 0:
                    move_x = (dx / dist) * self.speed * dt
                    move_y = (dy / dist) * self.speed * dt

                    new_x = self.x + move_x
                    margin = 0.3
                    if not _is_wall(map_data, new_x + margin, self.y) and \
                       not _is_wall(map_data, new_x - margin, self.y):
                        self.x = new_x

                    new_y = self.y + move_y
                    if not _is_wall(map_data, self.x, new_y + margin) and \
                       not _is_wall(map_data, self.x, new_y - margin):
                        self.y = new_y

    def get_render_color(self):
        if self.flash_timer > 0:
            return (255, 255, 255)
        if self.telegraphing:
            # Flash red when about to charge
            return (255, 50, 50) if int(self.telegraph_timer * 10) % 2 == 0 else self.color
        if self.phase == 2:
            return tuple(min(255, c + 40) for c in self.color)
        return self.color


class Item3D:
    """A pickup item in the 3D dungeon."""

    def __init__(self, x, y, item_type):
        self.x = float(x)
        self.y = float(y)
        self.type = item_type
        self.alive = True
        self.bob_timer = random.random() * math.pi * 2

        if item_type == "heart":
            self.color = (220, 50, 60)
            self.size = 0.3
        elif item_type == "key":
            self.color = (255, 215, 0)
            self.size = 0.3
        else:
            self.color = (200, 200, 200)
            self.size = 0.25

    def update(self, dt):
        self.bob_timer += dt * 3


def _is_wall(map_data, x, y):
    """Check if a tile position is a wall."""
    col = int(x)
    row = int(y)
    if row < 0 or row >= len(map_data) or col < 0 or col >= len(map_data[0]):
        return True
    return map_data[row][col] > 0


class Dungeon3DState(State):
    """First-person 3D dungeon exploration using raycasting."""

    def __init__(self, game, play_state):
        super().__init__(game)
        self.play_state = play_state
        self.map_data = [row[:] for row in DUNGEON_3D_MAP]

        # Raycaster
        self.raycaster = Raycaster(self.map_data)

        # Player state
        self.px, self.py = PLAYER_START
        self.angle = PLAYER_START_ANGLE
        self.move_speed = 3.0
        self.rot_speed = 2.5
        self.player_hp = play_state.player.hp
        self.player_max_hp = play_state.player.max_hp
        self.player_keys = play_state.player.keys

        # Invincibility
        self.invincible = False
        self.invincible_timer = 0.0
        self.blink_timer = 0.0

        # Attack state
        self.attacking = False
        self.attack_timer = 0.0
        self.attack_cooldown = 0.0
        self.attack_duration = 0.25
        self.attack_cooldown_max = 0.4
        self.attack_range = 1.5
        self.attack_cone = math.pi / 3  # 60 degree cone

        # Sword swing animation
        self.sword_swing_timer = 0.0

        # Enemies
        self.enemies = []
        for edef in ENEMY_DEFS:
            self.enemies.append(Enemy3D(**edef))

        # Boss
        self.boss = Boss3D(**BOSS_DEF)
        self.boss_defeated = False
        self.victory = False
        self.victory_timer = 0.0

        # Items
        self.items = []
        for idef in ITEM_DEFS:
            self.items.append(Item3D(idef["x"], idef["y"], idef["type"]))

        # Screen effects
        self.damage_flash = 0.0
        self.screen_shake = 0.0
        self.shake_intensity = 0

        # XP tracking
        self.xp_gained = 0

        # Fonts
        self.hud_font = None
        self.large_font = None

        # Boss intro
        self._boss_intro_shown = False

    def enter(self):
        get_sound_manager().play_music('boss')

    def _copy_stats_back(self):
        """Copy player stats back to the overworld player."""
        self.play_state.player.hp = self.player_hp
        self.play_state.player.keys = self.player_keys
        # Apply XP
        self.play_state.player.gain_xp(self.xp_gained)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # Return to overworld
                def exit_dungeon():
                    self._copy_stats_back()
                    self.game.pop_state()
                self.game.transition_to(exit_dungeon)

    def update(self, dt):
        if self.victory:
            self.victory_timer += dt
            if self.victory_timer >= 3.0:
                def return_to_overworld():
                    self._copy_stats_back()
                    self.game.pop_state()
                self.game.transition_to(return_to_overworld)
            return

        # Check death
        if self.player_hp <= 0:
            def show_game_over():
                from .gameover_state import GameOverState
                self.game.change_state(GameOverState(self.game))
            self.game.transition_to(show_game_over)
            return

        inp = self.game.input

        # ── Movement ──
        # Rotation with left/right
        if inp.move_x < 0:
            self.angle -= self.rot_speed * dt
        elif inp.move_x > 0:
            self.angle += self.rot_speed * dt

        # Forward/backward with up/down
        cos_a = math.cos(self.angle)
        sin_a = math.sin(self.angle)
        move = 0.0
        if inp.move_y < 0:
            move = self.move_speed * dt
        elif inp.move_y > 0:
            move = -self.move_speed * dt

        if move != 0:
            new_x = self.px + cos_a * move
            new_y = self.py + sin_a * move
            margin = 0.2

            # Slide along walls
            if not _is_wall(self.map_data, new_x + margin, self.py) and \
               not _is_wall(self.map_data, new_x - margin, self.py):
                self.px = new_x

            if not _is_wall(self.map_data, self.px, new_y + margin) and \
               not _is_wall(self.map_data, self.px, new_y - margin):
                self.py = new_y

        # ── Attack ──
        self.attack_cooldown = max(0, self.attack_cooldown - dt)
        if inp.attack and self.attack_cooldown <= 0 and not self.attacking:
            self.attacking = True
            self.attack_timer = self.attack_duration
            self.attack_cooldown = self.attack_cooldown_max
            self.sword_swing_timer = self.attack_duration
            get_sound_manager().play_sword_swing()
            self._do_attack()

        if self.attacking:
            self.attack_timer -= dt
            if self.attack_timer <= 0:
                self.attacking = False

        self.sword_swing_timer = max(0, self.sword_swing_timer - dt)

        # ── Update invincibility ──
        if self.invincible:
            self.invincible_timer -= dt
            self.blink_timer += dt
            if self.invincible_timer <= 0:
                self.invincible = False
                self.invincible_timer = 0
                self.blink_timer = 0

        # ── Update enemies ──
        for enemy in self.enemies:
            enemy.update(dt, self.px, self.py, self.map_data)
            if enemy.alive:
                self._check_enemy_collision(enemy)

        # Remove dead enemies
        for enemy in self.enemies:
            if not enemy.alive and enemy.hp <= 0:
                self.xp_gained += enemy.xp
        self.enemies = [e for e in self.enemies if e.alive]

        # ── Update boss ──
        if self.boss.alive:
            self.boss.update(dt, self.px, self.py, self.map_data)
            self._check_enemy_collision(self.boss)

            if not self.boss.alive:
                self.boss_defeated = True
                self.xp_gained += self.boss.xp
                self.victory = True
                self.victory_timer = 0
                self._trigger_shake(12, 0.8)
                get_sound_manager().play_victory_fanfare()
                get_sound_manager().stop_music()

        # ── Update items ──
        for item in self.items:
            item.update(dt)
            if item.alive:
                dx = self.px - item.x
                dy = self.py - item.y
                dist = math.sqrt(dx * dx + dy * dy)
                if dist < 0.5:
                    self._pickup_item(item)

        self.items = [i for i in self.items if i.alive]

        # ── Check exit ──
        ex, ey = EXIT_POS
        dist_to_exit = math.sqrt((self.px - ex) ** 2 + (self.py - ey) ** 2)
        if dist_to_exit < 0.7:
            def exit_dungeon():
                self._copy_stats_back()
                self.game.pop_state()
            self.game.transition_to(exit_dungeon)
            return

        # ── Update effects ──
        self.damage_flash = max(0, self.damage_flash - dt * 4)
        self.screen_shake = max(0, self.screen_shake - dt)

    def _do_attack(self):
        """Check enemies in attack cone and deal damage."""
        cos_a = math.cos(self.angle)
        sin_a = math.sin(self.angle)

        targets = list(self.enemies)
        if self.boss.alive:
            targets.append(self.boss)

        for enemy in targets:
            if not enemy.alive:
                continue

            dx = enemy.x - self.px
            dy = enemy.y - self.py
            dist = math.sqrt(dx * dx + dy * dy)

            if dist > self.attack_range:
                continue

            # Check if enemy is within attack cone
            enemy_angle = math.atan2(dy, dx)
            angle_diff = enemy_angle - self.angle
            while angle_diff > math.pi:
                angle_diff -= 2 * math.pi
            while angle_diff < -math.pi:
                angle_diff += 2 * math.pi

            if abs(angle_diff) < self.attack_cone / 2:
                enemy.take_damage(1)
                self._trigger_shake(3, 0.1)

    def _check_enemy_collision(self, enemy):
        """Check if enemy is touching the player and deal damage."""
        if not enemy.alive:
            return

        dx = self.px - enemy.x
        dy = self.py - enemy.y
        dist = math.sqrt(dx * dx + dy * dy)

        collision_dist = 0.5 + enemy.size * 0.3
        if dist < collision_dist and not self.invincible:
            self.player_hp -= enemy.damage
            self.invincible = True
            self.invincible_timer = 1.0
            self.damage_flash = 1.0
            self._trigger_shake(5, 0.3)

            # Push player away
            if dist > 0.01:
                push = 0.5
                self.px += (dx / dist) * push
                self.py += (dy / dist) * push
                # Clamp to valid position
                margin = 0.2
                if _is_wall(self.map_data, self.px + margin, self.py) or \
                   _is_wall(self.map_data, self.px - margin, self.py):
                    self.px -= (dx / dist) * push
                if _is_wall(self.map_data, self.px, self.py + margin) or \
                   _is_wall(self.map_data, self.px, self.py - margin):
                    self.py -= (dy / dist) * push

    def _pickup_item(self, item):
        """Pick up an item."""
        if item.type == "heart":
            self.player_hp = min(self.player_hp + 2, self.player_max_hp)
        elif item.type == "key":
            self.player_keys += 1
        item.alive = False

    def _trigger_shake(self, intensity, duration):
        self.shake_intensity = intensity
        self.screen_shake = duration

    def draw(self, surface):
        if self.hud_font is None:
            self.hud_font = pygame.font.Font(None, 28)
            self.large_font = pygame.font.Font(None, 48)

        # Calculate screen shake offset
        shake_x = 0
        shake_y = 0
        if self.screen_shake > 0:
            shake_x = random.randint(-self.shake_intensity, self.shake_intensity)
            shake_y = random.randint(-self.shake_intensity, self.shake_intensity)

        # Build sprite list for raycaster
        sprites = []

        # Enemies
        for enemy in self.enemies:
            if enemy.alive:
                hp_ratio = enemy.hp / enemy.max_hp if enemy.max_hp > 0 else 1.0
                sprites.append((
                    enemy.x, enemy.y,
                    enemy.get_render_color(),
                    enemy.size,
                    None,  # no sprite surface
                    hp_ratio,
                ))

        # Boss
        if self.boss.alive:
            hp_ratio = self.boss.hp / self.boss.max_hp if self.boss.max_hp > 0 else 1.0
            sprites.append((
                self.boss.x, self.boss.y,
                self.boss.get_render_color(),
                self.boss.size,
                None,
                hp_ratio,
            ))

        # Items
        for item in self.items:
            if item.alive:
                # Bob items up and down
                sprites.append((
                    item.x, item.y,
                    item.color,
                    item.size,
                    None,
                    None,
                ))

        # Render 3D view
        if shake_x != 0 or shake_y != 0:
            temp = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.raycaster.render(temp, self.px, self.py, self.angle, sprites)
            surface.fill(BLACK)
            surface.blit(temp, (shake_x, shake_y))
        else:
            self.raycaster.render(surface, self.px, self.py, self.angle, sprites)

        # Minimap
        enemy_data = [{"x": e.x, "y": e.y, "alive": e.alive} for e in self.enemies]
        if self.boss.alive:
            enemy_data.append({"x": self.boss.x, "y": self.boss.y, "alive": True})
        item_data = [{"x": i.x, "y": i.y, "alive": i.alive} for i in self.items]
        self.raycaster.draw_minimap(surface, self.px, self.py, self.angle, enemy_data, item_data)

        # Sword swing overlay
        if self.sword_swing_timer > 0:
            self._draw_sword_swing(surface)

        # Damage flash overlay
        if self.damage_flash > 0:
            flash_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            alpha = int(self.damage_flash * 120)
            flash_surf.fill((200, 0, 0, alpha))
            surface.blit(flash_surf, (0, 0))

        # Invincibility blink indicator
        if self.invincible and int(self.blink_timer * 10) % 2 == 0:
            indicator = pygame.Surface((SCREEN_WIDTH, 4), pygame.SRCALPHA)
            indicator.fill((255, 255, 255, 80))
            surface.blit(indicator, (0, SCREEN_HEIGHT // 2 - 2))

        # HUD
        self._draw_hud(surface)

        # Boss health bar
        if self.boss.alive:
            self._draw_boss_bar(surface)

        # Victory overlay
        if self.victory:
            self._draw_victory(surface)

        # Crosshair
        cx, cy = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        crosshair_color = (200, 200, 200, 150)
        cs = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.line(cs, crosshair_color, (10, 4), (10, 8), 1)
        pygame.draw.line(cs, crosshair_color, (10, 12), (10, 16), 1)
        pygame.draw.line(cs, crosshair_color, (4, 10), (8, 10), 1)
        pygame.draw.line(cs, crosshair_color, (12, 10), (16, 10), 1)
        surface.blit(cs, (cx - 10, cy - 10))

    def _draw_sword_swing(self, surface):
        """Draw a sword swing arc across the screen."""
        t = 1.0 - (self.sword_swing_timer / self.attack_duration)
        swing_angle = -60 + t * 120  # Sweep from -60 to +60 degrees

        cx = SCREEN_WIDTH // 2
        cy = SCREEN_HEIGHT - 80
        length = 120

        rad = math.radians(swing_angle - 90)
        end_x = cx + int(math.cos(rad) * length)
        end_y = cy + int(math.sin(rad) * length)

        # Sword blade
        color = (200, 200, 220)
        pygame.draw.line(surface, color, (cx, cy), (end_x, end_y), 4)
        # Sword glow
        glow_color = (255, 255, 180, int(100 * (1 - t)))
        glow_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        pygame.draw.line(glow_surf, glow_color, (cx, cy), (end_x, end_y), 8)
        surface.blit(glow_surf, (0, 0))

        # Handle
        handle_end_x = cx + int(math.cos(rad) * (-20))
        handle_end_y = cy + int(math.sin(rad) * (-20))
        pygame.draw.line(surface, (120, 80, 40), (cx, cy), (handle_end_x, handle_end_y), 6)

    def _draw_hud(self, surface):
        """Draw hearts, keys, and controls info."""
        # Background bar
        hud_bg = pygame.Surface((SCREEN_WIDTH, 40), pygame.SRCALPHA)
        hud_bg.fill((0, 0, 0, 160))
        surface.blit(hud_bg, (0, 0))

        # Hearts
        x = 8
        y = 8
        heart_size = 20
        for i in range(self.player_max_hp // 2):
            hp_for_heart = (i + 1) * 2
            if self.player_hp >= hp_for_heart:
                # Full heart
                pygame.draw.polygon(surface, HEART_RED, [
                    (x + heart_size // 2, y + heart_size - 4),
                    (x + 2, y + heart_size // 3),
                    (x + heart_size // 4, y + 2),
                    (x + heart_size // 2, y + heart_size // 4),
                    (x + 3 * heart_size // 4, y + 2),
                    (x + heart_size - 2, y + heart_size // 3),
                ])
            elif self.player_hp >= hp_for_heart - 1:
                # Half heart
                pygame.draw.polygon(surface, HEART_RED, [
                    (x + heart_size // 2, y + heart_size - 4),
                    (x + 2, y + heart_size // 3),
                    (x + heart_size // 4, y + 2),
                    (x + heart_size // 2, y + heart_size // 4),
                ])
                pygame.draw.polygon(surface, (80, 80, 80), [
                    (x + heart_size // 2, y + heart_size - 4),
                    (x + heart_size // 2, y + heart_size // 4),
                    (x + 3 * heart_size // 4, y + 2),
                    (x + heart_size - 2, y + heart_size // 3),
                ])
            else:
                # Empty heart
                pygame.draw.polygon(surface, (80, 80, 80), [
                    (x + heart_size // 2, y + heart_size - 4),
                    (x + 2, y + heart_size // 3),
                    (x + heart_size // 4, y + 2),
                    (x + heart_size // 2, y + heart_size // 4),
                    (x + 3 * heart_size // 4, y + 2),
                    (x + heart_size - 2, y + heart_size // 3),
                ])
            x += heart_size + 4

        # Keys
        key_text = self.hud_font.render(f"Keys: {self.player_keys}", True, KEY_YELLOW)
        surface.blit(key_text, (x + 10, 10))

        # Controls hint (bottom of screen)
        controls_bg = pygame.Surface((SCREEN_WIDTH, 24), pygame.SRCALPHA)
        controls_bg.fill((0, 0, 0, 120))
        surface.blit(controls_bg, (0, SCREEN_HEIGHT - 24))
        controls_font = pygame.font.Font(None, 20)
        controls = controls_font.render(
            "Arrow keys: Move/Turn | SPACE: Attack | ESC: Exit",
            True, (180, 180, 180)
        )
        surface.blit(controls, (SCREEN_WIDTH // 2 - controls.get_width() // 2, SCREEN_HEIGHT - 20))

    def _draw_boss_bar(self, surface):
        """Draw the boss health bar."""
        bar_w = 300
        bar_h = 16
        x = (SCREEN_WIDTH - bar_w) // 2
        y = 50

        # Label
        label = self.hud_font.render("Phantom Lord", True, (200, 50, 200))
        surface.blit(label, (SCREEN_WIDTH // 2 - label.get_width() // 2, y - 22))

        # Background
        pygame.draw.rect(surface, (40, 40, 40), (x - 1, y - 1, bar_w + 2, bar_h + 2))

        # Health fill
        hp_ratio = self.boss.hp / self.boss.max_hp
        fill_w = int(bar_w * hp_ratio)
        bar_color = (200, 50, 200) if self.boss.phase == 1 else (255, 80, 80)
        pygame.draw.rect(surface, bar_color, (x, y, fill_w, bar_h))

        # Border
        pygame.draw.rect(surface, (200, 200, 200), (x - 1, y - 1, bar_w + 2, bar_h + 2), 1)

    def _draw_victory(self, surface):
        """Draw victory overlay."""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        alpha = min(180, int(self.victory_timer / 3.0 * 180))
        overlay.fill((0, 0, 0, alpha))
        surface.blit(overlay, (0, 0))

        text = self.large_font.render("Victory!", True, GOLD)
        surface.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - 30))

        sub = self.hud_font.render("The Phantom Lord is vanquished!", True, WHITE)
        surface.blit(sub, (SCREEN_WIDTH // 2 - sub.get_width() // 2, SCREEN_HEIGHT // 2 + 20))
