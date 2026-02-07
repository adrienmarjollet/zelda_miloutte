import math
import random

import pygame

from .state import State
from ..settings import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, GOLD
from ..sounds import get_sound_manager


class CinematicState(State):
    """Cinematic sequence — intro, mid-game, or ending."""

    # Presets for different cutscene types
    INTRO_SCENES = [
        {"duration": 5.0, "text": "In a land of ancient magic...", "particle_color": (255, 200, 50)},
        {"duration": 5.0, "text": "A darkness awakened...", "particle_color": (150, 50, 200)},
        {"duration": 5.0, "text": "Its minions spread across the land...", "particle_color": (50, 180, 50)},
        {"duration": 5.0, "text": "But one hero remained...", "particle_color": (255, 200, 50)},
        {"duration": 5.0, "text": "Miloutte, the cat-eared adventurer, set out to save the world.", "particle_color": (255, 200, 50)},
    ]

    MIDGAME_SCENES = [
        {"duration": 4.0, "text": "The Forest Guardian has fallen...", "particle_color": (50, 180, 50)},
        {"duration": 4.0, "text": "But the corruption runs deeper than anyone knew.", "particle_color": (150, 50, 200)},
        {"duration": 4.0, "text": "An ancient tomb stirs beneath the desert sands...", "particle_color": (210, 180, 120)},
        {"duration": 4.0, "text": "Miloutte must journey south to stop the spreading evil.", "particle_color": (255, 200, 50)},
    ]

    ENDING_SCENES = [
        {"duration": 4.0, "text": "The Inferno Drake is slain!", "particle_color": (255, 120, 30)},
        {"duration": 4.0, "text": "The ancient seal is restored...", "particle_color": (255, 200, 50)},
        {"duration": 4.0, "text": "Peace returns to the land of Miloutte.", "particle_color": (100, 200, 100)},
        {"duration": 5.0, "text": "Thank you for playing!", "particle_color": (255, 200, 50)},
        {"duration": 4.0, "text": "Zelda Miloutte — A game by the Miloutte team", "particle_color": (255, 255, 255)},
    ]

    def __init__(self, game, cutscene_type="intro", on_complete=None):
        super().__init__(game)
        self._cutscene_type = cutscene_type
        self._on_complete = on_complete

        # Scene definitions
        if cutscene_type == "midgame":
            self.scenes = list(self.MIDGAME_SCENES)
        elif cutscene_type == "ending":
            self.scenes = list(self.ENDING_SCENES)
        else:
            self.scenes = list(self.INTRO_SCENES)

        self.current_scene = 0
        self.scene_timer = 0.0
        self.total_timer = 0.0

        # Typewriter text
        self.text_chars_revealed = 0.0
        self.chars_per_second = 25.0

        # Starfield
        self.stars = []
        for _ in range(80):
            self.stars.append((
                random.randint(0, SCREEN_WIDTH),
                random.randint(0, SCREEN_HEIGHT),
                random.randint(150, 255),
                random.uniform(1.0, 3.0),
            ))

        # Floating particles
        self.particles = []

        # Sprite caches (loaded lazily)
        self._player_surf = None
        self._player_right_frames = None
        self._boss_surf = None
        self._enemy_surfs = None
        self._archer_surfs = None
        self._sword_surf = None

        # Animation
        self.sprite_bob = 0.0
        self.walk_frame = 0
        self.walk_timer = 0.0

        # Scene fade
        self.scene_fade_alpha = 0  # 0 = fully visible, 255 = black
        self._fade_duration = 0.5

        # Fonts (lazy)
        self._font = None
        self._small_font = None

        # Enemy march positions (scene 3)
        self._enemy_positions = []
        for i in range(5):
            self._enemy_positions.append({
                "x": -60 - i * 80,
                "y": SCREEN_HEIGHT // 2 - 40 + random.randint(-20, 20),
                "is_archer": i >= 3,
            })

        # Player walk position (scene 5)
        self._player_x = SCREEN_WIDTH // 2 - 40

        # Skip fade
        self._skipping = False

    def enter(self):
        get_sound_manager().play_music('title')

    def _init_fonts(self):
        if self._font is None:
            self._font = pygame.font.Font(None, 36)
            self._small_font = pygame.font.Font(None, 24)

    def _get_player_surf(self):
        if self._player_surf is None:
            from ..sprites.player_sprites import get_player_frames
            frames = get_player_frames()
            base = frames["down"][0]
            w, h = base.get_size()
            self._player_surf = pygame.transform.scale(base, (w * 2, h * 2))
        return self._player_surf

    def _get_player_right_frames(self):
        if self._player_right_frames is None:
            from ..sprites.player_sprites import get_player_frames
            frames = get_player_frames()
            result = []
            for f in frames["right"]:
                w, h = f.get_size()
                result.append(pygame.transform.scale(f, (w * 2, h * 2)))
            self._player_right_frames = result
        return self._player_right_frames

    def _get_boss_surf(self):
        if self._boss_surf is None:
            from ..sprites.boss_sprites import get_boss_frames_phase1
            frames = get_boss_frames_phase1()
            base = frames["down"][0]
            w, h = base.get_size()
            self._boss_surf = pygame.transform.scale(base, (int(w * 1.5), int(h * 1.5)))
        return self._boss_surf

    def _get_enemy_surfs(self):
        if self._enemy_surfs is None:
            from ..sprites.enemy_sprites import get_enemy_frames
            frames = get_enemy_frames()
            result = []
            for f in frames["right"]:
                w, h = f.get_size()
                result.append(pygame.transform.scale(f, (w * 2, h * 2)))
            self._enemy_surfs = result
        return self._enemy_surfs

    def _get_archer_surfs(self):
        if self._archer_surfs is None:
            from ..sprites.archer_sprites import get_archer_frames
            frames = get_archer_frames()
            result = []
            for f in frames["right"]:
                w, h = f.get_size()
                result.append(pygame.transform.scale(f, (w * 2, h * 2)))
            self._archer_surfs = result
        return self._archer_surfs

    def _get_sword_surf(self):
        if self._sword_surf is None:
            from ..sprites.player_sprites import get_sword_surfaces
            swords = get_sword_surfaces()
            base = swords["right"]
            w, h = base.get_size()
            self._sword_surf = pygame.transform.scale(base, (w * 2, h * 2))
        return self._sword_surf

    def _go_to_title(self):
        if self._on_complete:
            self._on_complete()
        else:
            from .title_state import TitleState
            self.game.change_state(TitleState(self.game))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_SPACE):
            if not self._skipping:
                self._skipping = True
                self.game.transition_to(self._go_to_title)

    def _spawn_particles(self, dt):
        scene = self.scenes[self.current_scene]
        color = scene["particle_color"]
        # Spawn ~10 particles per second
        if random.random() < dt * 10:
            self.particles.append({
                "x": random.uniform(0, SCREEN_WIDTH),
                "y": random.uniform(SCREEN_HEIGHT * 0.3, SCREEN_HEIGHT * 0.7),
                "vx": random.uniform(-15, 15),
                "vy": random.uniform(-30, -10),
                "color": color,
                "life": random.uniform(1.5, 3.0),
                "max_life": 0.0,  # set below
                "size": random.uniform(1.5, 3.0),
            })
            self.particles[-1]["max_life"] = self.particles[-1]["life"]

    def _update_particles(self, dt):
        alive = []
        for p in self.particles:
            p["life"] -= dt
            if p["life"] > 0:
                p["x"] += p["vx"] * dt
                p["y"] += p["vy"] * dt
                alive.append(p)
        self.particles = alive

    def update(self, dt):
        if self._skipping:
            return

        self.total_timer += dt
        self.scene_timer += dt
        self.sprite_bob += dt

        # Walk animation timer
        self.walk_timer += dt
        if self.walk_timer >= 0.3:
            self.walk_timer = 0.0
            self.walk_frame = 1 - self.walk_frame

        # Typewriter text progress
        self.text_chars_revealed += self.chars_per_second * dt

        # Particles
        self._spawn_particles(dt)
        self._update_particles(dt)

        # Scene 3: move enemies
        if self.current_scene == 2:
            for e in self._enemy_positions:
                e["x"] += 60 * dt

        # Scene 5: player walks right
        if self.current_scene == 4:
            self._player_x += 40 * dt

        # Advance scene
        scene = self.scenes[self.current_scene]
        if self.scene_timer >= scene["duration"]:
            self.current_scene += 1
            if self.current_scene >= len(self.scenes):
                self.game.transition_to(self._go_to_title)
                self._skipping = True
                return
            self.scene_timer = 0.0
            self.text_chars_revealed = 0.0
            self.particles.clear()

    def _draw_starfield(self, surface):
        for x, y, brightness, speed in self.stars:
            b = brightness + math.sin(self.total_timer * speed) * 60
            b = max(0, min(255, int(b)))
            color = (b, b, b)
            size = 1 if brightness < 200 else 2
            pygame.draw.circle(surface, color, (x, y), size)

    def _draw_particles(self, surface):
        for p in self.particles:
            ratio = p["life"] / p["max_life"]
            alpha = int(200 * ratio)
            r, g, b = p["color"]
            # Draw as a simple colored circle (no alpha surface needed for small dots)
            c = (min(255, int(r * ratio + 80 * (1 - ratio))),
                 min(255, int(g * ratio + 80 * (1 - ratio))),
                 min(255, int(b * ratio + 80 * (1 - ratio))))
            sz = max(1, int(p["size"] * ratio))
            pygame.draw.circle(surface, c, (int(p["x"]), int(p["y"])), sz)

    def _draw_typewriter_text(self, surface, text, y=None):
        self._init_fonts()
        if y is None:
            y = SCREEN_HEIGHT * 3 // 4

        num_chars = int(self.text_chars_revealed)
        revealed = text[:num_chars]
        if not revealed:
            return

        # Shadow
        shadow = self._font.render(revealed, True, (40, 30, 10))
        sx = (SCREEN_WIDTH - shadow.get_width()) // 2
        surface.blit(shadow, (sx + 2, y + 2))

        # Main text
        txt = self._font.render(revealed, True, GOLD)
        tx = (SCREEN_WIDTH - txt.get_width()) // 2
        surface.blit(txt, (tx, y))

    def _draw_skip_hint(self, surface):
        self._init_fonts()
        hint = self._small_font.render("Press ENTER to skip", True, (120, 120, 120))
        surface.blit(hint, (SCREEN_WIDTH - hint.get_width() - 16, SCREEN_HEIGHT - 30))

    def _scene_progress(self):
        scene = self.scenes[self.current_scene]
        return min(1.0, self.scene_timer / scene["duration"])

    def _draw_scene_0(self, surface):
        """Black screen + text crawl with floating particles."""
        pass  # Just starfield + particles + text (handled by draw)

    def _draw_scene_1(self, surface):
        """The villain appears - boss sprite fades in."""
        progress = self._scene_progress()
        boss = self._get_boss_surf()

        # Fade in over first 1.5s
        alpha = min(255, int(255 * (self.scene_timer / 1.5)))

        # Pulsing scale
        pulse = 1.0 + 0.05 * math.sin(self.total_timer * 3)
        w = int(boss.get_width() * pulse)
        h = int(boss.get_height() * pulse)
        pulsed = pygame.transform.scale(boss, (w, h))

        # Apply alpha
        pulsed.set_alpha(alpha)

        bx = (SCREEN_WIDTH - w) // 2
        by = SCREEN_HEIGHT // 2 - h // 2 - 30 + int(math.sin(self.total_timer * 2) * 5)
        surface.blit(pulsed, (bx, by))

    def _draw_scene_2(self, surface):
        """Enemies marching across screen."""
        enemy_frames = self._get_enemy_surfs()
        archer_frames = self._get_archer_surfs()

        for e in self._enemy_positions:
            if e["is_archer"]:
                frames = archer_frames
            else:
                frames = enemy_frames
            frame = frames[self.walk_frame % len(frames)]
            bob = int(math.sin(self.total_timer * 4 + e["y"]) * 3)
            surface.blit(frame, (int(e["x"]), e["y"] + bob))

    def _draw_scene_3(self, surface):
        """The hero - player sprite fades in with sword flash."""
        progress = self._scene_progress()
        player = self._get_player_surf()

        # Fade in
        alpha = min(255, int(255 * (self.scene_timer / 1.5)))
        player_copy = player.copy()
        player_copy.set_alpha(alpha)

        px = SCREEN_WIDTH // 2 - player.get_width() // 2
        bob = int(math.sin(self.total_timer * 2) * 4)
        py = SCREEN_HEIGHT // 2 - player.get_height() // 2 - 20 + bob
        surface.blit(player_copy, (px, py))

        # Sword flash effect (appears after 1.5s for 0.5s)
        if 1.5 < self.scene_timer < 2.5:
            sword = self._get_sword_surf()
            flash_alpha = int(255 * (1.0 - abs(self.scene_timer - 2.0) / 0.5))
            flash_alpha = max(0, min(255, flash_alpha))
            sword_copy = sword.copy()
            sword_copy.set_alpha(flash_alpha)
            sx = px + player.get_width()
            sy = py + player.get_height() // 2 - sword.get_height() // 2
            surface.blit(sword_copy, (sx, sy))

    def _draw_scene_4(self, surface):
        """Player walks right toward edge."""
        frames = self._get_player_right_frames()
        frame = frames[self.walk_frame % len(frames)]

        # Fade to black near the end
        px = int(self._player_x)
        bob = int(math.sin(self.total_timer * 4) * 2)
        py = SCREEN_HEIGHT // 2 - frame.get_height() // 2 - 10 + bob
        surface.blit(frame, (px, py))

    def draw(self, surface):
        self._init_fonts()

        # Dark background
        surface.fill((5, 5, 15))

        # Starfield always visible
        self._draw_starfield(surface)

        if self.current_scene >= len(self.scenes):
            return

        # Scene-specific drawing
        scene_drawers = [
            self._draw_scene_0,
            self._draw_scene_1,
            self._draw_scene_2,
            self._draw_scene_3,
            self._draw_scene_4,
        ]
        scene_drawers[self.current_scene](surface)

        # Particles on top of scene
        self._draw_particles(surface)

        # Typewriter text
        scene = self.scenes[self.current_scene]
        self._draw_typewriter_text(surface, scene["text"])

        # Scene fade in/out overlay
        fade_alpha = 0
        if self.scene_timer < self._fade_duration:
            # Fade in from black
            fade_alpha = int(255 * (1.0 - self.scene_timer / self._fade_duration))
        elif self.scene_timer > self.scenes[self.current_scene]["duration"] - self._fade_duration:
            # Fade out to black
            remaining = self.scenes[self.current_scene]["duration"] - self.scene_timer
            fade_alpha = int(255 * (1.0 - remaining / self._fade_duration))

        if fade_alpha > 0:
            fade_alpha = max(0, min(255, fade_alpha))
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.fill(BLACK)
            overlay.set_alpha(fade_alpha)
            surface.blit(overlay, (0, 0))

        # Skip hint
        self._draw_skip_hint(surface)
