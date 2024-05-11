from settings import *
from sprites import Sprite, MovingSprite
from player import Player

class Level:
    def __init__(self, tmx_map):
        self.display_surface = pygame.display.get_surface()

        # groups
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()

        self.setup(tmx_map)

    def setup(self, tmx_map):

        # tiles
        for x, y, surface in tmx_map.get_layer_by_name('Terrain').tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), surface, (self.all_sprites, self.collision_sprites))

        # objects
        for obj in tmx_map.get_layer_by_name('Objects'):
            if obj.name == 'player':
                Player((obj.x, obj.y), self.all_sprites, self.collision_sprites)
        
        # moving objects
        for move_obj in tmx_map.get_layer_by_name('Moving Objects'):
            if move_obj.name == 'helicopter':
                if move_obj.width > move_obj.height: # horizontal movement
                    move_direction = 'x'
                    start_pos = (move_obj.x, move_obj.y + move_obj.height / 2)
                    end_pos =  (move_obj.x + move_obj.width, move_obj.y + move_obj.height / 2)
                else: # vertical movement
                    move_direction = 'y'
                    start_pos = (move_obj.x + move_obj.width / 2, move_obj.y)
                    end_pos = (move_obj.x + move_obj.width / 2, move_obj.y + move_obj.height)
                speed = move_obj.properties['speed']
                MovingSprite(self.all_sprites, start_pos, end_pos, move_direction, speed)
                



    def run(self, delta_time):
        self.display_surface.fill("black")
        self.all_sprites.update(delta_time)
        self.all_sprites.draw(self.display_surface)