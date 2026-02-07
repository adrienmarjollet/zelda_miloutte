"""Gold pickup entity that the player can collect."""

from .entity import Entity
from ..settings import ITEM_SIZE, GOLD as GOLD_COLOR
from ..sounds import get_sound_manager
from ..sprites.gold_sprites import get_gold_frames


class Gold(Entity):
    """A gold coin pickup that adds gold to the player."""

    def __init__(self, x, y, amount=1):
        """
        Args:
            x, y: Position in pixels
            amount: Gold value of this pickup
        """
        super().__init__(x + 8, y + 8, ITEM_SIZE, ITEM_SIZE, GOLD_COLOR)
        self.amount = amount

        # Bobbing animation
        self._bob_timer = 0.0
        self._bob_speed = 1.5
        self._bob_frame = 0
        self._frames = get_gold_frames()

    def pickup(self, player):
        """Add gold to player and play pickup sound."""
        player.gold += self.amount
        get_sound_manager().play_gold_pickup()
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
