import random
import math
from .settings import SCREEN_WIDTH, SCREEN_HEIGHT


class Camera:
    def __init__(self, map_width, map_height):
        self.x = 0.0
        self.y = 0.0
        self.map_width = map_width
        self.map_height = map_height

        # Screen shake state
        self.shake_timer = 0.0
        self.shake_duration = 0.0
        self.shake_intensity = 0.0
        self.shake_offset_x = 0.0
        self.shake_offset_y = 0.0

        # True camera position (without shake)
        self.true_x = 0.0
        self.true_y = 0.0

        # Zoom state (for boss intros)
        self.zoom = 1.0
        self._zoom_target = 1.0
        self._zoom_speed = 2.0

        # Camera punch (brief zoom impulse for big hits)
        self._punch_timer = 0.0
        self._punch_duration = 0.0
        self._punch_intensity = 0.0

        # Room-based camera: when a RoomManager is set, camera locks to room bounds
        self.room_manager = None

    def follow(self, target):
        """Center camera on target, clamped to map or room bounds."""
        if self.room_manager and self.room_manager.transitioning:
            # During room transition, the RoomManager controls camera position
            # (set via set_position), so don't override it here
            return

        if self.room_manager:
            # Lock camera to current room bounds
            cam_x, cam_y = self.room_manager.get_camera_pos_for_room(
                *self.room_manager.current_room
            )
            self.true_x = cam_x
            self.true_y = cam_y
        else:
            # Original behavior: center on target with map clamping
            target_cx = target.x + target.width / 2
            target_cy = target.y + target.height / 2

            self.true_x = target_cx - SCREEN_WIDTH / 2
            self.true_y = target_cy - SCREEN_HEIGHT / 2

            # Clamp to map bounds
            max_x = self.map_width - SCREEN_WIDTH
            max_y = self.map_height - SCREEN_HEIGHT

            if max_x < 0:
                self.true_x = max_x / 2  # Center if map smaller than screen
            else:
                self.true_x = max(0, min(self.true_x, max_x))

            if max_y < 0:
                self.true_y = max_y / 2
            else:
                self.true_y = max(0, min(self.true_y, max_y))

        # Apply shake offset to the actual camera position
        self.x = self.true_x + self.shake_offset_x
        self.y = self.true_y + self.shake_offset_y

    def set_position(self, x, y):
        """Set camera position directly (used during room transitions)."""
        self.true_x = x
        self.true_y = y
        self.x = self.true_x + self.shake_offset_x
        self.y = self.true_y + self.shake_offset_y

    def shake(self, intensity, duration):
        """Start a screen shake effect.

        Args:
            intensity: Maximum pixel offset (e.g., 4-8 pixels)
            duration: Duration in seconds
        """
        self.shake_intensity = intensity
        self.shake_duration = duration
        self.shake_timer = duration

    def start_zoom(self, target_zoom, speed=2.0):
        """Start a smooth zoom effect.

        Args:
            target_zoom: Target zoom level (1.0 = normal, 1.3 = zoomed in)
            speed: How fast to zoom (units per second)
        """
        self._zoom_target = target_zoom
        self._zoom_speed = speed

    def punch(self, intensity=0.05, duration=0.2):
        """Brief camera zoom punch for impactful moments.

        The zoom goes from 1.0 -> 1.0+intensity -> 1.0 over duration using
        a sine curve for smooth in/out.

        Args:
            intensity: How much extra zoom at peak (e.g. 0.05 = 5% zoom)
            duration: Total punch duration in seconds
        """
        self._punch_intensity = intensity
        self._punch_duration = duration
        self._punch_timer = duration

    def update_zoom(self, dt):
        """Update zoom interpolation and camera punch."""
        # Camera punch overlay
        if self._punch_timer > 0:
            self._punch_timer -= dt
            if self._punch_timer <= 0:
                self._punch_timer = 0.0
            else:
                # Sine curve: peaks at midpoint, returns to 0 at edges
                progress = 1.0 - (self._punch_timer / self._punch_duration)
                punch_zoom = self._punch_intensity * math.sin(progress * math.pi)
                self.zoom = self._zoom_target + punch_zoom
                return

        if abs(self.zoom - self._zoom_target) > 0.01:
            if self.zoom < self._zoom_target:
                self.zoom = min(self._zoom_target, self.zoom + self._zoom_speed * dt)
            else:
                self.zoom = max(self._zoom_target, self.zoom - self._zoom_speed * dt)
        else:
            self.zoom = self._zoom_target

    def update_shake(self, dt):
        """Update the shake effect. Call this each frame."""
        if self.shake_timer > 0:
            self.shake_timer -= dt

            if self.shake_timer <= 0:
                # Shake finished
                self.shake_timer = 0
                self.shake_offset_x = 0.0
                self.shake_offset_y = 0.0
            else:
                # Calculate shake with decay over time
                decay = self.shake_timer / self.shake_duration
                current_intensity = self.shake_intensity * decay

                # Random offset within intensity range
                self.shake_offset_x = random.uniform(-current_intensity, current_intensity)
                self.shake_offset_y = random.uniform(-current_intensity, current_intensity)
        else:
            self.shake_offset_x = 0.0
            self.shake_offset_y = 0.0
