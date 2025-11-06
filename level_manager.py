import pygame
import os
import random
from game_objects import Platform, AnimatedObstacle, AnimatedCollectible, AnimatedKey, LightSource, Water, Obstacle, Door

# Importa as constantes de dimensão da tela
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

class FinalGoal(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Carregar as imagens da estrela animada
        self.star_imgs = [pygame.image.load(os.path.join("assets", "sprites", f"star_{i}.png")).convert_alpha() for i in range(4)]
        self.current_frame = 0
        self.frame_count = 0
        self.frame_delay = 10
        self.image = self.star_imgs[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def update(self):
        self.frame_count += 1
        if self.frame_count >= self.frame_delay:
            self.current_frame = (self.current_frame + 1) % len(self.star_imgs)
            self.frame_count = 0
        self.image = self.star_imgs[self.current_frame]

class Level:
    def __init__(self, level_length=54000, scroll_speed=5):
        self.platforms = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        self.collectibles = pygame.sprite.Group()
        self.light_sources = pygame.sprite.Group()
        self.water = None
        self.level_length = level_length
        self.scroll_speed = scroll_speed
        self.final_goal = None
        self.ricardo = None
        self.generate_runner_level()

    def generate_intro_level(self):
        self.platforms.empty()
        self.obstacles.empty()
        self.collectibles.empty()
        self.platform_list = []
        # Plataformas baseadas nas linhas vermelhas da imagem
        plataformas = [
            Platform(0, 700, 1280, 30),      # chão
            Platform(120, 600, 800, 30),     # 2ª linha (mais baixa)
            Platform(700, 500, 500, 30),     # 3ª linha (mais baixa)
            Platform(100, 400, 700, 30),     # 4ª linha (mais baixa)
            Platform(600, 300, 600, 30),     # 5ª linha (mais baixa)
        ]
        for p in plataformas:
            self.platforms.add(p)
            self.platform_list.append(p)
        # Obstáculos animados (um em cada plataforma, velocidade menor)
        for plat in self.platform_list[1:]:
            self.obstacles.add(AnimatedObstacle(
                plat.rect.x + 60, plat.rect.y - 30, 40, 30,
                left_limit=plat.rect.left, right_limit=plat.rect.right, speed=1
            ))
        # Chave (colecionável) na 4ª plataforma
        plat = self.platform_list[3]
        self.collectibles.add(AnimatedKey(plat.rect.x + 100, plat.rect.y - 70))
        # Porta preta por cima da última plataforma (topo)
        plat = self.platform_list[-1]
        self.door = Door(plat.rect.right - 80, plat.rect.y - 60)  # ainda mais baixa
        self.door_group = pygame.sprite.Group()
        self.door_group.add(self.door)
        # Sem água, sem objetivo final neste nível
        self.water = None
        self.final_goal = None
        self.ricardo = None

    def generate_runner_level(self):
        ground_y = SCREEN_HEIGHT - 80
        self.platforms.empty()
        self.obstacles.empty()
        self.collectibles.empty()
        self.platform_list = []
        # Plataformas em segmentos (estilo escada/S)
        plataformas = [
            Platform(0, 650, 300, 30),    # início
            Platform(250, 550, 300, 30),  # sobe
            Platform(500, 450, 300, 30),  # desce
            Platform(800, 350, 300, 30),  # sobe
            Platform(1050, 250, 230, 30) # topo
        ]
        for p in plataformas:
            self.platforms.add(p)
            self.platform_list.append(p)
        # Obstáculos: associar cada um à plataforma correta
        plataformas_list = list(self.platforms.sprites())
        # 1º obstáculo na 4ª plataforma
        p = plataformas_list[3]
        self.obstacles.add(AnimatedObstacle(
            p.rect.x + 20, p.rect.y - 30, 40, 30,
            left_limit=p.rect.left, right_limit=p.rect.right, speed=1
        ))
        # 2º obstáculo na 2ª plataforma
        p = plataformas_list[1]
        self.obstacles.add(AnimatedObstacle(
            p.rect.x + 50, p.rect.y - 30, 40, 30,
            left_limit=p.rect.left, right_limit=p.rect.right, speed=1
        ))
        # 3º obstáculo na 3ª plataforma
        p = plataformas_list[2]
        self.obstacles.add(AnimatedObstacle(
            p.rect.x + 80, p.rect.y - 30, 40, 30,
            left_limit=p.rect.left, right_limit=p.rect.right, speed=1
        ))
        # Colecionáveis
        self.collectibles.add(AnimatedCollectible(270, 500))
        self.collectibles.add(AnimatedCollectible(750, 420))
        # Mover o colecionável da última plataforma para a 4ª plataforma
        p = plataformas_list[3]
        self.collectibles.add(AnimatedCollectible(p.rect.x + 120, p.rect.y - 30))
        # Água no fundo
        self.water = Water(0, SCREEN_HEIGHT - 24, SCREEN_WIDTH, tile_height=24)
        # Objetivo final e Ricardo
        self.final_goal = FinalGoal(1200, 200)
        self.ricardo = None  # Será adicionado no final do jogo
        # Plataforma extra para o final (centro superior)
        self.final_platform_x = 400
        self.final_platform_y = 120
        self.final_platform_width = 480
        self.final_platform_height = 30
        self.final_platform = Platform(self.final_platform_x, self.final_platform_y, self.final_platform_width, self.final_platform_height)
        self.platforms.add(self.final_platform)
        self.platform_list.append(self.final_platform)

    def get_all_sprites(self):
        all_sprites = []
        all_sprites.extend(self.platforms.sprites())
        all_sprites.extend(self.obstacles.sprites())
        all_sprites.extend(self.collectibles.sprites())
        if hasattr(self, 'door_group'):
            all_sprites.extend(self.door_group.sprites())
        if self.water:
            all_sprites.append(self.water)
        if self.final_goal:
            all_sprites.append(self.final_goal)
        if self.ricardo:
            all_sprites.append(self.ricardo)
        return all_sprites

    def update(self, scroll=0):
        # Move tudo para a esquerda/direita (scroll) apenas se scroll != 0
        if scroll != 0:
            for platform in self.platforms:
                platform.rect.x -= scroll
            for obstacle in self.obstacles:
                obstacle.rect.x -= scroll
            for collectible in self.collectibles:
                collectible.rect.x -= scroll
            if self.water:
                self.water.rect.x -= scroll
            if self.final_goal:
                self.final_goal.rect.x -= scroll
            if self.ricardo:
                self.ricardo.rect.x -= scroll
        # Atualiza animações
        self.obstacles.update()
        self.collectibles.update()
        if self.final_goal:
            self.final_goal.update()
        if self.water:
            self.water.update()
        if self.ricardo:
            self.ricardo.update()
        if hasattr(self, 'door_group'):
            self.door_group.update() 