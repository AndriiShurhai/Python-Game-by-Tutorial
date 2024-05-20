from settings import *
from sprites import Sprite, MovingSprite, AnimatedSprite
from player import Player
from groups import AllSprites

class Level:
    def __init__(self, tmx_map, level_frames):
        self.display_surface = pygame.display.get_surface()

        # groups
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.semicollision_sprites = pygame.sprite.Group()

        self.setup(tmx_map, level_frames)

    def setup(self, tmx_map, level_frames):

        # tiles
        for layer in ['BG', 'Terrain', 'FG', 'Platforms']:
            for x, y, surface in tmx_map.get_layer_by_name(layer).tiles():
                groups = [self.all_sprites]
                if layer == 'Terrain': groups.append(self.collision_sprites)
                if layer == 'Platforms': groups.append(self.semicollision_sprites)
                match layer:
                    case 'BG': z = Z_LAYERS['bg tiles']
                    case 'FG': z = Z_LAYERS['fg']
                    case _: z = Z_LAYERS['main']
                
                Sprite((x * TILE_SIZE, y * TILE_SIZE), surface, groups, z)

        # objects
        for obj in tmx_map.get_layer_by_name('Objects'):
            if obj.name == 'player':
                self.player = Player((obj.x, obj.y), self.all_sprites, self.collision_sprites, self.semicollision_sprites)
            else:
                if obj.name in ('barrel', 'crate'):
                    Sprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites))
                else:
                    if 'palm' not in obj.name:
                        frames = level_frames[obj.name]
                        AnimatedSprite((obj.x, obj.y), frames, self.all_sprites)
        
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
                MovingSprite((self.all_sprites, self.semicollision_sprites), start_pos, end_pos, move_direction, speed)
                

    def run(self, delta_time):
        self.display_surface.fill("black")
        self.all_sprites.update(delta_time)
        self.all_sprites.draw(self.player.hitbox_rect.center)