import pygame
import os
import wave
import struct

class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {}
        self.music = {}
        self.current_music = None
        self.volume = 0.5
        
        # Create sounds directory if it doesn't exist
        os.makedirs("assets/audio", exist_ok=True)
        
        # Create placeholder sound effects
        self.create_placeholder_sounds()
        
        # Load sounds
        self.load_sounds()
        
    def create_placeholder_sounds(self):
        # Create a simple sine wave for placeholder sounds
        def create_sine_wave(frequency, duration, volume=0.5, output_file="temp.wav"):
            sample_rate = 44100
            num_samples = int(duration * sample_rate)
            
            # Create the wave file
            with wave.open(output_file, 'w') as wav_file:
                wav_file.setnchannels(1)  # Mono
                wav_file.setsampwidth(2)  # 2 bytes per sample
                wav_file.setframerate(sample_rate)
                
                # Generate sine wave
                for i in range(num_samples):
                    value = int(volume * 32767.0 * 
                              (i % (sample_rate / frequency)) / (sample_rate / frequency))
                    data = struct.pack('<h', value)
                    wav_file.writeframes(data)
        
        # Create jump sound (short, high pitch)
        jump_file = "assets/audio/jump.wav"
        create_sine_wave(440, 0.1, output_file=jump_file)  # 440 Hz for 0.1 seconds
        
        # Create collect sound (medium pitch)
        collect_file = "assets/audio/collect.wav"
        create_sine_wave(880, 0.2, output_file=collect_file)  # 880 Hz for 0.2 seconds
        
        # Create background music (longer, lower pitch)
        background_file = "assets/audio/background.wav"
        create_sine_wave(220, 1.0, output_file=background_file)  # 220 Hz for 1 second
    
    def load_sounds(self):
        # Load sound effects
        self.sounds['jump'] = pygame.mixer.Sound("assets/audio/jump.wav")
        self.sounds['collect'] = pygame.mixer.Sound("assets/audio/collect.wav")
        
        # Load music
        self.music['background'] = "assets/audio/background.wav"
        
        # Set volume for all sounds
        for sound in self.sounds.values():
            sound.set_volume(self.volume)
    
    def play_sound(self, sound_name):
        if sound_name in self.sounds:
            self.sounds[sound_name].play()
    
    def play_music(self, music_name, loop=-1):
        if music_name in self.music:
            if self.current_music != music_name:
                pygame.mixer.music.load(self.music[music_name])
                pygame.mixer.music.play(loop)
                self.current_music = music_name
    
    def stop_music(self):
        pygame.mixer.music.stop()
        self.current_music = None
    
    def set_volume(self, volume):
        self.volume = max(0.0, min(1.0, volume))
        for sound in self.sounds.values():
            sound.set_volume(self.volume)
        pygame.mixer.music.set_volume(self.volume) 