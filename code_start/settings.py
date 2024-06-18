import pygame
import sys
from pygame.math import Vector2 as vector

pygame.init()


info = pygame.display.Info()
SCREEN_WIDTH, SCREEN_HEIGHT = info.current_w, info.current_h

WINDOW_WIDTH, WINDOW_HEIGHT = int(SCREEN_WIDTH), int(SCREEN_HEIGHT)
TILE_SIZE = 64
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