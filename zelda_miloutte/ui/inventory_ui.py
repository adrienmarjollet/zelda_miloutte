"""Inventory overlay UI with grid-based item display and equipment slots."""

import pygame
from ..settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, GOLD, GRAY
from ..data.inventory import EQUIP_SLOTS, get_item
from ..sprites.item_sprites import get_inventory_icon


# Layout constants
_GRID_COLS = 5
_GRID_ROWS = 4  # 5x4 = 20 slots max
_SLOT_SIZE = 36
_SLOT_PAD = 4
_ICON_SCALE = 2  # 16x16 -> 32x32 inside 36x36 slot

_PANEL_W = 560
_PANEL_H = 400
_PANEL_X = (SCREEN_WIDTH - _PANEL_W) // 2
_PANEL_Y = (SCREEN_HEIGHT - _PANEL_H) // 2

# Inventory grid origin (left side of panel)
_GRID_X = _PANEL_X + 20
_GRID_Y = _PANEL_Y + 60

# Equipment panel origin (right side of panel)
_EQUIP_X = _PANEL_X + 280
_EQUIP_Y = _PANEL_Y + 60

# Info area
_INFO_X = _PANEL_X + 20
_INFO_Y = _PANEL_Y + _PANEL_H - 90

# Action hints
_ACTION_Y = _PANEL_Y + _PANEL_H - 30

# Equipment slot display names
_SLOT_LABELS = {"weapon": "Weapon", "shield": "Shield", "ring": "Ring", "boots": "Boots"}


