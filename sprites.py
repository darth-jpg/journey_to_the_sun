import pygame
import os
from utils import resource_path

# Ensure the assets directory exists
def ensure_assets_exist():
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Create assets directory if it doesn't exist
    assets_dir = os.path.join(current_dir, "assets")
    sprites_dir = os.path.join(assets_dir, "sprites")
    os.makedirs(sprites_dir, exist_ok=True)
    return sprites_dir

class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, position, sprite_sheet_path, frame_count, frame_delay=5):
        super().__init__()
        self.sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
        self.frame_width = self.sprite_sheet.get_width() // frame_count
        self.frame_height = self.sprite_sheet.get_height()
        self.frames = []
        self.frame_count = frame_count
        self.current_frame = 0
        self.frame_delay = frame_delay
        self.frame_counter = 0
        
        # Split sprite sheet into frames
        for i in range(frame_count):
            frame = pygame.Surface((self.frame_width, self.frame_height), pygame.SRCALPHA)
            frame.blit(self.sprite_sheet, (0, 0), (i * self.frame_width, 0, self.frame_width, self.frame_height))
            self.frames.append(frame)
        
        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = position
        self.facing_right = True

    def update(self):
        # Animation
        self.frame_counter += 1
        if self.frame_counter >= self.frame_delay:
            self.frame_counter = 0
            self.current_frame = (self.current_frame + 1) % self.frame_count
            self.image = self.frames[self.current_frame]
            
            # Flip sprite based on direction
            if not self.facing_right:
                self.image = pygame.transform.flip(self.image, True, False)

class RaquelSprite(AnimatedSprite):
    def __init__(self, position):
        # Ensure assets directory exists and get path
        sprites_dir = ensure_assets_exist()
        
        # Load the three walking animation frames
        self.walking_frames = []
        for i in range(3):
            try:
                frame = pygame.image.load(resource_path("assets", "sprites", f"raquel_walk_{i+1}.png")).convert_alpha()
                print(f"Loaded frame {i+1} with size: {frame.get_size()}")  # Debug info
                self.walking_frames.append(frame)
            except Exception as e:
                print(f"Error loading raquel_walk_{i+1}.png: {str(e)}")
                # Create a placeholder frame if image is missing
                frame = pygame.Surface((32, 32), pygame.SRCALPHA)
                pygame.draw.rect(frame, (255, 0, 0), (0, 0, 32, 32))
                self.walking_frames.append(frame)
        
        if not self.walking_frames:
            raise Exception("No walking frames could be loaded!")
            
        # Get the dimensions from the first frame
        frame_width = self.walking_frames[0].get_width()
        frame_height = self.walking_frames[0].get_height()
        
        # Create a sprite sheet from the frames
        sprite_sheet = pygame.Surface((frame_width * len(self.walking_frames), frame_height), pygame.SRCALPHA)
        for i, frame in enumerate(self.walking_frames):
            sprite_sheet.blit(frame, (i * frame_width, 0))
        
        # Save temporary sprite sheet (use temp dir when packaged)
        import tempfile
        temp_dir = tempfile.gettempdir()
        sprite_path = os.path.join(temp_dir, "raquel_sheet.png")
        pygame.image.save(sprite_sheet, sprite_path)
        
        super().__init__(position, sprite_path, len(self.walking_frames))
        self.is_moving = False
        self.frame_delay = 5  # Ajuste este valor para controlar a velocidade da animação
        
    def update(self):
        # Atualiza a animação baseada no movimento
        if self.is_moving:
            self.frame_counter += 1
            if self.frame_counter >= self.frame_delay:
                self.frame_counter = 0
                self.current_frame = (self.current_frame + 1) % self.frame_count
                self.image = self.frames[self.current_frame]
        else:
            # Mantém o primeiro frame quando parado
            self.image = self.frames[0]
            
        # Aplica o flip horizontal se necessário
        if not self.facing_right:
            self.image = pygame.transform.flip(self.image, True, False)
            
    def set_moving(self, moving):
        self.is_moving = moving

class RicardoSprite(AnimatedSprite):
    def __init__(self, position):
        # Ensure assets directory exists and get path
        sprites_dir = ensure_assets_exist()
        
        # Load the four Ricardo animation frames
        self.ricardo_frames = []
        for i in range(4):
            try:
                frame = pygame.image.load(resource_path("assets", "sprites", f"ricardo{i+1}.png")).convert_alpha()
                print(f"Loaded Ricardo frame {i+1} with size: {frame.get_size()}")  # Debug info
                self.ricardo_frames.append(frame)
            except Exception as e:
                print(f"Error loading ricardo{i+1}.png: {str(e)}")
                # Create a placeholder frame if image is missing
                frame = pygame.Surface((32, 32), pygame.SRCALPHA)
                pygame.draw.rect(frame, (0, 255, 0), (0, 0, 32, 32))  # Green placeholder
                self.ricardo_frames.append(frame)
        
        if not self.ricardo_frames:
            raise Exception("No Ricardo frames could be loaded!")
            
        # Get the dimensions from the first frame
        frame_width = self.ricardo_frames[0].get_width()
        frame_height = self.ricardo_frames[0].get_height()
        
        # Create a sprite sheet from the frames
        sprite_sheet = pygame.Surface((frame_width * len(self.ricardo_frames), frame_height), pygame.SRCALPHA)
        for i, frame in enumerate(self.ricardo_frames):
            sprite_sheet.blit(frame, (i * frame_width, 0))
        
        # Save temporary sprite sheet (use temp dir when packaged)
        import tempfile
        temp_dir = tempfile.gettempdir()
        sprite_path = os.path.join(temp_dir, "ricardo_sheet.png")
        pygame.image.save(sprite_sheet, sprite_path)
        
        super().__init__(position, sprite_path, len(self.ricardo_frames)) 