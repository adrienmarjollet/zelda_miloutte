import pygame
from .entity import Entity
from ..settings import (
    PLAYER_SIZE, PLAYER_SPEED, PLAYER_MAX_HP, PLAYER_INVINCIBILITY_TIME,
    PLAYER_BLINK_RATE, GOLD, SWORD_LENGTH, SWORD_WIDTH, SWORD_DURATION,
    SWORD_COOLDOWN, SWORD_DAMAGE, WHITE, TILE_SIZE,
    XP_BASE, XP_EXPONENT, LEVEL_HP_INTERVAL, LEVEL_ATTACK_INTERVAL, LEVEL_DEFENSE_INTERVAL,
    PLAYER_MAX_MP, PLAYER_MP_REGEN,
    COMBO_WINDOW, COMBO_HIT2_DAMAGE_MULT, COMBO_HIT3_DAMAGE_MULT,
    COMBO_HIT3_KNOCKBACK_MULT, COMBO_HIT2_DURATION_MULT, COMBO_HIT3_WIDTH_MULT,
    CHARGE_ATTACK_TIME, CHARGE_ATTACK_DAMAGE_MULT, CHARGE_ATTACK_RADIUS,
    DODGE_ROLL_SPEED, DODGE_ROLL_DURATION, DODGE_ROLL_COOLDOWN,
    PARRY_WINDOW, PARRY_STUN_DURATION,
    STAMINA_MAX, STAMINA_REGEN_RATE, STAMINA_DODGE_COST,
)
from ..sounds import get_sound_manager
from ..sprites import AnimatedSprite
from ..sprites.player_sprites import get_player_frames, get_sword_surfaces
from ..data.inventory import Inventory


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

        # Stamina
        self.stamina = STAMINA_MAX
        self.max_stamina = STAMINA_MAX

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

        # Combo system
        self.combo_count = 0       # 0=first hit, 1=second, 2=third
        self.combo_timer = 0.0     # time left to chain next hit

        # Dodge roll
        self.dodge_rolling = False
        self.dodge_roll_timer = 0.0
        self.dodge_roll_cooldown = 0.0
        self.dodge_roll_dx = 0.0
        self.dodge_roll_dy = 0.0

        # Parry
        self.parry_window_timer = 0.0  # active parry window (first frames of attack)
        self.parried_successfully = False

        # Charged attack
        self.charge_hold_time = 0.0   # how long Space has been held
        self.charged = False          # True when fully charged (visual cue)
        self.charge_attacking = False # True during the spin release
        self.charge_attack_timer = 0.0
        self.charge_attack_rect = None  # AoE circle approximated as rect

        # Sprites
        self.anim = AnimatedSprite(get_player_frames(), frame_duration=0.15)
        self.sword_surfaces = get_sword_surfaces()

    @property
    def weapon_type(self):
        """Return weapon type from equipped weapon: 'sword', 'spear', or 'axe'."""
        weapon = self.inventory.get_equipped("weapon")
        if weapon is not None:
            return weapon.stats.get("weapon_type", "sword")
        return "sword"

    @property
    def attack_power(self):
        equip_atk = self.inventory.get_stat_bonus("attack")
        base = SWORD_DAMAGE + self.base_attack + equip_atk
        # Combo damage multiplier
        if self.combo_count == 1:
            return max(1, int(base * COMBO_HIT2_DAMAGE_MULT))
        elif self.combo_count == 2:
            return max(1, int(base * COMBO_HIT3_DAMAGE_MULT))
        return base

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
        from ..abilities import create_ability
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
        # Burn increases damage taken
        if "burn" in self.status_effects:
            mult = self.status_effects["burn"].get("damage_mult", 1.25)
            effective = max(1, int(effective * mult))
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
                    self.hp -= effect.get("damage", 1)
                    if self.hp <= 0:
                        self.hp = 0
                        self.alive = False
            elif name == "burn":
                effect["tick_timer"] -= dt
                if effect["tick_timer"] <= 0:
                    effect["tick_timer"] += effect.get("tick_interval", 1.0)
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
        elif name == "freeze":
            effect.setdefault("duration", duration)
        elif name == "burn":
            effect.setdefault("tick_timer", 1.0)
            effect.setdefault("tick_interval", 1.0)
            effect.setdefault("damage", 1)
            effect.setdefault("damage_mult", 1.25)  # take 25% more damage while burning
        elif name == "stun":
            pass  # just a timer — player can't move
        self.status_effects[name] = effect

    def start_attack(self):
        if self.attacking or self.attack_cooldown > 0:
            return
        # Stamina cost varies by weapon type
        wtype = self.weapon_type
        attack_cost = 10.0
        if wtype == "axe":
            attack_cost = 15.0
        if self.stamina < attack_cost:
            return
        self.stamina -= attack_cost
        # Combo chaining: if within combo window, advance combo
        if self.combo_timer > 0 and self.combo_count < 2:
            self.combo_count += 1
        elif self.combo_timer <= 0:
            self.combo_count = 0

        # Determine swing duration based on combo hit and weapon type
        duration = SWORD_DURATION
        if wtype == "spear":
            duration *= 1.15  # slightly slower thrust
        elif wtype == "axe":
            duration *= 1.4   # heavy swing
        if self.combo_count == 1:
            duration *= COMBO_HIT2_DURATION_MULT  # faster jab
        elif self.combo_count == 2:
            duration *= 1.1  # slightly longer for heavy finisher

        self.attacking = True
        self.attack_timer = duration
        self.combo_timer = 0.0  # reset until this swing finishes
        self.parry_window_timer = PARRY_WINDOW  # parry active in first frames
        self.parried_successfully = False
        self._update_sword_rect()
        get_sound_manager().play_sword_swing()

    def _update_sword_rect(self):
        cx, cy = self.center_x, self.center_y
        sw = SWORD_WIDTH
        sl = SWORD_LENGTH
        # Adjust dimensions by weapon type
        wtype = self.weapon_type
        if wtype == "spear":
            sl = int(SWORD_LENGTH * 1.5)  # longer reach
            sw = int(SWORD_WIDTH * 0.6)   # narrower
        elif wtype == "axe":
            sl = int(SWORD_LENGTH * 0.8)  # shorter reach
            sw = int(SWORD_WIDTH * 1.6)   # wider cleave
        # Widen the 3rd combo hit
        if self.combo_count == 2:
            sw = int(sw * COMBO_HIT3_WIDTH_MULT)
        if self.facing == "up":
            self.sword_rect = pygame.Rect(
                cx - sw // 2, self.y - sl, sw, sl)
        elif self.facing == "down":
            self.sword_rect = pygame.Rect(
                cx - sw // 2, self.y + self.height, sw, sl)
        elif self.facing == "left":
            self.sword_rect = pygame.Rect(
                self.x - sl, cy - sw // 2, sl, sw)
        elif self.facing == "right":
            self.sword_rect = pygame.Rect(
                self.x + self.width, cy - sw // 2, sl, sw)

    def _start_charge_attack(self):
        """Start the charged spin attack (AoE around player)."""
        charge_cost = 30.0
        if self.stamina < charge_cost:
            return
        self.stamina -= charge_cost
        self.charge_attacking = True
        self.charge_attack_timer = 0.35  # spin duration
        self.charge_hit_enemies = set()  # track who was hit this spin
        r = CHARGE_ATTACK_RADIUS
        self.charge_attack_rect = pygame.Rect(
            self.center_x - r, self.center_y - r, r * 2, r * 2)
        self.combo_count = 0
        self.combo_timer = 0.0
        get_sound_manager().play_sword_swing()

    @property
    def charge_attack_damage(self):
        equip_atk = self.inventory.get_stat_bonus("attack")
        base = SWORD_DAMAGE + self.base_attack + equip_atk
        return max(1, int(base * CHARGE_ATTACK_DAMAGE_MULT))

    def start_dodge_roll(self, direction):
        """Start a dodge roll in the given direction."""
        if self.dodge_rolling or self.dodge_roll_cooldown > 0:
            return
        if self.stamina < STAMINA_DODGE_COST:
            return
        self.stamina -= STAMINA_DODGE_COST
        self.dodge_rolling = True
        self.dodge_roll_timer = DODGE_ROLL_DURATION
        self.invincible = True
        self.invincible_timer = DODGE_ROLL_DURATION
        # Set roll direction
        dirs = {
            "left": (-1, 0), "right": (1, 0),
            "up": (0, -1), "down": (0, 1),
        }
        dx, dy = dirs.get(direction, (0, 0))
        self.dodge_roll_dx = dx * DODGE_ROLL_SPEED
        self.dodge_roll_dy = dy * DODGE_ROLL_SPEED

    def apply_input(self, input_handler, companion=None):
        # Dodge roll input (double-tap direction)
        if input_handler.dodge_direction and not self.dodge_rolling:
            self.start_dodge_roll(input_handler.dodge_direction)

        # Frozen or stunned: can't move or attack
        if "freeze" in self.status_effects or "stun" in self.status_effects:
            self.vx = 0
            self.vy = 0
            return

        # Skip normal movement input during dodge roll
        if self.dodge_rolling:
            self.vx = self.dodge_roll_dx
            self.vy = self.dodge_roll_dy
            return

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

        # Charged attack: hold Space to charge, release to spin
        if input_handler.attack_held and not self.attacking and not self.charge_attacking:
            self.charge_hold_time += 1.0 / 60.0  # approximate per-frame
            if self.charge_hold_time >= CHARGE_ATTACK_TIME:
                self.charged = True
        else:
            if not input_handler.attack_held and self.charge_hold_time > 0:
                if self.charged:
                    # Release charged attack
                    self._start_charge_attack()
                    self.charge_hold_time = 0.0
                    self.charged = False
                else:
                    self.charge_hold_time = 0.0

        if input_handler.attack and not self.charged:
            self.start_attack()

    def update(self, dt):
        # Knockback
        self.update_knockback(dt)

        # Dodge roll update
        if self.dodge_rolling:
            self.dodge_roll_timer -= dt
            if self.dodge_roll_timer <= 0:
                self.dodge_rolling = False
                self.dodge_roll_cooldown = DODGE_ROLL_COOLDOWN
                self.vx = 0
                self.vy = 0
        if self.dodge_roll_cooldown > 0:
            self.dodge_roll_cooldown -= dt

        # Parry window countdown
        if self.parry_window_timer > 0:
            self.parry_window_timer -= dt

        # Combo window countdown
        if self.combo_timer > 0:
            self.combo_timer -= dt
            if self.combo_timer <= 0:
                self.combo_count = 0  # combo expired

        # Attack timer
        if self.attacking:
            self.attack_timer -= dt
            self._update_sword_rect()
            if self.attack_timer <= 0:
                self.attacking = False
                self.sword_rect = None
                # Open combo window for chaining
                if self.combo_count < 2:
                    self.combo_timer = COMBO_WINDOW
                    self.attack_cooldown = 0.05  # tiny cooldown between combo hits
                else:
                    # Combo finished (3rd hit done), full cooldown
                    self.combo_timer = 0.0
                    self.combo_count = 0
                    self.attack_cooldown = SWORD_COOLDOWN * 1.3  # longer recovery after full combo

        if self.attack_cooldown > 0:
            self.attack_cooldown -= dt

        # Charged spin attack timer
        if self.charge_attacking:
            self.charge_attack_timer -= dt
            # Update AoE rect to follow player
            r = CHARGE_ATTACK_RADIUS
            self.charge_attack_rect = pygame.Rect(
                self.center_x - r, self.center_y - r, r * 2, r * 2)
            if self.charge_attack_timer <= 0:
                self.charge_attacking = False
                self.charge_attack_rect = None
                self.attack_cooldown = SWORD_COOLDOWN * 1.5

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

        # Stamina regeneration (regens when not attacking or dodging)
        if self.stamina < self.max_stamina and not self.attacking and not self.dodge_rolling:
            self.stamina = min(self.max_stamina, self.stamina + STAMINA_REGEN_RATE * dt)

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
        # Dodge roll: semi-transparent with blue tint
        if self.dodge_rolling:
            roll_frame = frame.copy()
            roll_frame.set_alpha(140)
            blue_tint = pygame.Surface(roll_frame.get_size(), pygame.SRCALPHA)
            blue_tint.fill((100, 150, 255, 40))
            roll_frame.blit(blue_tint, (0, 0))
            surface.blit(roll_frame, (fx, fy))
        elif "freeze" in self.status_effects:
            # Frozen: blue tint overlay
            frozen_frame = frame.copy()
            ice_overlay = pygame.Surface(frozen_frame.get_size(), pygame.SRCALPHA)
            ice_overlay.fill((100, 180, 255, 80))
            frozen_frame.blit(ice_overlay, (0, 0))
            surface.blit(frozen_frame, (fx, fy))
        elif "burn" in self.status_effects:
            # Burning: orange/red flickering tint
            import math as _m
            pulse = abs(_m.sin(pygame.time.get_ticks() * 0.01))
            burn_frame = frame.copy()
            fire_overlay = pygame.Surface(burn_frame.get_size(), pygame.SRCALPHA)
            fire_overlay.fill((255, 100, 30, int(60 * pulse)))
            burn_frame.blit(fire_overlay, (0, 0))
            surface.blit(burn_frame, (fx, fy))
        else:
            surface.blit(frame, (fx, fy))

        # Draw charge glow when charging
        if self.charge_hold_time > 0 and not self.charge_attacking:
            progress = min(1.0, self.charge_hold_time / CHARGE_ATTACK_TIME)
            glow_r = int(10 + 30 * progress)
            glow_alpha = int(60 + 120 * progress)
            glow_color = (255, 255, 100) if self.charged else (200, 200, 80)
            glow_surf = pygame.Surface((glow_r * 2, glow_r * 2), pygame.SRCALPHA)
            pygame.draw.circle(glow_surf, (*glow_color, glow_alpha), (glow_r, glow_r), glow_r)
            gx = body_rect.centerx - glow_r
            gy = body_rect.centery - glow_r
            surface.blit(glow_surf, (gx, gy))

        # Draw charge spin attack visual
        if self.charge_attacking and self.charge_attack_rect:
            spin_r = CHARGE_ATTACK_RADIUS
            spin_surf = pygame.Surface((spin_r * 2, spin_r * 2), pygame.SRCALPHA)
            alpha = int(120 * (self.charge_attack_timer / 0.35))
            pygame.draw.circle(spin_surf, (255, 255, 150, alpha), (spin_r, spin_r), spin_r, 3)
            pygame.draw.circle(spin_surf, (255, 200, 50, alpha // 2), (spin_r, spin_r), spin_r)
            sx = body_rect.centerx - spin_r
            sy = body_rect.centery - spin_r
            surface.blit(spin_surf, (sx, sy))

        # Draw sword sprite
        if self.attacking and self.sword_rect:
            sword_surf = self.sword_surfaces[self.facing]
            sr = self.sword_rect.move(ox, oy)
            # Center the sword surface on the sword collision rect
            sx = sr.centerx - sword_surf.get_width() // 2
            sy = sr.centery - sword_surf.get_height() // 2
            surface.blit(sword_surf, (sx, sy))
