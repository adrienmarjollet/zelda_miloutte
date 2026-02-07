"""State presented after the ending cinematic to offer New Game+ choice."""

import pygame
from .state import State
from ..settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, GOLD, BLACK, GRAY
from ..ng_plus import (
    init_ng_plus_save_data, get_ng_plus_label, format_play_time,
    check_speedrun_achievement,
)


class NGPlusChoiceState(State):
    """Presents the player with a choice: Start New Game+ or Return to Village."""

    def __init__(self, game, player_ref=None):
        super().__init__(game)
        self._player_ref = player_ref  # Reference to the player entity for stats
        self.selected = 0  # 0 = Start NG+, 1 = Return to Village
        self.choices = ["Start New Game+?", "Return to Village"]
        self._font = None
        self._title_font = None
        self._small_font = None
        self._blink_timer = 0.0
        self._show_cursor = True

    def enter(self):
        pass

    def _init_fonts(self):
        if self._font is None:
            self._font = pygame.font.Font(None, 32)
            self._title_font = pygame.font.Font(None, 48)
            self._small_font = pygame.font.Font(None, 24)

    def handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return
        if event.key == pygame.K_UP:
            self.selected = (self.selected - 1) % len(self.choices)
        elif event.key == pygame.K_DOWN:
            self.selected = (self.selected + 1) % len(self.choices)
        elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
            if self.selected == 0:
                # Start New Game+
                self._start_ng_plus()
            else:
                # Return to village (title screen)
                self._return_to_village()

    def _start_ng_plus(self):
        """Initialize NG+ cycle and start a new game with carried-over stats."""
        player = self._player_ref

        # Build NG+ save data
        ng_data = init_ng_plus_save_data(self.game.save_data, player)

        # Update game state
        self.game.ng_plus_count = ng_data["ng_plus_count"]
        self.game.play_time = 0.0  # Reset speedrun timer for this cycle
        self.game.world_state = ng_data["world_state"]
        self.game.save_data = ng_data

        # Reset quests
        self.game.quest_manager = None
        from ..quest_manager import QuestManager
        from ..data.quests import get_all_quests
        self.game.quest_manager = QuestManager()
        for quest in get_all_quests():
            self.game.quest_manager.register_quest(quest)

        # Restore player abilities from save
        unlocked = ng_data.get("unlocked_abilities", [])

        def do_ng_plus():
            from .play_state import PlayState
            play = PlayState(self.game, area_id="overworld", load_data=ng_data)
            # Restore unlocked abilities
            for ability_name in unlocked:
                play.player.unlock_ability(ability_name)
            # Apply Hero's Crown stat boost if earned
            if ng_data.get("has_heros_crown"):
                play.player.max_hp += 2
                play.player.hp = play.player.max_hp
                play.player.base_attack += 1
            self.game.change_state(play)

        self.game.transition_to(do_ng_plus)

    def _return_to_village(self):
        """Return to title screen."""
        def go_title():
            from .title_state import TitleState
            self.game.change_state(TitleState(self.game))
        self.game.transition_to(go_title)

    def update(self, dt):
        self._blink_timer += dt
        if self._blink_timer >= 0.5:
            self._blink_timer = 0.0
            self._show_cursor = not self._show_cursor

    def draw(self, surface):
        self._init_fonts()
        surface.fill((10, 10, 30))

        # Title
        ng_count = self.game.save_data.get("ng_plus_count", 0)
        next_label = get_ng_plus_label(ng_count + 1)
        title_text = f"Congratulations!"
        title = self._title_font.render(title_text, True, GOLD)
        tx = (SCREEN_WIDTH - title.get_width()) // 2
        surface.blit(title, (tx, 80))

        # Play time display
        play_time = self.game.play_time
        time_str = format_play_time(play_time)
        time_text = self._small_font.render(f"Clear Time: {time_str}", True, WHITE)
        surface.blit(time_text, ((SCREEN_WIDTH - time_text.get_width()) // 2, 140))

        # Speedrun achievement
        if check_speedrun_achievement(play_time):
            ach_text = self._small_font.render("Speedrun Achievement Unlocked! (Under 30 min)", True, (255, 200, 50))
            surface.blit(ach_text, ((SCREEN_WIDTH - ach_text.get_width()) // 2, 165))

        # NG+ info
        info_lines = [
            f"New cycle: {next_label}",
            "Keep: Level, stats, abilities",
            "Reset: Keys, quests, bosses, chests",
        ]
        if ng_count == 0:
            info_lines.append("Bonus: Hero's Crown (+2 HP, +1 ATK)")
        info_lines.append("Enemies scale with each cycle!")

        for i, line in enumerate(info_lines):
            text = self._small_font.render(line, True, (180, 180, 220))
            surface.blit(text, ((SCREEN_WIDTH - text.get_width()) // 2, 200 + i * 25))

        # Choices
        choice_y = SCREEN_HEIGHT // 2 + 60
        for i, choice in enumerate(self.choices):
            if i == self.selected:
                color = GOLD
                prefix = "> " if self._show_cursor else "  "
            else:
                color = GRAY
                prefix = "  "
            text = self._font.render(f"{prefix}{choice}", True, color)
            x = (SCREEN_WIDTH - text.get_width()) // 2
            surface.blit(text, (x, choice_y + i * 45))

        # Controls hint
        hint = self._small_font.render("Up/Down: Select    Enter/Space: Confirm", True, (120, 120, 120))
        surface.blit(hint, ((SCREEN_WIDTH - hint.get_width()) // 2, SCREEN_HEIGHT - 50))
