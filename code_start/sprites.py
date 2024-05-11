from settings import *

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surface=pygame.Surface((TILE_SIZE, TILE_SIZE)), groups=None):
        super().__init__(groups)
        self.image = surface
        self.image.fill('gray')
        self.rect = self.image.get_frect(topleft=pos)
        self.old_rect = self.rect.copy()

class MovingSprite(Sprite):
    def __init__(self, groups, start_pos, end_pos, move_direction, speed):
        surface = pygame.Surface((200, 50))
        super().__init__(start_pos, surface, groups)