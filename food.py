# food.py
import pygame
import random
import os # We need this to correctly handle file paths
from settings import *

class Food:
    def __init__(self):
        """Initializes the food's properties."""
        try:
            # Load the apple image
            self.image = pygame.image.load(os.path.join('assets', 'apple.png')).convert_alpha()
            
            # --- THIS IS THE FIX ---
            # Scale the image to be the same size as a snake block.
            # This makes sure your apple isn't too big or too small.
            self.image = pygame.transform.scale(self.image, (SNAKE_BLOCK_SIZE, SNAKE_BLOCK_SIZE))

        except pygame.error:
            # This is a fallback in case the image can't be found.
            print("Unable to load 'apple.png'. Make sure it's in the 'assets' folder.")
            self.image = pygame.Surface((SNAKE_BLOCK_SIZE, SNAKE_BLOCK_SIZE))
            self.image.fill(RED)

        self.spawn() # Set its first random position

    def spawn(self):
        """Places the food at a new random position on the screen."""
        self.x = round(random.randrange(0, SCREEN_WIDTH - SNAKE_BLOCK_SIZE) / SNAKE_BLOCK_SIZE) * SNAKE_BLOCK_SIZE
        self.y = round(random.randrange(0, SCREEN_HEIGHT - SNAKE_BLOCK_SIZE) / SNAKE_BLOCK_SIZE) * SNAKE_BLOCK_SIZE

    def draw(self, screen):
        """Draws the food image on the screen."""
        screen.blit(self.image, (self.x, self.y))
