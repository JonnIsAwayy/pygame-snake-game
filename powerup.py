import pygame
import random
import os
from settings import *

class PowerUp:
    def __init__(self, snake_body=None, food_pos=None):
        self.type = random.choice(POWERUP_TYPES) 
        if self.type == 'slow_mo':
            self.image = self.load_image('slow_mo.png', BLUE)
        elif self.type == 'double_points':
            self.image = self.load_image('double_points.png', GOLD)
            
        self.spawn(snake_body, food_pos)

    def load_image(self, filename, fallback_color):
        try:
            path = resource_path(os.path.join('assets', filename))
            image = pygame.image.load(path).convert_alpha()
            return pygame.transform.scale(image, (SNAKE_BLOCK_SIZE, SNAKE_BLOCK_SIZE))
        except pygame.error:
            print(f"Warning: '{filename}' not found. Using a colored square as a fallback.")
            fallback_surface = pygame.Surface((SNAKE_BLOCK_SIZE, SNAKE_BLOCK_SIZE))
            fallback_surface.fill(fallback_color)
            return fallback_surface

    def spawn(self, snake_body=None, food_pos=None):
        self.x = random.randrange(0, SCREEN_WIDTH, SNAKE_BLOCK_SIZE)
        self.y = random.randrange(0, SCREEN_HEIGHT, SNAKE_BLOCK_SIZE)
        def is_overlapping():
            if snake_body and [self.x, self.y] in snake_body: return True
            if food_pos and self.x == food_pos[0] and self.y == food_pos[1]: return True
            return False

        while is_overlapping():
            self.x = random.randrange(0, SCREEN_WIDTH, SNAKE_BLOCK_SIZE)
            self.y = random.randrange(0, SCREEN_HEIGHT, SNAKE_BLOCK_SIZE)

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
