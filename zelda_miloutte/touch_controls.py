import math
import pygame
from .settings import SCREEN_WIDTH, SCREEN_HEIGHT


# D-pad layout
DPAD_CENTER_X = 90
DPAD_CENTER_Y = SCREEN_HEIGHT - 90
DPAD_RADIUS = 60
DPAD_DEAD_ZONE = 15

# Action buttons
ATTACK_BTN_X = SCREEN_WIDTH - 80
ATTACK_BTN_Y = SCREEN_HEIGHT - 70
ATTACK_BTN_RADIUS = 38

INTERACT_BTN_X = SCREEN_WIDTH - 80
INTERACT_BTN_Y = SCREEN_HEIGHT - 150
INTERACT_BTN_RADIUS = 32

# Pause button
PAUSE_BTN_X = SCREEN_WIDTH - 40
PAUSE_BTN_Y = 60
PAUSE_BTN_RADIUS = 20

TOUCH_ALPHA = 90


class TouchControls:
    def __init__(self):
        self.visible = False
        self.move_x = 0.0
        self.move_y = 0.0
        self.attack_pressed = False
        self.interact_pressed = False
        self.pause_pressed = False
        # Track which finger is on the d-pad
        self._dpad_finger = None
        self._active_fingers = {}  # finger_id -> "dpad" | "attack" | "interact" | "pause"
        self._surfaces_dirty = True
        self._dpad_surface = None
        self._attack_surface = None
        self._interact_surface = None
        self._pause_surface = None

    def _build_surfaces(self):
        """Pre-render semi-transparent button surfaces."""
        # D-pad background circle
        size = DPAD_RADIUS * 2 + 4
        self._dpad_surface = pygame.Surface((size, size), pygame.SRCALPHA)
        center = size // 2
        pygame.draw.circle(self._dpad_surface, (255, 255, 255, TOUCH_ALPHA), (center, center), DPAD_RADIUS)
        # Draw directional arrows
        arrow_color = (200, 200, 200, TOUCH_ALPHA + 40)
        arrow_len = 18
        arrow_offset = DPAD_RADIUS * 0.55
        for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            ax = center + dx * arrow_offset
            ay = center + dy * arrow_offset
            # Draw a small triangle
            pts = []
            if dx == 0 and dy == -1:  # up
                pts = [(ax, ay - arrow_len // 2), (ax - 8, ay + arrow_len // 2), (ax + 8, ay + arrow_len // 2)]
            elif dx == 0 and dy == 1:  # down
                pts = [(ax, ay + arrow_len // 2), (ax - 8, ay - arrow_len // 2), (ax + 8, ay - arrow_len // 2)]
            elif dx == -1:  # left
                pts = [(ax - arrow_len // 2, ay), (ax + arrow_len // 2, ay - 8), (ax + arrow_len // 2, ay + 8)]
            elif dx == 1:  # right
                pts = [(ax + arrow_len // 2, ay), (ax - arrow_len // 2, ay - 8), (ax - arrow_len // 2, ay + 8)]
            pygame.draw.polygon(self._dpad_surface, arrow_color, pts)

        # Attack button
        asize = ATTACK_BTN_RADIUS * 2 + 4
        self._attack_surface = pygame.Surface((asize, asize), pygame.SRCALPHA)
        ac = asize // 2
        pygame.draw.circle(self._attack_surface, (255, 80, 80, TOUCH_ALPHA), (ac, ac), ATTACK_BTN_RADIUS)
        pygame.draw.circle(self._attack_surface, (255, 255, 255, TOUCH_ALPHA + 30), (ac, ac), ATTACK_BTN_RADIUS, 2)
        # Sword icon (simple line)
        pygame.draw.line(self._attack_surface, (255, 255, 255, TOUCH_ALPHA + 60), (ac, ac - 14), (ac, ac + 14), 3)
        pygame.draw.line(self._attack_surface, (255, 255, 255, TOUCH_ALPHA + 60), (ac - 8, ac - 6), (ac + 8, ac - 6), 3)

        # Interact button
        isize = INTERACT_BTN_RADIUS * 2 + 4
        self._interact_surface = pygame.Surface((isize, isize), pygame.SRCALPHA)
        ic = isize // 2
        pygame.draw.circle(self._interact_surface, (80, 180, 255, TOUCH_ALPHA), (ic, ic), INTERACT_BTN_RADIUS)
        pygame.draw.circle(self._interact_surface, (255, 255, 255, TOUCH_ALPHA + 30), (ic, ic), INTERACT_BTN_RADIUS, 2)
        # "E" letter
        font = pygame.font.Font(None, 28)
        txt = font.render("E", True, (255, 255, 255, TOUCH_ALPHA + 60))
        self._interact_surface.blit(txt, (ic - txt.get_width() // 2, ic - txt.get_height() // 2))

        # Pause button
        psize = PAUSE_BTN_RADIUS * 2 + 4
        self._pause_surface = pygame.Surface((psize, psize), pygame.SRCALPHA)
        pc = psize // 2
        pygame.draw.circle(self._pause_surface, (180, 180, 180, TOUCH_ALPHA), (pc, pc), PAUSE_BTN_RADIUS)
        # Pause bars
        bar_w, bar_h = 4, 14
        pygame.draw.rect(self._pause_surface, (255, 255, 255, TOUCH_ALPHA + 60), (pc - 6, pc - bar_h // 2, bar_w, bar_h))
        pygame.draw.rect(self._pause_surface, (255, 255, 255, TOUCH_ALPHA + 60), (pc + 2, pc - bar_h // 2, bar_w, bar_h))

        self._surfaces_dirty = False

    def _screen_pos(self, finger_x, finger_y):
        """Convert normalized finger coords (0-1) to screen pixels."""
        return finger_x * SCREEN_WIDTH, finger_y * SCREEN_HEIGHT

    def _hit_test(self, sx, sy):
        """Check which button a screen position hits. Returns 'dpad', 'attack', 'interact', 'pause', or None."""
        # D-pad
        dx = sx - DPAD_CENTER_X
        dy = sy - DPAD_CENTER_Y
        if math.sqrt(dx * dx + dy * dy) <= DPAD_RADIUS:
            return "dpad"

        # Attack
        dx = sx - ATTACK_BTN_X
        dy = sy - ATTACK_BTN_Y
        if math.sqrt(dx * dx + dy * dy) <= ATTACK_BTN_RADIUS:
            return "attack"

        # Interact
        dx = sx - INTERACT_BTN_X
        dy = sy - INTERACT_BTN_Y
        if math.sqrt(dx * dx + dy * dy) <= INTERACT_BTN_RADIUS:
            return "interact"

        # Pause
        dx = sx - PAUSE_BTN_X
        dy = sy - PAUSE_BTN_Y
        if math.sqrt(dx * dx + dy * dy) <= PAUSE_BTN_RADIUS:
            return "pause"

        return None

    def _update_dpad_direction(self, sx, sy):
        """Compute move_x/move_y from d-pad touch position."""
        dx = sx - DPAD_CENTER_X
        dy = sy - DPAD_CENTER_Y
        dist = math.sqrt(dx * dx + dy * dy)
        if dist < DPAD_DEAD_ZONE:
            self.move_x = 0.0
            self.move_y = 0.0
            return
        # Normalize
        nx = dx / dist
        ny = dy / dist
        # Snap to 8 directions for more precise control
        angle = math.atan2(ny, nx)
        # 8-direction snap (45 degree increments)
        sector = round(angle / (math.pi / 4))
        snapped = sector * (math.pi / 4)
        self.move_x = round(math.cos(snapped), 4)
        self.move_y = round(math.sin(snapped), 4)
        # Normalize diagonal
        if self.move_x != 0 and self.move_y != 0:
            self.move_x *= 0.7071
            self.move_y *= 0.7071

    def handle_event(self, event):
        """Process touch events. Returns True if the event was consumed."""
        if event.type == pygame.FINGERDOWN:
            self.visible = True
            sx, sy = self._screen_pos(event.x, event.y)
            hit = self._hit_test(sx, sy)
            if hit:
                self._active_fingers[event.finger_id] = hit
                if hit == "dpad":
                    self._dpad_finger = event.finger_id
                    self._update_dpad_direction(sx, sy)
                elif hit == "attack":
                    self.attack_pressed = True
                elif hit == "interact":
                    self.interact_pressed = True
                elif hit == "pause":
                    self.pause_pressed = True
                return True

        elif event.type == pygame.FINGERUP:
            finger_type = self._active_fingers.pop(event.finger_id, None)
            if finger_type == "dpad":
                self._dpad_finger = None
                self.move_x = 0.0
                self.move_y = 0.0
                return True
            elif finger_type is not None:
                return True

        elif event.type == pygame.FINGERMOTION:
            if event.finger_id in self._active_fingers:
                finger_type = self._active_fingers[event.finger_id]
                if finger_type == "dpad":
                    sx, sy = self._screen_pos(event.x, event.y)
                    self._update_dpad_direction(sx, sy)
                    return True

        return False

    def draw(self, surface):
        """Draw touch controls overlay."""
        if not self.visible:
            return

        if self._surfaces_dirty:
            self._build_surfaces()

        # D-pad
        surface.blit(self._dpad_surface, (DPAD_CENTER_X - DPAD_RADIUS - 2, DPAD_CENTER_Y - DPAD_RADIUS - 2))

        # Attack button
        surface.blit(self._attack_surface, (ATTACK_BTN_X - ATTACK_BTN_RADIUS - 2, ATTACK_BTN_Y - ATTACK_BTN_RADIUS - 2))

        # Interact button
        surface.blit(self._interact_surface, (INTERACT_BTN_X - INTERACT_BTN_RADIUS - 2, INTERACT_BTN_Y - INTERACT_BTN_RADIUS - 2))

        # Pause button
        surface.blit(self._pause_surface, (PAUSE_BTN_X - PAUSE_BTN_RADIUS - 2, PAUSE_BTN_Y - PAUSE_BTN_RADIUS - 2))

        # Draw d-pad touch indicator
        if self._dpad_finger is not None and (self.move_x != 0 or self.move_y != 0):
            ind_x = DPAD_CENTER_X + self.move_x * DPAD_RADIUS * 0.6
            ind_y = DPAD_CENTER_Y + self.move_y * DPAD_RADIUS * 0.6
            # Account for diagonal normalization in display
            if self.move_x != 0 and self.move_y != 0:
                ind_x = DPAD_CENTER_X + (self.move_x / 0.7071) * DPAD_RADIUS * 0.6
                ind_y = DPAD_CENTER_Y + (self.move_y / 0.7071) * DPAD_RADIUS * 0.6
            ind_surf = pygame.Surface((20, 20), pygame.SRCALPHA)
            pygame.draw.circle(ind_surf, (255, 255, 255, 140), (10, 10), 10)
            surface.blit(ind_surf, (int(ind_x) - 10, int(ind_y) - 10))
