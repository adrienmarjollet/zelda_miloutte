"""Enemy AI state machine with alert states and pathfinding integration."""

import math
import pygame
from enum import Enum
from zelda_miloutte.settings import TILE_SIZE
from zelda_miloutte.pathfinding import (
    find_path, has_line_of_sight, can_pathfind,
)


class AlertState(Enum):
    """Enemy alert states for awareness of the player."""
    IDLE = "idle"           # Patrolling or standing still
    SUSPICIOUS = "suspicious"  # Player detected, slow approach (? icon)
    ALERT = "alert"         # Full chase mode (! icon)
    LOST = "lost"           # Player escaped, returning to patrol


# Cached alert icon surfaces
_question_icon = None
_exclamation_icon = None


def _get_question_icon():
    """Create a small '?' icon surface."""
    global _question_icon
    if _question_icon is not None:
        return _question_icon
    from zelda_miloutte.sprites.pixel_art import surface_from_grid
    grid = [
        " yyy ",
        "y   y",
        "    y",
        "   y ",
        "  y  ",
        "     ",
        "  y  ",
    ]
    palette = {
        'y': (255, 255, 80),
        ' ': None,
    }
    _question_icon = surface_from_grid(grid, palette, scale=2)
    return _question_icon


def _get_exclamation_icon():
    """Create a small '!' icon surface."""
    global _exclamation_icon
    if _exclamation_icon is not None:
        return _exclamation_icon
    from zelda_miloutte.sprites.pixel_art import surface_from_grid
    grid = [
        " r ",
        " r ",
        " r ",
        " r ",
        "   ",
        " r ",
    ]
    palette = {
        'r': (255, 50, 50),
        ' ': None,
    }
    _exclamation_icon = surface_from_grid(grid, palette, scale=2)
    return _exclamation_icon


