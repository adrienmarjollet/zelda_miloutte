import pygame


class InputHandler:
    def __init__(self):
        self.move_x = 0.0
        self.move_y = 0.0
        self.attack = False
        self.confirm = False
        self.pause = False
        self.interact = False

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

    def reset_actions(self):
        """Reset one-shot action flags. Call once per frame before processing events."""
        self.attack = False
        self.confirm = False
        self.pause = False
        self.interact = False

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.attack = True
            if event.key == pygame.K_RETURN:
                self.confirm = True
            if event.key == pygame.K_ESCAPE:
                self.pause = True
            if event.key == pygame.K_e or event.key == pygame.K_RETURN:
                self.interact = True
