"""Classic Zelda-style textbox for displaying dialogue."""

import pygame
from ..settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK


class TextBox:
    """A dialogue textbox that appears at the bottom of the screen."""

    def __init__(self):
        """Initialize the textbox."""
        self.active = False
        self.text = ""
        self._revealed_chars = 0.0
        self._chars_per_second = 30.0
        self._fully_revealed = False

        # Box dimensions
        self.width = SCREEN_WIDTH - 80
        self.height = 80
        self.x = 40
        self.y = SCREEN_HEIGHT - self.height - 20

        # Text padding
        self.padding = 12

        # Font (lazy-init to avoid requiring pygame.font before display exists)
        self._font = None

        # Blinking arrow indicator
        self._blink_timer = 0.0
        self._blink_interval = 0.5
        self._show_arrow = False

    @property
    def font(self):
        if self._font is None:
            self._font = pygame.font.Font(None, 24)
        return self._font

    def show(self, text):
        """Start displaying the given text with typewriter effect.

        Args:
            text: The message to display
        """
        self.active = True
        self.text = text
        self._revealed_chars = 0.0
        self._fully_revealed = False
        self._blink_timer = 0.0
        self._show_arrow = False

    def update(self, dt):
        """Update the textbox state, revealing characters over time.

        Args:
            dt: Delta time in seconds
        """
        if not self.active:
            return

        # Reveal characters
        if not self._fully_revealed:
            self._revealed_chars += dt * self._chars_per_second
            if self._revealed_chars >= len(self.text):
                self._revealed_chars = len(self.text)
                self._fully_revealed = True

        # Update blinking arrow
        if self._fully_revealed:
            self._blink_timer += dt
            if self._blink_timer >= self._blink_interval:
                self._blink_timer = 0.0
                self._show_arrow = not self._show_arrow

    def dismiss(self):
        """Close the textbox."""
        self.active = False
        self.text = ""
        self._revealed_chars = 0.0
        self._fully_revealed = False

    def draw(self, surface):
        """Draw the textbox on the screen (NOT affected by camera).

        Args:
            surface: The pygame surface to draw on
        """
        if not self.active:
            return

        # Semi-transparent dark background
        bg_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        bg_surface.fill((0, 0, 0, 200))
        surface.blit(bg_surface, (self.x, self.y))

        # White border
        pygame.draw.rect(surface, WHITE, (self.x, self.y, self.width, self.height), 2)

        # Render text (word-wrapped)
        revealed_text = self.text[:int(self._revealed_chars)]
        self._draw_wrapped_text(surface, revealed_text, self.x + self.padding, self.y + self.padding,
                               self.width - 2 * self.padding)

        # Draw blinking indicator (triangle/arrow) at bottom-right when done
        if self._fully_revealed and self._show_arrow:
            arrow_x = self.x + self.width - 20
            arrow_y = self.y + self.height - 16
            # Draw a small triangle pointing down
            points = [
                (arrow_x, arrow_y),
                (arrow_x + 8, arrow_y),
                (arrow_x + 4, arrow_y + 6)
            ]
            pygame.draw.polygon(surface, WHITE, points)

    def _draw_wrapped_text(self, surface, text, x, y, max_width):
        """Draw text with word wrapping.

        Args:
            surface: The pygame surface to draw on
            text: The text to draw
            x, y: Position to start drawing
            max_width: Maximum width before wrapping
        """
        words = text.split(' ')
        lines = []
        current_line = ""

        for word in words:
            test_line = current_line + word + " " if current_line else word + " "
            test_surface = self.font.render(test_line, True, WHITE)

            if test_surface.get_width() <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line.rstrip())
                current_line = word + " "

        if current_line:
            lines.append(current_line.rstrip())

        # Draw each line
        line_height = self.font.get_height()
        for i, line in enumerate(lines):
            text_surface = self.font.render(line, True, WHITE)
            surface.blit(text_surface, (x, y + i * line_height))
