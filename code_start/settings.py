import pygame
import sys
from pygame.math import Vector2 as vector

pygame.init()


info = pygame.display.Info()
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720

print(SCREEN_WIDTH, SCREEN_HEIGHT)

WINDOW_WIDTH, WINDOW_HEIGHT = int(SCREEN_WIDTH), int(SCREEN_HEIGHT)
TILE_SIZE = 64
ANIMATION_SPEED = 6

font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
HIGHLIGHT = (100, 100, 100)

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