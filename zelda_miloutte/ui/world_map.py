"""Full-screen world map overlay showing area nodes, connections, and progress."""

import pygame
from zelda_miloutte.settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, GOLD, GRAY, BLACK
from zelda_miloutte.world.maps import AREAS


# Area node positions on the world map (hand-placed for visual layout)
AREA_NODES = {
    "overworld": {
        "pos": (200, 300),
        "name": "Miloutte Village",
        "color": (34, 139, 34),
        "boss_id": "boss_1",
        "has_dungeon": True,
    },
    "forest": {
        "pos": (400, 220),
        "name": "Dark Forest",
        "color": (0, 100, 0),
        "boss_id": "forest_guardian",
        "has_dungeon": True,
    },
    "desert": {
        "pos": (400, 400),
        "name": "Scorching Desert",
        "color": (210, 180, 120),
        "boss_id": "sand_worm",
        "has_dungeon": True,
    },
    "volcano": {
        "pos": (600, 400),
        "name": "Mount Inferno",
        "color": (200, 60, 20),
        "boss_id": "inferno_drake",
        "has_dungeon": True,
    },
}

# Connections between areas (draw lines between these)
AREA_CONNECTIONS = [
    ("overworld", "forest"),
    ("forest", "desert"),
    ("desert", "volcano"),
]


