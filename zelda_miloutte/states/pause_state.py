import time
import pygame
from zelda_miloutte.states.state import State
from zelda_miloutte.settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, GOLD, GRAY, GREEN


class PauseState(State):
    def __init__(self, game):
        super().__init__(game)
        self.title_font = None
        self.menu_font = None
        self.small_font = None
        self.mode = "main"  # "main" or "save_slots"
        self.menu_items = ["Resume", "Save Game", "Quit to Title"]
        self.selected_index = 0
        self.save_message = ""
        self.save_message_timer = 0.0

    def _init_fonts(self):
        if self.title_font is None:
            self.title_font = pygame.font.Font(None, 72)
            self.menu_font = pygame.font.Font(None, 36)
            self.small_font = pygame.font.Font(None, 22)

    def _get_save_data(self):
        """Collect current game state for saving."""
        # Find the play state in the stack
        play_state = None
        for state in self.game.states:
            from zelda_miloutte.states.play_state import PlayState
            if isinstance(state, PlayState):
                play_state = state
                break

        if play_state is None:
            return None

        player = play_state.player
        data = {
            "player": {
                "hp": player.hp,
                "max_hp": player.max_hp,
                "keys": player.keys,
                "level": getattr(player, "level", 1),
                "xp": getattr(player, "xp", 0),
                "xp_to_next": getattr(player, "xp_to_next", 100),
                "base_attack": getattr(player, "base_attack", 0),
                "base_defense": getattr(player, "base_defense", 0),
            },
            "defeated_bosses": self.game.world_state.get("defeated_bosses", []),
            "opened_chests": self.game.world_state.get("opened_chests", []),
            "current_area": self.game.world_state.get("current_area", "overworld"),
            "story_progress": self.game.world_state.get("story_progress", 0),
            "quests": self.game.world_state.get("quests", {}),
        }
        return data

    def _save_to_slot(self, slot):
        data = self._get_save_data()
        if data is None:
            self.save_message = "Cannot save right now!"
            self.save_message_timer = 2.0
            return
        self.game.save_manager.save_game(slot, data)
        self.save_message = f"Saved to Slot {slot}!"
        self.save_message_timer = 2.0
        self.mode = "main"
        self.selected_index = 0

    def handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return

        if self.mode == "main":
            if event.key == pygame.K_UP:
                self.selected_index = (self.selected_index - 1) % len(self.menu_items)
            elif event.key == pygame.K_DOWN:
                self.selected_index = (self.selected_index + 1) % len(self.menu_items)
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                self._select_option()
            elif event.key == pygame.K_ESCAPE:
                self.game.pop_state()
        elif self.mode == "save_slots":
            if event.key == pygame.K_UP:
                self.selected_index = (self.selected_index - 1) % 3
            elif event.key == pygame.K_DOWN:
                self.selected_index = (self.selected_index + 1) % 3
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                self._save_to_slot(self.selected_index + 1)
            elif event.key == pygame.K_ESCAPE:
                self.mode = "main"
                self.selected_index = 0

    def _select_option(self):
        if self.selected_index == 0:  # Resume
            self.game.pop_state()
        elif self.selected_index == 1:  # Save Game
            self.mode = "save_slots"
            self.selected_index = 0
        elif self.selected_index == 2:  # Quit to Title
            from zelda_miloutte.states.title_state import TitleState
            while len(self.game.states) > 0:
                self.game.pop_state()
            self.game.push_state(TitleState(self.game))

    def update(self, dt):
        if self.save_message_timer > 0:
            self.save_message_timer -= dt
            if self.save_message_timer <= 0:
                self.save_message = ""

    def draw(self, surface):
        self._init_fonts()

        # Draw the underlying game state
        if len(self.game.states) >= 2:
            self.game.states[-2].draw(surface)

        # Dark overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        surface.blit(overlay, (0, 0))

        # Title
        title = self.title_font.render("PAUSED", True, WHITE)
        tx = (SCREEN_WIDTH - title.get_width()) // 2
        ty = SCREEN_HEIGHT // 3 - 20
        surface.blit(title, (tx, ty))

        if self.mode == "main":
            menu_y_start = SCREEN_HEIGHT // 2
            for i, item in enumerate(self.menu_items):
                color = GOLD if i == self.selected_index else GRAY
                text = self.menu_font.render(item, True, color)
                x = (SCREEN_WIDTH - text.get_width()) // 2
                y = menu_y_start + i * 45
                surface.blit(text, (x, y))
        elif self.mode == "save_slots":
            header = self.menu_font.render("Select Save Slot", True, WHITE)
            hx = (SCREEN_WIDTH - header.get_width()) // 2
            surface.blit(header, (hx, SCREEN_HEIGHT // 2 - 10))

            saves = self.game.save_manager.list_saves()
            slot_y = SCREEN_HEIGHT // 2 + 35
            for i in range(3):
                slot = i + 1
                info = saves.get(slot)
                if info is not None:
                    ts = time.strftime("%m-%d %H:%M", time.localtime(info["timestamp"]))
                    label = f"Slot {slot}: Lv.{info['level']} - {info['area']} ({ts})"
                else:
                    label = f"Slot {slot}: Empty"
                color = GOLD if i == self.selected_index else GRAY
                text = self.small_font.render(label, True, color)
                x = (SCREEN_WIDTH - text.get_width()) // 2
                surface.blit(text, (x, slot_y + i * 30))

            back = self.small_font.render("ESC: Back", True, (120, 120, 120))
            surface.blit(back, ((SCREEN_WIDTH - back.get_width()) // 2, slot_y + 110))

        # Save message
        if self.save_message:
            msg = self.menu_font.render(self.save_message, True, GREEN)
            mx = (SCREEN_WIDTH - msg.get_width()) // 2
            surface.blit(msg, (mx, SCREEN_HEIGHT - 80))
