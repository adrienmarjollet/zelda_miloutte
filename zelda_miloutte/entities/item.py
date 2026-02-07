import pygame
from .entity import Entity
from ..settings import ITEM_SIZE, HEART_RED, KEY_YELLOW, HEART_HEAL
from ..sounds import get_sound_manager
from ..sprites.item_sprites import get_heart_frames, get_key_frames


class Item(Entity):
    def __init__(self, x, y, item_type):
        color = HEART_RED if item_type == "heart" else KEY_YELLOW
        super().__init__(x + 8, y + 8, ITEM_SIZE, ITEM_SIZE, color)
        self.item_type = item_type

        # Bobbing animation
        self._bob_timer = 0.0
        self._bob_speed = 1.5  # full cycle per second
        self._bob_frame = 0
        self._frames = get_heart_frames() if item_type == "heart" else get_key_frames()

    def pickup(self, player):
        if self.item_type == "heart":
            player.heal(HEART_HEAL)
            get_sound_manager().play_heart_pickup()
        elif self.item_type == "key":
            player.keys += 1
            get_sound_manager().play_key_pickup()
        self.alive = False

    def update(self, dt):
        self._bob_timer += dt * self._bob_speed
        if self._bob_timer >= 1.0:
            self._bob_timer -= 1.0
            self._bob_frame = (self._bob_frame + 1) % len(self._frames)

    def draw(self, surface, camera):
        if not self.alive:
            return
        ox, oy = -camera.x, -camera.y
        r = self.rect.move(ox, oy)
        frame = self._frames[self._bob_frame]
        surface.blit(frame, (r.x, r.y))
