import pygame
import os

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        tile_path = os.path.join("assets", "sprites", "crate_tile.png")
        tile_img = pygame.image.load(tile_path).convert_alpha()
        tile_w, tile_h = tile_img.get_size()
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        # Preencher a plataforma com o tile
        for i in range(0, width, tile_w):
            for j in range(0, height, tile_h):
                self.image.blit(tile_img, (i, j))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((255, 0, 0))  # Red color for obstacles
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class LightSource(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Animação das estrelas
        self.star_imgs = [pygame.image.load(os.path.join("assets", "sprites", f"star_{i}.png")).convert_alpha() for i in range(4)]
        self.current_frame = 0
        self.frame_count = 0
        self.frame_delay = 10
        self.image = self.star_imgs[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.radius = 150  # Light radius
    def update(self):
        self.frame_count += 1
        if self.frame_count >= self.frame_delay:
            self.current_frame = (self.current_frame + 1) % len(self.star_imgs)
            self.frame_count = 0
        self.image = self.star_imgs[self.current_frame]

class AnimatedCollectible(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Carregar as imagens da joia animada
        self.gem_imgs = [pygame.image.load(os.path.join("assets", "sprites", f"gem_{i}.png")).convert_alpha() for i in range(4)]
        self.current_frame = 0
        self.frame_count = 0
        self.frame_delay = 10
        self.image = self.gem_imgs[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.collected = False
    def update(self):
        self.frame_count += 1
        if self.frame_count >= self.frame_delay:
            self.current_frame = (self.current_frame + 1) % len(self.gem_imgs)
            self.frame_count = 0
        self.image = self.gem_imgs[self.current_frame]

class AnimatedKey(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Carregar as imagens da chave animada
        self.key_imgs = [pygame.image.load(os.path.join("assets", "sprites", f"key_{i}.png")).convert_alpha() for i in range(4)]
        self.current_frame = 0
        self.frame_count = 0
        self.frame_delay = 10
        self.image = self.key_imgs[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.collected = False
    def update(self):
        self.frame_count += 1
        if self.frame_count >= self.frame_delay:
            self.current_frame = (self.current_frame + 1) % len(self.key_imgs)
            self.frame_count = 0
        self.image = self.key_imgs[self.current_frame]

class AnimatedObstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, left_limit=None, right_limit=None, speed=2):
        super().__init__()
        self.frames = [pygame.transform.scale(
            pygame.image.load(os.path.join("assets", "sprites", f"obstacle_{i}.png")).convert_alpha(),
            (width, height)
        ) for i in range(4)]
        self.current_frame = 0
        self.frame_count = 0
        self.frame_delay = 10
        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        # Movimento horizontal
        self.left_limit = left_limit if left_limit is not None else x - 50
        self.right_limit = right_limit if right_limit is not None else x + 50
        self.speed = speed
        self.direction = 1  # 1: direita, -1: esquerda
    def update(self):
        # Animação
        self.frame_count += 1
        if self.frame_count >= self.frame_delay:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.frame_count = 0
        self.image = self.frames[self.current_frame]
        # Movimento horizontal
        self.rect.x += self.speed * self.direction
        if self.rect.right >= self.right_limit:
            self.rect.right = self.right_limit
            self.direction = -1
        elif self.rect.left <= self.left_limit:
            self.rect.left = self.left_limit
            self.direction = 1

class Water(pygame.sprite.Sprite):
    def __init__(self, x, y, width, tile_height=32):
        super().__init__()
        self.frames = []
        self.current_frame = 0
        self.frame_delay = 8
        self.frame_counter = 0
        self.tile_width = 32
        self.tile_height = tile_height

        # Carrega os 4 frames reais dos PNGs
        for i in range(4):
            try:
                image_path = f"assets/sprites/water_{i+1}.png"
                frame = pygame.image.load(image_path).convert_alpha()
                frame = pygame.transform.scale(frame, (self.tile_width, self.tile_height))
                self.frames.append(frame)
            except Exception as e:
                print(f"Erro ao carregar {image_path}: {e}")
                # Não adiciona frame de fallback
                pass

        # Se não carregou nenhum frame, adiciona um frame transparente
        if not self.frames:
            frame = pygame.Surface((self.tile_width, self.tile_height), pygame.SRCALPHA)
            self.frames.append(frame)

        # Cria uma superfície para a água que se repete
        self.image = pygame.Surface((width, self.tile_height), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = width
        self.height = self.tile_height

    def update(self):
        self.frame_counter += 1
        if self.frame_counter >= self.frame_delay:
            self.frame_counter = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)
        self.image.fill((0, 0, 0, 0))
        current_x = 0
        while current_x < self.width:
            self.image.blit(self.frames[self.current_frame], (current_x, 0))
            current_x += self.tile_width

    def draw(self, surface):
        surface.blit(self.image, self.rect) 

class Door(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Carregar os 4 frames da porta fechada
        self.closed_frames = []
        for i in range(4):
            try:
                frame = pygame.image.load(os.path.join("assets", "sprites", f"doorclosed_{i}.png")).convert_alpha()
                self.closed_frames.append(frame)
            except Exception as e:
                print(f"Erro ao carregar doorclosed_{i}.png: {e}")
                # Frame de fallback se não conseguir carregar
                frame = pygame.Surface((60, 80), pygame.SRCALPHA)
                frame.fill((50, 50, 50))
                pygame.draw.rect(frame, (200, 200, 200), (0, 0, 60, 80), 4)
                self.closed_frames.append(frame)
        
        # Frame da porta aberta
        try:
            self.open_frame = pygame.image.load(os.path.join("assets", "sprites", "dooropen00.png")).convert_alpha()
        except Exception as e:
            print(f"Erro ao carregar dooropen00.png: {e}")
            # Frame de fallback se não conseguir carregar
            self.open_frame = pygame.Surface((60, 80), pygame.SRCALPHA)
            self.open_frame.fill((0, 0, 0, 0))  # Totalmente transparente
        
        self.is_open = False
        self.current_frame = 0
        self.frame_count = 0
        self.frame_delay = 15  # Velocidade da animação
        
        self.image = self.closed_frames[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def update(self):
        if not self.is_open:
            # Animar a porta fechada
            self.frame_count += 1
            if self.frame_count >= self.frame_delay:
                self.frame_count = 0
                self.current_frame = (self.current_frame + 1) % len(self.closed_frames)
                self.image = self.closed_frames[self.current_frame]
        else:
            # Porta aberta (transparente)
            self.image = self.open_frame
    
    def open(self):
        self.is_open = True
        self.image = self.open_frame
    
    def close(self):
        self.is_open = False
        self.current_frame = 0
        self.image = self.closed_frames[0] 