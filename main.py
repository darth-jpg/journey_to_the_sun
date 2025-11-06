import pygame
import sys
import os
from game_objects import Platform, Obstacle, LightSource
from story import Dialogue, StoryProgress
from level_manager import Level
from sprites import RaquelSprite, RicardoSprite
from sound_manager import SoundManager
from lighting import LightingSystem
from visual_effects import ParallaxBackground, ParticleSystem, DialogueBox
from utils import resource_path

# Inicialize o mixer ANTES do pygame.init()
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()

# Constants
START_SCREEN_WIDTH = 810
START_SCREEN_HEIGHT = 540
GAME_SCREEN_WIDTH = 1280
GAME_SCREEN_HEIGHT = 720
SCREEN_WIDTH = START_SCREEN_WIDTH
SCREEN_HEIGHT = START_SCREEN_HEIGHT
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GOLD = (255, 215, 0)
DARK_BLUE = (10, 10, 30)  # Cor de fundo mais suave

# Create the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Raquel's Journey to the Sun")
clock = pygame.time.Clock()

# No início do seu main.py, depois de criar a janela:
music_path = resource_path("assets", "audio", "background_music.ogg")
pygame.mixer.music.load(music_path)
pygame.mixer.music.set_volume(0.25)  # Volume reduzido para 25%
pygame.mixer.music.play(-1)  # -1 faz a música repetir para sempre

class Player(RaquelSprite):
    def __init__(self):
        super().__init__((100, SCREEN_HEIGHT - 100))
        self.velocity_y = 0
        self.jumping = False
        self.speed = 5
        self.on_ground = False
        self.last_x = self.rect.x
        self.move_left_pressed = False
        self.move_right_pressed = False
        self.invincible_timer = 0

    def update(self, platforms):
        self.last_x = self.rect.x
        # Movimento controlado pelo jogador
        if self.move_left_pressed:
            self.rect.x -= self.speed
        if self.move_right_pressed:
            self.rect.x += self.speed
        # Gravity
        self.velocity_y += 0.8
        self.rect.y += self.velocity_y
        # Platform collisions
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.velocity_y > 0:  # Falling
                    self.rect.bottom = platform.rect.top
                    self.velocity_y = 0
                    self.on_ground = True
                elif self.velocity_y < 0:  # Jumping
                    self.rect.top = platform.rect.bottom
                    self.velocity_y = 0
        # Keep player on screen (horizontal e vertical)
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
        # Update sprite animation
        super().update()
        
    def get_movement(self):
        return self.rect.x - self.last_x

    def jump(self):
        if self.on_ground:
            self.velocity_y = -15
            self.jumping = True
            self.on_ground = False

    def move_left(self):
        self.rect.x -= self.speed
        self.facing_right = False
        self.set_moving(True)

    def move_right(self):
        self.rect.x += self.speed
        self.facing_right = True
        self.set_moving(True)
        
    def stop_moving(self):
        self.set_moving(False)

