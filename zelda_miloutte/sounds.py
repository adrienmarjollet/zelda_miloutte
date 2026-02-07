import pygame
import math
import array


class SoundManager:
    """
    Manages programmatically generated sound effects for the game.
    Uses pygame.mixer to create simple synth sounds without external audio files.
    """

    def __init__(self):
        self.sounds_enabled = True
        self.sample_rate = 22050
        self.sounds = {}
        self._music_tracks = {}
        self._music_channel = None
        self._current_track = None
        self._music_volume = 0.2

        try:
            # Check if mixer is initialized
            if not pygame.mixer.get_init():
                pygame.mixer.init(frequency=self.sample_rate, size=-16, channels=1, buffer=512)

            # Reserve a channel for music
            pygame.mixer.set_num_channels(8)
            self._music_channel = pygame.mixer.Channel(7)  # Use last channel for music

            # Generate all sounds
            self._generate_sounds()
            # Generate all music tracks
            self._generate_music()
        except Exception as e:
            print(f"Warning: Could not initialize sound system: {e}")
            self.sounds_enabled = False

    def _generate_sounds(self):
        """Generate all game sounds and cache them."""
        self.sounds['sword_swing'] = self._make_sword_swing()
        self.sounds['enemy_hit'] = self._make_enemy_hit()
        self.sounds['enemy_death'] = self._make_enemy_death()
        self.sounds['player_hurt'] = self._make_player_hurt()
        self.sounds['heart_pickup'] = self._make_heart_pickup()
        self.sounds['key_pickup'] = self._make_key_pickup()
        self.sounds['boss_roar'] = self._make_boss_roar()
        self.sounds['boss_death'] = self._make_boss_death()
        self.sounds['dungeon_enter'] = self._make_dungeon_enter()
        self.sounds['chest_open'] = self._make_chest_open()
        self.sounds['victory_fanfare'] = self._make_victory_fanfare()
        self.sounds['gold_pickup'] = self._make_gold_pickup()
        self.sounds['push_block'] = self._make_push_block()
        self.sounds['switch_click'] = self._make_switch_click()
        self.sounds['torch_ignite'] = self._make_torch_ignite()
        self.sounds['door_open'] = self._make_door_open()
        self.sounds['ability_spin'] = self._make_ability_spin()
        self.sounds['ability_dash'] = self._make_ability_dash()
        self.sounds['room_clear'] = self._make_room_clear()
        self.sounds['door_lock'] = self._make_door_lock()
        self.sounds['parry_clang'] = self._make_parry_clang()
        self.sounds['dodge_whoosh'] = self._make_dodge_whoosh()
        self.sounds['charge_hum'] = self._make_charge_hum()
        self.sounds['combo_hit_1'] = self._make_combo_hit(1)
        self.sounds['combo_hit_2'] = self._make_combo_hit(2)
        self.sounds['combo_hit_3'] = self._make_combo_hit(3)
        self.sounds['shield_block'] = self._make_shield_block()
        self.sounds['ability_fire'] = self._make_ability_fire()
        self.sounds['ability_shield'] = self._make_ability_shield()
        self.sounds['ability_fail'] = self._make_ability_fail()
        self.sounds['thunder'] = self._make_thunder()
        self.sounds['rain_ambient'] = self._make_rain_ambient()
        self.sounds['wind_howl'] = self._make_wind_howl()
        self.sounds['fire_crackle'] = self._make_fire_crackle()

    def _generate_music(self):
        """Generate all music tracks and cache them."""
        self._music_tracks['title'] = self._generate_title_music()
        self._music_tracks['overworld'] = self._generate_overworld_music()
        self._music_tracks['dungeon'] = self._generate_dungeon_music()
        self._music_tracks['forest'] = self._generate_forest_music()
        self._music_tracks['desert'] = self._generate_desert_music()
        self._music_tracks['volcano'] = self._generate_volcano_music()
        self._music_tracks['boss'] = self._generate_boss_music()

    def _make_sound(self, duration, generator_func):
        """
        Create a pygame Sound from a generator function.

        Args:
            duration: Sound duration in seconds
            generator_func: Function that takes (t, sample_rate) and returns amplitude [-1, 1]

        Returns:
            pygame.mixer.Sound object
        """
        num_samples = int(duration * self.sample_rate)
        samples = array.array('h', [0] * num_samples)

        for i in range(num_samples):
            t = i / self.sample_rate
            amplitude = generator_func(t, self.sample_rate)
            # Clamp and convert to 16-bit signed integer
            amplitude = max(-1.0, min(1.0, amplitude))
            samples[i] = int(amplitude * 32767)

        sound = pygame.mixer.Sound(buffer=samples)
        return sound

    def _envelope(self, t, duration, attack=0.01, decay=0.05, sustain=0.7, release=0.1):
        """
        ADSR envelope for shaping sound amplitude.

        Args:
            t: Current time in seconds
            duration: Total duration
            attack: Attack time (0 to peak)
            decay: Decay time (peak to sustain)
            sustain: Sustain level (0-1)
            release: Release time (sustain to 0)

        Returns:
            Envelope value (0-1)
        """
        if t < attack:
            return t / attack
        elif t < attack + decay:
            return 1.0 - ((1.0 - sustain) * (t - attack) / decay)
        elif t < duration - release:
            return sustain
        else:
            return sustain * (duration - t) / release

    def _make_sword_swing(self):
        """Short whoosh sound - white noise burst with quick fade."""
        duration = 0.15

        def generator(t, sr):
            # White noise
            import random
            noise = random.random() * 2 - 1
            # Quick envelope
            env = self._envelope(t, duration, attack=0.01, decay=0.02, sustain=0.3, release=0.08)
            # High-pass filter effect (emphasize higher frequencies)
            return noise * env * 0.3

        sound = self._make_sound(duration, generator)
        sound.set_volume(0.4)
        return sound

    def _make_enemy_hit(self):
        """Thud/impact sound - low frequency burst."""
        duration = 0.12

        def generator(t, sr):
            # Low frequency tone (100-200 Hz sweep down)
            freq = 200 - (t / duration) * 100
            tone = math.sin(2 * math.pi * freq * t)
            # Sharp envelope
            env = self._envelope(t, duration, attack=0.005, decay=0.03, sustain=0.2, release=0.08)
            return tone * env * 0.6

        sound = self._make_sound(duration, generator)
        sound.set_volume(0.4)
        return sound

    def _make_enemy_death(self):
        """Descending tone for enemy death."""
        duration = 0.4

        def generator(t, sr):
            # Descending frequency (300 Hz to 80 Hz)
            freq = 300 - (t / duration) * 220
            tone = math.sin(2 * math.pi * freq * t)
            # Fade out envelope
            env = self._envelope(t, duration, attack=0.01, decay=0.1, sustain=0.5, release=0.2)
            return tone * env * 0.5

        sound = self._make_sound(duration, generator)
        sound.set_volume(0.35)
        return sound

    def _make_player_hurt(self):
        """Short buzz/pain sound - harsh dissonant tone."""
        duration = 0.2

        def generator(t, sr):
            # Two dissonant frequencies
            freq1 = 220
            freq2 = 235
            tone = (math.sin(2 * math.pi * freq1 * t) +
                   math.sin(2 * math.pi * freq2 * t)) / 2
            # Sharp attack and decay
            env = self._envelope(t, duration, attack=0.01, decay=0.05, sustain=0.3, release=0.1)
            return tone * env * 0.6

        sound = self._make_sound(duration, generator)
        sound.set_volume(0.4)
        return sound

    def _make_heart_pickup(self):
        """Ascending happy tone - healing sound."""
        duration = 0.3

        def generator(t, sr):
            # Ascending arpeggio: C (261.63) -> E (329.63) -> G (392.00)
            if t < 0.1:
                freq = 261.63
            elif t < 0.2:
                freq = 329.63
            else:
                freq = 392.00

            tone = math.sin(2 * math.pi * freq * t)
            env = self._envelope(t, duration, attack=0.02, decay=0.05, sustain=0.6, release=0.15)
            return tone * env * 0.5

        sound = self._make_sound(duration, generator)
        sound.set_volume(0.35)
        return sound

    def _make_key_pickup(self):
        """Sparkle/chime sound - bright high frequency."""
        duration = 0.35

        def generator(t, sr):
            # High frequency chime (800 Hz with harmonics)
            freq = 800
            tone = (math.sin(2 * math.pi * freq * t) +
                   0.5 * math.sin(2 * math.pi * freq * 2 * t) +
                   0.25 * math.sin(2 * math.pi * freq * 3 * t)) / 1.75

            env = self._envelope(t, duration, attack=0.01, decay=0.1, sustain=0.4, release=0.2)
            return tone * env * 0.5

        sound = self._make_sound(duration, generator)
        sound.set_volume(0.35)
        return sound

    def _make_boss_roar(self):
        """Low rumble for boss phase 2 transition."""
        duration = 0.6

        def generator(t, sr):
            # Low frequency rumble with some noise
            import random
            freq = 60 + math.sin(2 * math.pi * 5 * t) * 20  # Oscillating low freq
            tone = math.sin(2 * math.pi * freq * t)
            noise = (random.random() * 2 - 1) * 0.3

            env = self._envelope(t, duration, attack=0.05, decay=0.15, sustain=0.6, release=0.25)
            return (tone * 0.7 + noise * 0.3) * env * 0.7

        sound = self._make_sound(duration, generator)
        sound.set_volume(0.45)
        return sound

    def _make_boss_death(self):
        """Long descending explosion-like sound."""
        duration = 1.0

        def generator(t, sr):
            import random
            # Descending frequency with noise
            freq = 150 - (t / duration) * 120
            tone = math.sin(2 * math.pi * freq * t)
            noise = (random.random() * 2 - 1)

            # Mix tone and noise, gradually more noise
            noise_mix = t / duration
            combined = tone * (1 - noise_mix) + noise * noise_mix

            env = self._envelope(t, duration, attack=0.02, decay=0.2, sustain=0.5, release=0.4)
            return combined * env * 0.6

        sound = self._make_sound(duration, generator)
        sound.set_volume(0.4)
        return sound

    def _make_dungeon_enter(self):
        """Ominous descending tone."""
        duration = 0.5

        def generator(t, sr):
            # Descending minor chord
            freq1 = 220 - (t / duration) * 80  # A
            freq2 = 261.63 - (t / duration) * 95  # C
            freq3 = 329.63 - (t / duration) * 120  # E

            tone = (math.sin(2 * math.pi * freq1 * t) +
                   math.sin(2 * math.pi * freq2 * t) +
                   math.sin(2 * math.pi * freq3 * t)) / 3

            env = self._envelope(t, duration, attack=0.05, decay=0.1, sustain=0.6, release=0.2)
            return tone * env * 0.5

        sound = self._make_sound(duration, generator)
        sound.set_volume(0.4)
        return sound

    def _make_chest_open(self):
        """Satisfying unlocking/opening sound - rising chime."""
        duration = 0.3

        def generator(t, sr):
            # Rising frequency chime (400 Hz to 800 Hz)
            freq = 400 + (t / duration) * 400
            # Add harmonics for richness
            tone = (math.sin(2 * math.pi * freq * t) +
                   0.4 * math.sin(2 * math.pi * freq * 2 * t) +
                   0.2 * math.sin(2 * math.pi * freq * 3 * t)) / 1.6

            env = self._envelope(t, duration, attack=0.01, decay=0.08, sustain=0.5, release=0.15)
            return tone * env * 0.5

        sound = self._make_sound(duration, generator)
        sound.set_volume(0.4)
        return sound

    def _make_gold_pickup(self):
        """Bright coin jingle - quick ascending chime."""
        duration = 0.25

        def generator(t, sr):
            # Two quick ascending tones like coins
            if t < 0.1:
                freq = 600
            elif t < 0.15:
                freq = 800
            else:
                freq = 1000

            tone = (math.sin(2 * math.pi * freq * t) +
                   0.4 * math.sin(2 * math.pi * freq * 2 * t)) / 1.4
            env = self._envelope(t, duration, attack=0.01, decay=0.05, sustain=0.4, release=0.12)
            return tone * env * 0.5

        sound = self._make_sound(duration, generator)
        sound.set_volume(0.35)
        return sound

    def _make_push_block(self):
        """Scraping stone sound - low rumble with noise."""
        duration = 0.3

        def generator(t, sr):
            import random
            # Low rumble
            freq = 80 + (t / duration) * 20
            tone = math.sin(2 * math.pi * freq * t)
            noise = (random.random() * 2 - 1) * 0.5
            env = self._envelope(t, duration, attack=0.02, decay=0.05, sustain=0.5, release=0.15)
            return (tone * 0.5 + noise * 0.5) * env * 0.5

        sound = self._make_sound(duration, generator)
        sound.set_volume(0.3)
        return sound

    def _make_switch_click(self):
        """Short metallic click sound."""
        duration = 0.1

        def generator(t, sr):
            # High frequency click
            freq = 600 - (t / duration) * 200
            tone = math.sin(2 * math.pi * freq * t)
            harmonic = 0.3 * math.sin(2 * math.pi * freq * 2 * t)
            env = self._envelope(t, duration, attack=0.005, decay=0.02, sustain=0.3, release=0.05)
            return (tone + harmonic) / 1.3 * env * 0.6

        sound = self._make_sound(duration, generator)
        sound.set_volume(0.4)
        return sound

    def _make_torch_ignite(self):
        """Whoosh/ignite sound - rising noise burst."""
        duration = 0.25

        def generator(t, sr):
            import random
            # Rising frequency with noise
            freq = 200 + (t / duration) * 400
            tone = math.sin(2 * math.pi * freq * t) * 0.3
            noise = (random.random() * 2 - 1) * 0.7
            env = self._envelope(t, duration, attack=0.03, decay=0.05, sustain=0.4, release=0.12)
            return (tone + noise) * env * 0.4

        sound = self._make_sound(duration, generator)
        sound.set_volume(0.35)
        return sound

    def _make_door_open(self):
        """Heavy door opening sound - low descending rumble."""
        duration = 0.5

        def generator(t, sr):
            import random
            # Low descending tone
            freq = 150 - (t / duration) * 60
            tone = math.sin(2 * math.pi * freq * t)
            # Add some grind noise
            noise = (random.random() * 2 - 1) * 0.2
            env = self._envelope(t, duration, attack=0.05, decay=0.1, sustain=0.5, release=0.2)
            return (tone * 0.7 + noise * 0.3) * env * 0.5

        sound = self._make_sound(duration, generator)
        sound.set_volume(0.4)
        return sound

    def _make_note(self, frequency, duration, amplitude=0.5, warm=False, tone_type='sine'):
        """
        Generate a single note with envelope.

        Args:
            frequency: Note frequency in Hz
            duration: Note duration in seconds
            amplitude: Base amplitude (0-1)
            warm: If True, use softer envelope and warmer harmonics
            tone_type: 'sine', 'triangle', or 'square' base waveform

        Returns:
            array of samples
        """
        num_samples = int(duration * self.sample_rate)
        samples = array.array('h', [0] * num_samples)

        for i in range(num_samples):
            t = i / self.sample_rate
            phase = 2 * math.pi * frequency * t

            # Base waveform selection
            if tone_type == 'triangle':
                base = 2 * abs(2 * (frequency * t % 1) - 1) - 1
            elif tone_type == 'square':
                base = 1.0 if math.sin(phase) >= 0 else -1.0
                # Soften the square wave to avoid harshness
                base *= 0.6
            else:
                base = math.sin(phase)

            if warm:
                octave = 0.15 * math.sin(phase * 2)
                fifth = 0.08 * math.sin(phase * 1.5)
                third = 0.05 * math.sin(phase * 1.25)
                tone = (base + octave + fifth + third) / 1.28
                env = self._envelope(t, duration, attack=0.08, decay=0.15, sustain=0.6, release=max(0.2, duration * 0.3))
            else:
                octave = 0.3 * math.sin(phase * 2)
                fifth = 0.1 * math.sin(phase * 1.5)
                tone = (base + octave + fifth) / 1.4
                env = self._envelope(t, duration, attack=0.02, decay=0.05, sustain=0.8, release=0.1)

            value = tone * env * amplitude
            value = max(-1.0, min(1.0, value))
            samples[i] = int(value * 32767)

        return samples

    def _make_rest(self, duration):
        """Generate silence for a rest."""
        num_samples = int(duration * self.sample_rate)
        return array.array('h', [0] * num_samples)

    def _mix_layers(self, *layers):
        """Mix multiple sample arrays together by summing and normalizing."""
        if not layers:
            return array.array('h')
        max_len = max(len(layer) for layer in layers)
        mixed = array.array('h', [0] * max_len)
        n = len(layers)
        for i in range(max_len):
            total = 0
            for layer in layers:
                if i < len(layer):
                    total += layer[i]
            total = total / n
            total = max(-32767, min(32767, int(total)))
            mixed[i] = total
        return mixed

    def _scale_tempo(self, notes, factor, rest_extra=1.0):
        """Scale all note/rest durations by factor. rest_extra applies additional scaling to rests."""
        return [(freq, dur * factor * (rest_extra if freq == 0 else 1.0)) for freq, dur in notes]

    def _notes_to_samples(self, notes, amplitude=0.3, warm=True, tone_type='sine'):
        """Convert a list of (freq, duration) tuples to a sample array."""
        note_arrays = []
        for freq, dur in notes:
            if freq == 0:
                note_arrays.append(self._make_rest(dur))
            else:
                note_arrays.append(self._make_note(freq, dur, amplitude=amplitude, warm=warm, tone_type=tone_type))
        combined = array.array('h')
        for arr in note_arrays:
            combined.extend(arr)
        return combined

    def _concatenate_notes(self, note_arrays):
        """Concatenate multiple note arrays into a single sound."""
        if not note_arrays:
            return None

        # Combine all note arrays
        combined = array.array('h')
        for note_arr in note_arrays:
            combined.extend(note_arr)

        # Create pygame sound from combined array
        sound = pygame.mixer.Sound(buffer=combined)
        return sound

    def _generate_title_music(self):
        """Generate epic Zelda-inspired title theme — heroic Bb major fanfare."""
        # Iconic opening fanfare — bold, triumphant (like the Zelda main theme)
        # Uses Bb major tonality with heroic leaps and dotted rhythms
        fanfare = [
            (466, 0.15),  # Bb4 (pickup)
            (0, 0.05),
            (466, 0.6),   # Bb4 (held)
            (466, 0.2),   # Bb4
            (466, 0.2),   # Bb4
            (466, 0.2),   # Bb4
            (466, 0.6),   # Bb4 (held)
            (0, 0.1),
            (466, 0.2),   # Bb4
            (466, 0.2),   # Bb4
            (466, 0.2),   # Bb4
            (466, 0.6),   # Bb4 (held)
            (0, 0.1),
            (466, 0.15),  # Bb4
            (523, 0.15),  # C5
            (587, 0.15),  # D5
            (0, 0.05),
        ]

        # Section A: The heroic main melody
        melody_a = [
            (587, 0.8),   # D5 (hero note)
            (0, 0.1),
            (466, 0.3),   # Bb4
            (0, 0.1),
            (466, 0.2),   # Bb4
            (523, 0.2),   # C5
            (587, 0.8),   # D5
            (0, 0.1),
            (466, 0.3),   # Bb4
            (0, 0.1),
            (466, 0.2),   # Bb4
            (523, 0.2),   # C5
            (587, 0.4),   # D5
            (659, 0.4),   # E5
            (698, 0.9),   # F5 (soaring peak!)
            (0, 0.3),
            (698, 0.3),   # F5
            (659, 0.2),   # E5
            (587, 0.2),   # D5
            (523, 0.2),   # C5
            (466, 0.8),   # Bb4 (resolve)
            (0, 0.3),
        ]

        # Section B: Adventurous climbing phrase
        melody_b = [
            (349, 0.3),   # F4
            (392, 0.3),   # G4
            (440, 0.3),   # A4
            (466, 0.6),   # Bb4
            (0, 0.1),
            (440, 0.2),   # A4
            (466, 0.2),   # Bb4
            (523, 0.6),   # C5
            (0, 0.1),
            (587, 0.3),   # D5
            (523, 0.3),   # C5
            (466, 0.3),   # Bb4
            (440, 0.3),   # A4
            (392, 0.8),   # G4
            (0, 0.2),
            (349, 0.3),   # F4
            (392, 0.3),   # G4
            (440, 0.4),   # A4
            (466, 1.0),   # Bb4 (triumphant resolve)
            (0, 0.4),
        ]

        # Section C: Majestic ending — slower, grander
        melody_c = [
            (587, 0.5),   # D5
            (0, 0.1),
            (587, 0.5),   # D5
            (659, 0.5),   # E5
            (698, 1.0),   # F5 (grand!)
            (0, 0.2),
            (659, 0.3),   # E5
            (587, 0.3),   # D5
            (523, 0.5),   # C5
            (466, 0.5),   # Bb4
            (0, 0.1),
            (440, 0.3),   # A4
            (466, 0.3),   # Bb4
            (523, 0.5),   # C5
            (587, 1.2),   # D5 (final heroic hold)
            (0, 0.3),
            (466, 1.5),   # Bb4 (resolve home)
            (0, 0.8),
        ]

        # Bass layer — strong root movement, march-like
        bass = [
            # Under fanfare
            (117, 1.2),   # Bb2
            (117, 1.2),   # Bb2
            (117, 0.8),   # Bb2
            (131, 0.4),   # C3
            (147, 0.4),   # D3
            # Under A
            (147, 1.2),   # D3
            (0, 0.2),
            (117, 1.0),   # Bb2
            (147, 1.2),   # D3
            (0, 0.2),
            (117, 1.0),   # Bb2
            (147, 0.6),   # D3
            (165, 0.6),   # E3
            (175, 1.2),   # F3
            (0, 0.2),
            (175, 0.6),   # F3
            (147, 0.6),   # D3
            (117, 1.2),   # Bb2
            (0, 0.3),
            # Under B
            (175, 1.0),   # F3
            (0, 0.2),
            (175, 0.8),   # F3
            (131, 1.0),   # C3
            (0, 0.2),
            (147, 0.8),   # D3
            (131, 0.6),   # C3
            (117, 0.6),   # Bb2
            (98, 1.0),    # G2
            (0, 0.2),
            (175, 0.8),   # F3
            (131, 0.6),   # C3
            (117, 1.2),   # Bb2
            (0, 0.4),
            # Under C
            (147, 1.0),   # D3
            (147, 0.8),   # D3
            (165, 0.6),   # E3
            (175, 1.2),   # F3
            (0, 0.2),
            (147, 0.8),   # D3
            (131, 0.8),   # C3
            (117, 0.8),   # Bb2
            (0, 0.1),
            (131, 0.6),   # C3
            (117, 0.6),   # Bb2
            (147, 1.4),   # D3
            (117, 1.8),   # Bb2 (final)
            (0, 0.8),
        ]

        tempo = 1.1  # Majestic but not too slow
        melody = self._scale_tempo(fanfare + melody_a + melody_b + melody_c, tempo, rest_extra=1.0)
        bass_scaled = self._scale_tempo(bass, tempo, rest_extra=1.0)
        melody_samples = self._notes_to_samples(melody, amplitude=0.32, warm=True, tone_type='square')
        bass_samples = self._notes_to_samples(bass_scaled, amplitude=0.20, warm=True, tone_type='triangle')
        mixed = self._mix_layers(melody_samples, bass_samples)
        return pygame.mixer.Sound(buffer=mixed)

    def _generate_overworld_music(self):
        """Generate pastoral overworld theme with melody + bass — G major, A/B/A/C structure."""
        # Section A: Bright, hopeful G major melody
        melody_a = [
            (392, 0.45),  # G4
            (440, 0.35),  # A4
            (494, 0.55),  # B4
            (523, 0.7),   # C5
            (0, 0.2),
            (494, 0.4),   # B4
            (440, 0.4),   # A4
            (392, 0.7),   # G4
            (0, 0.3),
            (330, 0.4),   # E4
            (370, 0.4),   # F#4
            (392, 0.55),  # G4
            (440, 0.7),   # A4 (linger)
            (0, 0.25),
            (392, 0.4),   # G4
            (370, 0.4),   # F#4
            (330, 0.55),  # E4
            (294, 0.7),   # D4
            (0, 0.4),
        ]
        # Section B: Rising energy — climbing phrase
        melody_b = [
            (294, 0.4),   # D4
            (330, 0.35),  # E4
            (370, 0.4),   # F#4
            (392, 0.55),  # G4
            (440, 0.55),  # A4
            (494, 0.7),   # B4
            (0, 0.2),
            (523, 0.8),   # C5 (peak)
            (494, 0.4),   # B4
            (440, 0.4),   # A4
            (0, 0.2),
            (494, 0.5),   # B4
            (523, 0.5),   # C5
            (587, 0.8),   # D5 (soar!)
            (0, 0.3),
            (523, 0.45),  # C5
            (494, 0.45),  # B4
            (440, 0.5),   # A4
            (392, 0.8),   # G4 (settle)
            (0, 0.4),
        ]
        # Section C: Gentle descent — winding down
        melody_c = [
            (523, 0.6),   # C5
            (494, 0.45),  # B4
            (440, 0.45),  # A4
            (392, 0.6),   # G4
            (0, 0.25),
            (370, 0.45),  # F#4
            (330, 0.5),   # E4
            (294, 0.6),   # D4
            (0, 0.3),
            (262, 0.5),   # C4
            (294, 0.45),  # D4
            (330, 0.5),   # E4
            (370, 0.55),  # F#4
            (392, 1.0),   # G4 (long resolve home)
            (0, 0.6),
        ]

        # Bass: Root note movement following the harmony
        bass = [
            # Under A
            (196, 1.4),   # G3
            (0, 0.2),
            (196, 1.0),   # G3
            (220, 1.2),   # A3
            (0, 0.2),
            (165, 1.2),   # E3
            (147, 1.2),   # D3
            (0, 0.3),
            # Under B
            (147, 1.0),   # D3
            (165, 0.8),   # E3
            (185, 0.8),   # F#3
            (196, 1.2),   # G3
            (0, 0.2),
            (220, 1.0),   # A3
            (196, 1.0),   # G3
            (0, 0.2),
            (165, 1.0),   # E3
            (147, 1.0),   # D3
            (196, 1.2),   # G3
            (0, 0.4),
            # Under C
            (131, 1.2),   # C3
            (147, 1.0),   # D3
            (165, 1.0),   # E3
            (0, 0.2),
            (131, 1.2),   # C3
            (147, 1.0),   # D3
            (196, 1.6),   # G3
            (0, 0.5),
        ]

        tempo = 1.35  # Relaxed pastoral feel
        melody = self._scale_tempo(melody_a + melody_b + melody_c, tempo, rest_extra=1.2)
        bass_scaled = self._scale_tempo(bass, tempo, rest_extra=1.1)
        melody_samples = self._notes_to_samples(melody, amplitude=0.28, warm=True)
        bass_samples = self._notes_to_samples(bass_scaled, amplitude=0.16, warm=True, tone_type='triangle')
        mixed = self._mix_layers(melody_samples, bass_samples)
        return pygame.mixer.Sound(buffer=mixed)

    def _generate_dungeon_music(self):
        """Generate haunting dungeon theme — sparse C minor with droning bass and chromatic tension."""
        # Section A: Sparse, hollow melody
        melody_a = [
            (262, 0.8),   # C4
            (0, 0.6),
            (311, 0.7),   # Eb4
            (294, 0.6),   # D4 (chromatic)
            (262, 1.0),   # C4
            (0, 0.7),
            (233, 0.8),   # Bb3
            (262, 0.6),   # C4
            (247, 0.7),   # B3 (tension!)
            (233, 1.2),   # Bb3 (resolve down)
            (0, 0.8),
        ]
        # Section B: Higher, more anxious
        melody_b = [
            (311, 0.7),   # Eb4
            (349, 0.6),   # F4
            (392, 0.9),   # G4 (peak)
            (0, 0.5),
            (370, 0.6),   # F#4 (chromatic!)
            (349, 0.6),   # F4
            (311, 0.8),   # Eb4
            (0, 0.4),
            (262, 0.7),   # C4
            (233, 0.7),   # Bb3
            (196, 1.2),   # G3 (low resolve)
            (0, 0.9),
        ]
        # Section C: Resolution — dark calm
        melody_c = [
            (196, 0.9),   # G3
            (0, 0.5),
            (233, 0.7),   # Bb3
            (262, 0.8),   # C4
            (0, 0.4),
            (233, 0.6),   # Bb3
            (196, 0.8),   # G3
            (175, 0.7),   # F3
            (165, 1.2),   # E3 (unexpected)
            (0, 0.5),
            (175, 0.6),   # F3
            (196, 1.4),   # G3 (long hollow)
            (0, 1.0),
        ]

        # Bass: Slow droning pedal tones
        bass = [
            # Under A
            (131, 2.0),   # C3 (drone)
            (0, 0.4),
            (131, 1.6),   # C3
            (117, 1.8),   # Bb2
            (0, 0.6),
            # Under B
            (156, 1.6),   # Eb3
            (0, 0.3),
            (131, 1.8),   # C3
            (0, 0.4),
            (98, 2.0),    # G2 (very low)
            (0, 0.8),
            # Under C
            (98, 1.8),    # G2
            (0, 0.4),
            (117, 1.6),   # Bb2
            (131, 1.4),   # C3
            (0, 0.3),
            (98, 2.0),    # G2
            (0, 1.0),
        ]

        tempo = 1.45  # Very slow, eerie
        melody = self._scale_tempo(melody_a + melody_b + melody_c, tempo, rest_extra=1.3)
        bass_scaled = self._scale_tempo(bass, tempo, rest_extra=1.2)
        melody_samples = self._notes_to_samples(melody, amplitude=0.22, warm=True)
        bass_samples = self._notes_to_samples(bass_scaled, amplitude=0.15, warm=True, tone_type='triangle')
        mixed = self._mix_layers(melody_samples, bass_samples)
        return pygame.mixer.Sound(buffer=mixed)

    def _generate_forest_music(self):
        """Generate mysterious forest theme — E minor with layered melody and nature-like bass."""
        # Section A: Gentle, winding E minor melody
        melody_a = [
            (330, 0.6),   # E4
            (370, 0.5),   # F#4
            (392, 0.7),   # G4
            (440, 0.8),   # A4
            (0, 0.3),
            (392, 0.5),   # G4
            (370, 0.5),   # F#4
            (330, 0.8),   # E4
            (0, 0.4),
            (294, 0.5),   # D4
            (330, 0.5),   # E4
            (370, 0.6),   # F#4
            (392, 0.9),   # G4 (linger)
            (0, 0.5),
        ]
        # Section B: Darker — descend into C major territory
        melody_b = [
            (440, 0.6),   # A4
            (392, 0.5),   # G4
            (349, 0.6),   # F4 (borrow from C)
            (330, 0.8),   # E4
            (0, 0.3),
            (294, 0.6),   # D4
            (262, 0.7),   # C4
            (247, 0.8),   # B3
            (0, 0.5),
            (262, 0.5),   # C4
            (294, 0.5),   # D4
            (330, 0.7),   # E4
            (0, 0.4),
            (370, 0.5),   # F#4
            (392, 0.8),   # G4
            (0, 0.4),
        ]
        # Section C: Return to E minor — ethereal resolution
        melody_c = [
            (494, 0.7),   # B4 (high, ethereal)
            (440, 0.5),   # A4
            (392, 0.6),   # G4
            (0, 0.3),
            (370, 0.5),   # F#4
            (330, 0.7),   # E4
            (294, 0.6),   # D4
            (330, 0.9),   # E4 (resolve)
            (0, 0.4),
            (247, 0.6),   # B3
            (262, 0.5),   # C4
            (294, 0.6),   # D4
            (330, 1.2),   # E4 (long, final)
            (0, 0.7),
        ]
        # Section D: Brief, whimsical coda
        melody_d = [
            (392, 0.5),   # G4
            (440, 0.4),   # A4
            (494, 0.6),   # B4
            (0, 0.3),
            (440, 0.4),   # A4
            (392, 0.5),   # G4
            (330, 0.6),   # E4
            (294, 0.5),   # D4
            (247, 0.7),   # B3
            (0, 0.3),
            (262, 0.5),   # C4
            (247, 0.4),   # B3
            (196, 0.8),   # G3
            (165, 1.0),   # E3 (deep resolve)
            (0, 0.8),
        ]

        # Bass: Slow arpeggiated roots — like wind through leaves
        bass = [
            # Under A
            (165, 1.4),   # E3
            (0, 0.3),
            (165, 1.0),   # E3
            (147, 1.2),   # D3
            (0, 0.2),
            (196, 1.4),   # G3
            (0, 0.4),
            # Under B
            (220, 1.2),   # A3
            (196, 1.0),   # G3
            (0, 0.2),
            (175, 1.2),   # F3
            (165, 1.0),   # E3
            (0, 0.3),
            (147, 1.0),   # D3
            (196, 1.2),   # G3
            (0, 0.4),
            # Under C
            (247, 1.4),   # B3
            (0, 0.2),
            (220, 1.2),   # A3
            (196, 1.0),   # G3
            (0, 0.3),
            (165, 1.6),   # E3
            (0, 0.4),
            # Under D
            (196, 1.0),   # G3
            (0, 0.2),
            (165, 1.0),   # E3
            (147, 1.0),   # D3
            (0, 0.2),
            (131, 1.2),   # C3
            (165, 1.6),   # E3
            (0, 0.6),
        ]

        tempo = 1.4  # Slow, mysterious
        melody = self._scale_tempo(melody_a + melody_b + melody_c + melody_d, tempo, rest_extra=1.25)
        bass_scaled = self._scale_tempo(bass, tempo, rest_extra=1.15)
        melody_samples = self._notes_to_samples(melody, amplitude=0.24, warm=True)
        bass_samples = self._notes_to_samples(bass_scaled, amplitude=0.14, warm=True, tone_type='triangle')
        mixed = self._mix_layers(melody_samples, bass_samples)
        return pygame.mixer.Sound(buffer=mixed)

    def _generate_desert_music(self):
        """Generate exotic desert theme — A harmonic minor with staccato melody and drone bass."""
        # Section A: Exotic, dance-like phrase
        melody_a = [
            (220, 0.35),  # A3
            (0, 0.15),
            (247, 0.35),  # B3
            (262, 0.4),   # C4
            (0, 0.15),
            (330, 0.5),   # E4
            (311, 0.35),  # Eb4 (flat — exotic)
            (0, 0.2),
            (262, 0.4),   # C4
            (247, 0.35),  # B3
            (220, 0.5),   # A3
            (0, 0.3),
            (208, 0.35),  # Ab3 (chromatic neighbor)
            (220, 0.5),   # A3
            (0, 0.4),
        ]
        # Section B: Higher, more intense
        melody_b = [
            (330, 0.4),   # E4
            (349, 0.35),  # F4
            (0, 0.15),
            (416, 0.5),   # Ab4 (tension!)
            (392, 0.35),  # G#4→G4 (resolve)
            (0, 0.2),
            (330, 0.4),   # E4
            (311, 0.35),  # Eb4
            (262, 0.5),   # C4
            (0, 0.2),
            (247, 0.35),  # B3
            (220, 0.4),   # A3
            (0, 0.15),
            (262, 0.4),   # C4
            (247, 0.35),  # B3
            (220, 0.6),   # A3 (settle)
            (0, 0.35),
        ]
        # Section C: Call and response — lower register
        melody_c = [
            (175, 0.4),   # F3
            (196, 0.35),  # G3 (call)
            (0, 0.2),
            (220, 0.5),   # A3 (response)
            (0, 0.3),
            (196, 0.4),   # G3 (call)
            (175, 0.35),  # F3
            (0, 0.2),
            (165, 0.5),   # E3 (response)
            (0, 0.3),
            (175, 0.35),  # F3
            (196, 0.35),  # G3
            (208, 0.4),   # Ab3
            (220, 0.6),   # A3 (resolve)
            (0, 0.4),
            (247, 0.35),  # B3
            (262, 0.35),  # C4
            (247, 0.4),   # B3
            (220, 0.7),   # A3 (final)
            (0, 0.5),
        ]

        # Bass: Droning open fifths — desert wind
        bass = [
            # Under A
            (110, 2.0),   # A2 (drone)
            (0, 0.3),
            (110, 1.5),   # A2
            (131, 1.2),   # C3
            (0, 0.4),
            # Under B
            (110, 1.4),   # A2
            (131, 1.2),   # C3
            (0, 0.2),
            (98, 1.4),    # G2
            (110, 1.6),   # A2
            (0, 0.4),
            # Under C
            (87, 1.6),    # F2
            (0, 0.3),
            (110, 1.4),   # A2
            (0, 0.2),
            (87, 1.2),    # F2
            (98, 1.0),    # G2
            (110, 1.8),   # A2
            (0, 0.5),
        ]

        tempo = 1.35  # Unhurried, hypnotic
        melody = self._scale_tempo(melody_a + melody_b + melody_c, tempo, rest_extra=1.3)
        bass_scaled = self._scale_tempo(bass, tempo, rest_extra=1.15)
        melody_samples = self._notes_to_samples(melody, amplitude=0.26, warm=False)
        bass_samples = self._notes_to_samples(bass_scaled, amplitude=0.15, warm=True, tone_type='triangle')
        mixed = self._mix_layers(melody_samples, bass_samples)
        return pygame.mixer.Sound(buffer=mixed)

    def _generate_volcano_music(self):
        """Generate ominous volcano theme — C minor with heavy bass and aggressive melody."""
        # Section A: Ominous, pounding C minor
        melody_a = [
            (262, 0.5),   # C4
            (0, 0.15),
            (311, 0.45),  # Eb4
            (294, 0.4),   # D4
            (262, 0.6),   # C4
            (0, 0.2),
            (233, 0.5),   # Bb3
            (262, 0.45),  # C4
            (311, 0.6),   # Eb4
            (0, 0.2),
            (349, 0.5),   # F4
            (311, 0.45),  # Eb4
            (262, 0.7),   # C4 (heavy)
            (0, 0.35),
        ]
        # Section B: Climbing tension
        melody_b = [
            (311, 0.4),   # Eb4
            (349, 0.4),   # F4
            (392, 0.5),   # G4
            (0, 0.15),
            (415, 0.5),   # Ab4
            (392, 0.4),   # G4
            (349, 0.5),   # F4
            (0, 0.2),
            (392, 0.4),   # G4
            (415, 0.45),  # Ab4
            (466, 0.6),   # Bb4 (peak!)
            (0, 0.2),
            (415, 0.4),   # Ab4
            (392, 0.45),  # G4
            (349, 0.5),   # F4
            (311, 0.6),   # Eb4
            (262, 0.7),   # C4 (fall back)
            (0, 0.35),
        ]
        # Section C: Dark, low resolution
        melody_c = [
            (196, 0.6),   # G3
            (0, 0.2),
            (233, 0.5),   # Bb3
            (262, 0.6),   # C4
            (233, 0.5),   # Bb3
            (0, 0.2),
            (196, 0.6),   # G3
            (175, 0.5),   # F3
            (156, 0.6),   # Eb3
            (131, 0.8),   # C3 (very low)
            (0, 0.3),
            (156, 0.5),   # Eb3
            (175, 0.5),   # F3
            (196, 0.6),   # G3
            (175, 0.5),   # F3
            (131, 1.0),   # C3 (heavy end)
            (0, 0.5),
        ]

        # Bass: Pounding low register — rumbling earth
        bass = [
            # Under A
            (65, 1.0),    # C2 (very low)
            (0, 0.15),
            (65, 0.8),    # C2
            (0, 0.15),
            (78, 1.0),    # Eb2
            (65, 1.0),    # C2
            (0, 0.2),
            (58, 1.2),    # Bb1
            (0, 0.3),
            # Under B
            (78, 0.8),    # Eb2
            (0, 0.15),
            (87, 1.0),    # F2
            (0, 0.15),
            (98, 1.0),    # G2
            (87, 0.8),    # F2
            (0, 0.15),
            (78, 1.0),    # Eb2
            (65, 1.2),    # C2
            (0, 0.3),
            # Under C
            (98, 1.0),    # G2
            (0, 0.2),
            (78, 1.0),    # Eb2
            (65, 0.8),    # C2
            (0, 0.15),
            (58, 1.2),    # Bb1
            (65, 1.0),    # C2
            (0, 0.2),
            (65, 1.4),    # C2 (long)
            (0, 0.4),
        ]

        tempo = 1.25  # Slower but still heavy
        melody = self._scale_tempo(melody_a + melody_b + melody_c, tempo, rest_extra=1.2)
        bass_scaled = self._scale_tempo(bass, tempo, rest_extra=1.1)
        melody_samples = self._notes_to_samples(melody, amplitude=0.27, warm=False, tone_type='square')
        bass_samples = self._notes_to_samples(bass_scaled, amplitude=0.18, warm=False, tone_type='triangle')
        mixed = self._mix_layers(melody_samples, bass_samples)
        return pygame.mixer.Sound(buffer=mixed)

    def _generate_boss_music(self):
        """Generate intense boss battle theme — D minor with driving bass and aggressive melody."""
        # Section A: Fast, aggressive D minor riff
        melody_a = [
            (294, 0.25),  # D4
            (349, 0.2),   # F4
            (392, 0.3),   # G4
            (0, 0.1),
            (440, 0.25),  # A4
            (466, 0.3),   # Bb4 (tension)
            (440, 0.2),   # A4
            (392, 0.25),  # G4
            (0, 0.1),
            (349, 0.3),   # F4
            (294, 0.4),   # D4 (resolve)
            (0, 0.15),
            (262, 0.25),  # C4
            (294, 0.25),  # D4
            (349, 0.25),  # F4
            (392, 0.3),   # G4
            (0, 0.1),
        ]
        # Section B: Climbing — builds intensity
        melody_b = [
            (440, 0.25),  # A4
            (466, 0.25),  # Bb4
            (523, 0.35),  # C5
            (0, 0.1),
            (587, 0.4),   # D5 (peak!)
            (523, 0.25),  # C5
            (466, 0.25),  # Bb4
            (0, 0.1),
            (440, 0.3),   # A4
            (392, 0.25),  # G4
            (349, 0.3),   # F4
            (0, 0.1),
            (392, 0.25),  # G4
            (440, 0.25),  # A4
            (466, 0.35),  # Bb4
            (523, 0.4),   # C5
            (0, 0.15),
        ]
        # Section C: Breakdown — syncopated hits
        melody_c = [
            (587, 0.35),  # D5
            (0, 0.15),
            (523, 0.25),  # C5
            (0, 0.1),
            (466, 0.35),  # Bb4
            (0, 0.15),
            (440, 0.25),  # A4
            (0, 0.1),
            (392, 0.3),   # G4
            (349, 0.25),  # F4
            (294, 0.4),   # D4
            (0, 0.2),
            (262, 0.3),   # C4
            (294, 0.25),  # D4
            (349, 0.3),   # F4
            (294, 0.5),   # D4 (heavy resolve)
            (0, 0.2),
        ]
        # Section D: Final push — rapid fire
        melody_d = [
            (294, 0.2),   # D4
            (349, 0.2),   # F4
            (294, 0.2),   # D4
            (392, 0.2),   # G4
            (0, 0.1),
            (349, 0.2),   # F4
            (440, 0.2),   # A4
            (349, 0.2),   # F4
            (466, 0.3),   # Bb4
            (0, 0.1),
            (440, 0.25),  # A4
            (523, 0.25),  # C5
            (466, 0.25),  # Bb4
            (440, 0.25),  # A4
            (392, 0.25),  # G4
            (349, 0.3),   # F4
            (294, 0.5),   # D4 (final)
            (0, 0.25),
        ]

        # Bass: Driving, rhythmic bass line — pumping energy
        bass = [
            # Under A
            (147, 0.4),   # D3
            (0, 0.1),
            (147, 0.3),   # D3
            (175, 0.4),   # F3
            (0, 0.1),
            (196, 0.3),   # G3
            (175, 0.3),   # F3
            (147, 0.4),   # D3
            (0, 0.1),
            (131, 0.3),   # C3
            (147, 0.4),   # D3
            (0, 0.1),
            (175, 0.3),   # F3
            (196, 0.4),   # G3
            (0, 0.1),
            # Under B
            (220, 0.4),   # A3
            (0, 0.1),
            (233, 0.35),  # Bb3
            (220, 0.3),   # A3
            (0, 0.1),
            (196, 0.35),  # G3
            (175, 0.35),  # F3
            (0, 0.1),
            (147, 0.4),   # D3
            (0, 0.1),
            (175, 0.35),  # F3
            (196, 0.35),  # G3
            (220, 0.4),   # A3
            (0, 0.15),
            # Under C
            (147, 0.5),   # D3
            (0, 0.15),
            (131, 0.4),   # C3
            (0, 0.1),
            (117, 0.5),   # Bb2
            (0, 0.15),
            (110, 0.4),   # A2
            (0, 0.1),
            (98, 0.45),   # G2
            (110, 0.35),  # A2
            (131, 0.4),   # C3
            (147, 0.5),   # D3
            (0, 0.2),
            # Under D
            (147, 0.3),   # D3
            (0, 0.1),
            (147, 0.3),   # D3
            (175, 0.3),   # F3
            (0, 0.1),
            (175, 0.3),   # F3
            (196, 0.3),   # G3
            (0, 0.1),
            (196, 0.3),   # G3
            (220, 0.35),  # A3
            (196, 0.3),   # G3
            (175, 0.3),   # F3
            (147, 0.5),   # D3
            (0, 0.25),
        ]

        tempo = 1.2  # Still intense but not frantic
        melody = self._scale_tempo(melody_a + melody_b + melody_c + melody_d, tempo, rest_extra=1.15)
        bass_scaled = self._scale_tempo(bass, tempo, rest_extra=1.1)
        melody_samples = self._notes_to_samples(melody, amplitude=0.3, warm=False, tone_type='square')
        bass_samples = self._notes_to_samples(bass_scaled, amplitude=0.2, warm=False, tone_type='triangle')
        mixed = self._mix_layers(melody_samples, bass_samples)
        return pygame.mixer.Sound(buffer=mixed)

    def _make_victory_fanfare(self):
        """Ascending triumphant fanfare — C major ascending."""
        notes = [
            (262, 0.15), (330, 0.15), (392, 0.15), (523, 0.4),
            (0, 0.1),
            (392, 0.15), (523, 0.15), (659, 0.5),
        ]
        note_arrays = []
        for freq, dur in notes:
            if freq == 0:
                note_arrays.append(self._make_rest(dur))
            else:
                note_arrays.append(self._make_note(freq, dur, amplitude=0.4, warm=True))
        sound = self._concatenate_notes(note_arrays)
        if sound:
            sound.set_volume(0.45)
        return sound

    def _make_ability_spin(self):
        """Whooshing spin sound - white noise with frequency sweep."""
        duration = 0.35

        def generator(t, sr):
            import random
            noise = random.random() * 2 - 1
            # Sweep up then down
            freq = 300 + 200 * math.sin(math.pi * t / duration)
            tone = math.sin(2 * math.pi * freq * t)
            env = self._envelope(t, duration, attack=0.02, decay=0.05, sustain=0.5, release=0.15)
            return (noise * 0.4 + tone * 0.6) * env * 0.4

        sound = self._make_sound(duration, generator)
        sound.set_volume(0.4)
        return sound

    def _make_ability_dash(self):
        """Quick swoosh for dash - high-pass noise burst."""
        duration = 0.2

        def generator(t, sr):
            import random
            noise = random.random() * 2 - 1
            # Rising pitch
            freq = 400 + (t / duration) * 600
            tone = math.sin(2 * math.pi * freq * t) * 0.3
            env = self._envelope(t, duration, attack=0.01, decay=0.03, sustain=0.4, release=0.12)
            return (noise * 0.5 + tone * 0.5) * env * 0.35

        sound = self._make_sound(duration, generator)
        sound.set_volume(0.35)
        return sound

    def _make_ability_fire(self):
        """Fire blast - crackling burst with low rumble."""
        duration = 0.4

        def generator(t, sr):
            import random
            noise = random.random() * 2 - 1
            # Low rumble + crackling
            freq = 120 - (t / duration) * 60
            tone = math.sin(2 * math.pi * freq * t)
            crackle = noise * (0.5 + 0.5 * math.sin(2 * math.pi * 30 * t))
            env = self._envelope(t, duration, attack=0.02, decay=0.1, sustain=0.5, release=0.2)
            return (tone * 0.5 + crackle * 0.5) * env * 0.5

        sound = self._make_sound(duration, generator)
        sound.set_volume(0.4)
        return sound

    def _make_ability_shield(self):
        """Shield activation - resonant chime with shimmer."""
        duration = 0.5

        def generator(t, sr):
            # Bright resonant tone
            freq = 600
            tone = (math.sin(2 * math.pi * freq * t) +
                    0.4 * math.sin(2 * math.pi * freq * 1.5 * t) +
                    0.2 * math.sin(2 * math.pi * freq * 2 * t)) / 1.6
            env = self._envelope(t, duration, attack=0.03, decay=0.1, sustain=0.5, release=0.25)
            return tone * env * 0.4

        sound = self._make_sound(duration, generator)
        sound.set_volume(0.35)
        return sound

    def _make_ability_fail(self):
        """Short buzz for failed ability use (not enough MP)."""
        duration = 0.15

        def generator(t, sr):
            freq = 150
            tone = math.sin(2 * math.pi * freq * t)
            env = self._envelope(t, duration, attack=0.01, decay=0.03, sustain=0.3, release=0.08)
            return tone * env * 0.3

        sound = self._make_sound(duration, generator)
        sound.set_volume(0.3)
        return sound

    def _make_parry_clang(self):
        """Sharp metallic clang for perfect parry."""
        duration = 0.25

        def generator(t, sr):
            f1 = 800
            f2 = 1200
            f3 = 1600
            tone = (math.sin(2 * math.pi * f1 * t) +
                    0.6 * math.sin(2 * math.pi * f2 * t) +
                    0.3 * math.sin(2 * math.pi * f3 * t)) / 1.9
            env = self._envelope(t, duration, attack=0.002, decay=0.04, sustain=0.3, release=0.15)
            return tone * env * 0.6

        sound = self._make_sound(duration, generator)
        sound.set_volume(0.5)
        return sound

    def _make_dodge_whoosh(self):
        """Quick whoosh for dodge roll."""
        duration = 0.18

        def generator(t, sr):
            import random
            noise = random.random() * 2 - 1
            freq = 300 + (t / duration) * 500
            tone = math.sin(2 * math.pi * freq * t) * 0.3
            env = self._envelope(t, duration, attack=0.01, decay=0.02, sustain=0.4, release=0.1)
            return (noise * 0.6 + tone * 0.4) * env * 0.35

        sound = self._make_sound(duration, generator)
        sound.set_volume(0.35)
        return sound

    def _make_charge_hum(self):
        """Building hum for charge attack."""
        duration = 0.6

        def generator(t, sr):
            freq = 100 + (t / duration) * 300
            tone = math.sin(2 * math.pi * freq * t)
            harmonic = 0.3 * math.sin(2 * math.pi * freq * 2 * t)
            env = self._envelope(t, duration, attack=0.1, decay=0.1, sustain=0.7, release=0.2)
            return (tone + harmonic) / 1.3 * env * 0.4

        sound = self._make_sound(duration, generator)
        sound.set_volume(0.3)
        return sound

    def _make_combo_hit(self, hit_number):
        """Combo hit sounds - progressively more impactful."""
        durations = {1: 0.12, 2: 0.1, 3: 0.2}
        duration = durations.get(hit_number, 0.12)

        def generator(t, sr, _hit=hit_number, _dur=duration):
            base_freq = 150 + (_hit - 1) * 80
            freq = base_freq + (1 - t / _dur) * 100
            tone = math.sin(2 * math.pi * freq * t)
            if _hit >= 2:
                tone += 0.3 * math.sin(2 * math.pi * freq * 1.5 * t)
            if _hit >= 3:
                tone += 0.2 * math.sin(2 * math.pi * freq * 2 * t)
                import random
                tone += (random.random() * 2 - 1) * 0.15
            env = self._envelope(t, _dur, attack=0.005, decay=0.03, sustain=0.3, release=_dur * 0.4)
            return tone * env * (0.4 + _hit * 0.1)

        sound = self._make_sound(duration, generator)
        sound.set_volume(0.35 + hit_number * 0.05)
        return sound

    def _make_shield_block(self):
        """Dull thud for shield blocking an attack."""
        duration = 0.15

        def generator(t, sr):
            freq = 180 - (t / duration) * 80
            tone = math.sin(2 * math.pi * freq * t)
            env = self._envelope(t, duration, attack=0.005, decay=0.03, sustain=0.2, release=0.08)
            return tone * env * 0.5

        sound = self._make_sound(duration, generator)
        sound.set_volume(0.4)
        return sound

    def _make_room_clear(self):
        """Ascending chime for clearing all enemies in a room."""
        duration = 0.6

        def generator(t, sr):
            # Ascending arpeggio: C5 -> E5 -> G5 -> C6
            if t < 0.15:
                freq = 523.25
            elif t < 0.3:
                freq = 659.25
            elif t < 0.45:
                freq = 783.99
            else:
                freq = 1046.5

            tone = (math.sin(2 * math.pi * freq * t) +
                    0.4 * math.sin(2 * math.pi * freq * 2 * t) +
                    0.2 * math.sin(2 * math.pi * freq * 3 * t)) / 1.6

            env = self._envelope(t, duration, attack=0.02, decay=0.08, sustain=0.5, release=0.2)
            return tone * env * 0.5

        sound = self._make_sound(duration, generator)
        sound.set_volume(0.4)
        return sound

    def _make_door_lock(self):
        """Ominous locking sound - descending metallic clang."""
        duration = 0.35

        def generator(t, sr):
            freq = 400 - (t / duration) * 200
            tone = math.sin(2 * math.pi * freq * t)
            harmonic = 0.4 * math.sin(2 * math.pi * freq * 3 * t)
            env = self._envelope(t, duration, attack=0.01, decay=0.05, sustain=0.4, release=0.15)
            return (tone + harmonic) / 1.4 * env * 0.6

        sound = self._make_sound(duration, generator)
        sound.set_volume(0.4)
        return sound

    # ── Weather sounds ──────────────────────────────────────────

    def _make_thunder(self):
        """Deep rumbling thunder crack."""
        duration = 0.8

        def generator(t, sr):
            import random
            # Low rumble base
            freq = 40 + 30 * math.sin(2 * math.pi * 3 * t)
            tone = math.sin(2 * math.pi * freq * t)
            # Add noise for crack texture
            noise = (random.random() * 2 - 1)
            # Initial crack then rumble
            if t < 0.1:
                mix = tone * 0.3 + noise * 0.7
            else:
                mix = tone * 0.6 + noise * 0.4
            env = self._envelope(t, duration, attack=0.01, decay=0.15, sustain=0.4, release=0.4)
            return mix * env * 0.7

        sound = self._make_sound(duration, generator)
        sound.set_volume(0.5)
        return sound

    def _make_rain_ambient(self):
        """Soft rain ambient loop - white noise with filtering."""
        duration = 2.0

        def generator(t, sr):
            import random
            noise = random.random() * 2 - 1
            # Gentle filtering with slow modulation
            mod = 0.5 + 0.5 * math.sin(2 * math.pi * 0.5 * t)
            return noise * mod * 0.15

        sound = self._make_sound(duration, generator)
        sound.set_volume(0.2)
        return sound

    def _make_wind_howl(self):
        """Howling wind for sandstorm/blizzard."""
        duration = 1.5

        def generator(t, sr):
            import random
            noise = random.random() * 2 - 1
            # Slow oscillating pitch for howl
            freq = 200 + 100 * math.sin(2 * math.pi * 1.5 * t)
            tone = math.sin(2 * math.pi * freq * t)
            env = self._envelope(t, duration, attack=0.1, decay=0.2, sustain=0.5, release=0.4)
            return (noise * 0.5 + tone * 0.5) * env * 0.25

        sound = self._make_sound(duration, generator)
        sound.set_volume(0.25)
        return sound

    def _make_fire_crackle(self):
        """Crackling fire sound for ash fall weather."""
        duration = 1.0

        def generator(t, sr):
            import random
            noise = random.random() * 2 - 1
            # Random crackle bursts
            crackle = noise * (0.3 + 0.7 * max(0, math.sin(2 * math.pi * random.uniform(5, 20) * t)))
            # Low hum base
            tone = math.sin(2 * math.pi * 80 * t) * 0.2
            env = self._envelope(t, duration, attack=0.05, decay=0.1, sustain=0.5, release=0.3)
            return (crackle * 0.7 + tone * 0.3) * env * 0.2

        sound = self._make_sound(duration, generator)
        sound.set_volume(0.2)
        return sound

    # Public play methods

    def play_sword_swing(self):
        """Play sword swing sound."""
        if self.sounds_enabled and 'sword_swing' in self.sounds:
            self.sounds['sword_swing'].play()

    def play_enemy_hit(self):
        """Play enemy hit sound."""
        if self.sounds_enabled and 'enemy_hit' in self.sounds:
            self.sounds['enemy_hit'].play()

    def play_enemy_death(self):
        """Play enemy death sound."""
        if self.sounds_enabled and 'enemy_death' in self.sounds:
            self.sounds['enemy_death'].play()

    def play_player_hurt(self):
        """Play player hurt sound."""
        if self.sounds_enabled and 'player_hurt' in self.sounds:
            self.sounds['player_hurt'].play()

    def play_heart_pickup(self):
        """Play heart pickup sound."""
        if self.sounds_enabled and 'heart_pickup' in self.sounds:
            self.sounds['heart_pickup'].play()

    def play_key_pickup(self):
        """Play key pickup sound."""
        if self.sounds_enabled and 'key_pickup' in self.sounds:
            self.sounds['key_pickup'].play()

    def play_boss_roar(self):
        """Play boss roar sound."""
        if self.sounds_enabled and 'boss_roar' in self.sounds:
            self.sounds['boss_roar'].play()

    def play_boss_death(self):
        """Play boss death sound."""
        if self.sounds_enabled and 'boss_death' in self.sounds:
            self.sounds['boss_death'].play()

    def play_dungeon_enter(self):
        """Play dungeon enter sound."""
        if self.sounds_enabled and 'dungeon_enter' in self.sounds:
            self.sounds['dungeon_enter'].play()

    def play_chest_open(self):
        """Play chest open sound."""
        if self.sounds_enabled and 'chest_open' in self.sounds:
            self.sounds['chest_open'].play()

    def play_gold_pickup(self):
        """Play gold coin pickup sound."""
        if self.sounds_enabled and 'gold_pickup' in self.sounds:
            self.sounds['gold_pickup'].play()

    def play_victory_fanfare(self):
        """Play victory fanfare after boss defeat."""
        if self.sounds_enabled and 'victory_fanfare' in self.sounds:
            self.sounds['victory_fanfare'].play()

    def play_push_block(self):
        """Play push block scraping sound."""
        if self.sounds_enabled and 'push_block' in self.sounds:
            self.sounds['push_block'].play()

    def play_switch_click(self):
        """Play switch/plate click sound."""
        if self.sounds_enabled and 'switch_click' in self.sounds:
            self.sounds['switch_click'].play()

    def play_torch_ignite(self):
        """Play torch ignite sound."""
        if self.sounds_enabled and 'torch_ignite' in self.sounds:
            self.sounds['torch_ignite'].play()

    def play_door_open(self):
        """Play door open sound."""
        if self.sounds_enabled and 'door_open' in self.sounds:
            self.sounds['door_open'].play()

    def play_ability_spin(self):
        """Play spin attack whoosh sound."""
        if self.sounds_enabled and 'ability_spin' in self.sounds:
            self.sounds['ability_spin'].play()

    def play_ability_dash(self):
        """Play dash swoosh sound."""
        if self.sounds_enabled and 'ability_dash' in self.sounds:
            self.sounds['ability_dash'].play()

    def play_ability_fire(self):
        """Play fire blast sound."""
        if self.sounds_enabled and 'ability_fire' in self.sounds:
            self.sounds['ability_fire'].play()

    def play_ability_shield(self):
        """Play shield activation sound."""
        if self.sounds_enabled and 'ability_shield' in self.sounds:
            self.sounds['ability_shield'].play()

    def play_ability_fail(self):
        """Play ability fail sound (not enough MP)."""
        if self.sounds_enabled and 'ability_fail' in self.sounds:
            self.sounds['ability_fail'].play()

    def play_parry_clang(self):
        """Play perfect parry metallic clang."""
        if self.sounds_enabled and 'parry_clang' in self.sounds:
            self.sounds['parry_clang'].play()

    def play_dodge_whoosh(self):
        """Play dodge roll whoosh."""
        if self.sounds_enabled and 'dodge_whoosh' in self.sounds:
            self.sounds['dodge_whoosh'].play()

    def play_charge_hum(self):
        """Play charge attack buildup hum."""
        if self.sounds_enabled and 'charge_hum' in self.sounds:
            self.sounds['charge_hum'].play()

    def play_combo_hit(self, hit_number):
        """Play combo hit sound for the given hit number (1, 2, or 3)."""
        key = f'combo_hit_{hit_number}'
        if self.sounds_enabled and key in self.sounds:
            self.sounds[key].play()

    def play_shield_block(self):
        """Play shield block thud."""
        if self.sounds_enabled and 'shield_block' in self.sounds:
            self.sounds['shield_block'].play()

    def play_room_clear(self):
        """Play room clear chime."""
        if self.sounds_enabled and 'room_clear' in self.sounds:
            self.sounds['room_clear'].play()

    def play_door_lock(self):
        """Play door lock sound."""
        if self.sounds_enabled and 'door_lock' in self.sounds:
            self.sounds['door_lock'].play()

    # Music playback methods

    def play_music(self, track_name):
        """
        Play a music track on loop.

        Args:
            track_name: Name of the track ('title', 'overworld', 'dungeon', 'forest', 'desert', 'volcano')
        """
        if not self.sounds_enabled:
            return

        # Don't restart if already playing this track
        if self._current_track == track_name and self._music_channel and self._music_channel.get_busy():
            return

        # Stop current music
        if self._music_channel:
            self._music_channel.stop()

        # Play new track
        if track_name in self._music_tracks:
            self._current_track = track_name
            sound = self._music_tracks[track_name]
            if sound:
                self._music_channel.play(sound, loops=-1)  # Loop infinitely
                self._music_channel.set_volume(self._music_volume)

    def stop_music(self):
        """Stop the current music with a short fade."""
        if self.sounds_enabled and self._music_channel:
            self._music_channel.fadeout(500)  # 500ms fade
            self._current_track = None

    def set_music_volume(self, volume):
        """
        Set music volume.

        Args:
            volume: Volume level (0.0 to 1.0)
        """
        self._music_volume = max(0.0, min(1.0, volume))
        if self.sounds_enabled and self._music_channel:
            self._music_channel.set_volume(self._music_volume)

    def set_sfx_volume(self, volume):
        """
        Set SFX volume for all sound effects.

        Args:
            volume: Volume level (0.0 to 1.0)
        """
        volume = max(0.0, min(1.0, volume))
        if self.sounds_enabled:
            for sound in self.sounds.values():
                if sound:
                    sound.set_volume(volume * 0.4)  # Scale relative to original volumes

    def get_music_volume(self):
        """Get current music volume (0.0 to 1.0)."""
        return self._music_volume

    def play_secret(self):
        """Play a secret discovery sound — ascending sparkle."""
        if self.sounds_enabled and 'key_pickup' in self.sounds:
            self.sounds['key_pickup'].play()


# Global sound manager instance
_sound_manager = None


def get_sound_manager():
    """Get or create the global SoundManager instance."""
    global _sound_manager
    if _sound_manager is None:
        _sound_manager = SoundManager()
    return _sound_manager
