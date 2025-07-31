# main.py
import pygame
import os
import random
from settings import *
from snake import Snake
from food import Food
from powerup import PowerUp

# --- High Score Functions ---
def save_high_score(score):
    """Saves the high score to a file."""
    try:
        with open("highscore.txt", "w") as f:
            f.write(str(score))
    except IOError:
        print("Unable to save the high score.")

def load_high_score():
    """Loads the high score from a file."""
    if not os.path.exists("highscore.txt"):
        return 0
    try:
        with open("highscore.txt", "r") as f:
            return int(f.read())
    except (IOError, ValueError):
        return 0

# --- Drawing and UI Functions ---
def draw_grid(screen):
    """Draws a grid on the screen."""
    for x in range(0, SCREEN_WIDTH, SNAKE_BLOCK_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, SNAKE_BLOCK_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (0, y), (SCREEN_WIDTH, y))

def display_score(screen, score):
    """Displays the current score."""
    score_font = pygame.font.SysFont("comicsansms", 35)
    value = score_font.render("Score: " + str(score), True, YELLOW)
    screen.blit(value, [10, 10])

# --- Game State Functions ---
def main_menu(screen, clock, high_score):
    """Displays the main menu and waits for the player to start."""
    title_font = pygame.font.SysFont("bahnschrift", 70)
    prompt_font = pygame.font.SysFont("bahnschrift", 25)
    
    waiting = True
    while waiting:
        screen.fill(BLACK)
        draw_grid(screen)

        title_text = title_font.render("SNAKE", True, GREEN)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 100))
        screen.blit(title_text, title_rect)
        
        score_text = prompt_font.render(f"High Score: {high_score}", True, YELLOW)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        screen.blit(score_text, score_rect)

        prompt_text = prompt_font.render("Press any key to play", True, WHITE)
        prompt_rect = prompt_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50))
        screen.blit(prompt_text, prompt_rect)

        pygame.display.update()
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYUP:
                waiting = False

def game_loop(screen, clock):
    """Runs the main gameplay session and returns the final score."""
    player_snake = Snake()
    apple = Food()
    power_up = None
    
    slow_mo_timer = 0
    current_fps = FPS
    
    last_powerup_spawn_time = pygame.time.get_ticks()
    
    score = 0
    running = True

    while running:
        if slow_mo_timer > 0:
            slow_mo_timer -= 1
            if slow_mo_timer == 0:
                current_fps = FPS
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT: player_snake.go_left()
                elif event.key == pygame.K_RIGHT: player_snake.go_right()
                elif event.key == pygame.K_UP: player_snake.go_up()
                elif event.key == pygame.K_DOWN: player_snake.go_down()

        snake_head = player_snake.move()

        if player_snake.check_wall_collision() or player_snake.check_self_collision(snake_head):
            running = False

        if player_snake.x == apple.x and player_snake.y == apple.y:
            player_snake.grow()
            score += 1
            apple.spawn()
            
        current_time = pygame.time.get_ticks()
        if power_up is None and current_time - last_powerup_spawn_time > POWERUP_SPAWN_INTERVAL:
            power_up = PowerUp()
            last_powerup_spawn_time = current_time

        if power_up and player_snake.x == power_up.x and player_snake.y == power_up.y:
            if power_up.type == 'slow_mo':
                current_fps = SLOW_MO_FPS
                slow_mo_timer = SLOW_MO_DURATION
            elif power_up.type == 'double_points':
                score += 1
            power_up = None

        screen.fill(BLACK)
        draw_grid(screen)
        pygame.draw.rect(screen, WHITE, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), 5)
        player_snake.draw(screen)
        apple.draw(screen)
        if power_up:
            power_up.draw(screen)
        display_score(screen, score)
        pygame.display.update()
        clock.tick(current_fps)
        
    return score

def game_over_screen(screen, clock, score, high_score):
    """Displays the game over screen and waits for player input."""
    font_style = pygame.font.SysFont("bahnschrift", 50)
    font_style_small = pygame.font.SysFont("bahnschrift", 25)
    
    waiting = True
    while waiting:
        screen.fill(BLACK)
        draw_grid(screen)
        
        mesg = font_style.render("GAME OVER", True, RED)
        text_rect = mesg.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 80))
        screen.blit(mesg, text_rect)
        
        score_text = font_style_small.render(f"Your Score: {score}", True, YELLOW)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 10))
        screen.blit(score_text, score_rect)
        
        high_score_text = font_style_small.render(f"High Score: {high_score}", True, YELLOW)
        high_score_rect = high_score_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 20))
        screen.blit(high_score_text, high_score_rect)
        
        if score > high_score:
            hs_text = font_style_small.render("New High Score!", True, GREEN)
            hs_rect = hs_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 60))
            screen.blit(hs_text, hs_rect)

        prompt_text = font_style_small.render("Press C to Play Again or Q to Quit", True, WHITE)
        prompt_rect = prompt_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 100))
        screen.blit(prompt_text, prompt_rect)

        pygame.display.update()
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return False
                if event.key == pygame.K_c:
                    return True

def main():
    """Main function that controls the overall game flow."""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(CAPTION)
    clock = pygame.time.Clock()
    
    high_score = load_high_score()
    
    playing = True
    while playing:
        main_menu(screen, clock, high_score)
        score = game_loop(screen, clock)
        
        if score > high_score:
            high_score = score
            save_high_score(high_score)
            
        playing = game_over_screen(screen, clock, score, high_score)

    pygame.quit()

if __name__ == '__main__':
    main()
