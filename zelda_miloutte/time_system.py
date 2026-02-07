"""Day/night cycle time system.

Game clock: 1 real second = 1 game minute, full day = 24 game hours (24 minutes real time).

Time phases:
    Dawn  (5:00 - 7:00)  - warm orange tint
    Day   (7:00 - 18:00) - clear / no overlay
    Dusk  (18:00 - 20:00) - golden/amber tint
    Night (20:00 - 5:00)  - dark blue overlay with limited visibility
"""

import math
import random
import pygame
from zelda_miloutte.settings import SCREEN_WIDTH, SCREEN_HEIGHT


# Phase constants
PHASE_DAWN = "dawn"
PHASE_DAY = "day"
PHASE_DUSK = "dusk"
PHASE_NIGHT = "night"

# Phase hour boundaries
DAWN_START = 5.0
DAY_START = 7.0
DUSK_START = 18.0
NIGHT_START = 20.0
HOURS_IN_DAY = 24.0

# Phase colors (R, G, B, A)
DAWN_COLOR = (255, 140, 50, 40)
DAY_COLOR = (0, 0, 0, 0)
DUSK_COLOR = (255, 180, 60, 50)
NIGHT_COLOR = (10, 10, 60, 120)

# Light radius
LIGHT_RADIUS_DEFAULT = 100
LIGHT_RADIUS_LANTERN = 200

# Star count for night sky
STAR_COUNT = 60


