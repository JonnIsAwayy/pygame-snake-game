import sys
import os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 15
CAPTION = "Snake with Power-Ups!"

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 102)
GRID_COLOR = (40, 40, 40)
BLUE = (100, 100, 255)
GOLD = (255, 215, 0)

SNAKE_BLOCK_SIZE = 20

POWERUP_SPAWN_INTERVAL = 10000
SLOW_MO_DURATION = 50
SLOW_MO_FPS = 5
POWERUP_TYPES = ['slow_mo', 'double_points']
