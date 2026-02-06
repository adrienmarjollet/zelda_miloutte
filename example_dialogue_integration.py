"""Example of integrating DialogueBox into a game state."""

import pygame
from zelda_miloutte.ui.dialogue_box import DialogueBox


class ExampleGameState:
    """Example showing DialogueBox integration pattern."""

    def __init__(self):
        """Initialize the game state."""
        self.dialogue = DialogueBox()
        self.current_npc = None

        # Example NPC data
        self.npcs = {
            "elder": {
                "name": "Village Elder",
                "initial_dialogue": {
                    "messages": [
                        "Welcome, brave traveler!",
                        "Our village has been plagued by monsters.",
                        "Will you help us defeat them?"
                    ],
                    "choices": ["Yes, I will help!", "Not right now"]
                },
                "quest_accepted": {
                    "messages": [
                        "Thank you, hero!",
                        "The monsters lurk in the forest to the east."
                    ]
                },
                "quest_declined": {
                    "messages": ["I understand. Come back if you change your mind."]
                }
            },
            "merchant": {
                "name": "Traveling Merchant",
                "initial_dialogue": {
                    "messages": [
                        "Greetings! I have rare wares for sale.",
                        "What interests you?"
                    ],
                    "choices": ["Potions", "Weapons", "Leave"]
                }
            }
        }

    def interact_with_npc(self, npc_id):
        """Start dialogue with an NPC.

        Args:
            npc_id: The ID of the NPC to interact with
        """
        if npc_id not in self.npcs:
            return

        self.current_npc = npc_id
        npc_data = self.npcs[npc_id]
        dialogue_data = npc_data["initial_dialogue"]

        self.dialogue.show(
            npc_data["name"],
            dialogue_data["messages"],
            dialogue_data.get("choices")
        )

    def update(self, dt):
        """Update the game state.

        Args:
            dt: Delta time in seconds
        """
        self.dialogue.update(dt)

        # Don't update gameplay while dialogue is active
        if self.dialogue.active:
            return

        # Normal gameplay updates here...
        pass

    def draw(self, surface):
        """Draw the game state.

        Args:
            surface: The pygame surface to draw on
        """
        # Draw gameplay elements here...
        pass

        # Draw dialogue on top (UI layer)
        self.dialogue.draw(surface)

    def handle_event(self, event):
        """Handle input events.

        Args:
            event: The pygame event to handle
        """
        if event.type == pygame.KEYDOWN:
            # Handle dialogue interactions
            if self.dialogue.active:
                if event.key in (pygame.K_SPACE, pygame.K_RETURN, pygame.K_e):
                    self.dialogue.advance()

                    # Check if dialogue ended with a choice
                    if not self.dialogue.active and self.dialogue.selected_choice is not None:
                        self._handle_dialogue_choice(self.dialogue.selected_choice)

                    return  # Block other input while dialogue is active

                elif event.key == pygame.K_UP:
                    self.dialogue.move_choice(-1)
                    return

                elif event.key == pygame.K_DOWN:
                    self.dialogue.move_choice(1)
                    return

            # Normal gameplay input here...
            elif event.key == pygame.K_e:
                # Example: Check for nearby NPCs and interact
                # self.check_npc_interaction()
                pass

    def _handle_dialogue_choice(self, choice_index):
        """Handle the player's dialogue choice.

        Args:
            choice_index: The index of the selected choice
        """
        if not self.current_npc:
            return

        npc_id = self.current_npc
        npc_data = self.npcs[npc_id]

        # Handle choices based on NPC and context
        if npc_id == "elder":
            if choice_index == 0:  # Accepted quest
                dialogue_data = npc_data["quest_accepted"]
                # Add quest to player here...
                # self.player.add_quest("defeat_monsters")
            else:  # Declined quest
                dialogue_data = npc_data["quest_declined"]

            self.dialogue.show(
                npc_data["name"],
                dialogue_data["messages"]
            )

        elif npc_id == "merchant":
            if choice_index == 0:  # Potions
                self.dialogue.show("Traveling Merchant", ["Here are my potions!"])
                # Open shop UI for potions...
            elif choice_index == 1:  # Weapons
                self.dialogue.show("Traveling Merchant", ["These weapons are top quality!"])
                # Open shop UI for weapons...
            else:  # Leave
                self.dialogue.show("Traveling Merchant", ["Safe travels!"])

        self.current_npc = None


# Usage in main game:
"""
# In your State class:
def __init__(self):
    self.gameplay = ExampleGameState()

def update(self, dt):
    self.gameplay.update(dt)

def draw(self, surface):
    self.gameplay.draw(surface)

def handle_event(self, event):
    self.gameplay.handle_event(event)
"""