class EnemyAI:
    """Mixin providing smarter AI with alert states and pathfinding.

    Add this to an enemy by calling init_ai() in __init__ and
    update_ai() in the update method.
    """

    def init_ai(self, detection_range=None, lose_range=None,
                pathfind_interval=0.5, use_pathfinding=True,
                suspicious_duration=1.0, lost_duration=3.0):
        """Initialize AI state tracking.

        Args:
            detection_range: Range at which enemy detects the player (defaults to self.chase_range)
            lose_range: Range at which enemy loses the player (defaults to 2x detection_range)
            pathfind_interval: Seconds between pathfinding recalculations
            use_pathfinding: Whether this enemy uses A* pathfinding
            suspicious_duration: How long the suspicious state lasts before alert
            lost_duration: How long the lost state lasts before returning to idle
        """
        self.ai_state = AlertState.IDLE
        self.detection_range = detection_range or getattr(self, 'chase_range', 150.0)
        self.lose_range = lose_range or self.detection_range * 2.0
        self.pathfind_interval = pathfind_interval
        self.use_pathfinding = use_pathfinding
        self.suspicious_duration = suspicious_duration
        self.lost_duration = lost_duration

        # Timers
        self._ai_state_timer = 0.0
        self._pathfind_timer = 0.0
        self._cached_path = []
        self._path_index = 0

        # Icon display timer (for fade effect)
        self._icon_timer = 0.0
        self._icon_duration = 1.5  # How long to show the icon

        # Last known player position (for lost state)
        self._last_known_px = 0.0
        self._last_known_py = 0.0

        # Group behavior
        self._group_offset_x = 0.0
        self._group_offset_y = 0.0

    def update_ai(self, dt, player, tilemap):
        """Update AI state machine. Returns the target (px, py) to move toward,
        the speed to use, or None if enemy should not move (idle/paused).

        This does NOT move the enemy -- the caller should set vx/vy based on the
        returned target.

        Returns:
            tuple (target_x, target_y, speed) or None
        """
        dist = self._ai_distance_to(player)
        has_los = has_line_of_sight(
            tilemap, self.center_x, self.center_y,
            player.center_x, player.center_y
        )

        # Update pathfinding timer
        self._pathfind_timer -= dt

        old_state = self.ai_state

        # State transitions
        if self.ai_state == AlertState.IDLE:
            if dist < self.detection_range and has_los:
                self.ai_state = AlertState.SUSPICIOUS
                self._ai_state_timer = self.suspicious_duration
                self._icon_timer = self._icon_duration
                self._last_known_px = player.center_x
                self._last_known_py = player.center_y

        elif self.ai_state == AlertState.SUSPICIOUS:
            self._ai_state_timer -= dt
            if has_los:
                self._last_known_px = player.center_x
                self._last_known_py = player.center_y
            if self._ai_state_timer <= 0:
                self.ai_state = AlertState.ALERT
                self._icon_timer = self._icon_duration
                self._cached_path = []
                self._pathfind_timer = 0.0  # Force immediate pathfind
            elif dist > self.detection_range or not has_los:
                # Player left detection range or broke LOS during suspicious
                self.ai_state = AlertState.IDLE
                self._cached_path = []

        elif self.ai_state == AlertState.ALERT:
            if has_los:
                self._last_known_px = player.center_x
                self._last_known_py = player.center_y
            if dist > self.lose_range or (not has_los and dist > self.detection_range):
                self.ai_state = AlertState.LOST
                self._ai_state_timer = self.lost_duration
                self._icon_timer = self._icon_duration

        elif self.ai_state == AlertState.LOST:
            self._ai_state_timer -= dt
            if dist < self.detection_range and has_los:
                # Re-detected player
                self.ai_state = AlertState.ALERT
                self._icon_timer = self._icon_duration
                self._last_known_px = player.center_x
                self._last_known_py = player.center_y
                self._cached_path = []
                self._pathfind_timer = 0.0
            elif self._ai_state_timer <= 0:
                self.ai_state = AlertState.IDLE
                self._cached_path = []

        # Update icon timer
        if self._icon_timer > 0:
            self._icon_timer -= dt

        # Determine movement target based on state
        if self.ai_state == AlertState.IDLE:
            return None  # Let enemy handle its own patrol

        elif self.ai_state == AlertState.SUSPICIOUS:
            # Slow approach toward last known position
            chase_speed = getattr(self, 'speed', 60.0) * 0.5
            return (self._last_known_px, self._last_known_py, chase_speed)

        elif self.ai_state == AlertState.ALERT:
            chase_speed = getattr(self, 'chase_speed', getattr(self, 'speed', 90.0))
            target_x = player.center_x + self._group_offset_x
            target_y = player.center_y + self._group_offset_y

            if self.use_pathfinding:
                target = self._follow_path(dt, tilemap, target_x, target_y, chase_speed)
                if target is not None:
                    return target

            # Fallback: direct movement
            return (target_x, target_y, chase_speed)

        elif self.ai_state == AlertState.LOST:
            # Move toward last known player position
            speed = getattr(self, 'speed', 60.0)
            return (self._last_known_px, self._last_known_py, speed)

        return None

    def _follow_path(self, dt, tilemap, target_x, target_y, speed):
        """Follow a cached A* path, recalculating when needed.

        Returns (target_x, target_y, speed) for the next waypoint, or None
        if no path is available.
        """
        # Recalculate path if timer expired
        if self._pathfind_timer <= 0 and can_pathfind():
            self._pathfind_timer = self.pathfind_interval
            self._cached_path = find_path(
                tilemap,
                self.center_x, self.center_y,
                target_x, target_y,
                max_distance=20,
                avoid_hazards=True,
            )
            self._path_index = 0

        if not self._cached_path:
            return None

        # Follow the path waypoints
        if self._path_index >= len(self._cached_path):
            return None

        wx, wy = self._cached_path[self._path_index]
        dx = wx - self.center_x
        dy = wy - self.center_y
        dist_to_wp = math.sqrt(dx * dx + dy * dy)

        # Advance to next waypoint when close enough
        if dist_to_wp < TILE_SIZE * 0.5:
            self._path_index += 1
            if self._path_index >= len(self._cached_path):
                return None
            wx, wy = self._cached_path[self._path_index]

        return (wx, wy, speed)

    def _ai_distance_to(self, target):
        """Calculate distance to a target entity."""
        dx = target.center_x - self.center_x
        dy = target.center_y - self.center_y
        return math.sqrt(dx * dx + dy * dy)

    def draw_alert_icon(self, surface, camera):
        """Draw the alert state icon (? or !) above the enemy."""
        if self._icon_timer <= 0:
            return

        icon = None
        if self.ai_state == AlertState.SUSPICIOUS:
            icon = _get_question_icon()
        elif self.ai_state == AlertState.ALERT:
            icon = _get_exclamation_icon()
        elif self.ai_state == AlertState.LOST:
            icon = _get_question_icon()

        if icon is None:
            return

        # Position above the enemy's head
        screen_x = int(self.center_x - camera.x - icon.get_width() // 2)
        screen_y = int(self.y - camera.y - icon.get_height() - 4)

        # Fade effect based on icon timer
        alpha = min(255, int(255 * (self._icon_timer / 0.3))) if self._icon_timer < 0.3 else 255

        if alpha < 255:
            icon_copy = icon.copy()
            icon_copy.set_alpha(alpha)
            surface.blit(icon_copy, (screen_x, screen_y))
        else:
            surface.blit(icon, (screen_x, screen_y))

    def set_group_offset(self, offset_x, offset_y):
        """Set an offset for group spread/flanking behavior."""
        self._group_offset_x = offset_x
        self._group_offset_y = offset_y


def update_group_behavior(enemies, player):
    """Update group offsets for enemies that are chasing the player.

    If 2+ enemies are chasing, spread them out to avoid clumping.
    Second enemy tries to approach from opposite side (flanking).
    """
    # Collect enemies that are in ALERT state and have AI
    alert_enemies = []
    for enemy in enemies:
        if not enemy.alive:
            continue
        if hasattr(enemy, 'ai_state') and enemy.ai_state == AlertState.ALERT:
            alert_enemies.append(enemy)

    if len(alert_enemies) < 2:
        # Reset offsets for single or no enemies
        for e in alert_enemies:
            e.set_group_offset(0, 0)
        return

    # Calculate spread offsets
    # Place enemies at evenly spaced angles around the player
    angle_step = 2 * math.pi / len(alert_enemies)
    spread_distance = TILE_SIZE * 1.5  # How far apart enemies try to be

    for i, enemy in enumerate(alert_enemies):
        angle = angle_step * i
        ox = math.cos(angle) * spread_distance
        oy = math.sin(angle) * spread_distance
        enemy.set_group_offset(ox, oy)
