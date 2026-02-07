"""NPC entity that can talk, give quests, and react to game state."""

import pygame
from zelda_miloutte.entities.entity import Entity
from zelda_miloutte.settings import ENEMY_SIZE, BROWN


class NPC(Entity):
    """A non-player character that the player can interact with."""

    def __init__(self, x, y, name, variant="elder", dialogue_tree=None, quest_id=None, shop_id=None):
        """
        Args:
            x, y: Position in pixels
            name: Display name for dialogue
            variant: Sprite variant ("elder", "villager", "merchant", "guard")
            dialogue_tree: Dict mapping state -> list of message strings.
                           e.g. {"default": ["Hello!", "Welcome."], "quest_done": ["Thank you!"]}
            quest_id: Optional quest ID this NPC is associated with
            shop_id: Optional shop ID — if set, opens a shop after dialogue
        """
        super().__init__(x, y, ENEMY_SIZE, ENEMY_SIZE, BROWN)
        self.name = name
        self.variant = variant
        self.dialogue_tree = dialogue_tree or {"default": ["..."]}
        self.quest_id = quest_id
        self.shop_id = shop_id
        self.dialogue_state = "default"

        # Sprites
        self._anim = None
        self._load_sprites()

    def _load_sprites(self):
        from zelda_miloutte.sprites import AnimatedSprite
        from zelda_miloutte.sprites.npc_sprites import (
            get_elder_frames, get_villager_frames, get_merchant_frames, get_guard_frames,
        )
        frame_fns = {
            "elder": get_elder_frames,
            "villager": get_villager_frames,
            "merchant": get_merchant_frames,
            "guard": get_guard_frames,
        }
        fn = frame_fns.get(self.variant, get_villager_frames)
        self._anim = AnimatedSprite(fn(), frame_duration=0.4)

    def update_dialogue_state(self, quest_manager):
        """Update dialogue state based on quest progress."""
        if not self.quest_id:
            return
        quest = quest_manager.get_quest(self.quest_id)
        if quest is None:
            return
        if quest.status == "completed":
            self.dialogue_state = "quest_done"
        elif quest.status == "active":
            self.dialogue_state = "quest_active"
        else:
            self.dialogue_state = "default"

    def get_dialogue(self):
        """Return the current dialogue messages based on state."""
        return self.dialogue_tree.get(self.dialogue_state,
                                       self.dialogue_tree.get("default", ["..."]))

    def get_choices(self):
        """Return dialogue choices if any for current state."""
        key = self.dialogue_state + "_choices"
        return self.dialogue_tree.get(key, None)

    def update(self, dt):
        # NPCs are mostly static, just animate idle
        self._anim.update(dt, False)

    def draw(self, surface, camera):
        if not self.alive:
            return
        ox, oy = -camera.x, -camera.y
        r = self.rect.move(ox, oy)
        frame = self._anim.get_frame(self.facing)
        fx = r.centerx - frame.get_width() // 2
        fy = r.centery - frame.get_height() // 2
        surface.blit(frame, (fx, fy))