class WorldMap:
    """Full-screen world map overlay."""

    def __init__(self):
        self.active = False
        self.selected_area = "overworld"
        self._font = None
        self._title_font = None
        self._small_font = None
        # Navigation order for arrow keys
        self._nav_order = ["overworld", "forest", "desert", "volcano"]
        # Fast travel message
        self._message = ""
        self._message_timer = 0.0

    def _ensure_fonts(self):
        if self._font is None:
            self._font = pygame.font.Font(None, 28)
            self._title_font = pygame.font.Font(None, 48)
            self._small_font = pygame.font.Font(None, 20)

    def open(self, current_area):
        """Open the world map, selecting the current area."""
        self.active = True
        self.selected_area = current_area

    def close(self):
        """Close the world map."""
        self.active = False

    def handle_event(self, event):
        """Handle navigation and closing. Returns 'close', 'fast_travel:area_id', or None."""
        if not self.active:
            return None

        if event.type != pygame.KEYDOWN:
            return None

        if event.key == pygame.K_ESCAPE or event.key == pygame.K_m:
            return "close"

        idx = self._nav_order.index(self.selected_area) if self.selected_area in self._nav_order else 0

        if event.key == pygame.K_LEFT or event.key == pygame.K_a:
            idx = (idx - 1) % len(self._nav_order)
            self.selected_area = self._nav_order[idx]
        elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            idx = (idx + 1) % len(self._nav_order)
            self.selected_area = self._nav_order[idx]
        elif event.key == pygame.K_UP or event.key == pygame.K_w:
            idx = (idx - 1) % len(self._nav_order)
            self.selected_area = self._nav_order[idx]
        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
            idx = (idx + 1) % len(self._nav_order)
            self.selected_area = self._nav_order[idx]
        elif event.key == pygame.K_RETURN:
            return f"fast_travel:{self.selected_area}"

        return None

    def update(self, dt):
        """Update message timer."""
        if self._message_timer > 0:
            self._message_timer -= dt
            if self._message_timer <= 0:
                self._message = ""

    def show_message(self, text):
        """Show a temporary message on the world map."""
        self._message = text
        self._message_timer = 2.0

    def draw(self, surface, current_area, world_state, quest_manager, visited_areas=None):
        """Draw the world map overlay."""
        if not self.active:
            return

        self._ensure_fonts()

        # Dark overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        surface.blit(overlay, (0, 0))

        # Title
        title = self._title_font.render("WORLD MAP", True, WHITE)
        tx = (SCREEN_WIDTH - title.get_width()) // 2
        surface.blit(title, (tx, 20))

        defeated_bosses = world_state.get("defeated_bosses", [])
        story_progress = world_state.get("story_progress", 0)

        # Draw connections (lines between area nodes)
        for a1, a2 in AREA_CONNECTIONS:
            if a1 in AREA_NODES and a2 in AREA_NODES:
                p1 = AREA_NODES[a1]["pos"]
                p2 = AREA_NODES[a2]["pos"]
                line_color = (100, 100, 100)
                # Brighter line if both areas are unlocked
                if self._is_area_unlocked(a1, quest_manager) and self._is_area_unlocked(a2, quest_manager):
                    line_color = (160, 160, 160)
                pygame.draw.line(surface, line_color, p1, p2, 2)

        # Draw area nodes
        for area_id, node in AREA_NODES.items():
            pos = node["pos"]
            name = node["name"]
            base_color = node["color"]
            boss_id = node.get("boss_id")
            unlocked = self._is_area_unlocked(area_id, quest_manager)
            is_selected = area_id == self.selected_area
            is_current = area_id == current_area

            # Node appearance
            if unlocked:
                node_color = base_color
            else:
                # Greyed out / darker
                node_color = tuple(c // 3 for c in base_color)

            # Draw node circle
            radius = 22 if is_selected else 18
            pygame.draw.circle(surface, node_color, pos, radius)

            # Highlight ring for selected
            if is_selected:
                pygame.draw.circle(surface, GOLD, pos, radius + 3, 2)

            # Current area indicator (white ring)
            if is_current:
                pygame.draw.circle(surface, WHITE, pos, radius + 6, 2)

            # Area name
            name_surf = self._font.render(name, True, WHITE if unlocked else GRAY)
            name_x = pos[0] - name_surf.get_width() // 2
            name_y = pos[1] - radius - 22
            surface.blit(name_surf, (name_x, name_y))

            # Boss status icon (below node)
            if node.get("has_dungeon") and boss_id:
                boss_defeated = boss_id in defeated_bosses
                icon_y = pos[1] + radius + 8
                if boss_defeated:
                    # Checkmark
                    check_surf = self._small_font.render("V", True, (50, 200, 50))
                    surface.blit(check_surf, (pos[0] - check_surf.get_width() // 2, icon_y))
                elif unlocked:
                    # Skull icon (text-based)
                    skull_surf = self._small_font.render("BOSS", True, (200, 50, 50))
                    surface.blit(skull_surf, (pos[0] - skull_surf.get_width() // 2, icon_y))

            # Completion percentage
            if unlocked:
                pct = self._get_area_completion(area_id, world_state)
                pct_text = f"{pct}%"
                pct_surf = self._small_font.render(pct_text, True, (180, 180, 180))
                pct_y = pos[1] + radius + 22
                surface.blit(pct_surf, (pos[0] - pct_surf.get_width() // 2, pct_y))

            # Quest markers
            quest_icon = self._get_quest_marker(area_id, quest_manager)
            if quest_icon:
                icon_surf = self._font.render(quest_icon[0], True, quest_icon[1])
                surface.blit(icon_surf, (pos[0] + radius + 4, pos[1] - 10))

        # Selected area info panel
        self._draw_info_panel(surface, self.selected_area, world_state, quest_manager)

        # Controls help
        help_text = "Arrow Keys: Navigate | Enter: Fast Travel | M/Esc: Close"
        help_surf = self._small_font.render(help_text, True, (140, 140, 140))
        surface.blit(help_surf, ((SCREEN_WIDTH - help_surf.get_width()) // 2, SCREEN_HEIGHT - 30))

        # Temporary message
        if self._message and self._message_timer > 0:
            msg_surf = self._font.render(self._message, True, (255, 200, 50))
            msg_x = (SCREEN_WIDTH - msg_surf.get_width()) // 2
            surface.blit(msg_surf, (msg_x, SCREEN_HEIGHT - 60))

    def _draw_info_panel(self, surface, area_id, world_state, quest_manager):
        """Draw an info panel for the selected area."""
        if area_id not in AREA_NODES:
            return

        node = AREA_NODES[area_id]
        panel_x = SCREEN_WIDTH - 220
        panel_y = 80
        panel_w = 200
        panel_h = 150

        # Panel background
        panel = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
        panel.fill((20, 20, 40, 180))
        pygame.draw.rect(panel, (100, 100, 120), (0, 0, panel_w, panel_h), 1)
        surface.blit(panel, (panel_x, panel_y))

        # Area name
        name_surf = self._font.render(node["name"], True, WHITE)
        surface.blit(name_surf, (panel_x + 10, panel_y + 8))

        # Unlocked status
        unlocked = self._is_area_unlocked(area_id, quest_manager)
        status_text = "Unlocked" if unlocked else "Locked"
        status_color = (100, 200, 100) if unlocked else (200, 100, 100)
        status_surf = self._small_font.render(status_text, True, status_color)
        surface.blit(status_surf, (panel_x + 10, panel_y + 35))

        # Boss status
        boss_id = node.get("boss_id")
        defeated_bosses = world_state.get("defeated_bosses", [])
        if boss_id:
            if boss_id in defeated_bosses:
                boss_text = "Boss: Defeated"
                boss_color = (100, 200, 100)
            elif unlocked:
                boss_text = "Boss: Alive"
                boss_color = (200, 100, 100)
            else:
                boss_text = "Boss: Unknown"
                boss_color = GRAY
            boss_surf = self._small_font.render(boss_text, True, boss_color)
            surface.blit(boss_surf, (panel_x + 10, panel_y + 55))

        # Completion
        pct = self._get_area_completion(area_id, world_state)
        comp_surf = self._small_font.render(f"Completion: {pct}%", True, (180, 180, 180))
        surface.blit(comp_surf, (panel_x + 10, panel_y + 75))

        # Active quests in this area
        active_quests = self._get_area_quests(area_id, quest_manager)
        if active_quests:
            q_y = panel_y + 100
            quest_header = self._small_font.render("Quests:", True, GOLD)
            surface.blit(quest_header, (panel_x + 10, q_y))
            for i, q in enumerate(active_quests[:2]):  # Show max 2
                q_text = self._small_font.render(f"- {q.name}", True, (200, 200, 200))
                surface.blit(q_text, (panel_x + 10, q_y + 16 + i * 14))

    def _is_area_unlocked(self, area_id, quest_manager):
        """Check if an area is unlocked based on quest progress."""
        # Overworld is always unlocked
        if area_id == "overworld":
            return True
        # Forest: unlocked after talking to Elder Mira (story_1 must be active or complete)
        if area_id == "forest":
            q = quest_manager.get_quest("story_1")
            if q and q.status != "inactive":
                return True
            return False
        # Desert: unlocked after forest boss (story_2 completed)
        if area_id == "desert":
            q = quest_manager.get_quest("story_2")
            if q and q.status == "completed":
                return True
            return False
        # Volcano: unlocked after desert boss (story_4 completed)
        if area_id == "volcano":
            q = quest_manager.get_quest("story_4")
            if q and q.status == "completed":
                return True
            return False
        return True

    def _get_area_completion(self, area_id, world_state):
        """Calculate completion percentage for an area."""
        defeated_bosses = world_state.get("defeated_bosses", [])
        node = AREA_NODES.get(area_id, {})
        boss_id = node.get("boss_id")

        # Simple completion: boss defeated = 100%, otherwise 50% if visited
        # A more detailed system could track chests, enemies, etc.
        total = 2  # Boss + visited
        done = 0

        # Check if area has been visited (it's in the current/past areas)
        current = world_state.get("current_area", "overworld")
        if current == area_id or area_id == "overworld":
            done += 1

        if boss_id and boss_id in defeated_bosses:
            done += 1

        return int(done / total * 100) if total > 0 else 0

    def _get_quest_marker(self, area_id, quest_manager):
        """Return quest marker (char, color) or None for an area."""
        # Check for active quests related to this area
        for quest in quest_manager.quests.values():
            if quest.status == "active":
                # Check if any objective references this area
                for obj in quest.objectives:
                    if obj.get("target") == area_id or obj.get("type") == "visit":
                        return ("!", (255, 220, 50))
            elif quest.status == "inactive":
                # Available quest marker
                for prereq_id in quest.prerequisites:
                    prereq = quest_manager.get_quest(prereq_id)
                    if prereq and prereq.status == "completed":
                        return ("?", (140, 140, 140))
        return None

    def _get_area_quests(self, area_id, quest_manager):
        """Get active quests that may be relevant to an area."""
        relevant = []
        for quest in quest_manager.quests.values():
            if quest.status == "active":
                # Check if quest has objectives related to this area
                for obj in quest.objectives:
                    if obj.get("target") == area_id:
                        relevant.append(quest)
                        break
                else:
                    # Also include story quests relevant by area mapping
                    area_quest_map = {
                        "overworld": ["story_1", "side_1", "side_2"],
                        "forest": ["story_2"],
                        "desert": ["story_3", "story_4"],
                        "volcano": ["story_5", "story_6"],
                    }
                    if quest.id in area_quest_map.get(area_id, []):
                        relevant.append(quest)
        return relevant
