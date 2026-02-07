"""Options menu accessible from title screen and pause menu."""

import pygame
from zelda_miloutte.states.state import State
from zelda_miloutte.settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, GOLD, GRAY, BLACK
from zelda_miloutte.sounds import get_sound_manager
from zelda_miloutte.user_settings import load_settings, save_settings


class OptionsState(State):
    """Full options menu with volume sliders, screen scale, fullscreen toggle, and controls display."""

    def __init__(self, game, from_pause=False):
        super().__init__(game)
        self.from_pause = from_pause
        self.title_font = None
        self.menu_font = None
        self.small_font = None
        self.settings = load_settings()
        self.selected_index = 0
        self.items = [
            "music_volume",
            "sfx_volume",
            "screen_scale",
            "fullscreen",
            "controls",
            "back",
        ]
        self.labels = {
            "music_volume": "Music Volume",
            "sfx_volume": "SFX Volume",
            "screen_scale": "Screen Scale",
            "fullscreen": "Fullscreen",
            "controls": "Controls",
            "back": "Back",
        }

    def _init_fonts(self):
        if self.title_font is None:
            self.title_font = pygame.font.Font(None, 52)
            self.menu_font = pygame.font.Font(None, 28)
            self.small_font = pygame.font.Font(None, 22)

    def enter(self):
        self.settings = load_settings()

    def _apply_settings(self):
        """Apply current settings to the game systems."""
        sm = get_sound_manager()
        sm.set_music_volume(self.settings["music_volume"] / 100.0)
        sm.set_sfx_volume(self.settings["sfx_volume"] / 100.0)
        save_settings(self.settings)

    def handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return

        item = self.items[self.selected_index]

        if event.key == pygame.K_UP:
            self.selected_index = (self.selected_index - 1) % len(self.items)
        elif event.key == pygame.K_DOWN:
            self.selected_index = (self.selected_index + 1) % len(self.items)
        elif event.key == pygame.K_LEFT:
            self._adjust(item, -1)
        elif event.key == pygame.K_RIGHT:
            self._adjust(item, 1)
        elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
            if item == "back":
                self._apply_settings()
                self.game.pop_state()
            elif item == "fullscreen":
                self._adjust(item, 1)
        elif event.key == pygame.K_ESCAPE:
            self._apply_settings()
            self.game.pop_state()

    def _adjust(self, item, direction):
        """Adjust a setting value by direction (-1 or +1)."""
        if item == "music_volume":
            self.settings["music_volume"] = max(0, min(100, self.settings["music_volume"] + direction * 5))
            get_sound_manager().set_music_volume(self.settings["music_volume"] / 100.0)
        elif item == "sfx_volume":
            self.settings["sfx_volume"] = max(0, min(100, self.settings["sfx_volume"] + direction * 5))
            get_sound_manager().set_sfx_volume(self.settings["sfx_volume"] / 100.0)
        elif item == "screen_scale":
            scales = [1, 2, 3]
            idx = scales.index(self.settings.get("screen_scale", 1))
            idx = max(0, min(2, idx + direction))
            self.settings["screen_scale"] = scales[idx]
        elif item == "fullscreen":
            self.settings["fullscreen"] = not self.settings["fullscreen"]

    def update(self, dt):
        pass

    def draw(self, surface):
        self._init_fonts()

        # If from pause, draw the underlying states
        if self.from_pause and len(self.game.states) >= 2:
            # Draw the state below us (could be pause which draws gameplay)
            self.game.states[-2].draw(surface)
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            surface.blit(overlay, (0, 0))
        else:
            surface.fill((20, 30, 20))

        # Title
        title = self.title_font.render("Options", True, WHITE)
        tx = (SCREEN_WIDTH - title.get_width()) // 2
        surface.blit(title, (tx, 50))

        # Menu items
        start_y = 120
        spacing = 42

        for i, key in enumerate(self.items):
            y = start_y + i * spacing
            is_selected = (i == self.selected_index)
            label_color = GOLD if is_selected else GRAY
            label = self.labels[key]

            if key == "music_volume":
                self._draw_slider(surface, label, self.settings["music_volume"], y, is_selected)
            elif key == "sfx_volume":
                self._draw_slider(surface, label, self.settings["sfx_volume"], y, is_selected)
            elif key == "screen_scale":
                val_text = f"{self.settings['screen_scale']}x"
                self._draw_option_row(surface, label, val_text, y, is_selected)
            elif key == "fullscreen":
                val_text = "On" if self.settings["fullscreen"] else "Off"
                self._draw_option_row(surface, label, val_text, y, is_selected)
            elif key == "controls":
                text = self.menu_font.render(label, True, label_color)
                x = (SCREEN_WIDTH - text.get_width()) // 2
                surface.blit(text, (x, y))
                if is_selected:
                    self._draw_controls_panel(surface, y + 28)
            elif key == "back":
                # Push back item further down if controls is expanded
                actual_y = y
                if self.selected_index == 4:  # controls selected
                    actual_y = y + 130
                text = self.menu_font.render(label, True, label_color)
                x = (SCREEN_WIDTH - text.get_width()) // 2
                surface.blit(text, (x, actual_y))

        # Navigation hint
        hint = self.small_font.render("Left/Right: Adjust    Enter: Select    ESC: Back", True, (120, 120, 120))
        hx = (SCREEN_WIDTH - hint.get_width()) // 2
        surface.blit(hint, (hx, SCREEN_HEIGHT - 40))

    def _draw_slider(self, surface, label, value, y, selected):
        """Draw a labeled slider bar."""
        label_color = GOLD if selected else GRAY
        text = self.menu_font.render(f"{label}:", True, label_color)
        label_x = SCREEN_WIDTH // 2 - 180
        surface.blit(text, (label_x, y))

        # Slider bar
        bar_x = SCREEN_WIDTH // 2 + 20
        bar_w = 150
        bar_h = 12
        bar_y = y + 6

        # Background
        pygame.draw.rect(surface, (60, 60, 60), (bar_x, bar_y, bar_w, bar_h))
        # Fill
        fill_w = int(bar_w * value / 100)
        fill_color = GOLD if selected else (100, 160, 100)
        pygame.draw.rect(surface, fill_color, (bar_x, bar_y, fill_w, bar_h))
        # Border
        border_color = WHITE if selected else GRAY
        pygame.draw.rect(surface, border_color, (bar_x, bar_y, bar_w, bar_h), 1)

        # Value text
        val_text = self.small_font.render(f"{value}%", True, label_color)
        surface.blit(val_text, (bar_x + bar_w + 10, y + 2))

    def _draw_option_row(self, surface, label, value_text, y, selected):
        """Draw a label: <value> row with arrows."""
        label_color = GOLD if selected else GRAY
        text = self.menu_font.render(f"{label}:", True, label_color)
        label_x = SCREEN_WIDTH // 2 - 180
        surface.blit(text, (label_x, y))

        val_color = WHITE if selected else GRAY
        arrow_left = "< " if selected else "  "
        arrow_right = " >" if selected else "  "
        val = self.menu_font.render(f"{arrow_left}{value_text}{arrow_right}", True, val_color)
        val_x = SCREEN_WIDTH // 2 + 50
        surface.blit(val, (val_x, y))

    def _draw_controls_panel(self, surface, y):
        """Draw the read-only controls display panel."""
        controls = [
            ("Arrow Keys / WASD", "Move"),
            ("Space", "Attack"),
            ("E / Enter", "Interact"),
            ("Escape", "Pause"),
            ("Shift / Right Click", "Shield / Block"),
            ("Q", "Cycle Ability"),
            ("R", "Use Ability"),
            ("N", "Toggle Minimap"),
            ("M", "Toggle World Map"),
        ]
        panel_x = SCREEN_WIDTH // 2 - 160
        for i, (key, action) in enumerate(controls):
            row_y = y + i * 18
            key_text = self.small_font.render(key, True, (180, 180, 180))
            action_text = self.small_font.render(action, True, (140, 200, 140))
            surface.blit(key_text, (panel_x, row_y))
            surface.blit(action_text, (panel_x + 200, row_y))
