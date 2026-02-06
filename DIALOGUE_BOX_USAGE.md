# DialogueBox Usage Guide

The `DialogueBox` class provides an enhanced dialogue system with NPC names, sequential messages, and player choices.

## Location
`zelda_miloutte/ui/dialogue_box.py`

## Features

1. **NPC Name Header** - Displays the speaker's name in gold at the top
2. **Sequential Messages** - Shows multiple messages one after another
3. **Choice Selection** - Allows player to choose from options after messages
4. **Typewriter Effect** - Reveals text gradually for better readability
5. **Blinking Arrow** - Indicates when player can advance

## Basic Usage

```python
from zelda_miloutte.ui.dialogue_box import DialogueBox

# Create the dialogue box (typically in __init__)
self.dialogue = DialogueBox()

# Show a simple message
self.dialogue.show("Elder", ["Welcome to our village!"])

# Show multiple sequential messages
self.dialogue.show(
    "Merchant",
    [
        "Greetings, traveler!",
        "I have many fine wares for sale.",
        "What would you like to buy?"
    ]
)

# Show messages with choices
self.dialogue.show(
    "Guard",
    [
        "Halt! This area is restricted.",
        "Do you have permission to enter?"
    ],
    choices=["Yes, I do", "No, sorry"]
)
```

## Integration with Game Loop

### Update
```python
def update(self, dt):
    """Update game state."""
    self.dialogue.update(dt)

    # Don't update gameplay while dialogue is active
    if self.dialogue.active:
        return

    # Normal gameplay updates...
```

### Draw
```python
def draw(self, surface):
    """Draw game elements."""
    # Draw gameplay elements...

    # Draw dialogue on top
    self.dialogue.draw(surface)
```

### Event Handling
```python
def handle_event(self, event):
    """Handle player input."""
    if event.type == pygame.KEYDOWN:
        # Handle dialogue interaction
        if self.dialogue.active:
            if event.key in (pygame.K_SPACE, pygame.K_RETURN, pygame.K_e):
                self.dialogue.advance()

                # Check if player made a choice
                if not self.dialogue.active and self.dialogue.selected_choice is not None:
                    self._handle_dialogue_choice(self.dialogue.selected_choice)

                return  # Don't process other input while dialogue is active

            elif event.key == pygame.K_UP:
                self.dialogue.move_choice(-1)
                return

            elif event.key == pygame.K_DOWN:
                self.dialogue.move_choice(1)
                return

        # Normal gameplay input...
```

## Handling Dialogue Choices

```python
def _handle_dialogue_choice(self, choice_index):
    """Handle the player's dialogue choice.

    Args:
        choice_index: The index of the selected choice
    """
    # Example: Quest acceptance dialogue
    if self.current_npc == "elder":
        if choice_index == 0:  # Accepted quest
            self.player.add_quest("defeat_monsters")
            self.dialogue.show("Elder", ["Thank you, brave hero!"])
        else:  # Declined quest
            self.dialogue.show("Elder", ["I understand. Come back if you change your mind."])
```

## Example: NPC Interaction

```python
class NPC:
    """Example NPC entity."""

    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, 32, 32)
        self.talked_to = False

    def get_dialogue(self):
        """Get dialogue for this NPC."""
        if not self.talked_to:
            return {
                "messages": [
                    "Hello there!",
                    "I've been waiting for someone like you.",
                    "Would you help me with a task?"
                ],
                "choices": ["Of course!", "Maybe later"]
            }
        else:
            return {
                "messages": ["Thanks again for your help!"]
            }

# In gameplay state:
def interact_with_npc(self, npc):
    """Start dialogue with an NPC."""
    dialogue_data = npc.get_dialogue()
    self.current_npc = npc
    self.dialogue.show(
        npc.name,
        dialogue_data["messages"],
        dialogue_data.get("choices")
    )
```

## Advanced: Branching Dialogue

```python
class DialogueTree:
    """Manages complex branching dialogue."""

    def __init__(self):
        self.current_node = "start"
        self.nodes = {
            "start": {
                "npc": "Mysterious Stranger",
                "messages": ["Do you seek power or wisdom?"],
                "choices": ["Power", "Wisdom"],
                "next": ["power_path", "wisdom_path"]
            },
            "power_path": {
                "npc": "Mysterious Stranger",
                "messages": [
                    "Power comes at a price.",
                    "Are you willing to pay it?"
                ],
                "choices": ["Yes", "No"],
                "next": ["power_accept", "start"]
            },
            "wisdom_path": {
                "npc": "Mysterious Stranger",
                "messages": [
                    "A wise choice.",
                    "Knowledge is the true treasure."
                ]
            }
        }

    def show_node(self, dialogue_box, node_id=None):
        """Show a dialogue node."""
        if node_id:
            self.current_node = node_id

        node = self.nodes[self.current_node]
        dialogue_box.show(
            node["npc"],
            node["messages"],
            node.get("choices")
        )

    def handle_choice(self, choice_index):
        """Get the next node based on choice."""
        node = self.nodes[self.current_node]
        if "next" in node and choice_index < len(node["next"]):
            return node["next"][choice_index]
        return None

# In gameplay:
def _handle_dialogue_choice(self, choice_index):
    """Handle dialogue choice with branching."""
    next_node = self.dialogue_tree.handle_choice(choice_index)
    if next_node:
        self.dialogue_tree.show_node(self.dialogue, next_node)
```

## Tips

1. **Keep Messages Concise** - Each message should fit within the dialogue box (approximately 2-3 lines)
2. **Limit Choices** - 2-4 choices work best. More than that may not fit in the box.
3. **Block Gameplay** - Always disable player movement and combat while dialogue is active
4. **Clear Feedback** - Use the typewriter effect to pace information delivery
5. **Test Wrapping** - Long words or names may wrap awkwardly, test with actual content

## Properties

- `active` (bool) - Whether dialogue is currently shown
- `npc_name` (str) - Name displayed at the top
- `messages` (list[str]) - All messages to show
- `current_index` (int) - Current message being shown
- `choices` (list[str]) - Choice options (if any)
- `choice_index` (int) - Currently selected choice
- `selected_choice` (int | None) - Index of confirmed choice

## Methods

- `show(npc_name, messages, choices=None)` - Start dialogue
- `advance()` - Progress to next message or select choice
- `move_choice(direction)` - Move selection up (-1) or down (+1)
- `update(dt)` - Update typewriter and animations
- `draw(surface)` - Render the dialogue box
- `dismiss()` - Close the dialogue
