import pygame
import sys
from pygame.math import Vector2 as vector

pygame.init()


# Отримання розмірів екрану пристрою
info = pygame.display.Info()
SCREEN_WIDTH, SCREEN_HEIGHT = info.current_w, info.current_h

# Відносні розміри (наприклад, 90% від екрану)
WINDOW_WIDTH, WINDOW_HEIGHT = int(SCREEN_WIDTH), int(SCREEN_HEIGHT)
TILE_SIZE = 64  # наприклад, ширина вікна поділена на кількість плиток
ANIMATION_SPEED = 6

Z_LAYERS = {
    'bg': 0,
    'clouds': 1,
    'bg tiles': 2,
    'path': 3,
    'bg details': 4,
    'main': 5,
    'water': 6,
    'fg': 7
}