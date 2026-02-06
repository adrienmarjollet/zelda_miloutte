"""Floating text that rises and fades out - used for XP gains, level ups, etc."""

import pygame


class FloatingText:
    """A text label that floats upward and fades over time."""

    def __init__(self, text, x, y, color=(255, 255, 255), size=20, duration=1.0):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.size = size
        self.duration = duration
        self.timer = 0.0
        self.alive = True
        self.rise_speed = 40.0  # pixels per second
        self._font = None

    def update(self, dt):
        self.timer += dt
        self.y -= self.rise_speed * dt
        if self.timer >= self.duration:
            self.alive = False

    def draw(self, surface, camera):
        if not self.alive:
            return
        if self._font is None:
            self._font = pygame.font.Font(None, self.size)

        alpha = max(0, int(255 * (1.0 - self.timer / self.duration)))
        sx = int(self.x - camera.x)
        sy = int(self.y - camera.y)

        text_surf = self._font.render(self.text, True, self.color)
        text_surf.set_alpha(alpha)
        # Center horizontally
        surface.blit(text_surf, (sx - text_surf.get_width() // 2, sy))
