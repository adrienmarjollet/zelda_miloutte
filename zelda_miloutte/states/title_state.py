import math
import time
import random
import pygame
from .state import State
from ..settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, GOLD, BLACK, GREEN, GRAY
from ..sounds import get_sound_manager
from ..sprites.pixel_art import surface_from_grid


# ── Big Sword pixel art (32 wide x 64 tall, scale 4 = 128x256 on screen) ──
_SWORD_PAL = {
    '.': None,
    'o': (40, 40, 50),       # outline
    'w': (210, 215, 230),    # blade main
    'W': (240, 245, 255),    # blade highlight
    'b': (170, 175, 195),    # blade shadow
    'g': (255, 200, 50),     # gold guard
    'G': (200, 155, 30),     # gold dark
    'h': (110, 70, 35),      # handle brown
    'H': (85, 55, 30),       # handle dark
    'r': (180, 40, 40),      # ruby gem
    'R': (220, 80, 80),      # ruby highlight
    'e': (30, 180, 80),      # emerald
}

_SWORD_GRID = [
    "......oWo......",
    ".....oWWWo.....",
    ".....oWWWo.....",
    "....oWWWWWo....",
    "....oWwWwWo....",
    "....oWwWwWo....",
    "...oWWwWwWWo...",
    "...oWwwWwwWo...",
    "...oWwwWwwWo...",
    "...obwwWwwbo...",
    "...obwwWwwbo...",
    "...obwwWwwbo...",
    "..obbwwWwwbbo..",
    "..obbwwWwwbbo..",
    "..obbwwWwwbbo..",
    "..obbwwWwwbbo..",
    "..obbwwWwwbbo..",
    "..obbwwWwwbbo..",
    "..obbwwWwwbbo..",
    "..obbwwWwwbbo..",
    "..obbwwWwwbbo..",
    "..obbwwWwwbbo..",
    "..obbwwWwwbbo..",
    "..obwwwWwwwbo..",
    "..obwwwWwwwbo..",
    "..obwwwWwwwbo..",
    ".oGGGGGGGGGGGo.",
    ".oGggrRrggGGGo.",
    ".oGGGGGGGGGGGo.",
    "...oHhhhhhHo...",
    "...oHhHhHhHo...",
    "...oHhhhhhHo...",
    "...oHhHhHhHo...",
    "...oHhhhhhHo...",
    "...oHhHhHhHo...",
    "...oHhhhhhHo...",
    "....oGGeGGo....",
    ".....oGGGo.....",
    "......ooo......",
]


def _build_sword_surface():
    """Build the big title sword (scaled up)."""
    return surface_from_grid(_SWORD_GRID, _SWORD_PAL, scale=4)


class _Sparkle:
    """A floating light particle for the title screen."""
    def __init__(self):
        self.reset()
        self.y = random.random() * SCREEN_HEIGHT

    def reset(self):
        self.x = random.random() * SCREEN_WIDTH
        self.y = -10
        self.speed = random.uniform(20, 60)
        self.size = random.uniform(1.5, 3.5)
        self.alpha = random.randint(120, 255)
        self.drift = random.uniform(-15, 15)
        self.color = random.choice([
            (255, 200, 50),   # gold
            (255, 255, 200),  # warm white
            (200, 220, 255),  # cool white
            (100, 200, 255),  # blue
        ])

    def update(self, dt):
        self.y += self.speed * dt
        self.x += self.drift * dt
        if self.y > SCREEN_HEIGHT + 10:
            self.reset()

    def draw(self, surface):
        s = pygame.Surface((int(self.size * 2 + 2), int(self.size * 2 + 2)), pygame.SRCALPHA)
        pygame.draw.circle(s, (*self.color, self.alpha),
                           (int(self.size + 1), int(self.size + 1)), int(self.size))
        surface.blit(s, (int(self.x - self.size), int(self.y - self.size)))


