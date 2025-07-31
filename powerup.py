# powerup.py
import pygame
import random
import os
from settings import * # Import everything from settings, including the new list

class PowerUp:
    def __init__(self):
        """Initializes a random power-up and loads its image."""
        # Use the list from settings.py to choose a type
        self.type = random.choice(POWERUP_TYPES) 
        
        # Load the correct image based on the power-up type
        if self.type == 'slow_mo':
            self.image = self.load_image('slow_mo.png', BLUE)
        elif self.type == 'double_points':
            self.image = self.load_image('double_points.png', GOLD)
            
        self.spawn()

    def load_image(self, filename, fallback_color):
        """Helper function to load an image or create a fallback surface."""
        try:
            path = os.path.join('assets', filename)
            image = pygame.image.load(path).convert_alpha()
            return pygame.transform.scale(image, (SNAKE_BLOCK_SIZE, SNAKE_BLOCK_SIZE))
        except pygame.error:
            # If the image file doesn't exist, create a colored square instead.
            print(f"Warning: '{filename}' not found. Using a colored square as a fallback.")
            fallback_surface = pygame.Surface((SNAKE_BLOCK_SIZE, SNAKE_BLOCK_SIZE))
            fallback_surface.fill(fallback_color)
            return fallback_surface

    def spawn(self):
        """Places the power-up at a new random position."""
        self.x = round(random.randrange(0, SCREEN_WIDTH - SNAKE_BLOCK_SIZE) / SNAKE_BLOCK_SIZE) * SNAKE_BLOCK_SIZE
        self.y = round(random.randrange(0, SCREEN_HEIGHT - SNAKE_BLOCK_SIZE) / SNAKE_BLOCK_SIZE) * SNAKE_BLOCK_SIZE

    def draw(self, screen):
        """Draws the power-up's image on the screen."""
        screen.blit(self.image, (self.x, self.y))
