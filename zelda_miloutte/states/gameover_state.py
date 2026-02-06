import pygame
from zelda_miloutte.states.state import State
from zelda_miloutte.settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, RED, BLACK


class GameOverState(State):
    def __init__(self, game):
        super().__init__(game)
        self.title_font = None
        self.prompt_font = None
        self.blink_timer = 0.0
        self.show_prompt = True

    def _init_fonts(self):
        if self.title_font is None:
            self.title_font = pygame.font.Font(None, 56)
            self.prompt_font = pygame.font.Font(None, 28)

    def _return_to_title(self):
        """Callback to return to title screen (called during transition)."""
        from zelda_miloutte.states.title_state import TitleState
        self.game.change_state(TitleState(self.game))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            self.game.transition_to(self._return_to_title)

    def update(self, dt):
        self.blink_timer += dt
        if self.blink_timer >= 0.6:
            self.blink_timer = 0.0
            self.show_prompt = not self.show_prompt

    def draw(self, surface):
        self._init_fonts()
        surface.fill((30, 10, 10))

        title = self.title_font.render("Game Over", True, RED)
        tx = (SCREEN_WIDTH - title.get_width()) // 2
        surface.blit(title, (tx, SCREEN_HEIGHT // 3))

        if self.show_prompt:
            prompt = self.prompt_font.render("Press ENTER to retry", True, WHITE)
            px = (SCREEN_WIDTH - prompt.get_width()) // 2
            surface.blit(prompt, (px, SCREEN_HEIGHT * 2 // 3))
