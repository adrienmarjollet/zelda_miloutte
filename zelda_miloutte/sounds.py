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

    def _make_note(self, frequency, duration, amplitude=0.5, warm=False):
        """
        Generate a single note with envelope.

        Args:
            frequency: Note frequency in Hz
            duration: Note duration in seconds
            amplitude: Base amplitude (0-1)
            warm: If True, use softer envelope and warmer harmonics

        Returns:
            array of samples
        """
        num_samples = int(duration * self.sample_rate)
        samples = array.array('h', [0] * num_samples)

        for i in range(num_samples):
            t = i / self.sample_rate
            # Base sine wave
            base = math.sin(2 * math.pi * frequency * t)
            if warm:
                # Warm tone: soft octave + gentle fifth for richness
                octave = 0.15 * math.sin(2 * math.pi * frequency * 2 * t)
                fifth = 0.08 * math.sin(2 * math.pi * frequency * 1.5 * t)
                tone = (base + octave + fifth) / 1.23
                env = self._envelope(t, duration, attack=0.08, decay=0.15, sustain=0.6, release=max(0.2, duration * 0.3))
            else:
                octave = 0.3 * math.sin(2 * math.pi * frequency * 2 * t)
                tone = (base + octave) / 1.3
                env = self._envelope(t, duration, attack=0.02, decay=0.05, sustain=0.8, release=0.1)

            # Clamp and convert to 16-bit signed integer
            value = tone * env * amplitude
            value = max(-1.0, min(1.0, value))
            samples[i] = int(value * 32767)

        return samples

    def _make_rest(self, duration):
        """Generate silence for a rest."""
        num_samples = int(duration * self.sample_rate)
        return array.array('h', [0] * num_samples)

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
        """Generate gentle, dreamy title screen music — slow arpeggios with breathing room."""
        # Slow, gentle arpeggio in C major with pauses — like a music box in a quiet forest
        # Uses longer note durations and rests for a contemplative feel
        notes = [
            (262, 0.6),   # C4
            (330, 0.6),   # E4
            (392, 0.8),   # G4 (linger)
            (0, 0.3),     # rest
            (523, 0.8),   # C5
            (392, 0.6),   # G4
            (330, 0.8),   # E4 (linger)
            (0, 0.4),     # rest
            (349, 0.6),   # F4
            (440, 0.6),   # A4
            (523, 0.8),   # C5
            (0, 0.3),     # rest
            (440, 0.6),   # A4
            (392, 0.8),   # G4 (resolve)
            (0, 0.6),     # longer rest — breathing space
            (330, 0.6),   # E4
            (294, 0.6),   # D4
            (262, 1.0),   # C4 (long resolve)
            (0, 0.8),     # rest
        ]

        note_arrays = []
        for freq, dur in notes:
            if freq == 0:
                note_arrays.append(self._make_rest(dur))
            else:
                note_arrays.append(self._make_note(freq, dur, amplitude=0.3, warm=True))

        sound = self._concatenate_notes(note_arrays)
        return sound

    def _generate_overworld_music(self):
        """Generate a gentle, pastoral overworld melody — unhurried and wistful."""
        # A slower, folk-like melody in G major — evokes open fields and soft wind
        # Think of it like a gentle flute over rolling hills
        notes = [
            (392, 0.5),   # G4
            (440, 0.5),   # A4
            (494, 0.7),   # B4
            (523, 0.9),   # C5 (linger)
            (0, 0.3),     # rest
            (494, 0.5),   # B4
            (440, 0.5),   # A4
            (392, 0.9),   # G4 (settle)
            (0, 0.4),     # rest
            (330, 0.5),   # E4
            (370, 0.5),   # F#4
            (392, 0.7),   # G4
            (440, 0.9),   # A4 (linger)
            (0, 0.3),     # rest
            (392, 0.5),   # G4
            (370, 0.5),   # F#4
            (330, 0.7),   # E4
            (294, 0.9),   # D4 (gentle fall)
            (0, 0.5),     # rest
            (262, 0.5),   # C4
            (294, 0.5),   # D4
            (330, 0.7),   # E4
            (392, 1.0),   # G4 (long resolve)
            (0, 0.7),     # rest — let it breathe
        ]

        note_arrays = []
        for freq, dur in notes:
            if freq == 0:
                note_arrays.append(self._make_rest(dur))
            else:
                note_arrays.append(self._make_note(freq, dur, amplitude=0.28, warm=True))

        sound = self._concatenate_notes(note_arrays)
        return sound

    def _generate_dungeon_music(self):
        """Generate a haunting, slow dungeon theme — sparse and eerie."""
        # Sparse, low notes in C minor with long rests — footsteps in an empty corridor
        notes = [
            (196, 0.8),   # G3
            (0, 0.5),     # rest
            (233, 0.8),   # Bb3
            (262, 1.0),   # C4 (linger)
            (0, 0.6),     # rest
            (311, 0.8),   # Eb4
            (262, 0.6),   # C4
            (233, 1.0),   # Bb3 (settle)
            (0, 0.7),     # rest
            (196, 0.8),   # G3
            (175, 0.6),   # F3
            (196, 1.2),   # G3 (long, hollow)
            (0, 0.8),     # rest
            (262, 0.6),   # C4
            (247, 0.6),   # B3 (chromatic tension)
            (233, 0.8),   # Bb3
            (196, 1.2),   # G3 (resolve low)
            (0, 1.0),     # long rest — silence is part of the music
        ]

        note_arrays = []
        for freq, dur in notes:
            if freq == 0:
                note_arrays.append(self._make_rest(dur))
            else:
                note_arrays.append(self._make_note(freq, dur, amplitude=0.25, warm=True))

        sound = self._concatenate_notes(note_arrays)
        return sound

    def _generate_forest_music(self):
        """Generate eerie, minor key forest theme — slower tempo with longer notes."""
        # E minor scale, eerie and mysterious with longer note durations
        notes = [
            (165, 0.9),   # E3 (long)
            (196, 0.7),   # G3
            (220, 0.8),   # A3
            (0, 0.4),     # rest
            (247, 0.9),   # B3 (long)
            (220, 0.7),   # A3
            (196, 0.8),   # G3
            (0, 0.5),     # rest
            (165, 0.7),   # E3
            (185, 0.7),   # F#3
            (196, 0.9),   # G3 (linger)
            (0, 0.4),     # rest
            (220, 0.8),   # A3
            (196, 0.7),   # G3
            (165, 1.0),   # E3 (resolve low)
            (0, 0.7),     # rest
            (196, 0.8),   # G3
            (220, 0.7),   # A3
            (247, 0.9),   # B3
            (262, 1.0),   # C4 (long)
            (0, 0.5),     # rest
            (247, 0.7),   # B3
            (196, 0.8),   # G3
            (165, 1.1),   # E3 (long resolve)
            (0, 0.8),     # long rest
        ]

        note_arrays = []
        for freq, dur in notes:
            if freq == 0:
                note_arrays.append(self._make_rest(dur))
            else:
                note_arrays.append(self._make_note(freq, dur, amplitude=0.26, warm=True))

        sound = self._concatenate_notes(note_arrays)
        return sound

    def _generate_desert_music(self):
        """Generate sparse, percussive desert theme — staccato notes with exotic scale."""
        # Harmonic minor feel (exotic), shorter durations, more rests
        notes = [
            (220, 0.4),   # A3 (short)
            (0, 0.3),     # rest
            (233, 0.4),   # Bb3 (short)
            (0, 0.3),     # rest
            (277, 0.5),   # C#4
            (311, 0.6),   # Eb4
            (0, 0.4),     # rest
            (330, 0.5),   # E4
            (277, 0.4),   # C#4
            (0, 0.3),     # rest
            (233, 0.5),   # Bb3
            (220, 0.6),   # A3 (settle)
            (0, 0.5),     # rest
            (196, 0.4),   # G3
            (0, 0.3),     # rest
            (220, 0.4),   # A3
            (0, 0.3),     # rest
            (247, 0.5),   # B3
            (277, 0.6),   # C#4
            (0, 0.4),     # rest
            (311, 0.5),   # Eb4
            (277, 0.4),   # C#4
            (0, 0.3),     # rest
            (247, 0.5),   # B3
            (220, 0.7),   # A3 (resolve)
            (0, 0.6),     # rest
        ]

        note_arrays = []
        for freq, dur in notes:
            if freq == 0:
                note_arrays.append(self._make_rest(dur))
            else:
                note_arrays.append(self._make_note(freq, dur, amplitude=0.27, warm=False))

        sound = self._concatenate_notes(note_arrays)
        return sound

    def _generate_volcano_music(self):
        """Generate ominous, aggressive volcano theme — low register C minor with heavy feel."""
        # Low, ominous C minor with short rests and aggressive feel
        notes = [
            (131, 0.7),   # C3 (low, heavy)
            (0, 0.2),     # short rest
            (147, 0.6),   # D3
            (156, 0.8),   # Eb3 (linger)
            (0, 0.3),     # rest
            (175, 0.7),   # F3
            (156, 0.6),   # Eb3
            (147, 0.8),   # D3
            (131, 0.9),   # C3 (resolve low)
            (0, 0.4),     # rest
            (196, 0.6),   # G3
            (175, 0.6),   # F3
            (156, 0.7),   # Eb3
            (0, 0.3),     # rest
            (147, 0.6),   # D3
            (131, 0.8),   # C3 (heavy)
            (0, 0.3),     # rest
            (117, 0.9),   # Bb2 (very low)
            (131, 0.8),   # C3
            (0, 0.3),     # rest
            (147, 0.6),   # D3
            (156, 0.7),   # Eb3
            (175, 0.8),   # F3
            (0, 0.3),     # rest
            (196, 0.7),   # G3
            (175, 0.6),   # F3
            (131, 1.0),   # C3 (long, heavy resolve)
            (0, 0.5),     # rest
        ]

        note_arrays = []
        for freq, dur in notes:
            if freq == 0:
                note_arrays.append(self._make_rest(dur))
            else:
                note_arrays.append(self._make_note(freq, dur, amplitude=0.29, warm=False))

        sound = self._concatenate_notes(note_arrays)
        return sound

    def _generate_boss_music(self):
        """Generate intense, fast-paced boss battle theme — aggressive D minor."""
        notes = [
            (147, 0.3),   # D3 (fast)
            (0, 0.1),
            (175, 0.3),   # F3
            (196, 0.4),   # G3
            (0, 0.1),
            (220, 0.3),   # A3
            (233, 0.4),   # Bb3 (tension)
            (220, 0.3),   # A3
            (196, 0.3),   # G3
            (0, 0.1),
            (175, 0.4),   # F3
            (147, 0.5),   # D3 (resolve)
            (0, 0.2),
            (131, 0.3),   # C3
            (147, 0.3),   # D3
            (175, 0.3),   # F3
            (0, 0.1),
            (196, 0.4),   # G3
            (220, 0.3),   # A3
            (233, 0.4),   # Bb3
            (0, 0.1),
            (262, 0.5),   # C4 (peak)
            (233, 0.3),   # Bb3
            (220, 0.3),   # A3
            (196, 0.3),   # G3
            (0, 0.1),
            (175, 0.3),   # F3
            (147, 0.6),   # D3 (heavy resolve)
            (0, 0.3),
        ]

        note_arrays = []
        for freq, dur in notes:
            if freq == 0:
                note_arrays.append(self._make_rest(dur))
            else:
                note_arrays.append(self._make_note(freq, dur, amplitude=0.32, warm=False))
        return self._concatenate_notes(note_arrays)

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

    def play_victory_fanfare(self):
        """Play victory fanfare after boss defeat."""
        if self.sounds_enabled and 'victory_fanfare' in self.sounds:
            self.sounds['victory_fanfare'].play()

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


# Global sound manager instance
_sound_manager = None


def get_sound_manager():
    """Get or create the global SoundManager instance."""
    global _sound_manager
    if _sound_manager is None:
        _sound_manager = SoundManager()
    return _sound_manager
