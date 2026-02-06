import pygame
from zelda_miloutte.touch_controls import TouchControls


class InputHandler:
    def __init__(self):
        self.move_x = 0.0
        self.move_y = 0.0
        self.attack = False
        self.confirm = False
        self.pause = False
        self.interact = False
        self.touch = TouchControls()
        self._prev_touch_move_y = 0.0

    def update(self):
        keys = pygame.key.get_pressed()
        self.move_x = 0.0
        self.move_y = 0.0

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.move_x -= 1.0
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.move_x += 1.0
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.move_y -= 1.0
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.move_y += 1.0

        # Normalize diagonal movement
        if self.move_x != 0 and self.move_y != 0:
            self.move_x *= 0.7071
            self.move_y *= 0.7071

        # Merge touch d-pad input (touch overrides keyboard if active)
        if self.touch.move_x != 0 or self.touch.move_y != 0:
            self.move_x = self.touch.move_x
            self.move_y = self.touch.move_y

        # Generate synthetic KEYDOWN events for d-pad direction changes
        # (for menu navigation in title/pause states)
        touch_y = self.touch.move_y
        if touch_y < -0.3 and self._prev_touch_move_y >= -0.3:
            pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UP))
        elif touch_y > 0.3 and self._prev_touch_move_y <= 0.3:
            pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN))
        self._prev_touch_move_y = touch_y

    def reset_actions(self):
        """Reset one-shot action flags. Call once per frame before processing events."""
        self.attack = False
        self.confirm = False
        self.pause = False
        self.interact = False
        self.touch.attack_pressed = False
        self.touch.interact_pressed = False
        self.touch.pause_pressed = False

    def handle_event(self, event):
        # Try touch controls first
        if self.touch.handle_event(event):
            # Map touch actions to input flags and post synthetic key events
            # so menu states (title, pause, gameover, cinematic) also respond
            if self.touch.attack_pressed:
                self.attack = True
                pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE))
            if self.touch.interact_pressed:
                self.interact = True
                self.confirm = True
                pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN))
            if self.touch.pause_pressed:
                self.pause = True
                pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE))
            return

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.attack = True
            if event.key == pygame.K_RETURN:
                self.confirm = True
            if event.key == pygame.K_ESCAPE:
                self.pause = True
            if event.key == pygame.K_e or event.key == pygame.K_RETURN:
                self.interact = True
