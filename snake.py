import pygame
import os
from settings import *

class Snake:
    def __init__(self):
        self.x = (SCREEN_WIDTH // 2) // SNAKE_BLOCK_SIZE * SNAKE_BLOCK_SIZE
        self.y = (SCREEN_HEIGHT // 2) // SNAKE_BLOCK_SIZE * SNAKE_BLOCK_SIZE
        self.x_change = 0
        self.y_change = 0
        self.body = []
        self.length = 1
        
        self.load_images()
        self.head_image = self.head_right 

    def load_images(self):
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
        path = resource_path(os.path.join('assets', filename))
        return pygame.transform.scale(
            pygame.image.load(path).convert_alpha(), 
            (SNAKE_BLOCK_SIZE, SNAKE_BLOCK_SIZE)
        )

    def create_fallback_surface(self):
        surface = pygame.Surface((SNAKE_BLOCK_SIZE, SNAKE_BLOCK_SIZE))
        surface.fill(GREEN)
        return surface

    def move(self):
        self.x += self.x_change
        self.y += self.y_change

        snake_head = [self.x, self.y]
        self.body.append(snake_head)
        
        if len(self.body) > self.length:
            del self.body[0]
        
        return snake_head

    def grow(self):
        self.length += 1

    def draw(self, screen):
        if not self.body:
            return

        head_pos = self.body[-1]
        screen.blit(self.head_image, (head_pos[0], head_pos[1]))

        for segment in self.body[1:-1]:
            screen.blit(self.body_image, (segment[0], segment[1]))
        
        if len(self.body) > 1:
            tail_pos = self.body[0]
            tail_direction_segment = self.body[1]
            dx = tail_direction_segment[0] - tail_pos[0]
            dy = tail_direction_segment[1] - tail_pos[1]
            if dx > 0: tail_image = self.tail_right 
            elif dx < 0: tail_image = self.tail_left
            elif dy > 0: tail_image = self.tail_down
            else: tail_image = self.tail_up           
            screen.blit(tail_image, (tail_pos[0], tail_pos[1]))

    def update_head_graphics(self):
        if self.x_change > 0: self.head_image = self.head_right
        elif self.x_change < 0: self.head_image = self.head_left
        elif self.y_change > 0: self.head_image = self.head_down
        elif self.y_change < 0: self.head_image = self.head_up

    def go_left(self):
        if self.x_change == 0 and self.head_image != self.head_right:
            self.x_change = -SNAKE_BLOCK_SIZE
            self.y_change = 0
            self.update_head_graphics()

    def go_right(self):
        if self.x_change == 0 and self.head_image != self.head_left:
            self.x_change = SNAKE_BLOCK_SIZE
            self.y_change = 0
            self.update_head_graphics()

    def go_up(self):
        if self.y_change == 0 and self.head_image != self.head_down:
            self.y_change = -SNAKE_BLOCK_SIZE
            self.x_change = 0
            self.update_head_graphics()

    def go_down(self):
        if self.y_change == 0 and self.head_image != self.head_up:
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
