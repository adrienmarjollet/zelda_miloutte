"""Dynamic weather system with gameplay effects and visual particles.

Weather types: CLEAR, RAIN, STORM, FOG, SANDSTORM, ASH_FALL, BLIZZARD.
Area-specific pools determine which weather can occur in each region.
Weather transitions gradually over 30 seconds.
"""

import random
import math
import pygame
from enum import Enum

from zelda_miloutte.settings import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE


class WeatherType(Enum):
    CLEAR = "clear"
    RAIN = "rain"
    STORM = "storm"
    FOG = "fog"
    SANDSTORM = "sandstorm"
    ASH_FALL = "ash_fall"
    BLIZZARD = "blizzard"


# Area-specific weather pools
AREA_WEATHER_POOLS = {
    "overworld": [WeatherType.CLEAR, WeatherType.RAIN, WeatherType.STORM, WeatherType.FOG],
    "forest": [WeatherType.CLEAR, WeatherType.RAIN, WeatherType.STORM, WeatherType.FOG],
    "desert": [WeatherType.CLEAR, WeatherType.SANDSTORM],
    "volcano": [WeatherType.CLEAR, WeatherType.ASH_FALL],
    "ice": [WeatherType.CLEAR, WeatherType.BLIZZARD],
}

# Default pool for unknown areas
DEFAULT_WEATHER_POOL = [WeatherType.CLEAR]

# Transition duration in seconds
TRANSITION_DURATION = 30.0

# Weather change interval range in seconds (3-8 minutes)
MIN_CHANGE_INTERVAL = 180.0
MAX_CHANGE_INTERVAL = 480.0


class WeatherParticle:
    """A single weather particle with screen-space position."""

    __slots__ = ('x', 'y', 'vx', 'vy', 'lifetime', 'max_lifetime', 'size', 'color', 'alive')

    def __init__(self, x, y, vx, vy, color, lifetime, size):
        self.x = float(x)
        self.y = float(y)
        self.vx = float(vx)
        self.vy = float(vy)
        self.color = color
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.size = size
        self.alive = True

    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.alive = False
        # Kill if off screen
        if self.x < -20 or self.x > SCREEN_WIDTH + 20 or self.y > SCREEN_HEIGHT + 20:
            self.alive = False


