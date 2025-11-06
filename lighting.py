import pygame

class LightingSystem:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.light_sources = []
        self.darkness_surface = pygame.Surface((screen_width, screen_height))
        self.darkness_surface.fill((0, 0, 0))
        self.darkness_surface.set_alpha(150)  # Reduzido de 200 para 150 para menos escuridão
        
    def add_light_source(self, x, y, radius, color=(255, 255, 200)):
        self.light_sources.append({
            'pos': (x, y),
            'radius': radius,
            'color': color
        })
    
    def clear_light_sources(self):
        self.light_sources = []
    
    def render(self, screen):
        # Create a surface for the lighting
        lighting_surface = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        lighting_surface.fill((0, 0, 0, 200))  # Reduzido de 255 para 200 para mais transparência
        
        # Draw light circles
        for light in self.light_sources:
            # Create a surface for this light
            light_surface = pygame.Surface((light['radius'] * 2, light['radius'] * 2), pygame.SRCALPHA)
            
            # Draw the light gradient
            for r in range(light['radius'], 0, -1):
                alpha = int(200 * (1 - r / light['radius']))  # Reduzido de 255 para 200
                color = (*light['color'], alpha)
                pygame.draw.circle(light_surface, color, (light['radius'], light['radius']), r)
            
            # Blit the light onto the lighting surface
            lighting_surface.blit(light_surface, 
                                (light['pos'][0] - light['radius'], 
                                 light['pos'][1] - light['radius']),
                                special_flags=pygame.BLEND_RGBA_SUB)
        
        # Apply the lighting to the screen
        screen.blit(lighting_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        
        # Add overall darkness with less intensity
        screen.blit(self.darkness_surface, (0, 0)) 