class TitleState(State):
    def __init__(self, game):
        super().__init__(game)
        self.title_font = None
        self.subtitle_font = None
        self.prompt_font = None
        self.small_font = None
        self.menu_font = None
        self.blink_timer = 0.0
        self.show_prompt = True
        self.elapsed = 0.0

        # Sword
        self.sword_surface = None
        self.sword_y_offset = 0.0

        # Sparkle particles
        self.sparkles = [_Sparkle() for _ in range(40)]

        # Phase: "intro" = press enter screen, "menu" = main menu
        self.phase = "intro"

        # Menu state
        self.mode = "main"  # "main", "load_slots"
        self.menu_items = ["New Game", "Continue"]
        self.selected_index = 0
        self.saves = {}

    def enter(self):
        get_sound_manager().play_music('title')
        self.saves = self.game.save_manager.list_saves()

    def _init_fonts(self):
        if self.title_font is None:
            self.title_font = pygame.font.Font(None, 80)
            self.subtitle_font = pygame.font.Font(None, 32)
            self.prompt_font = pygame.font.Font(None, 28)
            self.small_font = pygame.font.Font(None, 22)
            self.menu_font = pygame.font.Font(None, 36)

    def _init_sword(self):
        if self.sword_surface is None:
            self.sword_surface = _build_sword_surface()

    def _has_saves(self):
        return any(v is not None for v in self.saves.values())

    def _start_new_game(self):
        from .play_state import PlayState
        self.game.world_state = {
            "defeated_bosses": [],
            "opened_chests": [],
            "current_area": "overworld",
            "story_progress": 0,
        }
        self.game.save_data = {}
        play = PlayState(self.game)
        self.game.change_state(play)

    def _load_slot(self, slot):
        data = self.game.save_manager.load_game(slot)
        if data is None:
            return
        self.game.save_data = data
        self.game.world_state = {
            "defeated_bosses": data.get("defeated_bosses", []),
            "opened_chests": data.get("opened_chests", []),
            "current_area": data.get("current_area", "overworld"),
            "story_progress": data.get("story_progress", 0),
        }

        from .play_state import PlayState
        play = PlayState(self.game, load_data=data)
        self.game.change_state(play)

    def handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return

        if self.phase == "intro":
            if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                self.phase = "menu"
            return

        # Menu phase
        if self.mode == "main":
            if event.key == pygame.K_UP:
                self.selected_index = (self.selected_index - 1) % len(self.menu_items)
            elif event.key == pygame.K_DOWN:
                self.selected_index = (self.selected_index + 1) % len(self.menu_items)
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                if self.selected_index == 0:  # New Game
                    self.game.transition_to(self._start_new_game)
                elif self.selected_index == 1:  # Continue
                    if self._has_saves():
                        self.mode = "load_slots"
                        self.selected_index = 0
            elif event.key == pygame.K_ESCAPE:
                pass

        elif self.mode == "load_slots":
            if event.key == pygame.K_UP:
                self.selected_index = (self.selected_index - 1) % 3
            elif event.key == pygame.K_DOWN:
                self.selected_index = (self.selected_index + 1) % 3
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                slot = self.selected_index + 1
                if self.saves.get(slot) is not None:
                    self.game.transition_to(lambda: self._load_slot(slot))
            elif event.key == pygame.K_ESCAPE:
                self.mode = "main"
                self.selected_index = 0

    def update(self, dt):
        self.elapsed += dt
        self.blink_timer += dt
        if self.blink_timer >= 0.5:
            self.blink_timer = 0.0
            self.show_prompt = not self.show_prompt

        # Sword gentle float
        self.sword_y_offset = math.sin(self.elapsed * 1.2) * 8

        # Sparkles
        for s in self.sparkles:
            s.update(dt)

    def draw(self, surface):
        self._init_fonts()
        self._init_sword()

        # Dark gradient background
        for y in range(SCREEN_HEIGHT):
            t = y / SCREEN_HEIGHT
            r = int(10 + 15 * t)
            g = int(15 + 30 * t)
            b = int(25 + 10 * t)
            pygame.draw.line(surface, (r, g, b), (0, y), (SCREEN_WIDTH, y))

        # Sparkles behind sword
        for s in self.sparkles:
            s.draw(surface)

        if self.phase == "intro":
            self._draw_intro(surface)
        else:
            self._draw_menu_phase(surface)

    def _draw_intro(self, surface):
        # Big sword centered
        sw = self.sword_surface.get_width()
        sh = self.sword_surface.get_height()
        sx = (SCREEN_WIDTH - sw) // 2
        sy = (SCREEN_HEIGHT - sh) // 2 - 40 + int(self.sword_y_offset)

        # Glow behind sword
        glow_alpha = int(80 + 40 * math.sin(self.elapsed * 2))
        glow = pygame.Surface((sw + 60, sh + 60), pygame.SRCALPHA)
        pygame.draw.ellipse(glow, (255, 200, 50, glow_alpha),
                            (0, 0, sw + 60, sh + 60))
        surface.blit(glow, (sx - 30, sy - 30))

        surface.blit(self.sword_surface, (sx, sy))

        # Title with shadow
        title_text = "ZELDA MILOUTTE"
        # Fade in title over first 2 seconds
        alpha = min(255, int(self.elapsed * 127))

        shadow = self.title_font.render(title_text, True, (20, 20, 20))
        shadow.set_alpha(alpha)
        title = self.title_font.render(title_text, True, GOLD)
        title.set_alpha(alpha)

        tx = (SCREEN_WIDTH - title.get_width()) // 2
        ty = 30
        surface.blit(shadow, (tx + 2, ty + 2))
        surface.blit(title, (tx, ty))

        # Subtitle
        sub_text = "~ A Tiny Adventure ~"
        sub = self.subtitle_font.render(sub_text, True, (150, 220, 150))
        sub.set_alpha(alpha)
        stx = (SCREEN_WIDTH - sub.get_width()) // 2
        surface.blit(sub, (stx, ty + 70))

        # "Press Enter" blinking at bottom
        if self.elapsed > 1.5 and self.show_prompt:
            press = self.prompt_font.render("- Press Enter -", True, WHITE)
            px = (SCREEN_WIDTH - press.get_width()) // 2
            py = SCREEN_HEIGHT - 80
            press.set_alpha(200)
            surface.blit(press, (px, py))

    def _draw_menu_phase(self, surface):
        # Smaller sword on the left side
        sw = self.sword_surface.get_width()
        sh = self.sword_surface.get_height()
        # Scale down for menu background
        small_sword = pygame.transform.smoothscale(self.sword_surface, (sw // 2, sh // 2))
        ssw = small_sword.get_width()
        ssh = small_sword.get_height()
        small_sword.set_alpha(80)
        surface.blit(small_sword, (40, (SCREEN_HEIGHT - ssh) // 2 + int(self.sword_y_offset)))

        # Title at top
        title = self.title_font.render("ZELDA MILOUTTE", True, GOLD)
        shadow = self.title_font.render("ZELDA MILOUTTE", True, (20, 20, 20))
        tx = (SCREEN_WIDTH - title.get_width()) // 2
        surface.blit(shadow, (tx + 2, 32))
        surface.blit(title, (tx, 30))

        sub = self.subtitle_font.render("~ A Tiny Adventure ~", True, (150, 220, 150))
        stx = (SCREEN_WIDTH - sub.get_width()) // 2
        surface.blit(sub, (stx, 100))

        if self.mode == "main":
            self._draw_main_menu(surface)
        elif self.mode == "load_slots":
            self._draw_load_slots(surface)

        # Controls at bottom
        controls = self.small_font.render("WASD/Arrows: Move    Space: Attack    E: Interact", True, (150, 150, 150))
        cx = (SCREEN_WIDTH - controls.get_width()) // 2
        surface.blit(controls, (cx, SCREEN_HEIGHT - 50))

    def _draw_main_menu(self, surface):
        menu_y = SCREEN_HEIGHT // 2 + 20
        for i, item in enumerate(self.menu_items):
            if i == 1 and not self._has_saves():
                color = (80, 80, 80)
            elif i == self.selected_index:
                color = GOLD
            else:
                color = GRAY

            # Draw selector arrow
            text = self.menu_font.render(item, True, color)
            x = (SCREEN_WIDTH - text.get_width()) // 2
            y = menu_y + i * 50

            if i == self.selected_index and not (i == 1 and not self._has_saves()):
                arrow = self.menu_font.render(">", True, GOLD)
                surface.blit(arrow, (x - 30, y))

            surface.blit(text, (x, y))

    def _draw_load_slots(self, surface):
        header = self.prompt_font.render("Select Save Slot", True, WHITE)
        hx = (SCREEN_WIDTH - header.get_width()) // 2
        surface.blit(header, (hx, SCREEN_HEIGHT // 2 - 20))

        slot_y = SCREEN_HEIGHT // 2 + 30
        for i in range(3):
            slot = i + 1
            info = self.saves.get(slot)
            if info is not None:
                ts = time.strftime("%Y-%m-%d %H:%M", time.localtime(info["timestamp"]))
                label = f"Slot {slot}: Lv.{info['level']} - {info['area']} ({ts})"
            else:
                label = f"Slot {slot}: Empty"
            color = GOLD if i == self.selected_index else GRAY
            if info is None:
                color = (80, 80, 80) if i != self.selected_index else (100, 100, 100)
            text = self.small_font.render(label, True, color)
            x = (SCREEN_WIDTH - text.get_width()) // 2
            surface.blit(text, (x, slot_y + i * 35))

        back = self.small_font.render("ESC: Back", True, (120, 120, 120))
        surface.blit(back, ((SCREEN_WIDTH - back.get_width()) // 2, slot_y + 130))
