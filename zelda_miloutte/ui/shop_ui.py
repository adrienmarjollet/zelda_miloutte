"""Shop buy/sell interface opened when interacting with merchant NPCs."""

import pygame
from zelda_miloutte.settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, GOLD, GRAY, BLACK
from zelda_miloutte.data.inventory import get_item, ITEMS
from zelda_miloutte.data.shops import get_shop


# ── Layout constants ─────────────────────────────────────────────────
_MARGIN = 20
_PANEL_GAP = 12
_HEADER_H = 36
_ITEM_ROW_H = 26
_DESC_H = 60
_FOOTER_H = 32

# Colors
_BG_COLOR = (10, 10, 20, 220)
_PANEL_BG = (20, 25, 40, 200)
_SELECTED_BG = (50, 60, 90)
_GOLD_COLOR = (255, 200, 50)
_ERROR_COLOR = (220, 60, 60)
_SUCCESS_COLOR = (60, 220, 80)
_DISABLED_COLOR = (100, 100, 100)
_BORDER_COLOR = (120, 130, 160)


class ShopUI:
    """Full-screen shop buy/sell interface.

    Modes:
        "buy"  — browse shop stock, purchase items
        "sell" — browse player inventory, sell items

    Controls:
        Up/Down  — navigate item list
        Left/Right — switch between Buy and Sell tabs
        Space/Enter — confirm purchase/sale
        Escape — close shop
    """

    def __init__(self):
        self.active = False
        self.shop_id = None
        self.shop_data = None
        self.player = None

        # Navigation
        self.mode = "buy"  # "buy" or "sell"
        self.cursor = 0
        self._items_list = []  # current list of item_ids displayed

        # Feedback message
        self._message = ""
        self._message_timer = 0.0
        self._message_color = WHITE

        # Fonts (lazy init)
        self._font = None
        self._small_font = None
        self._title_font = None

    def _ensure_fonts(self):
        if self._font is None:
            self._font = pygame.font.Font(None, 24)
            self._small_font = pygame.font.Font(None, 20)
            self._title_font = pygame.font.Font(None, 32)
            self._title_font.set_bold(True)

    def open(self, shop_id, player):
        """Open the shop UI for the given shop and player.

        Args:
            shop_id: Key into SHOPS dict
            player: Player entity (must have .gold and .inventory attributes)
        """
        self.shop_data = get_shop(shop_id)
        if self.shop_data is None:
            return
        self.shop_id = shop_id
        self.player = player
        self.active = True
        self.mode = "buy"
        self.cursor = 0
        self._message = ""
        self._message_timer = 0.0
        self._rebuild_items_list()

    def close(self):
        """Close the shop UI."""
        self.active = False
        self.shop_id = None
        self.shop_data = None
        self.player = None

    def _rebuild_items_list(self):
        """Rebuild the displayed item list based on current mode."""
        if self.mode == "buy":
            self._items_list = list(self.shop_data.get("items", []))
        else:
            # Sell mode: show player inventory items that have a sell value
            self._items_list = [
                iid for iid, qty in self.player.inventory.get_all()
                if get_item(iid) is not None
            ]
        # Clamp cursor
        if self._items_list:
            self.cursor = min(self.cursor, len(self._items_list) - 1)
        else:
            self.cursor = 0

    def handle_event(self, event):
        """Handle keyboard input. Returns True if event was consumed."""
        if not self.active:
            return False

        if event.type != pygame.KEYDOWN:
            return False

        if event.key == pygame.K_ESCAPE:
            self.close()
            return True

        if event.key == pygame.K_UP:
            if self._items_list:
                self.cursor = (self.cursor - 1) % len(self._items_list)
            return True

        if event.key == pygame.K_DOWN:
            if self._items_list:
                self.cursor = (self.cursor + 1) % len(self._items_list)
            return True

        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
            # Toggle buy/sell
            self.mode = "sell" if self.mode == "buy" else "buy"
            self.cursor = 0
            self._rebuild_items_list()
            return True

        if event.key in (pygame.K_SPACE, pygame.K_RETURN, pygame.K_e):
            self._confirm_action()
            return True

        return True  # Consume all keys while shop is open

    def _confirm_action(self):
        """Execute buy or sell for the currently selected item."""
        if not self._items_list:
            return

        item_id = self._items_list[self.cursor]
        item_def = get_item(item_id)
        if item_def is None:
            return

        if self.mode == "buy":
            self._do_buy(item_id, item_def)
        else:
            self._do_sell(item_id, item_def)

    def _do_buy(self, item_id, item_def):
        """Attempt to buy an item."""
        price = item_def.buy_price
        if self.player.gold < price:
            self._show_message("Not enough gold!", _ERROR_COLOR)
            return

        self.player.gold -= price
        self.player.inventory.add(item_id)
        self._show_message(f"Bought {item_def.name}!", _SUCCESS_COLOR)

    def _do_sell(self, item_id, item_def):
        """Attempt to sell an item."""
        if not self.player.inventory.remove(item_id):
            self._show_message("Nothing to sell!", _ERROR_COLOR)
            return

        sell_price = item_def.sell_price
        self.player.gold += sell_price
        self._show_message(f"Sold {item_def.name} for {sell_price}G!", _SUCCESS_COLOR)
        # Rebuild list since inventory changed
        self._rebuild_items_list()

    def _show_message(self, text, color=WHITE):
        self._message = text
        self._message_color = color
        self._message_timer = 2.0

    def update(self, dt):
        """Update timers."""
        if not self.active:
            return
        if self._message_timer > 0:
            self._message_timer -= dt
            if self._message_timer <= 0:
                self._message = ""

    def draw(self, surface):
        """Draw the full shop UI."""
        if not self.active:
            return

        self._ensure_fonts()

        # Full-screen dim overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill(_BG_COLOR)
        surface.blit(overlay, (0, 0))

        # Calculate layout
        total_w = SCREEN_WIDTH - _MARGIN * 2
        panel_w = (total_w - _PANEL_GAP) // 2
        left_x = _MARGIN
        right_x = _MARGIN + panel_w + _PANEL_GAP
        top_y = _MARGIN + _HEADER_H + 8

        # ── Header ─────────────────────────────────────────────────────
        shop_name = self.shop_data.get("name", "Shop")
        title_surf = self._title_font.render(shop_name, True, _GOLD_COLOR)
        surface.blit(title_surf, (_MARGIN, _MARGIN))

        # Gold display in header (right side)
        gold_text = self._font.render(f"Gold: {self.player.gold}", True, _GOLD_COLOR)
        surface.blit(gold_text, (SCREEN_WIDTH - _MARGIN - gold_text.get_width(), _MARGIN + 6))

        # ── Tab bar ────────────────────────────────────────────────────
        tab_y = top_y - 4
        buy_color = _GOLD_COLOR if self.mode == "buy" else _DISABLED_COLOR
        sell_color = _GOLD_COLOR if self.mode == "sell" else _DISABLED_COLOR
        buy_tab = self._font.render("[Buy]", True, buy_color)
        sell_tab = self._font.render("[Sell]", True, sell_color)
        surface.blit(buy_tab, (left_x, tab_y))
        surface.blit(sell_tab, (left_x + buy_tab.get_width() + 20, tab_y))
        hint = self._small_font.render("<Left/Right> to switch", True, GRAY)
        surface.blit(hint, (left_x + buy_tab.get_width() + sell_tab.get_width() + 40, tab_y + 3))

        list_y = tab_y + 28

        # ── Left panel: Item list ──────────────────────────────────────
        panel_h = SCREEN_HEIGHT - list_y - _MARGIN - _DESC_H - _FOOTER_H - 8
        panel_bg = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
        panel_bg.fill(_PANEL_BG)
        surface.blit(panel_bg, (left_x, list_y))
        pygame.draw.rect(surface, _BORDER_COLOR, (left_x, list_y, panel_w, panel_h), 1)

        # Visible items (scrolling if needed)
        max_visible = panel_h // _ITEM_ROW_H
        scroll_offset = max(0, self.cursor - max_visible + 1)

        if not self._items_list:
            empty_text = "No items available." if self.mode == "buy" else "Inventory empty."
            empty_surf = self._small_font.render(empty_text, True, GRAY)
            surface.blit(empty_surf, (left_x + 8, list_y + 8))
        else:
            for i in range(min(max_visible, len(self._items_list) - scroll_offset)):
                idx = i + scroll_offset
                item_id = self._items_list[idx]
                item_def = get_item(item_id)
                if item_def is None:
                    continue

                row_y = list_y + i * _ITEM_ROW_H
                row_rect = (left_x + 1, row_y, panel_w - 2, _ITEM_ROW_H)

                # Highlight selected
                if idx == self.cursor:
                    pygame.draw.rect(surface, _SELECTED_BG, row_rect)

                # Item name
                name_color = WHITE if idx == self.cursor else GRAY
                name_surf = self._font.render(item_def.name, True, name_color)
                surface.blit(name_surf, (left_x + 8, row_y + 3))

                # Price
                if self.mode == "buy":
                    price = item_def.buy_price
                    affordable = self.player.gold >= price
                    price_color = _GOLD_COLOR if affordable else _ERROR_COLOR
                    price_text = f"{price}G"
                else:
                    price_text = f"{item_def.sell_price}G"
                    price_color = _GOLD_COLOR
                    # Show quantity
                    qty = self.player.inventory.count(item_id)
                    qty_surf = self._small_font.render(f"x{qty}", True, GRAY)
                    surface.blit(qty_surf, (left_x + panel_w - 60, row_y + 5))

                price_surf = self._small_font.render(price_text, True, price_color)
                surface.blit(price_surf, (left_x + panel_w - 35, row_y + 5))

        # ── Right panel: Selected item details ─────────────────────────
        detail_h = panel_h
        detail_bg = pygame.Surface((panel_w, detail_h), pygame.SRCALPHA)
        detail_bg.fill(_PANEL_BG)
        surface.blit(detail_bg, (right_x, list_y))
        pygame.draw.rect(surface, _BORDER_COLOR, (right_x, list_y, panel_w, detail_h), 1)

        if self._items_list:
            item_id = self._items_list[self.cursor]
            item_def = get_item(item_id)
            if item_def:
                # Item name (large)
                name_surf = self._title_font.render(item_def.name, True, WHITE)
                surface.blit(name_surf, (right_x + 12, list_y + 10))

                # Category
                cat_text = item_def.category.replace("_", " ").title()
                cat_surf = self._small_font.render(cat_text, True, GRAY)
                surface.blit(cat_surf, (right_x + 12, list_y + 40))

                # Description (wrapped)
                self._draw_wrapped(surface, item_def.description,
                                   right_x + 12, list_y + 60,
                                   panel_w - 24, self._font, WHITE)

                # Price info
                price_y = list_y + 120
                if self.mode == "buy":
                    price = item_def.buy_price
                    affordable = self.player.gold >= price
                    price_color = _GOLD_COLOR if affordable else _ERROR_COLOR
                    price_label = f"Buy price: {price}G"
                else:
                    price_label = f"Sell price: {item_def.sell_price}G"
                    price_color = _GOLD_COLOR
                price_surf = self._font.render(price_label, True, price_color)
                surface.blit(price_surf, (right_x + 12, price_y))

                # Player inventory count of this item
                inv_count = self.player.inventory.count(item_id)
                if inv_count > 0:
                    own_surf = self._small_font.render(f"Owned: {inv_count}", True, GRAY)
                    surface.blit(own_surf, (right_x + 12, price_y + 24))

                # Effect summary
                self._draw_effect_summary(surface, item_def, right_x + 12, price_y + 48)

        # ── Description / feedback area ────────────────────────────────
        desc_y = list_y + panel_h + 4
        desc_bg = pygame.Surface((total_w, _DESC_H), pygame.SRCALPHA)
        desc_bg.fill(_PANEL_BG)
        surface.blit(desc_bg, (left_x, desc_y))
        pygame.draw.rect(surface, _BORDER_COLOR, (left_x, desc_y, total_w, _DESC_H), 1)

        # Greeting or feedback message
        if self._message:
            msg_surf = self._font.render(self._message, True, self._message_color)
            surface.blit(msg_surf, (left_x + 12, desc_y + 8))
        else:
            greeting = self.shop_data.get("greeting", "Welcome!")
            greet_surf = self._font.render(greeting, True, GRAY)
            surface.blit(greet_surf, (left_x + 12, desc_y + 8))

        # Controls hint
        controls = "Up/Down: Navigate  |  Space: Confirm  |  Esc: Close"
        ctrl_surf = self._small_font.render(controls, True, GRAY)
        surface.blit(ctrl_surf, (left_x + 12, desc_y + _DESC_H - 22))

        # ── Footer: player gold ────────────────────────────────────────
        footer_y = desc_y + _DESC_H + 4
        gold_big = self._title_font.render(f"Your Gold: {self.player.gold}", True, _GOLD_COLOR)
        surface.blit(gold_big, (left_x, footer_y))

    def _draw_wrapped(self, surface, text, x, y, max_width, font, color):
        """Draw word-wrapped text."""
        words = text.split(' ')
        lines = []
        current_line = ""
        for word in words:
            test_line = current_line + word + " " if current_line else word + " "
            test_w = font.size(test_line)[0]
            if test_w <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line.rstrip())
                current_line = word + " "
        if current_line:
            lines.append(current_line.rstrip())

        line_h = font.get_height()
        for i, line in enumerate(lines):
            surf = font.render(line, True, color)
            surface.blit(surf, (x, y + i * line_h))

    def _draw_effect_summary(self, surface, item_def, x, y):
        """Draw a short summary of the item's effect."""
        effect = item_def.effect
        if not effect:
            return

        parts = []
        if "heal" in effect:
            parts.append(f"Heals {effect['heal']} HP")
        if "heal_full" in effect:
            parts.append("Fully restores HP")
        if "cure" in effect:
            parts.append(f"Cures {effect['cure']}")
        if "attack" in effect:
            parts.append(f"+{effect['attack']} Attack")
        if "defense" in effect:
            parts.append(f"+{effect['defense']} Defense")
        if "speed" in effect:
            dur = effect.get("duration", 0)
            parts.append(f"Speed x{effect['speed']} ({dur}s)")
        if "resist" in effect:
            dur = effect.get("duration", 0)
            parts.append(f"{effect['resist'].title()} resist ({dur}s)")

        if parts:
            text = "  |  ".join(parts)
            surf = self._small_font.render(text, True, (150, 200, 150))
            surface.blit(surf, (x, y))
