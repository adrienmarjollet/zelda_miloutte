"""How to Play screen showing controls and animated player demonstrations."""

import math
import pygame
from zelda_miloutte.states.state import State
from zelda_miloutte.settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, GOLD, GRAY, GREEN


class HowToPlayState(State):
    """Tutorial screen showing game controls with animated player sprite demonstrations."""

    def __init__(self, game):
        super().__init__(game)
        self.title_font = None
        self.heading_font = None
        self.text_font = None
        self.small_font = None
        self.timer = 0.0
        self.anim_frame = 0

    def _init_fonts(self):
        if self.title_font is None:
            self.title_font = pygame.font.Font(None, 48)
            self.heading_font = pygame.font.Font(None, 30)
            self.text_font = pygame.font.Font(None, 24)
            self.small_font = pygame.font.Font(None, 20)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            self.game.pop_state()

    def update(self, dt):
        self.timer += dt
        if self.timer >= 0.4:
            self.timer -= 0.4
            self.anim_frame = (self.anim_frame + 1) % 4

    def draw(self, surface):
        self._init_fonts()
        surface.fill((15, 25, 15))

        # Title
        title = self.title_font.render("How to Play", True, GOLD)
        tx = (SCREEN_WIDTH - title.get_width()) // 2
        surface.blit(title, (tx, 30))

        # Decorative line
        line_y = 70
        pygame.draw.line(surface, (80, 120, 80), (100, line_y), (SCREEN_WIDTH - 100, line_y), 1)

        # Control sections
        controls = [
            ("Movement", "Arrow Keys / WASD", "Move your character in 4 directions. Diagonal movement is supported."),
            ("Attack", "Space", "Swing your sword. Hold for a charged attack. Chain hits for combos."),
            ("Interact", "E / Enter", "Talk to NPCs, read signs, open chests, and enter doors."),
            ("Pause", "Escape", "Open the pause menu to save your progress or adjust settings."),
            ("Shield", "Shift / Right Click", "Block incoming attacks. Time it perfectly for a parry."),
            ("Dodge", "Double-tap Direction", "Quickly double-tap a direction key to dodge roll."),
            ("Abilities", "Q: Cycle / R: Use", "Switch between unlocked abilities and activate them."),
            ("Map", "N: Mini / M: World", "Toggle the minimap overlay or open the full world map."),
        ]

        start_y = 90
        row_height = 58

        for i, (action, keys, desc) in enumerate(controls):
            y = start_y + i * row_height

            # Draw small animated indicator
            indicator_x = 60
            dot_offset = math.sin(self.timer * 8 + i * 0.8) * 3
            pygame.draw.circle(surface, GREEN, (indicator_x, int(y + 14 + dot_offset)), 4)

            # Action name
            action_text = self.heading_font.render(action, True, GOLD)
            surface.blit(action_text, (85, y))

            # Key binding
            key_text = self.text_font.render(f"[{keys}]", True, (140, 200, 140))
            surface.blit(key_text, (85 + action_text.get_width() + 15, y + 3))

            # Description
            desc_text = self.small_font.render(desc, True, GRAY)
            surface.blit(desc_text, (85, y + 26))

        # Animated player character demo
        self._draw_player_demo(surface)

        # Footer
        footer = self.text_font.render("Press any key to return", True, (150, 150, 150))
        fx = (SCREEN_WIDTH - footer.get_width()) // 2
        surface.blit(footer, (fx, SCREEN_HEIGHT - 40))

    def _draw_player_demo(self, surface):
        """Draw a small animated pixel character in the corner."""
        # Simple 8x8 player character frames (walk cycle)
        base_x = SCREEN_WIDTH - 80
        base_y = SCREEN_HEIGHT - 120
        scale = 3

        # Simple character representation using rectangles
        frame = self.anim_frame
        body_color = (60, 140, 60)
        skin_color = (240, 210, 180)
        hair_color = (255, 200, 50)
        boot_color = (65, 45, 30)

        # Head (hair)
        pygame.draw.rect(surface, hair_color, (base_x, base_y, 8 * scale, 4 * scale))
        # Face
        pygame.draw.rect(surface, skin_color, (base_x + scale, base_y + 2 * scale, 6 * scale, 3 * scale))
        # Eyes
        pygame.draw.rect(surface, (30, 120, 60), (base_x + 2 * scale, base_y + 3 * scale, scale, scale))
        pygame.draw.rect(surface, (30, 120, 60), (base_x + 5 * scale, base_y + 3 * scale, scale, scale))
        # Body
        pygame.draw.rect(surface, body_color, (base_x + scale, base_y + 5 * scale, 6 * scale, 4 * scale))
        # Legs (animated)
        leg_offset = [0, 1, 0, -1][frame]
        pygame.draw.rect(surface, boot_color,
                         (base_x + 2 * scale, base_y + 9 * scale + leg_offset, 2 * scale, 2 * scale))
        pygame.draw.rect(surface, boot_color,
                         (base_x + 4 * scale, base_y + 9 * scale - leg_offset, 2 * scale, 2 * scale))

        # Sword (swings on frame 2)
        sword_color = (210, 215, 230)
        if frame == 2:
            pygame.draw.rect(surface, sword_color,
                             (base_x + 8 * scale, base_y + 4 * scale, 4 * scale, scale))
        else:
            pygame.draw.rect(surface, sword_color,
                             (base_x + 7 * scale, base_y + 3 * scale, scale, 4 * scale))
