import pygame
from .touch_controls import TouchControls
from .settings import DODGE_DOUBLE_TAP_WINDOW


class InputHandler:
    def __init__(self):
        self.move_x = 0.0
        self.move_y = 0.0
        self.attack = False
        self.confirm = False
        self.pause = False
        self.interact = False
        self.open_inventory = False
        self.toggle_minimap = False
        self.toggle_world_map = False
        self.toggle_timer = False
        self.touch = TouchControls()
        self._prev_touch_move_y = 0.0

        # Shield / block (hold)
        self.blocking = False

        # Dodge roll (double-tap detection)
        self.dodge_direction = None  # ("left","right","up","down") or None
        self._last_tap_dir = None
        self._last_tap_time = 0.0

        # Charge attack tracking
        self.attack_held = False     # True while Space is physically held
        self.attack_released = False  # one-shot: True the frame Space is released

        # Ability controls
        self.cycle_ability = False   # Q key - cycle selected ability
        self.use_ability = False     # R key - use selected ability

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

        # Shield: held state
        self.blocking = (
            keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]
            or pygame.mouse.get_pressed()[2]  # right mouse button
        )

        # Track whether Space is currently held (for charge attacks)
        self.attack_held = keys[pygame.K_SPACE]

    def reset_actions(self):
        """Reset one-shot action flags. Call once per frame before processing events."""
        self.attack = False
        self.confirm = False
        self.pause = False
        self.interact = False
        self.open_inventory = False
        self.toggle_minimap = False
        self.toggle_world_map = False
        self.toggle_timer = False
        self.touch.attack_pressed = False
        self.touch.interact_pressed = False
        self.touch.pause_pressed = False
        self.dodge_direction = None
        self.attack_released = False
        self.cycle_ability = False
        self.use_ability = False

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
            if event.key == pygame.K_n:
                self.toggle_minimap = True
            if event.key == pygame.K_m:
                self.toggle_world_map = True
            if event.key == pygame.K_q:
                self.cycle_ability = True
            if event.key == pygame.K_r:
                self.use_ability = True
            if event.key == pygame.K_t:
                self.toggle_timer = True
            if event.key == pygame.K_i or event.key == pygame.K_TAB:
                self.open_inventory = True

            # Double-tap detection for dodge roll
            self._check_double_tap(event.key)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                self.attack_released = True

    def _check_double_tap(self, key):
        """Detect double-tap on a direction key for dodge roll."""
        direction = None
        if key in (pygame.K_LEFT, pygame.K_a):
            direction = "left"
        elif key in (pygame.K_RIGHT, pygame.K_d):
            direction = "right"
        elif key in (pygame.K_UP, pygame.K_w):
            direction = "up"
        elif key in (pygame.K_DOWN, pygame.K_s):
            direction = "down"

        if direction is None:
            return

        now = pygame.time.get_ticks() / 1000.0
        if direction == self._last_tap_dir and (now - self._last_tap_time) < DODGE_DOUBLE_TAP_WINDOW:
            self.dodge_direction = direction
            self._last_tap_dir = None
            self._last_tap_time = 0.0
        else:
            self._last_tap_dir = direction
            self._last_tap_time = now
