"""Credits screen with scrolling text and starfield background."""

import math
import random
import pygame
from zelda_miloutte.states.state import State
from zelda_miloutte.settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, GOLD, GRAY


class CreditsState(State):
    """Scrolling credits with starfield particle background."""

    def __init__(self, game):
        super().__init__(game)
        self.title_font = None
        self.heading_font = None
        self.text_font = None
        self.small_font = None
        self.scroll_y = SCREEN_HEIGHT
        self.scroll_speed = 40.0  # pixels per second
        self.stars = []
        self._init_stars()

        self.credits_lines = [
            ("title", "Zelda Miloutte"),
            ("blank", ""),
            ("heading", "A Tiny Adventure"),
            ("blank", ""),
            ("blank", ""),
            ("heading", "Game Design & Programming"),
            ("text", "Built with love and code"),
            ("blank", ""),
            ("heading", "Technology"),
            ("text", "Python & pygame-ce (Community Edition)"),
            ("blank", ""),
            ("heading", "Art"),
            ("text", "All pixel art procedurally generated"),
            ("text", "Using ASCII grids and color palettes"),
            ("text", "No external image assets"),
            ("blank", ""),
            ("heading", "Music & Sound"),
            ("text", "Programmatically synthesized audio"),
            ("text", "All sounds generated from sine waves,"),
            ("text", "triangles, and noise functions"),
            ("blank", ""),
            ("heading", "World Building"),
            ("text", "Overworld, Forest, Desert, Volcano, and Ice"),
            ("text", "regions with unique enemies and bosses"),
            ("blank", ""),
            ("heading", "Features"),
            ("text", "Quest system with NPC interactions"),
            ("text", "Day/night cycle with dynamic lighting"),
            ("text", "Combo combat with parry and dodge"),
            ("text", "Achievement and bestiary tracking"),
            ("text", "Multiple save slots"),
            ("blank", ""),
            ("heading", "Special Thanks"),
            ("text", "The pygame-ce community"),
            ("text", "Everyone who plays this game"),
            ("blank", ""),
            ("blank", ""),
            ("heading", "Thank you for playing!"),
            ("blank", ""),
            ("blank", ""),
            ("text", "Press any key to return"),
        ]

    def _init_stars(self):
        """Create background starfield."""
        self.stars = []
        for _ in range(80):
            self.stars.append({
                "x": random.randint(0, SCREEN_WIDTH),
                "y": random.randint(0, SCREEN_HEIGHT),
                "speed": random.uniform(5, 25),
                "size": random.choice([1, 1, 1, 2]),
                "brightness": random.randint(100, 255),
                "twinkle_offset": random.uniform(0, 6.28),
            })

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            self.game.pop_state()

    def update(self, dt):
        self.scroll_y -= self.scroll_speed * dt

        # Update stars
        for star in self.stars:
            star["y"] += star["speed"] * dt
            if star["y"] > SCREEN_HEIGHT:
                star["y"] = 0
                star["x"] = random.randint(0, SCREEN_WIDTH)

        # Check if credits have fully scrolled
        total_height = self._get_total_height()
        if self.scroll_y < -total_height:
            self.game.pop_state()

    def _get_total_height(self):
        """Calculate total height of all credits lines."""
        height = 0
        for line_type, _ in self.credits_lines:
            if line_type == "title":
                height += 60
            elif line_type == "heading":
                height += 40
            elif line_type == "text":
                height += 28
            else:  # blank
                height += 20
        return height

    def draw(self, surface):
        self._init_fonts()
        surface.fill((5, 5, 15))

        # Draw starfield
        time_val = pygame.time.get_ticks() / 1000.0
        for star in self.stars:
            twinkle = math.sin(time_val * 2 + star["twinkle_offset"])
            brightness = int(star["brightness"] * (0.6 + 0.4 * twinkle))
            brightness = max(40, min(255, brightness))
            color = (brightness, brightness, brightness + min(20, 255 - brightness))
            if star["size"] == 1:
                surface.set_at((int(star["x"]), int(star["y"])), color)
            else:
                pygame.draw.circle(surface, color, (int(star["x"]), int(star["y"])), star["size"])

        # Draw scrolling credits
        y = self.scroll_y
        for line_type, text in self.credits_lines:
            if line_type == "title":
                rendered = self.title_font.render(text, True, GOLD)
                x = (SCREEN_WIDTH - rendered.get_width()) // 2
                if -60 < y < SCREEN_HEIGHT + 60:
                    surface.blit(rendered, (x, y))
                y += 60
            elif line_type == "heading":
                rendered = self.heading_font.render(text, True, GOLD)
                x = (SCREEN_WIDTH - rendered.get_width()) // 2
                if -40 < y < SCREEN_HEIGHT + 40:
                    surface.blit(rendered, (x, y))
                y += 40
            elif line_type == "text":
                rendered = self.text_font.render(text, True, (200, 200, 200))
                x = (SCREEN_WIDTH - rendered.get_width()) // 2
                if -28 < y < SCREEN_HEIGHT + 28:
                    surface.blit(rendered, (x, y))
                y += 28
            else:  # blank
                y += 20

    def _init_fonts(self):
        if self.title_font is None:
            self.title_font = pygame.font.Font(None, 56)
            self.heading_font = pygame.font.Font(None, 32)
            self.text_font = pygame.font.Font(None, 24)
            self.small_font = pygame.font.Font(None, 20)