class WeatherManager:
    """Manages weather state, transitions, particles, and gameplay effects."""

    def __init__(self):
        self.current_weather = WeatherType.CLEAR
        self.target_weather = WeatherType.CLEAR
        self.intensity = 0.0  # 0.0 = clear, 1.0 = full effect
        self.target_intensity = 0.0
        self.transition_speed = 1.0 / TRANSITION_DURATION

        # Timer for next weather change
        self._change_timer = random.uniform(MIN_CHANGE_INTERVAL, MAX_CHANGE_INTERVAL)

        # Current area
        self._area_id = "overworld"

        # Weather particles (screen-space)
        self._particles = []

        # Spawn timers
        self._spawn_timer = 0.0

        # Lightning state (STORM)
        self._lightning_flash_alpha = 0
        self._lightning_timer = 0.0
        self._lightning_interval = 0.0
        self._thunder_pending = False
        self._thunder_delay = 0.0
        self._reset_lightning_timer()

        # Lightning strike hazard (STORM)
        self._strike_timer = 0.0
        self._strike_interval = 8.0  # Lightning strikes every ~8 seconds during storms
        self._strike_pos = None
        self._strike_flash_timer = 0.0

        # Wind direction for sandstorm/blizzard (normalized)
        self.wind_dx = 1.0
        self.wind_dy = 0.0

        # Fog overlay surface (cached)
        self._fog_surface = None
        self._fog_needs_update = True

        # Paused flag (indoors/dungeons)
        self.paused = False

    def set_area(self, area_id):
        """Set the current area to determine weather pool."""
        if area_id != self._area_id:
            self._area_id = area_id
            # If current weather is not valid for the new area, schedule immediate change
            pool = AREA_WEATHER_POOLS.get(area_id, DEFAULT_WEATHER_POOL)
            if self.current_weather not in pool and self.target_weather not in pool:
                self._pick_new_weather()

    def pause(self):
        """Pause weather (indoors/dungeons)."""
        self.paused = True

    def resume(self):
        """Resume weather (outdoors)."""
        self.paused = False

    def _pick_new_weather(self):
        """Pick a new target weather from the current area's pool."""
        pool = AREA_WEATHER_POOLS.get(self._area_id, DEFAULT_WEATHER_POOL)
        if len(pool) <= 1:
            self.target_weather = pool[0]
        else:
            # Pick a different weather than current
            choices = [w for w in pool if w != self.current_weather]
            if not choices:
                choices = pool
            self.target_weather = random.choice(choices)

        if self.target_weather == WeatherType.CLEAR:
            self.target_intensity = 0.0
        else:
            self.target_intensity = 1.0

        # Reset change timer
        self._change_timer = random.uniform(MIN_CHANGE_INTERVAL, MAX_CHANGE_INTERVAL)

    def _reset_lightning_timer(self):
        """Set random interval for next lightning flash."""
        self._lightning_interval = random.uniform(4.0, 10.0)
        self._lightning_timer = self._lightning_interval

    def update(self, dt, player=None, enemies=None, tilemap=None):
        """Update weather state, particles, and effects.

        Args:
            dt: Delta time in seconds.
            player: Player entity (for gameplay effects).
            enemies: List of enemy entities (for gameplay effects).
            tilemap: TileMap instance (for lightning strike positions).
        """
        if self.paused:
            return

        # Update change timer
        self._change_timer -= dt
        if self._change_timer <= 0:
            self._pick_new_weather()

        # Transition intensity
        if self.target_weather != WeatherType.CLEAR and self.current_weather == WeatherType.CLEAR:
            # Transitioning from clear to a weather type
            self.current_weather = self.target_weather
            # Ramp up intensity
        elif self.target_weather == WeatherType.CLEAR and self.current_weather != WeatherType.CLEAR:
            # Transitioning from weather to clear -- ramp down
            pass
        elif self.target_weather != self.current_weather:
            # Transitioning between two weather types -- ramp down first, then switch
            if self.intensity <= 0.05:
                self.current_weather = self.target_weather
                if self.target_weather != WeatherType.CLEAR:
                    self.target_intensity = 1.0

        # Lerp intensity toward target
        if abs(self.intensity - self.target_intensity) > 0.01:
            if self.intensity < self.target_intensity:
                self.intensity = min(self.target_intensity,
                                     self.intensity + self.transition_speed * dt)
            else:
                self.intensity = max(self.target_intensity,
                                     self.intensity - self.transition_speed * dt)
        else:
            self.intensity = self.target_intensity

        # If intensity reached 0 and target is clear, reset weather type
        if self.intensity <= 0.01 and self.target_weather == WeatherType.CLEAR:
            self.current_weather = WeatherType.CLEAR

        # Update particles
        self._update_particles(dt)

        # Spawn new particles based on weather type and intensity
        self._spawn_particles(dt)

        # Update lightning for STORM
        if self.current_weather == WeatherType.STORM and self.intensity > 0.3:
            self._update_lightning(dt, player, enemies, tilemap)

        # Decay lightning flash
        if self._lightning_flash_alpha > 0:
            self._lightning_flash_alpha = max(0, self._lightning_flash_alpha - 800 * dt)

        # Decay strike flash
        if self._strike_flash_timer > 0:
            self._strike_flash_timer -= dt

        # Mark fog as needing update
        if self.current_weather == WeatherType.FOG:
            self._fog_needs_update = True

    def _update_particles(self, dt):
        """Update all weather particles."""
        for p in self._particles:
            p.update(dt)
        self._particles = [p for p in self._particles if p.alive]

    def _spawn_particles(self, dt):
        """Spawn weather-specific particles."""
        if self.intensity < 0.05:
            return

        self._spawn_timer += dt
        weather = self.current_weather

        if weather == WeatherType.RAIN or weather == WeatherType.STORM:
            self._spawn_rain(dt)
        elif weather == WeatherType.FOG:
            # Fog uses overlay, no particles needed
            pass
        elif weather == WeatherType.SANDSTORM:
            self._spawn_sandstorm(dt)
        elif weather == WeatherType.ASH_FALL:
            self._spawn_ash(dt)
        elif weather == WeatherType.BLIZZARD:
            self._spawn_blizzard(dt)

    def _spawn_rain(self, dt):
        """Spawn rain streak particles."""
        # Spawn rate scales with intensity
        count_per_sec = int(200 * self.intensity)
        count = max(1, int(count_per_sec * dt))

        for _ in range(count):
            x = random.uniform(-20, SCREEN_WIDTH + 20)
            y = random.uniform(-40, -5)
            vx = random.uniform(30, 60)  # Slight diagonal
            vy = random.uniform(500, 700)
            # Blue-ish rain colors
            blue = random.randint(150, 220)
            color = (100, 130, blue)
            lifetime = random.uniform(0.5, 0.9)
            size = random.uniform(1, 2)
            self._particles.append(WeatherParticle(x, y, vx, vy, color, lifetime, size))

        # Splash particles on ground (less frequent)
        if random.random() < 0.3 * self.intensity * dt * 60:
            sx = random.uniform(0, SCREEN_WIDTH)
            sy = SCREEN_HEIGHT - random.uniform(0, 40)
            for _ in range(random.randint(2, 4)):
                svx = random.uniform(-30, 30)
                svy = random.uniform(-60, -20)
                self._particles.append(
                    WeatherParticle(sx, sy, svx, svy, (140, 160, 200), 0.2, 1)
                )

    def _spawn_sandstorm(self, dt):
        """Spawn horizontal sand particles."""
        count_per_sec = int(120 * self.intensity)
        count = max(1, int(count_per_sec * dt))

        for _ in range(count):
            x = random.uniform(-30, -5)
            y = random.uniform(0, SCREEN_HEIGHT)
            vx = random.uniform(200, 400) * self.intensity
            vy = random.uniform(-20, 20)
            # Tan/brown sand colors
            r = random.randint(180, 220)
            g = random.randint(150, 180)
            b = random.randint(80, 120)
            color = (r, g, b)
            lifetime = random.uniform(1.5, 3.0)
            size = random.uniform(1, 3)
            self._particles.append(WeatherParticle(x, y, vx, vy, color, lifetime, size))

    def _spawn_ash(self, dt):
        """Spawn slow-falling ash/ember particles."""
        count_per_sec = int(30 * self.intensity)
        count = max(1, int(count_per_sec * dt))

        for _ in range(count):
            x = random.uniform(0, SCREEN_WIDTH)
            y = random.uniform(-20, -5)
            vx = random.uniform(-15, 15)
            vy = random.uniform(30, 80)
            # Grey/orange ash colors
            if random.random() < 0.3:
                # Ember (warm)
                color = (255, random.randint(100, 180), random.randint(20, 60))
            else:
                # Ash (grey)
                g = random.randint(120, 180)
                color = (g, g - 10, g - 20)
            lifetime = random.uniform(3.0, 6.0)
            size = random.uniform(1, 3)
            self._particles.append(WeatherParticle(x, y, vx, vy, color, lifetime, size))

    def _spawn_blizzard(self, dt):
        """Spawn fast diagonal snow/ice particles."""
        count_per_sec = int(150 * self.intensity)
        count = max(1, int(count_per_sec * dt))

        for _ in range(count):
            x = random.uniform(-30, SCREEN_WIDTH + 30)
            y = random.uniform(-30, -5)
            vx = random.uniform(80, 200) * self.intensity
            vy = random.uniform(200, 400)
            # White/light blue snow
            white = random.randint(200, 255)
            blue_tint = random.randint(0, 30)
            color = (white - blue_tint, white - blue_tint // 2, white)
            lifetime = random.uniform(1.0, 2.5)
            size = random.uniform(1, 3)
            self._particles.append(WeatherParticle(x, y, vx, vy, color, lifetime, size))

    def _update_lightning(self, dt, player, enemies, tilemap):
        """Update lightning flash and strike logic for storms."""
        # Visual lightning flash
        self._lightning_timer -= dt
        if self._lightning_timer <= 0:
            self._lightning_flash_alpha = 200
            self._reset_lightning_timer()
            # Schedule thunder sound
            self._thunder_pending = True
            self._thunder_delay = random.uniform(1.0, 2.0)

        # Thunder sound delay
        if self._thunder_pending:
            self._thunder_delay -= dt
            if self._thunder_delay <= 0:
                self._thunder_pending = False
                from zelda_miloutte.sounds import get_sound_manager
                get_sound_manager().play_thunder()

        # Lightning strike hazard
        self._strike_timer -= dt
        if self._strike_timer <= 0:
            self._strike_timer = random.uniform(6.0, 12.0)
            if player and tilemap:
                self._do_lightning_strike(player, enemies, tilemap)

    def _do_lightning_strike(self, player, enemies, tilemap):
        """Execute a lightning strike at a random outdoor tile near the player."""
        # Pick a random position within ~6 tiles of the player
        offset_x = random.randint(-6, 6) * TILE_SIZE
        offset_y = random.randint(-6, 6) * TILE_SIZE
        strike_x = player.center_x + offset_x
        strike_y = player.center_y + offset_y

        self._strike_pos = (strike_x, strike_y)
        self._strike_flash_timer = 0.3

        # Small screen flash
        self._lightning_flash_alpha = 150

        # Damage entities near the strike (radius ~40px)
        strike_radius = 40
        # Damage player
        dist = math.sqrt((player.center_x - strike_x) ** 2 +
                         (player.center_y - strike_y) ** 2)
        if dist < strike_radius:
            player.take_damage(2)
            player.apply_knockback(strike_x, strike_y, 200)

        # Damage enemies
        if enemies:
            for enemy in enemies:
                if not enemy.alive:
                    continue
                edist = math.sqrt((enemy.center_x - strike_x) ** 2 +
                                  (enemy.center_y - strike_y) ** 2)
                if edist < strike_radius:
                    enemy.take_damage(2)

    def get_movement_modifier(self, player_vx, player_vy):
        """Return modified (vx, vy) based on weather effects on player movement.

        Args:
            player_vx: Player's current x velocity.
            player_vy: Player's current y velocity.

        Returns:
            Tuple (modified_vx, modified_vy).
        """
        if self.intensity < 0.1:
            return player_vx, player_vy

        weather = self.current_weather

        if weather == WeatherType.SANDSTORM:
            # 15% slower against wind direction, 15% faster with it
            wind_factor = 0.15 * self.intensity
            # Wind blows from left to right (positive x)
            # If player moves against wind (negative vx), slow down
            mod_vx = player_vx
            if player_vx < 0:
                mod_vx = player_vx * (1.0 - wind_factor)
            elif player_vx > 0:
                mod_vx = player_vx * (1.0 + wind_factor * 0.3)
            return mod_vx, player_vy

        elif weather == WeatherType.BLIZZARD:
            # 20% slower all directions
            slow_factor = 1.0 - (0.20 * self.intensity)
            return player_vx * slow_factor, player_vy * slow_factor

        return player_vx, player_vy

    def get_enemy_detection_modifier(self):
        """Return a multiplier for enemy detection range based on weather.

        Returns:
            Float multiplier (1.0 = normal, 0.6 = reduced 40%).
        """
        if self.intensity < 0.1:
            return 1.0

        if self.current_weather == WeatherType.FOG:
            return 1.0 - (0.4 * self.intensity)

        return 1.0

    def get_fire_damage_modifier(self):
        """Return a damage multiplier for fire enemies during rain.

        Returns:
            Float multiplier (1.0 = normal, 0.8 = 20% less).
        """
        if self.intensity < 0.1:
            return 1.0

        if self.current_weather in (WeatherType.RAIN, WeatherType.STORM):
            return 1.0 - (0.2 * self.intensity)

        return 1.0

    def draw(self, surface, camera=None):
        """Draw weather effects on top of the game world.

        Args:
            surface: The main display surface.
            camera: Camera instance (for world-space conversion if needed).
        """
        if self.intensity < 0.01 and self._lightning_flash_alpha <= 0:
            return

        weather = self.current_weather

        # Draw weather particles
        if weather in (WeatherType.RAIN, WeatherType.STORM):
            self._draw_rain(surface)
        elif weather == WeatherType.SANDSTORM:
            self._draw_sandstorm(surface)
        elif weather == WeatherType.ASH_FALL:
            self._draw_ash(surface)
        elif weather == WeatherType.BLIZZARD:
            self._draw_blizzard(surface)

        # Draw fog overlay
        if weather == WeatherType.FOG:
            self._draw_fog(surface, camera)

        # Draw sandstorm/blizzard visibility overlay
        if weather == WeatherType.SANDSTORM:
            self._draw_sandstorm_overlay(surface)
        elif weather == WeatherType.BLIZZARD:
            self._draw_blizzard_overlay(surface)

        # Draw lightning flash (STORM)
        if self._lightning_flash_alpha > 0:
            flash_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            flash_surf.fill((255, 255, 255, int(self._lightning_flash_alpha)))
            surface.blit(flash_surf, (0, 0))

        # Draw lightning strike indicator
        if self._strike_flash_timer > 0 and self._strike_pos and camera:
            sx = int(self._strike_pos[0] - camera.x)
            sy = int(self._strike_pos[1] - camera.y)
            # Draw a bright bolt-like effect
            bolt_surf = pygame.Surface((80, 80), pygame.SRCALPHA)
            alpha = int(255 * (self._strike_flash_timer / 0.3))
            pygame.draw.circle(bolt_surf, (255, 255, 200, alpha), (40, 40), 30)
            pygame.draw.circle(bolt_surf, (255, 255, 255, min(255, alpha + 50)), (40, 40), 15)
            surface.blit(bolt_surf, (sx - 40, sy - 40))

    def _draw_rain(self, surface):
        """Draw rain streaks as thin angled lines."""
        for p in self._particles:
            # Rain streaks are thin lines
            end_x = p.x + p.vx * 0.02
            end_y = p.y + p.vy * 0.02
            alpha = int(180 * (p.lifetime / p.max_lifetime) * self.intensity)
            alpha = max(0, min(255, alpha))
            # Use a temporary surface for alpha
            # For performance, draw directly without alpha for most rain
            color = (*p.color[:3],)
            pygame.draw.line(surface, color,
                             (int(p.x), int(p.y)),
                             (int(end_x), int(end_y)), 1)

    def _draw_sandstorm(self, surface):
        """Draw sandstorm particles as small circles."""
        for p in self._particles:
            alpha = p.lifetime / p.max_lifetime
            size = max(1, int(p.size * alpha))
            # Draw as small rect for performance
            pygame.draw.circle(surface, p.color,
                               (int(p.x), int(p.y)), size)

    def _draw_ash(self, surface):
        """Draw ash particles as small glowing dots."""
        for p in self._particles:
            alpha = p.lifetime / p.max_lifetime
            size = max(1, int(p.size * alpha))
            temp = pygame.Surface((size * 2 + 2, size * 2 + 2), pygame.SRCALPHA)
            a = int(200 * alpha * self.intensity)
            pygame.draw.circle(temp, (*p.color, a), (size + 1, size + 1), size)
            surface.blit(temp, (int(p.x) - size - 1, int(p.y) - size - 1))

    def _draw_blizzard(self, surface):
        """Draw blizzard particles as white streaks."""
        for p in self._particles:
            end_x = p.x + p.vx * 0.015
            end_y = p.y + p.vy * 0.015
            pygame.draw.line(surface, p.color,
                             (int(p.x), int(p.y)),
                             (int(end_x), int(end_y)), max(1, int(p.size)))

    def _draw_fog(self, surface, camera):
        """Draw fog overlay with reduced visibility around player."""
        fog = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        fog_alpha = int(160 * self.intensity)
        fog.fill((200, 200, 210, fog_alpha))

        if camera:
            # Create a clear circle around the screen center (player)
            center_x = SCREEN_WIDTH // 2
            center_y = SCREEN_HEIGHT // 2
            clear_radius = int(150 * (1.0 - self.intensity * 0.3))
            fade_radius = clear_radius + 80

            # Draw concentric circles of decreasing alpha to create gradient
            for r in range(fade_radius, clear_radius, -4):
                t = (r - clear_radius) / (fade_radius - clear_radius)
                circle_alpha = int(fog_alpha * (1.0 - t))
                pygame.draw.circle(fog, (200, 200, 210, circle_alpha),
                                   (center_x, center_y), r)

            # Clear inner circle
            pygame.draw.circle(fog, (0, 0, 0, 0), (center_x, center_y), clear_radius)

        surface.blit(fog, (0, 0))

    def _draw_sandstorm_overlay(self, surface):
        """Draw semi-transparent tan overlay for sandstorm reduced visibility."""
        overlay_alpha = int(60 * self.intensity)
        if overlay_alpha > 0:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((210, 180, 120, overlay_alpha))
            surface.blit(overlay, (0, 0))

    def _draw_blizzard_overlay(self, surface):
        """Draw semi-transparent white overlay for blizzard reduced visibility."""
        overlay_alpha = int(80 * self.intensity)
        if overlay_alpha > 0:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((220, 225, 240, overlay_alpha))
            surface.blit(overlay, (0, 0))

    def get_weather_dialogue(self):
        """Return a weather-related dialogue line for NPCs.

        Returns:
            String with weather comment, or None for clear weather.
        """
        if self.intensity < 0.3:
            return None

        comments = {
            WeatherType.RAIN: [
                "Terrible weather today...",
                "This rain won't let up!",
                "Best to stay dry if you can.",
                "The crops will love this rain.",
            ],
            WeatherType.STORM: [
                "Be careful out there! Lightning is dangerous!",
                "This storm is fierce! Stay under cover!",
                "I heard thunder... scary!",
            ],
            WeatherType.FOG: [
                "I can barely see my hand in front of my face!",
                "This fog is thick... watch your step.",
                "Enemies could be lurking in this fog.",
            ],
            WeatherType.SANDSTORM: [
                "This sandstorm is blinding!",
                "The wind is brutal today.",
                "Sand gets everywhere in this weather.",
            ],
            WeatherType.ASH_FALL: [
                "The ash is falling heavier than usual.",
                "The volcano must be active again...",
                "Try not to breathe in too much ash.",
            ],
            WeatherType.BLIZZARD: [
                "Brrr! This blizzard is terrible!",
                "Be careful not to freeze out there!",
                "The snow is blinding!",
            ],
        }

        lines = comments.get(self.current_weather)
        if lines:
            return random.choice(lines)
        return None
