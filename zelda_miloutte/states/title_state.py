import time
import pygame
from zelda_miloutte.states.state import State
from zelda_miloutte.settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, GOLD, BLACK, GREEN, GRAY
from zelda_miloutte.sounds import get_sound_manager


class TitleState(State):
    def __init__(self, game):
        super().__init__(game)
        self.title_font = None
        self.prompt_font = None
        self.small_font = None
        self.blink_timer = 0.0
        self.show_prompt = True

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
            self.title_font = pygame.font.Font(None, 64)
            self.prompt_font = pygame.font.Font(None, 28)
            self.small_font = pygame.font.Font(None, 22)

    def _has_saves(self):
        return any(v is not None for v in self.saves.values())

    def _start_new_game(self):
        from zelda_miloutte.states.play_state import PlayState
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

        from zelda_miloutte.states.play_state import PlayState
        play = PlayState(self.game, load_data=data)
        self.game.change_state(play)

    def handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return

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
        self.blink_timer += dt
        if self.blink_timer >= 0.6:
            self.blink_timer = 0.0
            self.show_prompt = not self.show_prompt

    def draw(self, surface):
        self._init_fonts()
        surface.fill((20, 40, 20))

        # Title
        title = self.title_font.render("Zelda Miloutte", True, GOLD)
        tx = (SCREEN_WIDTH - title.get_width()) // 2
        surface.blit(title, (tx, 80))

        # Subtitle
        sub = self.prompt_font.render("A tiny adventure", True, GREEN)
        sx = (SCREEN_WIDTH - sub.get_width()) // 2
        surface.blit(sub, (sx, 145))

        if self.mode == "main":
            self._draw_main_menu(surface)
        elif self.mode == "load_slots":
            self._draw_load_slots(surface)

        # Controls
        controls = self.small_font.render("WASD/Arrows: Move    Space: Attack    E: Interact", True, (150, 150, 150))
        cx = (SCREEN_WIDTH - controls.get_width()) // 2
        surface.blit(controls, (cx, SCREEN_HEIGHT - 50))

    def _draw_main_menu(self, surface):
        menu_y = SCREEN_HEIGHT // 2 + 20
        for i, item in enumerate(self.menu_items):
            if i == 1 and not self._has_saves():
                color = (80, 80, 80)  # Dim if no saves
            elif i == self.selected_index:
                color = GOLD
            else:
                color = GRAY
            text = self.prompt_font.render(item, True, color)
            x = (SCREEN_WIDTH - text.get_width()) // 2
            surface.blit(text, (x, menu_y + i * 40))

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
