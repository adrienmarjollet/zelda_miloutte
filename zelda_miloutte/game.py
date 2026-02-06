import asyncio
import pygame
from zelda_miloutte.settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TITLE, BLACK
from zelda_miloutte.input_handler import InputHandler
from zelda_miloutte.transition import Transition
from zelda_miloutte.save_manager import SaveManager
from zelda_miloutte.quest_manager import QuestManager
from zelda_miloutte.data.quests import get_all_quests


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.input = InputHandler()
        self.states = []
        self.transition = Transition()
        self.save_manager = SaveManager()
        self.save_data = {}
        self.world_state = {
            "defeated_bosses": [],
            "opened_chests": [],
            "current_area": "overworld",
            "story_progress": 0,
        }
        self.quest_manager = QuestManager()
        self._init_quests()

    def _init_quests(self):
        """Register all quests."""
        for quest in get_all_quests():
            self.quest_manager.register_quest(quest)

    def save_game(self, slot=1):
        """Save current game state."""
        data = {
            "world_state": self.world_state,
            "quest_state": self.quest_manager.to_dict(),
        }
        # Include player data if we have an active gameplay state
        if self.current_state and hasattr(self.current_state, 'player'):
            p = self.current_state.player
            data["player"] = {
                "hp": p.hp, "max_hp": p.max_hp, "keys": p.keys,
                "level": p.level, "xp": p.xp, "xp_to_next": p.xp_to_next,
                "base_attack": p.base_attack, "base_defense": p.base_defense,
            }
        data["current_area"] = self.world_state.get("current_area", "overworld")
        self.save_manager.save_game(slot, data)

    def load_game(self, slot=1):
        """Load game state from a save slot."""
        data = self.save_manager.load_game(slot)
        if data is None:
            return False
        self.world_state = data.get("world_state", self.world_state)
        quest_data = data.get("quest_state")
        if quest_data:
            self.quest_manager.from_dict(quest_data)
        self.save_data = data
        return True

    def push_state(self, state):
        state.enter()
        self.states.append(state)

    def pop_state(self):
        if self.states:
            self.states[-1].exit()
            self.states.pop()

    def change_state(self, state):
        if self.states:
            self.states[-1].exit()
            self.states.pop()
        state.enter()
        self.states.append(state)

    def transition_to(self, callback, duration=0.4):
        """Start a transition. The callback will be called between fade-out and fade-in."""
        if not self.transition.active:
            self.transition.start(callback, duration)

    @property
    def current_state(self):
        return self.states[-1] if self.states else None

    async def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            dt = min(dt, 0.05)  # Cap delta time

            self.input.reset_actions()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return
                self.input.handle_event(event)
                # Don't handle events during transitions
                if self.current_state and not self.transition.active:
                    self.current_state.handle_event(event)

            self.input.update()

            # Update transition if active, otherwise update game state
            if self.transition.active:
                self.transition.update(dt)
            elif self.current_state:
                self.current_state.update(dt)

            # Draw current state and transition overlay
            if self.current_state:
                self.screen.fill(BLACK)
                self.current_state.draw(self.screen)

            # Draw touch controls on top of game, under transitions
            self.input.touch.draw(self.screen)

            # Draw transition overlay on top
            self.transition.draw(self.screen)

            pygame.display.flip()
            await asyncio.sleep(0)

        pygame.quit()
