"""Special abilities and magic system for the player."""

import math
import pygame
from .settings import TILE_SIZE, PLAYER_SPEED, PROJECTILE_SPEED
from .entities.projectile import Projectile
from .sprites.ability_sprites import (
    create_spin_arc_surface,
    create_fireball_surface,
    create_shield_bubble_surface,
    create_dash_afterimage,
)


class Ability:
    """Base class for player abilities."""

    name = "ability"
    display_name = "Ability"
    mp_cost = 0
    cooldown_time = 1.0  # seconds

    def __init__(self):
        self.cooldown_timer = 0.0
        self.active = False
        self.active_timer = 0.0

    @property
    def ready(self):
        return self.cooldown_timer <= 0 and not self.active

    def can_use(self, player):
        """Check if the ability can be used (enough MP and off cooldown)."""
        return self.ready and player.mp >= self.mp_cost

    def use(self, player, enemies, projectiles, particles, camera):
        """Activate the ability. Returns True if successfully used."""
        if not self.can_use(player):
            return False
        player.mp -= self.mp_cost
        self.cooldown_timer = self.cooldown_time
        self.active = True
        self._activate(player, enemies, projectiles, particles, camera)
        return True

    def _activate(self, player, enemies, projectiles, particles, camera):
        """Override in subclasses for ability-specific activation logic."""
        pass

    def update(self, dt, player, enemies, projectiles, particles):
        """Update ability state each frame."""
        if self.cooldown_timer > 0:
            self.cooldown_timer -= dt
        if self.active:
            self.active_timer -= dt
            self._update_active(dt, player, enemies, projectiles, particles)
            if self.active_timer <= 0:
                self.active = False
                self._deactivate(player)

    def _update_active(self, dt, player, enemies, projectiles, particles):
        """Override for per-frame active logic."""
        pass

    def _deactivate(self, player):
        """Override for cleanup when ability ends."""
        pass

    def draw(self, surface, camera, player):
        """Override for visual effects while active."""
        pass


