import pygame
from zelda_miloutte.settings import (
    SCREEN_WIDTH, HUD_HEIGHT, HUD_HEART_SIZE, HUD_HEART_SPACING,
    HUD_MARGIN, HEART_RED, KEY_YELLOW, BLACK, WHITE, DARK_RED,
    BOSS_BAR_WIDTH, BOSS_BAR_HEIGHT, BOSS_PURPLE, RED,
)
from zelda_miloutte.sprites.hud_sprites import (
    get_hud_heart_full, get_hud_heart_half, get_hud_heart_empty,
    get_hud_key_icon,
)


class HUD:
    def __init__(self):
        self.font = None
        self.small_font = None
        self.boss = None
        self._heart_full = None
        self._heart_half = None
        self._heart_empty = None
        self._key_icon = None
        # Smooth XP bar animation
        self._displayed_xp_ratio = 0.0

    def _ensure_sprites(self):
        if self._heart_full is None:
            self._heart_full = get_hud_heart_full()
            self._heart_half = get_hud_heart_half()
            self._heart_empty = get_hud_heart_empty()
            self._key_icon = get_hud_key_icon()

    def _get_font(self):
        if self.font is None:
            self.font = pygame.font.Font(None, 24)
            self.small_font = pygame.font.Font(None, 18)
        return self.font

    def draw(self, surface, player, boss=None):
        self._ensure_sprites()

        # HUD background
        hud_surface = pygame.Surface((SCREEN_WIDTH, HUD_HEIGHT), pygame.SRCALPHA)
        hud_surface.fill((0, 0, 0, 160))
        surface.blit(hud_surface, (0, 0))

        # Hearts
        for i in range(player.max_hp // 2):
            x = HUD_MARGIN + i * (HUD_HEART_SIZE + HUD_HEART_SPACING)
            y = HUD_MARGIN
            heart_val = player.hp - i * 2

            if heart_val >= 2:
                surface.blit(self._heart_full, (x, y))
            elif heart_val == 1:
                surface.blit(self._heart_half, (x, y))
            else:
                surface.blit(self._heart_empty, (x, y))

        # Key icon + count
        font = self._get_font()
        key_x = HUD_MARGIN + (player.max_hp // 2) * (HUD_HEART_SIZE + HUD_HEART_SPACING) + 20
        surface.blit(self._key_icon, (key_x, HUD_MARGIN))
        text = font.render(f"x{player.keys}", True, WHITE)
        surface.blit(text, (key_x + self._key_icon.get_width() + 4, HUD_MARGIN + 4))

        # Level + XP bar (below hearts)
        level = getattr(player, 'level', 1)
        xp = getattr(player, 'xp', 0)
        xp_to_next = getattr(player, 'xp_to_next', 100)
        xp_ratio = xp / xp_to_next if xp_to_next > 0 else 0

        # Smooth animation
        diff = xp_ratio - self._displayed_xp_ratio
        if abs(diff) > 0.01:
            self._displayed_xp_ratio += diff * 0.15
        else:
            self._displayed_xp_ratio = xp_ratio

        # Level number
        lv_text = self.small_font.render(f"Lv.{level}", True, (200, 200, 255))
        lv_x = HUD_MARGIN
        lv_y = HUD_MARGIN + HUD_HEART_SIZE + 2
        surface.blit(lv_text, (lv_x, lv_y))

        # XP bar
        xp_bar_x = lv_x + lv_text.get_width() + 4
        xp_bar_y = lv_y + 2
        xp_bar_w = 80
        xp_bar_h = 8
        # Background
        pygame.draw.rect(surface, (40, 40, 60), (xp_bar_x, xp_bar_y, xp_bar_w, xp_bar_h))
        # Fill
        fill_w = int(xp_bar_w * self._displayed_xp_ratio)
        if fill_w > 0:
            pygame.draw.rect(surface, (100, 180, 255), (xp_bar_x, xp_bar_y, fill_w, xp_bar_h))
        # Border
        pygame.draw.rect(surface, (80, 80, 100), (xp_bar_x, xp_bar_y, xp_bar_w, xp_bar_h), 1)

        # Status effect icons
        self._draw_status_effects(surface, player)

        # Boss health bar
        if boss and boss.alive and not boss.dying:
            self._draw_boss_bar(surface, boss)

    def _draw_status_effects(self, surface, player):
        """Draw status effect indicators next to hearts."""
        effects = getattr(player, 'status_effects', {})
        if not effects:
            return
        font = self._get_font()
        ex = SCREEN_WIDTH - HUD_MARGIN - 60
        ey = HUD_MARGIN + 2
        for name in effects:
            if name == "poison":
                color = (80, 200, 80)
                label = "PSN"
            elif name == "slow":
                color = (80, 150, 255)
                label = "SLW"
            else:
                color = WHITE
                label = name[:3].upper()
            txt = font.render(label, True, color)
            surface.blit(txt, (ex, ey))
            ex -= 40

    def _draw_boss_bar(self, surface, boss):
        bar_x = (SCREEN_WIDTH - BOSS_BAR_WIDTH) // 2
        bar_y = HUD_MARGIN
        # Background
        pygame.draw.rect(surface, (40, 40, 40),
                         (bar_x - 1, bar_y - 1, BOSS_BAR_WIDTH + 2, BOSS_BAR_HEIGHT + 2))
        # HP fill
        hp_ratio = max(0, boss.hp / boss.max_hp)
        fill_width = int(BOSS_BAR_WIDTH * hp_ratio)
        bar_color = RED if boss.phase == 2 else BOSS_PURPLE
        pygame.draw.rect(surface, bar_color,
                         (bar_x, bar_y, fill_width, BOSS_BAR_HEIGHT))
        # Border
        pygame.draw.rect(surface, WHITE,
                         (bar_x - 1, bar_y - 1, BOSS_BAR_WIDTH + 2, BOSS_BAR_HEIGHT + 2), 1)
        # Label
        font = self._get_font()
        label = font.render("BOSS", True, WHITE)
        surface.blit(label, (bar_x + BOSS_BAR_WIDTH // 2 - label.get_width() // 2,
                             bar_y + BOSS_BAR_HEIGHT + 2))
