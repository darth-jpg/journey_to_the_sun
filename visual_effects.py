import pygame
import math
import random
import os

class ParallaxBackground:
    def __init__(self, screen_width, screen_height, image_path=None):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.layers = []
        self.scroll = 0
        self.static_image = None
        if image_path:
            try:
                img = pygame.image.load(image_path).convert()
                self.static_image = pygame.transform.scale(img, (screen_width, screen_height))
            except Exception as e:
                print(f"Erro ao carregar background: {e}")
        else:
            self.background = pygame.Surface((screen_width, screen_height))
            self.create_gradient()
    def create_gradient(self):
        for y in range(self.screen_height):
            progress = y / self.screen_height
            r = int(10 + (40 * progress))
            g = int(10 + (0 * progress))
            b = int(30 + (50 * progress))
            pygame.draw.line(self.background, (r, g, b), (0, y), (self.screen_width, y))
    def add_layer(self, image, scroll_speed):
        self.layers.append({"image": image, "scroll_speed": scroll_speed})
    def update(self, player_movement):
        self.scroll += player_movement
    def draw(self, screen):
        if self.static_image:
            screen.blit(self.static_image, (0, 0))
        else:
            screen.blit(self.background, (0, 0))
            for layer in self.layers:
                x = -(self.scroll * layer["scroll_speed"]) % self.screen_width
                screen.blit(layer["image"], (x, 0))
                screen.blit(layer["image"], (x - self.screen_width, 0))

class ParticleSystem:
    def __init__(self):
        self.particles = []
        
    def create_particle(self, x, y, color, velocity, lifetime, size):
        self.particles.append({
            "x": x,
            "y": y,
            "color": color,
            "velocity": velocity,
            "lifetime": lifetime,
            "size": size,
            "age": 0
        })
        
    def create_collection_effect(self, x, y):
        for _ in range(20):
            angle = math.radians(random.randint(0, 360))
            speed = random.uniform(2, 5)
            velocity = [math.cos(angle) * speed, math.sin(angle) * speed]
            self.create_particle(
                x, y,
                (255, 215, 0),  # Gold color
                velocity,
                30,  # Lifetime in frames
                random.randint(2, 4)  # Size
            )
            
    def update(self):
        # Update and remove dead particles
        self.particles = [p for p in self.particles if p["age"] < p["lifetime"]]
        for p in self.particles:
            p["x"] += p["velocity"][0]
            p["y"] += p["velocity"][1]
            p["age"] += 1
            
    def draw(self, screen):
        for p in self.particles:
            alpha = 255 * (1 - p["age"] / p["lifetime"])
            color = (*p["color"], int(alpha))
            surf = pygame.Surface((p["size"] * 2, p["size"] * 2), pygame.SRCALPHA)
            pygame.draw.circle(surf, color, (p["size"], p["size"]), p["size"])
            screen.blit(surf, (p["x"] - p["size"], p["y"] - p["size"]))

class DialogueBox:
    def __init__(self, width, height, font_size=36):
        self.width = width
        self.height = height
        self.font = pygame.font.Font(None, font_size)
        self.target_alpha = 255
        self.current_alpha = 0
        self.fade_speed = 15
        
    def create_box_surface(self, speaker, text):
        surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        
        # Create semi-transparent background
        background = pygame.Surface((self.width, self.height))
        background.fill((30, 30, 50))
        background.set_alpha(200)
        surface.blit(background, (0, 0))
        
        # Add border
        pygame.draw.rect(surface, (255, 255, 255), 
                        surface.get_rect(), 2)
        
        # Render text
        speaker_text = self.font.render(speaker + ":", True, (255, 215, 0))
        dialogue_text = self.font.render(text, True, (255, 255, 255))
        
        # Position text
        surface.blit(speaker_text, (20, 20))
        surface.blit(dialogue_text, (20, 60))
        
        return surface
        
    def update(self):
        if self.current_alpha < self.target_alpha:
            self.current_alpha = min(self.current_alpha + self.fade_speed, 
                                   self.target_alpha)
        
    def draw(self, screen, speaker, text, pos):
        box_surface = self.create_box_surface(speaker, text)
        box_surface.set_alpha(self.current_alpha)
        screen.blit(box_surface, pos) 