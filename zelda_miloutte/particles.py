import pygame
import random
import math
from .settings import WHITE, GOLD, BROWN, LIGHT_BROWN, BOSS_PURPLE, RED


class Particle:
    """A single particle with position, velocity, color, lifetime, and gravity support."""

    def __init__(self, x, y, vx, vy, color, lifetime, size, gravity=0):
        self.x = float(x)
        self.y = float(y)
        self.vx = float(vx)
        self.vy = float(vy)
        self.color = color
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.size = size
        self.gravity = gravity
        self.alive = True

    def update(self, dt):
        """Update particle position, apply gravity, and reduce lifetime."""
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.vy += self.gravity * dt
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.alive = False

    @property
    def alpha(self):
        """Calculate alpha based on remaining lifetime (fade out)."""
        return int(255 * (self.lifetime / self.max_lifetime))


class ParticleSystem:
    """Manages and renders a collection of particles."""

    def __init__(self):
        self.particles = []

    def emit(self, x, y, count, color, speed_range, lifetime_range, size_range, gravity=0):
        """
        Emit particles at a position with randomized properties.

        Args:
            x, y: Spawn position
            count: Number of particles to spawn
            color: RGB tuple or list of RGB tuples for random selection
            speed_range: (min, max) speed in pixels/sec
            lifetime_range: (min, max) lifetime in seconds
            size_range: (min, max) size in pixels
            gravity: Downward acceleration (pixels/sec^2)
        """
        for _ in range(count):
            # Random direction (360 degrees)
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(speed_range[0], speed_range[1])
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed

            # Random properties
            lifetime = random.uniform(lifetime_range[0], lifetime_range[1])
            size = random.uniform(size_range[0], size_range[1])

            # Handle color being a list of colors
            if isinstance(color[0], (list, tuple)):
                particle_color = random.choice(color)
            else:
                particle_color = color

            particle = Particle(x, y, vx, vy, particle_color, lifetime, size, gravity)
            self.particles.append(particle)

    def update(self, dt):
        """Update all particles and remove dead ones."""
        for particle in self.particles:
            particle.update(dt)
        self.particles = [p for p in self.particles if p.alive]

    def draw(self, surface, camera):
        """Draw all particles as small circles with alpha blending."""
        for particle in self.particles:
            # Calculate screen position
            screen_x = int(particle.x - camera.x)
            screen_y = int(particle.y - camera.y)

            # Create a temporary surface for alpha blending
            size = int(particle.size)
            if size < 1:
                size = 1

            # Create surface with alpha
            temp_surf = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
            color_with_alpha = (*particle.color, particle.alpha)
            pygame.draw.circle(temp_surf, color_with_alpha, (size, size), size)

            # Blit to main surface
            surface.blit(temp_surf, (screen_x - size, screen_y - size))

    # Convenience methods for specific effects

    def emit_directional(self, x, y, angle, spread, count, color, speed_range,
                         lifetime_range, size_range, gravity=0):
        """Emit particles in a directional cone.

        Args:
            x, y: Spawn position
            angle: Center angle in radians (0 = right, pi/2 = down)
            spread: Half-spread angle in radians
            count: Number of particles
            color: RGB tuple or list of RGB tuples
            speed_range: (min, max) speed
            lifetime_range: (min, max) lifetime
            size_range: (min, max) size
            gravity: Downward acceleration
        """
        for _ in range(count):
            a = angle + random.uniform(-spread, spread)
            speed = random.uniform(speed_range[0], speed_range[1])
            vx = math.cos(a) * speed
            vy = math.sin(a) * speed
            lifetime = random.uniform(lifetime_range[0], lifetime_range[1])
            size = random.uniform(size_range[0], size_range[1])
            if isinstance(color[0], (list, tuple)):
                particle_color = random.choice(color)
            else:
                particle_color = color
            self.particles.append(Particle(x, y, vx, vy, particle_color, lifetime, size, gravity))

    def emit_sword_sparks(self, x, y):
        """White/yellow sparks when sword hits enemy (fast, short-lived)."""
        colors = [WHITE, GOLD, (255, 255, 200)]
        self.emit(
            x, y,
            count=random.randint(6, 10),
            color=colors,
            speed_range=(120, 200),
            lifetime_range=(0.15, 0.3),
            size_range=(2, 4),
            gravity=0
        )

    def emit_directional_hit(self, x, y, source_x, source_y, count=7, color=None,
                             speed_range=(150, 250)):
        """Emit directional sparks away from the attack source.

        Args:
            x, y: Hit position (on the enemy)
            source_x, source_y: Position of the attacker
            count: Number of particles (5-8 typical)
            color: RGB tuple or list; defaults to white/yellow sword sparks
            speed_range: Speed range for particles
        """
        if color is None:
            color = [WHITE, GOLD, (255, 255, 200)]
        # Angle from source to hit point
        dx = x - source_x
        dy = y - source_y
        angle = math.atan2(dy, dx)
        self.emit_directional(
            x, y, angle, spread=0.5, count=count, color=color,
            speed_range=speed_range, lifetime_range=(0.12, 0.25),
            size_range=(2, 5), gravity=0
        )

    def emit_dust(self, x, y):
        """Brown/tan dust when player walks (slow, subtle)."""
        colors = [BROWN, LIGHT_BROWN, (160, 120, 80)]
        self.emit(
            x, y,
            count=random.randint(2, 3),
            color=colors,
            speed_range=(20, 40),
            lifetime_range=(0.3, 0.5),
            size_range=(1, 3),
            gravity=30
        )

    def emit_death_burst(self, x, y, color):
        """Explosion of particles when enemy dies."""
        self.emit(
            x, y,
            count=random.randint(15, 20),
            color=color,
            speed_range=(80, 150),
            lifetime_range=(0.4, 0.7),
            size_range=(2, 5),
            gravity=200
        )

    def emit_boss_death(self, x, y):
        """Big dramatic explosion when boss dies (multiple colors)."""
        colors = [BOSS_PURPLE, RED, WHITE, GOLD, (180, 50, 200)]
        self.emit(
            x, y,
            count=random.randint(30, 40),
            color=colors,
            speed_range=(100, 250),
            lifetime_range=(0.5, 1.0),
            size_range=(3, 7),
            gravity=150
        )

    def emit_sand_burst(self, x, y):
        """Emit sand burst particles for worm emerge/burrow."""
        self.emit(
            x, y,
            count=16,
            color=(210, 180, 120),
            speed_range=(60, 120),
            lifetime_range=(0.3, 0.6),
            size_range=(3, 6),
            gravity=100
        )

    def emit_fire_burst(self, x, y):
        """Emit fire burst particles for dragon attacks."""
        colors = [(255, 120, 30), (200, 80, 20), (255, 200, 50)]
        self.emit(
            x, y,
            count=random.randint(20, 25),
            color=colors,
            speed_range=(100, 200),
            lifetime_range=(0.3, 0.6),
            size_range=(3, 6),
            gravity=150
        )

    # ── Ambient particles ──────────────────────────────────────────

    def emit_ambient_grass(self, screen_w, screen_h, camera_x, camera_y):
        """Grass sway — green wisps that float upward (overworld)."""
        x = random.uniform(camera_x, camera_x + screen_w)
        y = random.uniform(camera_y + screen_h * 0.5, camera_y + screen_h)
        colors = [(100, 180, 60), (80, 160, 50), (120, 200, 70)]
        self.emit(x, y, count=1, color=colors,
                  speed_range=(8, 20), lifetime_range=(2.0, 3.5),
                  size_range=(1, 3), gravity=-5)

    def emit_ambient_spores(self, screen_w, screen_h, camera_x, camera_y):
        """Floating spores — glowing dots that drift slowly (forest)."""
        x = random.uniform(camera_x, camera_x + screen_w)
        y = random.uniform(camera_y, camera_y + screen_h)
        colors = [(120, 220, 100), (180, 255, 120), (80, 180, 60)]
        self.emit(x, y, count=1, color=colors,
                  speed_range=(5, 15), lifetime_range=(3.0, 5.0),
                  size_range=(1, 3), gravity=-3)

    def emit_ambient_sand(self, screen_w, screen_h, camera_x, camera_y):
        """Sand wind — tan particles blowing rightward (desert)."""
        x = random.uniform(camera_x - 20, camera_x + screen_w * 0.3)
        y = random.uniform(camera_y, camera_y + screen_h)
        self.particles.append(Particle(
            x, y,
            random.uniform(40, 80), random.uniform(-5, 5),
            (210, 180, 120), random.uniform(2.0, 4.0),
            random.uniform(1, 2), gravity=0
        ))

    def emit_ambient_embers(self, screen_w, screen_h, camera_x, camera_y):
        """Floating embers — orange dots rising (volcano)."""
        x = random.uniform(camera_x, camera_x + screen_w)
        y = random.uniform(camera_y + screen_h * 0.3, camera_y + screen_h)
        colors = [(255, 120, 30), (255, 80, 20), (255, 200, 50)]
        self.emit(x, y, count=1, color=colors,
                  speed_range=(10, 30), lifetime_range=(2.0, 4.0),
                  size_range=(1, 3), gravity=-15)

    # ── Enhanced effects ───────────────────────────────────────────

    def emit_death_burst_dramatic(self, x, y, color):
        """More dramatic enemy death burst with extra particles."""
        self.emit(x, y, count=random.randint(20, 30), color=color,
                  speed_range=(100, 200), lifetime_range=(0.4, 0.8),
                  size_range=(2, 6), gravity=200)
        # Add white flash particles
        self.emit(x, y, count=5, color=(255, 255, 255),
                  speed_range=(60, 100), lifetime_range=(0.1, 0.2),
                  size_range=(4, 8), gravity=0)

    def emit_levelup_burst(self, x, y):
        """Golden particle explosion on level up."""
        colors = [(255, 200, 50), (255, 220, 100), (255, 180, 30), (255, 255, 150)]
        self.emit(x, y, count=random.randint(25, 35), color=colors,
                  speed_range=(80, 180), lifetime_range=(0.5, 1.0),
                  size_range=(2, 5), gravity=-30)

    def emit_item_glow(self, x, y):
        """Subtle glow particles around pickups."""
        colors = [(255, 255, 200), (255, 220, 100)]
        self.emit(x, y, count=1, color=colors,
                  speed_range=(5, 15), lifetime_range=(0.5, 1.0),
                  size_range=(1, 3), gravity=-10)

    def emit_fairy_sparkle(self, x, y):
        """Small sparkle trail behind fairy companion."""
        colors = [(150, 220, 255), (200, 240, 255), (255, 255, 255)]
        self.emit(x, y, count=1, color=colors,
                  speed_range=(5, 20), lifetime_range=(0.3, 0.7),
                  size_range=(1, 2), gravity=-8)

    def emit_companion_happy(self, x, y):
        """Heart/sparkle burst when petting companion."""
        colors = [(255, 100, 120), (255, 150, 170), (255, 200, 210)]
        self.emit(x, y, count=8, color=colors,
                  speed_range=(30, 60), lifetime_range=(0.4, 0.8),
                  size_range=(2, 4), gravity=-20)
