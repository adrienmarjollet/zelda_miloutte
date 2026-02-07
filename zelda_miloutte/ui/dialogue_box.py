"""Enhanced dialogue box with NPC names, sequential messages, and choices."""

import pygame
from ..settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, GOLD, GRAY


class DialogueBox:
    """An enhanced dialogue box that supports NPC names, multiple messages, and choices."""

    def __init__(self):
        """Initialize the dialogue box."""
        # State
        self.active = False
        self.npc_name = ""
        self.messages = []      # list of str
        self.current_index = 0
        self.choices = []       # list of str, shown after messages
        self.choice_index = 0
        self.selected_choice = None  # set when player confirms a choice
        self._in_choice_mode = False

        # Typewriter effect
        self._revealed_chars = 0.0
        self._chars_per_second = 30.0
        self._fully_revealed = False

        # Blinking arrow
        self._blink_timer = 0.0
        self._blink_interval = 0.5
        self._show_arrow = False

        # Box dimensions
        self.width = SCREEN_WIDTH - 80
        self.height = 100
        self.x = 40
        self.y = SCREEN_HEIGHT - self.height - 20
        self.padding = 12

        # Fonts (lazy-init to avoid requiring pygame.font before display exists)
        self._font = None
        self._name_font = None

    @property
    def font(self):
        """Get the main text font."""
        if self._font is None:
            self._font = pygame.font.Font(None, 24)
        return self._font

    @property
    def name_font(self):
        """Get the NPC name font (slightly larger and bold)."""
        if self._name_font is None:
            self._name_font = pygame.font.Font(None, 28)
            self._name_font.set_bold(True)
        return self._name_font

    def show(self, npc_name, messages, choices=None):
        """Start showing dialogue. messages is a list of strings.

        Args:
            npc_name: The name of the NPC speaking
            messages: List of message strings to show sequentially
            choices: Optional list of choice strings to show after messages
        """
        self.active = True
        self.npc_name = npc_name
        self.messages = messages if isinstance(messages, list) else [messages]
        self.current_index = 0
        self.choices = choices if choices else []
        self.choice_index = 0
        self.selected_choice = None
        self._in_choice_mode = False
        self._revealed_chars = 0.0
        self._fully_revealed = False
        self._blink_timer = 0.0
        self._show_arrow = False

    def advance(self):
        """Called when player presses interact. Advances text or selects choice."""
        if not self.active:
            return

        # If in choice mode, select the current choice
        if self._in_choice_mode:
            self.selected_choice = self.choice_index
            self.dismiss()
            return

        # If text not fully revealed, reveal it all
        if not self._fully_revealed:
            self._revealed_chars = len(self._get_current_message())
            self._fully_revealed = True
            return

        # Move to next message
        if self.current_index < len(self.messages) - 1:
            self.current_index += 1
            self._revealed_chars = 0.0
            self._fully_revealed = False
            self._blink_timer = 0.0
            self._show_arrow = False
        else:
            # No more messages
            if self.choices:
                # Enter choice mode
                self._in_choice_mode = True
                self._blink_timer = 0.0
                self._show_arrow = False
            else:
                # No choices, just dismiss
                self.dismiss()

    def move_choice(self, direction):
        """Move choice selection up (-1) or down (+1).

        Args:
            direction: -1 for up, +1 for down
        """
        if not self._in_choice_mode or not self.choices:
            return

        self.choice_index = (self.choice_index + direction) % len(self.choices)

    def update(self, dt):
        """Update typewriter and blink.

        Args:
            dt: Delta time in seconds
        """
        if not self.active:
            return

        # Update typewriter if not in choice mode
        if not self._in_choice_mode and not self._fully_revealed:
            self._revealed_chars += dt * self._chars_per_second
            current_message = self._get_current_message()
            if self._revealed_chars >= len(current_message):
                self._revealed_chars = len(current_message)
                self._fully_revealed = True

        # Update blinking arrow (show when fully revealed or in choice mode)
        if self._fully_revealed or self._in_choice_mode:
            self._blink_timer += dt
            if self._blink_timer >= self._blink_interval:
                self._blink_timer = 0.0
                self._show_arrow = not self._show_arrow

    def draw(self, surface):
        """Draw the dialogue box with name header, text, and optionally choices.

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

        # Draw NPC name in gold at top-left
        name_surface = self.name_font.render(self.npc_name, True, GOLD)
        surface.blit(name_surface, (self.x + self.padding, self.y + self.padding))

        # Calculate starting Y position for message text (below name)
        name_height = self.name_font.get_height()
        text_y = self.y + self.padding + name_height + 4

        if self._in_choice_mode:
            # Draw choices
            self._draw_choices(surface, text_y)
        else:
            # Draw current message with word-wrapping
            revealed_text = self._get_current_message()[:int(self._revealed_chars)]
            self._draw_wrapped_text(
                surface,
                revealed_text,
                self.x + self.padding,
                text_y,
                self.width - 2 * self.padding
            )

        # Draw blinking indicator at bottom-right when ready to advance
        if (self._fully_revealed or self._in_choice_mode) and self._show_arrow:
            arrow_x = self.x + self.width - 20
            arrow_y = self.y + self.height - 16
            # Draw a small triangle pointing down
            points = [
                (arrow_x, arrow_y),
                (arrow_x + 8, arrow_y),
                (arrow_x + 4, arrow_y + 6)
            ]
            pygame.draw.polygon(surface, WHITE, points)

    def dismiss(self):
        """Close the dialogue."""
        self.active = False
        self.npc_name = ""
        self.messages = []
        self.current_index = 0
        self.choices = []
        self.choice_index = 0
        self._in_choice_mode = False
        self._revealed_chars = 0.0
        self._fully_revealed = False

    def _get_current_message(self):
        """Get the current message being displayed.

        Returns:
            The current message string
        """
        if 0 <= self.current_index < len(self.messages):
            return self.messages[self.current_index]
        return ""

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

    def _draw_choices(self, surface, start_y):
        """Draw the choice selection menu.

        Args:
            surface: The pygame surface to draw on
            start_y: Y position to start drawing choices
        """
        line_height = self.font.get_height() + 4
        x = self.x + self.padding + 20  # Indent choices slightly

        for i, choice in enumerate(self.choices):
            # Determine color based on selection
            color = GOLD if i == self.choice_index else GRAY

            # Draw selection arrow for current choice
            if i == self.choice_index:
                arrow_surface = self.font.render(">", True, GOLD)
                surface.blit(arrow_surface, (x - 16, start_y + i * line_height))

            # Draw choice text
            choice_surface = self.font.render(choice, True, color)
            surface.blit(choice_surface, (x, start_y + i * line_height))
