import pygame
import random
import os
from settings import *

class Food:
    def __init__(self):
        """Initializes the food's properties."""
        try:
            self.image = pygame.image.load(resource_path(os.path.join('assets', 'apple.png'))).convert_alpha()
            self.image = pygame.transform.scale(self.image, (SNAKE_BLOCK_SIZE, SNAKE_BLOCK_SIZE))

        except pygame.error:
            print("Unable to load 'apple.png'. Make sure it's in the 'assets' folder.")
            self.image = pygame.Surface((SNAKE_BLOCK_SIZE, SNAKE_BLOCK_SIZE))
            self.image.fill(RED)

        self.spawn()

    def spawn(self, snake_body=None):
        """Places the food at a new random position on the screen."""
        self.x = random.randrange(0, SCREEN_WIDTH, SNAKE_BLOCK_SIZE)
        self.y = random.randrange(0, SCREEN_HEIGHT, SNAKE_BLOCK_SIZE)
        if snake_body:
            while [self.x, self.y] in snake_body:
                self.x = random.randrange(0, SCREEN_WIDTH, SNAKE_BLOCK_SIZE)
                self.y = random.randrange(0, SCREEN_HEIGHT, SNAKE_BLOCK_SIZE)

    def draw(self, screen):
        """Draws the food image on the screen."""
        screen.blit(self.image, (self.x, self.y))