class SpinAttack(Ability):
    """AoE sword spin around player, damages all nearby enemies."""

    name = "spin_attack"
    display_name = "Spin Attack"
    mp_cost = 20
    cooldown_time = 2.0

    SPIN_RADIUS = 50  # pixels
    SPIN_DURATION = 0.4  # seconds
    SPIN_DAMAGE_MULTIPLIER = 1.5

    def __init__(self):
        super().__init__()
        self._spin_surface = None
        self._hit_enemies = set()
        self._spin_angle = 0.0

    def _activate(self, player, enemies, projectiles, particles, camera):
        self.active_timer = self.SPIN_DURATION
        self._hit_enemies = set()
        self._spin_angle = 0.0
        if self._spin_surface is None:
            self._spin_surface = create_spin_arc_surface()
        # Emit spin particles
        particles.emit(
            player.center_x, player.center_y,
            count=16,
            color=[(220, 230, 255), (180, 200, 240), (255, 255, 255)],
            speed_range=(80, 150),
            lifetime_range=(0.2, 0.4),
            size_range=(2, 5),
            gravity=0,
        )
        # Camera shake
        camera.shake(4, 0.3)
        # Play sound
        from .sounds import get_sound_manager
        get_sound_manager().play_ability_spin()

    def _update_active(self, dt, player, enemies, projectiles, particles):
        self._spin_angle += dt * 720  # 2 full rotations over duration
        # Damage enemies within radius
        damage = int(player.attack_power * self.SPIN_DAMAGE_MULTIPLIER)
        for enemy in enemies:
            if not enemy.alive or id(enemy) in self._hit_enemies:
                continue
            dx = enemy.center_x - player.center_x
            dy = enemy.center_y - player.center_y
            dist = math.sqrt(dx * dx + dy * dy)
            if dist <= self.SPIN_RADIUS:
                enemy.take_damage(damage)
                enemy.apply_knockback(player.center_x, player.center_y, 250)
                particles.emit_sword_sparks(enemy.center_x, enemy.center_y)
                self._hit_enemies.add(id(enemy))

    def draw(self, surface, camera, player):
        if not self.active or self._spin_surface is None:
            return
        # Draw rotating spin arc centered on player
        rotated = pygame.transform.rotate(self._spin_surface, self._spin_angle)
        sx = int(player.center_x - camera.x - rotated.get_width() // 2)
        sy = int(player.center_y - camera.y - rotated.get_height() // 2)
        # Apply alpha fade near end
        progress = self.active_timer / self.SPIN_DURATION
        alpha = int(255 * min(1.0, progress * 2))
        rotated.set_alpha(alpha)
        surface.blit(rotated, (sx, sy))


class Dash(Ability):
    """Quick movement burst in facing direction with brief invincibility."""

    name = "dash"
    display_name = "Dash"
    mp_cost = 10
    cooldown_time = 1.0

    DASH_DISTANCE = 4 * TILE_SIZE  # ~4 tiles
    DASH_DURATION = 0.2  # seconds
    INVINCIBILITY_DURATION = 0.35  # slightly longer than dash

    def __init__(self):
        super().__init__()
        self._afterimages = []  # list of (surface, x, y, alpha)
        self._dash_vx = 0.0
        self._dash_vy = 0.0
        self._prev_invincible = False

    def _activate(self, player, enemies, projectiles, particles, camera):
        self.active_timer = self.DASH_DURATION
        self._afterimages = []
        # Calculate dash velocity based on facing
        speed = self.DASH_DISTANCE / self.DASH_DURATION
        directions = {
            "up": (0, -1),
            "down": (0, 1),
            "left": (-1, 0),
            "right": (1, 0),
        }
        dx, dy = directions.get(player.facing, (0, 1))
        self._dash_vx = dx * speed
        self._dash_vy = dy * speed
        # Save and set invincibility
        self._prev_invincible = player.invincible
        player.invincible = True
        player.invincible_timer = max(player.invincible_timer, self.INVINCIBILITY_DURATION)
        # Emit dash particles
        particles.emit(
            player.center_x, player.center_y,
            count=10,
            color=[(60, 140, 255), (120, 200, 255), (200, 230, 255)],
            speed_range=(40, 80),
            lifetime_range=(0.2, 0.4),
            size_range=(2, 4),
            gravity=0,
        )
        # Play sound
        from .sounds import get_sound_manager
        get_sound_manager().play_ability_dash()

    def _update_active(self, dt, player, enemies, projectiles, particles):
        # Override player velocity with dash velocity
        player.vx = self._dash_vx
        player.vy = self._dash_vy
        # Create afterimage
        frame = player.anim.get_frame(player.facing)
        afterimage = create_dash_afterimage(frame, alpha=120)
        if afterimage:
            self._afterimages.append({
                "surf": afterimage,
                "x": player.center_x,
                "y": player.center_y,
                "alpha": 120,
            })

    def _deactivate(self, player):
        # Stop dash velocity
        player.vx = 0
        player.vy = 0

    def update(self, dt, player, enemies, projectiles, particles):
        super().update(dt, player, enemies, projectiles, particles)
        # Fade afterimages
        for img in self._afterimages:
            img["alpha"] -= dt * 400
        self._afterimages = [img for img in self._afterimages if img["alpha"] > 0]

    def draw(self, surface, camera, player):
        # Draw afterimages
        for img in self._afterimages:
            surf = img["surf"]
            if surf is None:
                continue
            a = max(0, int(img["alpha"]))
            surf.set_alpha(a)
            sx = int(img["x"] - camera.x - surf.get_width() // 2)
            sy = int(img["y"] - camera.y - surf.get_height() // 2)
            surface.blit(surf, (sx, sy))


class FireBlast(Ability):
    """Shoots a fireball projectile in the facing direction."""

    name = "fire_blast"
    display_name = "Fire Blast"
    mp_cost = 30
    cooldown_time = 1.5

    FIRE_DAMAGE = 3
    FIRE_SPEED = PROJECTILE_SPEED * 1.2

    def __init__(self):
        super().__init__()
        self._fireball_sprite = None

    def _activate(self, player, enemies, projectiles, particles, camera):
        self.active_timer = 0  # Instant activation, no sustained effect
        self.active = False

        if self._fireball_sprite is None:
            self._fireball_sprite = create_fireball_surface()

        # Calculate target point in facing direction
        dist = 500  # max projectile travel distance
        directions = {
            "up": (0, -1),
            "down": (0, 1),
            "left": (-1, 0),
            "right": (1, 0),
        }
        dx, dy = directions.get(player.facing, (0, 1))
        target_x = player.center_x + dx * dist
        target_y = player.center_y + dy * dist

        # Create fireball projectile
        fireball = Projectile(
            player.center_x, player.center_y,
            target_x, target_y,
            self.FIRE_DAMAGE,
            sprite=self._fireball_sprite,
        )
        # Override speed for fire blast
        fireball_dist = math.sqrt(
            (target_x - player.center_x) ** 2 + (target_y - player.center_y) ** 2
        )
        if fireball_dist > 0:
            fireball.vx = dx * self.FIRE_SPEED
            fireball.vy = dy * self.FIRE_SPEED
        fireball.lifetime = 2.0
        # Mark as player-owned so it doesn't hurt the player
        fireball.owner = "player"
        fireball.color = (255, 120, 30)
        projectiles.append(fireball)

        # Emit fire particles at launch
        particles.emit(
            player.center_x + dx * 16, player.center_y + dy * 16,
            count=12,
            color=[(255, 120, 30), (255, 200, 50), (200, 80, 20)],
            speed_range=(60, 120),
            lifetime_range=(0.2, 0.4),
            size_range=(2, 5),
            gravity=0,
        )
        # Play sound
        from .sounds import get_sound_manager
        get_sound_manager().play_ability_fire()


class ShieldBarrier(Ability):
    """Temporary invincibility bubble for 3 seconds."""

    name = "shield_barrier"
    display_name = "Shield"
    mp_cost = 40
    cooldown_time = 3.0

    SHIELD_DURATION = 3.0

    def __init__(self):
        super().__init__()
        self._bubble_surface = None
        self._pulse_timer = 0.0

    def _activate(self, player, enemies, projectiles, particles, camera):
        self.active_timer = self.SHIELD_DURATION
        self._pulse_timer = 0.0
        if self._bubble_surface is None:
            self._bubble_surface = create_shield_bubble_surface()
        # Set player invincibility
        player.invincible = True
        player.invincible_timer = self.SHIELD_DURATION + 0.1
        # Don't blink while shielded
        player.visible = True
        # Emit shield activation particles
        particles.emit(
            player.center_x, player.center_y,
            count=20,
            color=[(80, 220, 120), (160, 255, 180), (40, 180, 80)],
            speed_range=(60, 120),
            lifetime_range=(0.3, 0.6),
            size_range=(2, 5),
            gravity=-20,
        )
        # Play sound
        from .sounds import get_sound_manager
        get_sound_manager().play_ability_shield()

    def _update_active(self, dt, player, enemies, projectiles, particles):
        self._pulse_timer += dt
        # Keep player invincible and visible while shield is active
        player.invincible = True
        player.invincible_timer = max(player.invincible_timer, self.active_timer + 0.1)
        player.visible = True
        # Subtle ongoing particles
        if self._pulse_timer >= 0.3:
            self._pulse_timer = 0.0
            particles.emit(
                player.center_x, player.center_y,
                count=3,
                color=[(80, 220, 120), (160, 255, 180)],
                speed_range=(20, 40),
                lifetime_range=(0.4, 0.8),
                size_range=(1, 3),
                gravity=-15,
            )

    def _deactivate(self, player):
        # Shield expired - invincibility timer will handle the rest naturally
        pass

    def draw(self, surface, camera, player):
        if not self.active or self._bubble_surface is None:
            return
        # Draw pulsing shield bubble
        pulse = 1.0 + 0.1 * math.sin(self._pulse_timer * 8)
        w = int(self._bubble_surface.get_width() * pulse)
        h = int(self._bubble_surface.get_height() * pulse)
        scaled = pygame.transform.scale(self._bubble_surface, (w, h))
        # Fade near end
        remaining = self.active_timer / self.SHIELD_DURATION
        if remaining < 0.3:
            alpha = int(255 * (remaining / 0.3))
            scaled.set_alpha(alpha)
        sx = int(player.center_x - camera.x - w // 2)
        sy = int(player.center_y - camera.y - h // 2)
        surface.blit(scaled, (sx, sy))


# ── Registry ─────────────────────────────────────────────────────────

# Maps boss_id -> ability name that is unlocked upon defeating that boss
BOSS_ABILITY_UNLOCKS = {
    "forest_guardian": "spin_attack",
    "sand_worm": "dash",
    "inferno_drake": "fire_blast",
    # shield_barrier is found in a secret chest, not a boss unlock
}

# All ability classes by name
ABILITY_CLASSES = {
    "spin_attack": SpinAttack,
    "dash": Dash,
    "fire_blast": FireBlast,
    "shield_barrier": ShieldBarrier,
}


def create_ability(name):
    """Create an ability instance by name."""
    cls = ABILITY_CLASSES.get(name)
    if cls is None:
        return None
    return cls()
