# settings.py
# This file contains all the settings and constants for the game.

# -- Display Settings --
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 15
CAPTION = "Snake with Power-Ups!"

# -- Color Palette (RGB) --
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 102)
GRID_COLOR = (40, 40, 40)
BLUE = (100, 100, 255)
GOLD = (255, 215, 0)

# -- Game Properties --
SNAKE_BLOCK_SIZE = 20

# -- Power-up Settings --
POWERUP_SPAWN_INTERVAL = 10000 # Time in milliseconds (10000ms = 10 seconds)
SLOW_MO_DURATION = 50     # UPDATED: 50 frames / 5 FPS = 10 seconds
SLOW_MO_FPS = 5
POWERUP_TYPES = ['slow_mo', 'double_points']
