import random
from zelda_miloutte.settings import SCREEN_WIDTH, SCREEN_HEIGHT


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

    def follow(self, target):
        # Center camera on target
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

    def shake(self, intensity, duration):
        """Start a screen shake effect.

        Args:
            intensity: Maximum pixel offset (e.g., 4-8 pixels)
            duration: Duration in seconds
        """
        self.shake_intensity = intensity
        self.shake_duration = duration
        self.shake_timer = duration

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