class Game:
    def __init__(self):
        self.state = "start"
        self.menu_options = ["Start", "Exit"]
        self.selected_option = 0
        self.player = Player()
        self.story = StoryProgress()
        self.dialogue = Dialogue()
        self.current_level = None
        self.ricardo = None
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)
        self.show_dialogue = True
        self.current_dialogue = self.dialogue.get_dialogue("start")
        self.game_completed = False
        self.lighting = LightingSystem(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.background_night = pygame.image.load(resource_path("assets", "sprites", "background_night.png")).convert()
        self.background_night = pygame.transform.scale(self.background_night, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.background_day = pygame.image.load(resource_path("assets", "sprites", "background_day.png")).convert()
        self.background_day = pygame.transform.scale(self.background_day, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.particles = ParticleSystem()
        self.dialogue_box = DialogueBox(SCREEN_WIDTH - 100, 150)
        self.start_time = pygame.time.get_ticks()
        self.time_limit = 210
        self.time_up = False
        self.dialogue_shown_in_playing = False
        self.has_gem = False

    def start_intro_level(self):
        global screen, SCREEN_WIDTH, SCREEN_HEIGHT
        SCREEN_WIDTH = GAME_SCREEN_WIDTH
        SCREEN_HEIGHT = GAME_SCREEN_HEIGHT
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.current_level = Level()
        self.current_level.generate_intro_level()
        # Posição inicial: mais à esquerda, em cima da primeira plataforma
        first_platform = self.current_level.platform_list[0]
        self.player.rect.x = first_platform.rect.x + 40
        self.player.rect.bottom = first_platform.rect.top
        self.has_gem = False
        self.ricardo = None
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)
        self.all_sprites.add(*self.current_level.get_all_sprites())
        self.state = "playing"
        self.show_dialogue = False
        self.dialogue_shown_in_playing = True

    def start_final_level(self):
        global screen, SCREEN_WIDTH, SCREEN_HEIGHT
        SCREEN_WIDTH = GAME_SCREEN_WIDTH
        SCREEN_HEIGHT = GAME_SCREEN_HEIGHT
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.current_level = Level()
        self.current_level.generate_runner_level()
        self.player.rect.x = 100
        self.player.rect.y = SCREEN_HEIGHT - 100
        self.has_gem = False
        self.ricardo = None
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)
        self.all_sprites.add(*self.current_level.get_all_sprites())
        self.state = "playing"
        self.show_dialogue = False
        self.dialogue_shown_in_playing = True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if self.state == "start":
                    if event.key == pygame.K_UP:
                        self.selected_option = (self.selected_option - 1) % len(self.menu_options)
                    elif event.key == pygame.K_DOWN:
                        self.selected_option = (self.selected_option + 1) % len(self.menu_options)
                    elif event.key == pygame.K_RETURN:
                        if self.selected_option == 0:  # Start
                            self.start_intro_level()
                            return True
                        elif self.selected_option == 1:  # Exit
                            return False
                elif self.state == "playing":
                    if event.key == pygame.K_SPACE:
                        self.player.jump()
                    elif event.key == pygame.K_LEFT:
                        self.player.move_left_pressed = True
                    elif event.key == pygame.K_RIGHT:
                        self.player.move_right_pressed = True
                    elif event.key == pygame.K_RETURN:
                        # Só avança diálogo se estiver a ser mostrado
                        if self.show_dialogue:
                            self.show_dialogue = False

                elif self.state == "game_over":
                    if event.key == pygame.K_RETURN:
                        self.state = "start"
            elif event.type == pygame.KEYUP:
                if self.state == "playing":
                    if event.key == pygame.K_LEFT:
                        self.player.move_left_pressed = False
                    elif event.key == pygame.K_RIGHT:
                        self.player.move_right_pressed = False
        return True

    def update(self):
        if self.state == "start":
            return
        if self.state == "game_over":
            return
        elapsed = (pygame.time.get_ticks() - self.start_time) / 1000
        time_left = max(0, int(self.time_limit - elapsed))
        if time_left == 0 and not self.time_up:
            self.time_up = True
            self.show_dialogue = True
            self.current_dialogue = {"speaker": "Narrador", "text": "O tempo acabou! Tenta novamente."}
            self.state = "game_over"
            return
        is_moving = False
        if self.player.move_right_pressed:
            self.player.rect.x += self.player.speed
            is_moving = True
        if self.player.move_left_pressed:
            self.player.rect.x -= self.player.speed
            is_moving = True
        self.player.set_moving(is_moving)
        self.current_level.update(0)
        self.player.update(self.current_level.platforms)
        # Lógica do nível inicial
        if hasattr(self.current_level, 'door'):
            for collectible in self.current_level.collectibles:
                if self.player.rect.colliderect(collectible.rect) and not collectible.collected:
                    collectible.collected = True
                    self.has_gem = True
                    self.current_level.door.open()
                    self.particles.create_collection_effect(
                        collectible.rect.centerx,
                        collectible.rect.centery
                    )
                    collectible.kill()
            if self.current_level.door.is_open and self.player.rect.colliderect(self.current_level.door.rect):
                # Avança para o nível final
                self.start_final_level()
                return
        # Lógica do nível final (restante igual)
        # Check for collectible collisions
        for collectible in self.current_level.collectibles:
            if self.player.rect.colliderect(collectible.rect) and not collectible.collected:
                collectible.collected = True
                self.story.update_progress(collectible_found=True)
                self.particles.create_collection_effect(
                    collectible.rect.centerx,
                    collectible.rect.centery
                )
                collectible.kill()
        # Check for obstacle collisions
        for obstacle in self.current_level.obstacles:
            if self.player.rect.colliderect(obstacle.rect):
                self.safe_reset_player()
        # Check for water collision
        if self.current_level.water and self.player.rect.colliderect(self.current_level.water.rect):
            self.safe_reset_player()
        # Check for final goal
        if self.current_level.final_goal and self.player.rect.colliderect(self.current_level.final_goal.rect):
            # Mover Raquel e Ricardo para a plataforma final
            final_plat = self.current_level.final_platform
            self.player.rect.midbottom = (final_plat.rect.centerx - 40, final_plat.rect.top)
            self.player.move_left_pressed = False
            self.player.move_right_pressed = False
            from sprites import RicardoSprite
            self.current_level.ricardo = RicardoSprite((final_plat.rect.centerx + 40, final_plat.rect.top - 96))
            # Remover a estrela final para não repetir
            self.current_level.final_goal = None
            # Mudar para o dia imediatamente quando apanha o objetivo final
            self.story.game_completed = True
            print("Final goal reached! Background should change to day.")
            # Mostrar mensagem de vitória
            self.state = "completed"
            self.show_dialogue = True
            self.current_dialogue = {"speaker": "Ricardo", "text": "Parabéns! A Raquel encontrou o Sol e restaurou a luz ao mundo!"}
        if self.current_level.ricardo:
            self.current_level.ricardo.update()
        self.particles.update()
        self.current_level.collectibles.update()
        self.current_level.obstacles.update()
        if self.current_level.water:
            self.current_level.water.update()
        if self.show_dialogue:
            self.dialogue_box.update()

    def safe_reset_player(self):
        # Coloca a Raquel centralizada na primeira plataforma
        first_platform = min(self.current_level.platforms, key=lambda p: p.rect.x)
        self.player.rect.x = first_platform.rect.x + (first_platform.rect.width // 2) - (self.player.rect.width // 2)
        self.player.rect.bottom = first_platform.rect.top
        self.player.velocity_y = 0
        self.player.on_ground = True  # Garante que está em cima da plataforma
        self.player.invincible_timer = pygame.time.get_ticks()

    def draw_intro_screen(self):
        screen.fill((10, 10, 30))
        
        # Título do jogo
        title_font = pygame.font.Font(None, 72)
        title_text = title_font.render("Raquel's Journey to the Sun", True, GOLD)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 150))
        screen.blit(title_text, title_rect)
        
        # Texto de introdução
        intro_font = pygame.font.Font(None, 36)
        intro_lines = [
            "O mundo foi mergulhado na escuridão...",
            "A Raquel, uma jovem corajosa, decide partir",
            "em busca do Sol perdido para restaurar a luz.",
            "",
            "Ajude a Raquel nesta jornada épica!",
            "Colete as estrelas, evite os obstáculos,",
            "e encontre o Ricardo no final da aventura."
        ]
        
        y_start = 250
        for i, line in enumerate(intro_lines):
            if line.strip():  # Só desenhar linhas não vazias
                intro_text = intro_font.render(line, True, WHITE)
                text_rect = intro_text.get_rect(center=(SCREEN_WIDTH // 2, y_start + i * 40))
                screen.blit(intro_text, text_rect)
        
        # Instruções
        instruction_font = pygame.font.Font(None, 28)
        instruction_text = instruction_font.render("Pressiona qualquer tecla para continuar...", True, (200, 200, 200))
        instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100))
        screen.blit(instruction_text, instruction_rect)
        
        pygame.display.flip()

    def draw_start_screen(self):
        screen.fill((10, 10, 30))
        # Carrega a imagem apenas uma vez
        if not hasattr(self, 'start_img'):
            self.start_img = pygame.image.load(resource_path("assets", "sprites", "start_screen.png")).convert_alpha()
        # Centralizar verticalmente tudo (imagem + opções)
        img_height = self.start_img.get_height()
        options_height = len(self.menu_options) * 56 + (len(self.menu_options) - 1) * 30
        total_height = img_height + 40 + options_height
        y_start = (SCREEN_HEIGHT - total_height) // 2
        img_rect = self.start_img.get_rect(center=(SCREEN_WIDTH // 2, y_start + img_height // 2))
        screen.blit(self.start_img, img_rect)
        option_font = pygame.font.Font(None, 56)
        y_base = img_rect.bottom + 40
        for i, option in enumerate(self.menu_options):
            color = (255, 255, 255) if i != self.selected_option else (255, 215, 0)
            opt = option_font.render(option, True, color)
            opt_rect = opt.get_rect(center=(SCREEN_WIDTH // 2, y_base + i * 86))
            screen.blit(opt, opt_rect)
        pygame.display.flip()

    def draw(self):
        if self.state == "start":
            self.draw_start_screen()
            return
        all_collected = all(c.collected for c in self.current_level.collectibles)
        print(f"Game completed: {self.story.game_completed}, State: {self.state}")
        if self.story.game_completed:
            bg = pygame.transform.scale(self.background_day, (SCREEN_WIDTH, SCREEN_HEIGHT))
        else:
            bg = pygame.transform.scale(self.background_night, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(bg, (0, 0))
        if self.current_level.water:
            self.current_level.water.draw(screen)
        screen.blit(self.player.image, self.player.rect)
        self.current_level.platforms.draw(screen)
        self.current_level.obstacles.draw(screen)
        self.current_level.collectibles.draw(screen)
        if hasattr(self.current_level, 'door_group'):
            self.current_level.door_group.draw(screen)
        if self.current_level.final_goal:
            screen.blit(self.current_level.final_goal.image, self.current_level.final_goal.rect)
        if self.current_level.ricardo:
            screen.blit(self.current_level.ricardo.image, self.current_level.ricardo.rect)
        self.particles.draw(screen)

        if self.state in ["playing"]:
            elapsed = (pygame.time.get_ticks() - self.start_time) / 1000
            time_left = max(0, int(self.time_limit - elapsed))
            font = pygame.font.Font(None, 36)
            timer_text = font.render(f"Tempo: {time_left}s", True, (255, 255, 255))
            screen.blit(timer_text, (20, 20))
            
            # Texto de instrução
            instruction_font = pygame.font.Font(None, 24)
            instruction_text = instruction_font.render("Encontra o Sol e salva o mundo! Boa sorte, Raquel!", True, (255, 255, 0))
            screen.blit(instruction_text, (20, 60))
        if self.state == "completed":
            # Carrega a imagem apenas uma vez
            if not hasattr(self, 'victory_img'):
                self.victory_img = pygame.image.load(resource_path("assets", "sprites", "imagem.png")).convert_alpha()
            
            # Renderiza o texto de vitória mais para cima
            victory_text = pygame.font.Font(None, 48).render(
                "Conseguiste! Trouxes-te de volta a luz e desbloqueaste um romance :)", True, GOLD
            )
            text_rect = victory_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
            screen.blit(victory_text, text_rect)
            
            # Renderiza a imagem abaixo do texto (redimensionada se necessário)
            img_width = self.victory_img.get_width()
            img_height = self.victory_img.get_height()
            
            # Redimensiona a imagem se for muito grande
            max_width = 400
            max_height = 300
            if img_width > max_width or img_height > max_height:
                scale = min(max_width / img_width, max_height / img_height)
                new_width = int(img_width * scale)
                new_height = int(img_height * scale)
                scaled_img = pygame.transform.scale(self.victory_img, (new_width, new_height))
                img_rect = scaled_img.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150))
                screen.blit(scaled_img, img_rect)
            else:
                img_rect = self.victory_img.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150))
                screen.blit(self.victory_img, img_rect)
        if self.state == "game_over":
            defeat_text = pygame.font.Font(None, 48).render(
                "O tempo acabou! Pressiona ENTER para tentar novamente.", True, (255, 0, 0)
            )
            text_rect = defeat_text.get_rect(center=(SCREEN_WIDTH // 2, 200))
            screen.blit(defeat_text, text_rect)
        pygame.display.flip()

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            clock.tick(FPS)

# Start the game
if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()
    sys.exit() 