class TimeSystem:
    """Manages the in-game time of day and generates visual overlays."""

    def __init__(self, game_hour=8.0):
        """Initialize with a starting hour (0-24, default 8:00 AM)."""
        self.game_hour = game_hour % HOURS_IN_DAY
        self.paused = False

        # Stars for night sky (screen-space positions)
        self._stars = [
            {
                "x": random.randint(0, SCREEN_WIDTH),
                "y": random.randint(0, SCREEN_HEIGHT),
                "size": random.choice([1, 1, 1, 2]),
                "twinkle_offset": random.uniform(0, math.pi * 2),
                "twinkle_speed": random.uniform(1.5, 4.0),
            }
            for _ in range(STAR_COUNT)
        ]
        self._twinkle_timer = 0.0

        # Cached overlay surface
        self._overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)

    # ── Time update ──────────────────────────────────────────────

    def update(self, dt):
        """Advance the game clock. 1 real second = 1 game minute."""
        if self.paused:
            return
        # dt is in seconds; 1 second = 1 minute = 1/60 of an hour
        self.game_hour += dt / 60.0
        if self.game_hour >= HOURS_IN_DAY:
            self.game_hour -= HOURS_IN_DAY
        self._twinkle_timer += dt

    def skip_to_dawn(self):
        """Jump time to dawn (5:00)."""
        self.game_hour = DAWN_START

    # ── Phase queries ────────────────────────────────────────────

    @property
    def phase(self):
        """Return the current time phase string."""
        h = self.game_hour
        if DAWN_START <= h < DAY_START:
            return PHASE_DAWN
        elif DAY_START <= h < DUSK_START:
            return PHASE_DAY
        elif DUSK_START <= h < NIGHT_START:
            return PHASE_DUSK
        else:
            return PHASE_NIGHT

    @property
    def is_night(self):
        return self.phase == PHASE_NIGHT

    @property
    def hour_int(self):
        return int(self.game_hour)

    @property
    def minute_int(self):
        return int((self.game_hour % 1.0) * 60)

    @property
    def time_string(self):
        """Return formatted time like '08:30'."""
        return f"{self.hour_int:02d}:{self.minute_int:02d}"

    # ── Overlay color interpolation ──────────────────────────────

    def _get_overlay_color(self):
        """Calculate the current overlay color with smooth interpolation between phases."""
        h = self.game_hour

        if DAWN_START <= h < DAY_START:
            # Dawn -> Day transition
            t = (h - DAWN_START) / (DAY_START - DAWN_START)
            return self._lerp_color(DAWN_COLOR, DAY_COLOR, t)
        elif DAY_START <= h < DUSK_START:
            # Pure day (no overlay)
            return DAY_COLOR
        elif DUSK_START <= h < NIGHT_START:
            # Dusk -> Night transition
            t = (h - DUSK_START) / (NIGHT_START - DUSK_START)
            return self._lerp_color(DUSK_COLOR, NIGHT_COLOR, t)
        elif h >= NIGHT_START:
            # Night (before midnight)
            return NIGHT_COLOR
        else:
            # Night (after midnight, before dawn)
            if h < DAWN_START - 1.0:
                return NIGHT_COLOR
            else:
                # Approaching dawn
                t = (h - (DAWN_START - 1.0)) / 1.0
                return self._lerp_color(NIGHT_COLOR, DAWN_COLOR, t)

    @staticmethod
    def _lerp_color(c1, c2, t):
        """Linearly interpolate between two RGBA color tuples."""
        t = max(0.0, min(1.0, t))
        return (
            int(c1[0] + (c2[0] - c1[0]) * t),
            int(c1[1] + (c2[1] - c1[1]) * t),
            int(c1[2] + (c2[2] - c1[2]) * t),
            int(c1[3] + (c2[3] - c1[3]) * t),
        )

    # ── Light radius ─────────────────────────────────────────────

    def get_light_radius(self, has_lantern):
        """Return the player's visibility radius at night."""
        if not self.is_night:
            return 0  # No light needed during day
        return LIGHT_RADIUS_LANTERN if has_lantern else LIGHT_RADIUS_DEFAULT

    # ── Drawing ──────────────────────────────────────────────────

    def draw_overlay(self, surface, player_screen_x, player_screen_y, has_lantern=False):
        """Draw the day/night overlay onto the given surface.

        Args:
            surface: The game display surface.
            player_screen_x: Player center X in screen space.
            player_screen_y: Player center Y in screen space.
            has_lantern: Whether the player has a lantern.
        """
        color = self._get_overlay_color()

        # Skip if fully transparent
        if color[3] <= 0:
            return

        self._overlay.fill((0, 0, 0, 0))

        if self.is_night:
            self._draw_night_overlay(
                self._overlay, player_screen_x, player_screen_y, has_lantern, color
            )
        else:
            # Simple tinted overlay for dawn/dusk
            self._overlay.fill(color)

        surface.blit(self._overlay, (0, 0))

    def _draw_night_overlay(self, overlay, px, py, has_lantern, color):
        """Draw night overlay with light circle around player and stars."""
        # Fill with dark night color
        overlay.fill(color)

        # Draw light radius around player by punching a gradient hole
        radius = LIGHT_RADIUS_LANTERN if has_lantern else LIGHT_RADIUS_DEFAULT
        light_color = (255, 200, 100) if has_lantern else (200, 200, 220)

        # Create a radial gradient light mask
        light_size = radius * 2
        light_surf = pygame.Surface((light_size, light_size), pygame.SRCALPHA)

        # Draw concentric circles from outside in, decreasing alpha to create gradient
        steps = 20
        for i in range(steps):
            t = i / steps  # 0 = outermost, 1 = center
            r = int(radius * (1.0 - t))
            if r <= 0:
                continue
            # Alpha: full at edge (overlay alpha), zero at center
            a = int(color[3] * (1.0 - t * t))  # Quadratic falloff for softer light
            # Erase overlay pixels by blitting with special blend
            pygame.draw.circle(
                light_surf, (0, 0, 0, a), (radius, radius), r
            )

        # We need to subtract light from the overlay.
        # Strategy: fill overlay, then use a per-pixel alpha surface to cut a hole.
        # Rebuild overlay with light hole:
        overlay.fill(color)

        # Create light mask: full alpha = dark, zero alpha where light is
        for i in range(steps, 0, -1):
            t = i / steps
            r = int(radius * t)
            if r <= 0:
                continue
            # Closer to center = less darkness
            alpha_factor = t * t  # Quadratic: dark at edge, clear at center
            clear_alpha = int(color[3] * (1.0 - alpha_factor))
            circle_color = (color[0], color[1], color[2], clear_alpha)
            pygame.draw.circle(overlay, circle_color, (int(px), int(py)), r)

        # Warm glow effect for lantern
        if has_lantern:
            glow_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            glow_radius = radius + 20
            for i in range(5):
                t = i / 5
                r = int(glow_radius * (1.0 - t))
                a = int(15 * (1.0 - t))
                pygame.draw.circle(
                    glow_surf, (255, 180, 80, a), (int(px), int(py)), r
                )
            overlay.blit(glow_surf, (0, 0))

        # Draw twinkling stars
        self._draw_stars(overlay)

    def _draw_stars(self, overlay):
        """Draw twinkling white dots on the night overlay."""
        for star in self._stars:
            # Twinkle using sine wave
            twinkle = math.sin(
                self._twinkle_timer * star["twinkle_speed"] + star["twinkle_offset"]
            )
            # Map from [-1, 1] to alpha [60, 220]
            alpha = int(140 + 80 * twinkle)
            alpha = max(30, min(255, alpha))

            size = star["size"]
            sx, sy = star["x"], star["y"]

            if size == 1:
                overlay.set_at((sx, sy), (255, 255, 255, alpha))
            else:
                star_surf = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
                pygame.draw.circle(
                    star_surf, (255, 255, 255, alpha), (size, size), size
                )
                overlay.blit(star_surf, (sx - size, sy - size))

    # ── Serialization ────────────────────────────────────────────

    def to_dict(self):
        """Serialize time state for saving."""
        return {"game_hour": self.game_hour}

    def from_dict(self, data):
        """Restore time state from save data."""
        self.game_hour = data.get("game_hour", 8.0) % HOURS_IN_DAY