class InventoryUI:
    """Overlay UI for the inventory screen."""

    def __init__(self):
        self.active = False
        self.cursor = 0  # index into displayed items list
        self.mode = "grid"  # "grid" or "equip"
        self.equip_cursor = 0  # index into EQUIP_SLOTS
        self._fonts_init = False
        self._title_font = None
        self._font = None
        self._small_font = None

    def _init_fonts(self):
        if self._fonts_init:
            return
        self._title_font = pygame.font.Font(None, 36)
        self._font = pygame.font.Font(None, 24)
        self._small_font = pygame.font.Font(None, 20)
        self._fonts_init = True

    def open(self):
        self.active = True
        self.cursor = 0
        self.mode = "grid"
        self.equip_cursor = 0

    def close(self):
        self.active = False

    def handle_event(self, event, inventory, player):
        """Handle input for the inventory screen.

        Returns:
            A dict describing any action that needs gameplay-level handling,
            or None.  Example: {"action": "bomb", "damage": 3, "radius": 64}
        """
        if not self.active:
            return None
        if event.type != pygame.KEYDOWN:
            return None

        # Close inventory
        if event.key in (pygame.K_i, pygame.K_TAB, pygame.K_ESCAPE):
            self.close()
            return None

        if self.mode == "grid":
            return self._handle_grid_input(event, inventory, player)
        elif self.mode == "equip":
            return self._handle_equip_input(event, inventory)
        return None

    def _handle_grid_input(self, event, inventory, player):
        items_list = inventory.get_all()
        num_items = len(items_list)

        if event.key == pygame.K_UP:
            self.cursor = max(0, self.cursor - _GRID_COLS)
        elif event.key == pygame.K_DOWN:
            self.cursor = min(max(num_items - 1, 0), self.cursor + _GRID_COLS)
        elif event.key == pygame.K_LEFT:
            if self.cursor > 0:
                self.cursor -= 1
        elif event.key == pygame.K_RIGHT:
            if self.cursor < num_items - 1:
                self.cursor += 1
            else:
                # Switch to equipment panel
                self.mode = "equip"
                self.equip_cursor = 0
        elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
            # Use or equip selected item
            if 0 <= self.cursor < num_items:
                item_id, qty = items_list[self.cursor]
                defn = get_item(item_id)
                if defn is None:
                    return None
                if defn.category == "equipment":
                    inventory.equip_item(item_id)
                    # Clamp cursor
                    new_list = inventory.get_all()
                    if self.cursor >= len(new_list):
                        self.cursor = max(0, len(new_list) - 1)
                elif defn.category == "consumable":
                    effect = defn.effect
                    # Check for bomb — needs gameplay-level handling
                    if effect.get("bomb"):
                        if inventory.use_consumable(item_id, player):
                            new_list = inventory.get_all()
                            if self.cursor >= len(new_list):
                                self.cursor = max(0, len(new_list) - 1)
                            return {"action": "bomb",
                                    "damage": effect.get("damage", 3),
                                    "radius": effect.get("radius", 64)}
                    else:
                        inventory.use_consumable(item_id, player)
                        new_list = inventory.get_all()
                        if self.cursor >= len(new_list):
                            self.cursor = max(0, len(new_list) - 1)
        elif event.key == pygame.K_x:
            # Drop item
            if 0 <= self.cursor < num_items:
                item_id, qty = items_list[self.cursor]
                inventory.remove(item_id)
                new_list = inventory.get_all()
                if self.cursor >= len(new_list):
                    self.cursor = max(0, len(new_list) - 1)
        return None

    def _handle_equip_input(self, event, inventory):
        if event.key == pygame.K_UP:
            self.equip_cursor = max(0, self.equip_cursor - 1)
        elif event.key == pygame.K_DOWN:
            self.equip_cursor = min(len(EQUIP_SLOTS) - 1, self.equip_cursor + 1)
        elif event.key == pygame.K_LEFT:
            # Switch back to grid
            self.mode = "grid"
            items_list = inventory.get_all()
            self.cursor = min(self.cursor, max(0, len(items_list) - 1))
        elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
            # Unequip selected slot
            slot = EQUIP_SLOTS[self.equip_cursor]
            inventory.unequip_item(slot)
        return None

    def draw(self, surface, inventory, player):
        """Draw the inventory overlay."""
        if not self.active:
            return
        self._init_fonts()

        # Dim background
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        surface.blit(overlay, (0, 0))

        # Panel background
        panel = pygame.Surface((_PANEL_W, _PANEL_H), pygame.SRCALPHA)
        panel.fill((20, 20, 40, 230))
        surface.blit(panel, (_PANEL_X, _PANEL_Y))
        pygame.draw.rect(surface, (100, 100, 140), (_PANEL_X, _PANEL_Y, _PANEL_W, _PANEL_H), 2)

        # Title
        title = self._title_font.render("Inventory", True, GOLD)
        surface.blit(title, (_PANEL_X + 20, _PANEL_Y + 15))

        # Stats summary
        atk = player.base_attack + inventory.get_stat_bonus("attack")
        dfn = player.base_defense + inventory.get_stat_bonus("defense")
        spd_bonus = inventory.get_stat_bonus("speed")
        stats_text = f"ATK:{atk}  DEF:{dfn}  SPD:+{spd_bonus}"
        stats_surf = self._small_font.render(stats_text, True, (180, 180, 200))
        surface.blit(stats_surf, (_PANEL_X + 200, _PANEL_Y + 22))

        # Draw inventory grid
        items_list = inventory.get_all()
        self._draw_grid(surface, items_list)

        # Draw equipment panel
        self._draw_equipment(surface, inventory)

        # Draw item info for selected item
        self._draw_info(surface, inventory, items_list)

        # Draw action hints
        self._draw_hints(surface, inventory, items_list)

    def _draw_grid(self, surface, items_list):
        """Draw the 5x4 inventory grid."""
        for slot_idx in range(_GRID_COLS * _GRID_ROWS):
            col = slot_idx % _GRID_COLS
            row = slot_idx // _GRID_COLS
            x = _GRID_X + col * (_SLOT_SIZE + _SLOT_PAD)
            y = _GRID_Y + row * (_SLOT_SIZE + _SLOT_PAD)

            # Slot background
            if self.mode == "grid" and slot_idx == self.cursor and slot_idx < len(items_list):
                bg_color = (60, 60, 100)
                border_color = GOLD
            else:
                bg_color = (30, 30, 50)
                border_color = (70, 70, 90)

            pygame.draw.rect(surface, bg_color, (x, y, _SLOT_SIZE, _SLOT_SIZE))
            pygame.draw.rect(surface, border_color, (x, y, _SLOT_SIZE, _SLOT_SIZE), 1)

            # Draw item icon
            if slot_idx < len(items_list):
                item_id, qty = items_list[slot_idx]
                defn = get_item(item_id)
                if defn is not None:
                    icon = get_inventory_icon(defn.icon)
                    # Scale 16x16 to 32x32
                    scaled = pygame.transform.scale(icon, (32, 32))
                    surface.blit(scaled, (x + 2, y + 2))

                    # Quantity badge for consumables with qty > 1
                    if qty > 1:
                        qty_surf = self._small_font.render(str(qty), True, WHITE)
                        surface.blit(qty_surf, (x + _SLOT_SIZE - qty_surf.get_width() - 2,
                                                y + _SLOT_SIZE - qty_surf.get_height()))

    def _draw_equipment(self, surface, inventory):
        """Draw the equipment slots panel."""
        header = self._font.render("Equipment", True, (180, 180, 220))
        surface.blit(header, (_EQUIP_X, _EQUIP_Y - 20))

        for i, slot in enumerate(EQUIP_SLOTS):
            y = _EQUIP_Y + i * (_SLOT_SIZE + _SLOT_PAD + 8)
            x = _EQUIP_X

            # Label
            label = self._small_font.render(_SLOT_LABELS[slot] + ":", True, (140, 140, 160))
            surface.blit(label, (x, y))

            # Slot box
            box_x = x + 70
            if self.mode == "equip" and i == self.equip_cursor:
                bg_color = (60, 60, 100)
                border_color = GOLD
            else:
                bg_color = (30, 30, 50)
                border_color = (70, 70, 90)

            pygame.draw.rect(surface, bg_color, (box_x, y - 2, _SLOT_SIZE, _SLOT_SIZE))
            pygame.draw.rect(surface, border_color, (box_x, y - 2, _SLOT_SIZE, _SLOT_SIZE), 1)

            equipped = inventory.get_equipped(slot)
            if equipped is not None:
                icon = get_inventory_icon(equipped.icon)
                scaled = pygame.transform.scale(icon, (32, 32))
                surface.blit(scaled, (box_x + 2, y))

                # Item name next to slot
                name_surf = self._small_font.render(equipped.name, True, WHITE)
                surface.blit(name_surf, (box_x + _SLOT_SIZE + 6, y + 6))
            else:
                empty = self._small_font.render("---", True, (80, 80, 100))
                surface.blit(empty, (box_x + _SLOT_SIZE + 6, y + 6))

    def _draw_info(self, surface, inventory, items_list):
        """Draw selected item info panel."""
        defn = None
        if self.mode == "grid" and 0 <= self.cursor < len(items_list):
            item_id, qty = items_list[self.cursor]
            defn = get_item(item_id)
        elif self.mode == "equip":
            slot = EQUIP_SLOTS[self.equip_cursor]
            defn = inventory.get_equipped(slot)

        # Info background
        pygame.draw.rect(surface, (15, 15, 30), (_INFO_X, _INFO_Y, _PANEL_W - 40, 55))
        pygame.draw.rect(surface, (70, 70, 90), (_INFO_X, _INFO_Y, _PANEL_W - 40, 55), 1)

        if defn is None:
            empty = self._small_font.render("No item selected", True, (100, 100, 120))
            surface.blit(empty, (_INFO_X + 8, _INFO_Y + 8))
            return

        # Name
        is_equip = defn.category == "equipment"
        name_color = GOLD if is_equip else (100, 220, 100)
        name_surf = self._font.render(defn.name, True, name_color)
        surface.blit(name_surf, (_INFO_X + 8, _INFO_Y + 4))

        # Type tag
        tag = f"[{defn.category.upper()}]"
        if defn.equip_slot:
            tag += f" {_SLOT_LABELS.get(defn.equip_slot, defn.equip_slot)}"
        tag_surf = self._small_font.render(tag, True, (140, 140, 160))
        surface.blit(tag_surf, (_INFO_X + name_surf.get_width() + 12, _INFO_Y + 8))

        # Description
        desc_surf = self._small_font.render(defn.description, True, (200, 200, 210))
        surface.blit(desc_surf, (_INFO_X + 8, _INFO_Y + 30))

    def _draw_hints(self, surface, inventory, items_list):
        """Draw action key hints at the bottom."""
        if self.mode == "grid" and 0 <= self.cursor < len(items_list):
            item_id, qty = items_list[self.cursor]
            defn = get_item(item_id)
            if defn and defn.category == "equipment":
                hint = "ENTER: Equip   X: Drop   I/TAB: Close"
            else:
                hint = "ENTER: Use   X: Drop   I/TAB: Close"
        elif self.mode == "equip":
            slot = EQUIP_SLOTS[self.equip_cursor]
            if inventory.equipment[slot] is not None:
                hint = "ENTER: Unequip   I/TAB: Close"
            else:
                hint = "I/TAB: Close"
        else:
            hint = "I/TAB: Close"

        hint_surf = self._small_font.render(hint, True, (140, 140, 160))
        surface.blit(hint_surf, (_PANEL_X + (_PANEL_W - hint_surf.get_width()) // 2, _ACTION_Y))
