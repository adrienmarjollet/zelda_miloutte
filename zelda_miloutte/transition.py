import pygame
from .settings import SCREEN_WIDTH, SCREEN_HEIGHT


class Transition:
    """Manages fade-out -> callback -> fade-in screen transitions."""

    def __init__(self):
        self.active = False
        self.phase = "fade_out"  # "fade_out" or "fade_in"
        self.alpha = 0
        self.duration = 0.4  # Duration per phase in seconds
        self.callback = None
        self.timer = 0.0
        self.overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.overlay.fill((0, 0, 0))

    def start(self, callback, duration=0.4):
        """Start a transition with the given callback and duration per phase."""
        self.active = True
        self.phase = "fade_out"
        self.alpha = 0
        self.duration = duration
        self.callback = callback
        self.timer = 0.0

    def update(self, dt):
        """Update the transition state. Advances alpha and calls callback when appropriate."""
        if not self.active:
            return

        self.timer += dt
        progress = min(1.0, self.timer / self.duration)

        if self.phase == "fade_out":
            # Fade from transparent (0) to opaque (255)
            self.alpha = int(progress * 255)

            if progress >= 1.0:
                # Fade-out complete, call the callback and switch to fade-in
                if self.callback:
                    try:
                        self.callback()
                    except Exception as e:
                        import traceback
                        print(f"TRANSITION CALLBACK ERROR: {e}")
                        traceback.print_exc()
                self.phase = "fade_in"
                self.timer = 0.0
                self.alpha = 255

        elif self.phase == "fade_in":
            # Fade from opaque (255) to transparent (0)
            self.alpha = int((1.0 - progress) * 255)

            if progress >= 1.0:
                # Fade-in complete, end transition
                self.active = False
                self.alpha = 0

    def draw(self, surface):
        """Draw the transition overlay if active."""
        if self.active:
            self.overlay.set_alpha(self.alpha)
            surface.blit(self.overlay, (0, 0))
