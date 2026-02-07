import pygame
from zelda_miloutte.entities.entity import Entity
from zelda_miloutte.settings import (
    PLAYER_SIZE, PLAYER_SPEED, PLAYER_MAX_HP, PLAYER_INVINCIBILITY_TIME,
    PLAYER_BLINK_RATE, GOLD, SWORD_LENGTH, SWORD_WIDTH, SWORD_DURATION,
    SWORD_COOLDOWN, SWORD_DAMAGE, WHITE, TILE_SIZE,
    XP_BASE, XP_EXPONENT, LEVEL_HP_INTERVAL, LEVEL_ATTACK_INTERVAL, LEVEL_DEFENSE_INTERVAL,
    PLAYER_MAX_MP, PLAYER_MP_REGEN,
)
from zelda_miloutte.sounds import get_sound_manager
from zelda_miloutte.sprites import AnimatedSprite
from zelda_miloutte.sprites.player_sprites import get_player_frames, get_sword_surfaces
from zelda_miloutte.data.inventory import Inventory


class Player(Entity):
    def __init__(self, x, y):
        # Collision rect is slightly smaller than tile for comfort
        super().__init__(x, y, PLAYER_SIZE, PLAYER_SIZE, GOLD)
        self.hp = PLAYER_MAX_HP
        self.max_hp = PLAYER_MAX_HP
        self.speed = PLAYER_SPEED
        self.keys = 0
        self.gold = 0

        # Inventory
        self.inventory = Inventory()

        # Mana
        self.mp = PLAYER_MAX_MP
        self.max_mp = PLAYER_MAX_MP

        # Abilities
        self.abilities = []            # list of Ability instances
        self.active_ability_index = 0  # index into self.abilities
        self.unlocked_abilities = []   # list of ability name strings

        # RPG Stats
        self.level = 1
        self.xp = 0
        self.xp_to_next = XP_BASE
        self.base_attack = 0
        self.base_defense = 0

        # Status effects
        self.status_effects = {}

        # Invincibility
        self.invincible = False
        self.invincible_timer = 0.0
        self.blink_timer = 0.0
        self.visible = True

        # Sword
        self.attacking = False
        self.attack_timer = 0.0
        self.attack_cooldown = 0.0
        self.sword_rect = None

        # Sprites
        self.anim = AnimatedSprite(get_player_frames(), frame_duration=0.15)
        self.sword_surfaces = get_sword_surfaces()

    @property
    def attack_power(self):
        equip_atk = self.inventory.get_stat_bonus("attack")
        return SWORD_DAMAGE + self.base_attack + equip_atk

    @property
    def active_ability(self):
        """Return the currently selected ability, or None if no abilities."""
        if not self.abilities:
            return None
        idx = self.active_ability_index % len(self.abilities)
        return self.abilities[idx]

    def cycle_ability(self):
        """Cycle to the next ability. Returns the new active ability or None."""
        if not self.abilities:
            return None
        self.active_ability_index = (self.active_ability_index + 1) % len(self.abilities)
        return self.active_ability

    def unlock_ability(self, ability_name):
        """Unlock an ability by name. Returns True if newly unlocked."""
        if ability_name in self.unlocked_abilities:
            return False
        from zelda_miloutte.abilities import create_ability
        ability = create_ability(ability_name)
        if ability is None:
            return False
        self.unlocked_abilities.append(ability_name)
        self.abilities.append(ability)
        return True

    def take_damage(self, amount):
        if self.invincible:
            return False
        equip_def = self.inventory.get_stat_bonus("defense")
        effective = max(1, amount - self.base_defense - equip_def)
        self.hp -= effective
        get_sound_manager().play_player_hurt()
        if self.hp <= 0:
            self.hp = 0
            self.alive = False
        else:
            self.invincible = True
            self.invincible_timer = PLAYER_INVINCIBILITY_TIME
        return True

    def heal(self, amount):
        self.hp = min(self.hp + amount, self.max_hp)

    def gain_xp(self, amount):
        """Add XP and check for level ups. Returns True if leveled up."""
        self.xp += amount
        leveled = False
        while self.xp >= self.xp_to_next:
            self.xp -= self.xp_to_next
            self.level += 1
            self.xp_to_next = int(XP_BASE * (self.level ** XP_EXPONENT))
            # Stat bonuses
            if self.level % LEVEL_HP_INTERVAL == 0:
                self.max_hp += 2
                self.hp = min(self.hp + 2, self.max_hp)
            if self.level % LEVEL_ATTACK_INTERVAL == 0:
                self.base_attack += 1
            if self.level % LEVEL_DEFENSE_INTERVAL == 0:
                self.base_defense += 1
            leveled = True
        return leveled

    def update_statuses(self, dt):
        """Update active status effects."""
        expired = []
        for name, effect in self.status_effects.items():
            effect["timer"] -= dt
            if effect["timer"] <= 0:
                expired.append(name)
            elif name == "poison":
                effect["tick_timer"] -= dt
                if effect["tick_timer"] <= 0:
                    effect["tick_timer"] += effect.get("tick_interval", 2.0)
                    # Poison damage bypasses defense and invincibility
                    self.hp -= effect.get("damage", 1)
                    if self.hp <= 0:
                        self.hp = 0
                        self.alive = False
        for name in expired:
            del self.status_effects[name]

    def apply_status(self, name, duration, params=None):
        """Apply a status effect."""
        effect = {"timer": duration}
        if params:
            effect.update(params)
        if name == "poison":
            effect.setdefault("tick_timer", 2.0)
            effect.setdefault("tick_interval", 2.0)
            effect.setdefault("damage", 1)
        elif name == "slow":
            effect.setdefault("multiplier", 0.5)
        self.status_effects[name] = effect

    def start_attack(self):
        if self.attacking or self.attack_cooldown > 0:
            return
        self.attacking = True
        self.attack_timer = SWORD_DURATION
        self._update_sword_rect()
        get_sound_manager().play_sword_swing()

    def _update_sword_rect(self):
        cx, cy = self.center_x, self.center_y
        if self.facing == "up":
            self.sword_rect = pygame.Rect(
                cx - SWORD_WIDTH // 2, self.y - SWORD_LENGTH,
                SWORD_WIDTH, SWORD_LENGTH)
        elif self.facing == "down":
            self.sword_rect = pygame.Rect(
                cx - SWORD_WIDTH // 2, self.y + self.height,
                SWORD_WIDTH, SWORD_LENGTH)
        elif self.facing == "left":
            self.sword_rect = pygame.Rect(
                self.x - SWORD_LENGTH, cy - SWORD_WIDTH // 2,
                SWORD_LENGTH, SWORD_WIDTH)
        elif self.facing == "right":
            self.sword_rect = pygame.Rect(
                self.x + self.width, cy - SWORD_WIDTH // 2,
                SWORD_LENGTH, SWORD_WIDTH)

    def apply_input(self, input_handler, companion=None):
        # Skip normal movement input during knockback
        if self.knockback_timer > 0:
            self.vx = self.knockback_vx
            self.vy = self.knockback_vy
        else:
            speed = self.speed + self.inventory.get_stat_bonus("speed")
            # Apply companion speed bonus (Fox)
            if companion is not None:
                speed += speed * companion.get_perk_speed_bonus()
            # Apply slow status effect
            if "slow" in self.status_effects:
                speed *= self.status_effects["slow"].get("multiplier", 0.5)
            self.vx = input_handler.move_x * speed
            self.vy = input_handler.move_y * speed

            # Update facing based on movement
            if input_handler.move_x < 0:
                self.facing = "left"
            elif input_handler.move_x > 0:
                self.facing = "right"
            elif input_handler.move_y < 0:
                self.facing = "up"
            elif input_handler.move_y > 0:
                self.facing = "down"

        if input_handler.attack:
            self.start_attack()

    def update(self, dt):
        # Knockback
        self.update_knockback(dt)

        # Attack timer
        if self.attacking:
            self.attack_timer -= dt
            self._update_sword_rect()
            if self.attack_timer <= 0:
                self.attacking = False
                self.sword_rect = None
                self.attack_cooldown = SWORD_COOLDOWN

        if self.attack_cooldown > 0:
            self.attack_cooldown -= dt

        # Invincibility
        if self.invincible:
            self.invincible_timer -= dt
            # Don't blink if shield barrier is active
            shield_active = any(
                ab.name == "shield_barrier" and ab.active for ab in self.abilities
            )
            if not shield_active:
                self.blink_timer += dt
                if self.blink_timer >= PLAYER_BLINK_RATE:
                    self.blink_timer = 0
                    self.visible = not self.visible
            if self.invincible_timer <= 0:
                self.invincible = False
                self.visible = True

        # Mana regeneration (with companion bonus from Fairy)
        if self.mp < self.max_mp:
            regen = PLAYER_MP_REGEN
            # Apply Fairy MP regen bonus (pass via update)
            if hasattr(self, '_companion_mp_bonus'):
                regen *= (1.0 + self._companion_mp_bonus)
            self.mp = min(self.max_mp, self.mp + regen * dt)

        # Status effects
        self.update_statuses(dt)

        # Animation
        self.anim.update(dt, self.is_moving)

    def move_x(self, dt):
        self.x += self.vx * dt

    def move_y(self, dt):
        self.y += self.vy * dt

    def draw(self, surface, camera):
        if not self.visible:
            return
        ox, oy = -camera.x, -camera.y

        # Draw body sprite -- center the sprite surface on the collision rect
        frame = self.anim.get_frame(self.facing)
        body_rect = self.rect.move(ox, oy)
        fx = body_rect.centerx - frame.get_width() // 2
        fy = body_rect.centery - frame.get_height() // 2
        surface.blit(frame, (fx, fy))

        # Draw sword sprite
        if self.attacking and self.sword_rect:
            sword_surf = self.sword_surfaces[self.facing]
            sr = self.sword_rect.move(ox, oy)
            # Center the sword surface on the sword collision rect
            sx = sr.centerx - sword_surf.get_width() // 2
            sy = sr.centery - sword_surf.get_height() // 2
            surface.blit(sword_surf, (sx, sy))
