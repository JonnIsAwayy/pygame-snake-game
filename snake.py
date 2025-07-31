# snake.py
import pygame
import os
from settings import *

class Snake:
    def __init__(self):
        """Initializes the snake's properties and loads all graphics."""
        self.x = SCREEN_WIDTH / 2
        self.y = SCREEN_HEIGHT / 2
        self.x_change = 0
        self.y_change = 0
        self.body = []
        self.length = 1
        
        self.load_images()
        self.head_image = self.head_right 

    def load_images(self):
        """A helper method to load and scale all the snake images."""
        try:
            self.head_up = self.load_and_scale('snakehead_up.png')
            self.head_down = self.load_and_scale('snakehead_down.png')
            self.head_left = self.load_and_scale('snakehead_left.png')
            self.head_right = self.load_and_scale('snakehead_right.png')
            
            self.tail_up = self.load_and_scale('snaketail_up.png')
            self.tail_down = self.load_and_scale('snaketail_down.png')
            self.tail_left = self.load_and_scale('snaketail_left.png')
            self.tail_right = self.load_and_scale('snaketail_right.png')

            self.body_image = self.load_and_scale('snakebody.png')

        except pygame.error as e:
            print(f"Error loading snake assets: {e}")
            print("Please ensure all snake images are in the 'assets' folder.")
            self.head_up = self.head_down = self.head_left = self.head_right = self.create_fallback_surface()
            self.tail_up = self.tail_down = self.tail_left = self.tail_right = self.create_fallback_surface()
            self.body_image = self.create_fallback_surface()
    
    def load_and_scale(self, filename):
        """Loads an image and scales it to the block size."""
        path = os.path.join('assets', filename)
        return pygame.transform.scale(
            pygame.image.load(path).convert_alpha(), 
            (SNAKE_BLOCK_SIZE, SNAKE_BLOCK_SIZE)
        )

    def create_fallback_surface(self):
        """Creates a green square as a fallback image."""
        surface = pygame.Surface((SNAKE_BLOCK_SIZE, SNAKE_BLOCK_SIZE))
        surface.fill(GREEN)
        return surface

    def move(self):
        """Updates the snake's position and body segments."""
        self.x += self.x_change
        self.y += self.y_change

        snake_head = [self.x, self.y]
        self.body.append(snake_head)
        
        if len(self.body) > self.length:
            del self.body[0]
        
        return snake_head

    def grow(self):
        """Increases the length of the snake."""
        self.length += 1

    def draw(self, screen):
        """Draws the entire snake with head, body, and tail."""
        if not self.body:
            return

        # Draw the head
        head_pos = self.body[-1]
        screen.blit(self.head_image, (head_pos[0], head_pos[1]))

        # Draw the body segments (all except the head and tail)
        for segment in self.body[1:-1]:
            screen.blit(self.body_image, (segment[0], segment[1]))
        
        if len(self.body) > 1:
            tail_pos = self.body[0]
            tail_direction_segment = self.body[1]
            
            dx = tail_direction_segment[0] - tail_pos[0]
            dy = tail_direction_segment[1] - tail_pos[1]

            # --- BUG FIX IS HERE ---
            # The logic is now reversed to point the tail away from the body.
            if dx > 0: tail_image = self.tail_right 
            elif dx < 0: tail_image = self.tail_left
            elif dy > 0: tail_image = self.tail_down
            else: tail_image = self.tail_up
            
            screen.blit(tail_image, (tail_pos[0], tail_pos[1]))

    def update_head_graphics(self):
        """Selects the correct head image based on the direction."""
        if self.x_change > 0: self.head_image = self.head_right
        elif self.x_change < 0: self.head_image = self.head_left
        elif self.y_change > 0: self.head_image = self.head_down
        elif self.y_change < 0: self.head_image = self.head_up

    def go_left(self):
        if self.x_change == 0:
            self.x_change = -SNAKE_BLOCK_SIZE
            self.y_change = 0
            self.update_head_graphics()

    def go_right(self):
        if self.x_change == 0:
            self.x_change = SNAKE_BLOCK_SIZE
            self.y_change = 0
            self.update_head_graphics()

    def go_up(self):
        if self.y_change == 0:
            self.y_change = -SNAKE_BLOCK_SIZE
            self.x_change = 0
            self.update_head_graphics()

    def go_down(self):
        if self.y_change == 0:
            self.y_change = SNAKE_BLOCK_SIZE
            self.x_change = 0
            self.update_head_graphics()
            
    def check_wall_collision(self):
        if self.x >= SCREEN_WIDTH or self.x < 0 or self.y >= SCREEN_HEIGHT or self.y < 0:
            return True
        return False

    def check_self_collision(self, head):
        for segment in self.body[:-1]:
            if segment == head:
                return True
        return False
