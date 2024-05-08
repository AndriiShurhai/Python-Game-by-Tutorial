from settings import *
from sprites import Sprite

class Level:
    def __init__(self, tmx_map):
        self.display_surface = pygame.display.get_surface()

        # groups
        self.all_sprites = pygame.sprite.Group()

        self.setup(tmx_map)

    def setup(self, tmx_map):
        for x, y, surface in tmx_map.get_layer_by_name('Terrain').tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), surface, self.all_sprites)

        for obj in tmx_map.get_layer_by_name('Objects'):
            if obj.name == 'player':
                print(obj.x)
                print(obj.y)

    def run(self):
        self.display_surface.fill("black")
        self.all_sprites.draw(self.display_surface)