from settings import *
from sprites import Sprite, MovingSprite, AnimatedSprite, Spike
from player import Player
from groups import AllSprites
from random import uniform

class Level:
    def __init__(self, tmx_map, level_frames):
        self.display_surface = pygame.display.get_surface()

        # groups
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.semi_collision_sprites = pygame.sprite.Group()
        self.damage_sprites = pygame.sprite.Group()

        self.setup(tmx_map, level_frames)

    def setup(self, tmx_map, level_frames):
        # tiles
        for layer in ['BG', 'Terrain', 'FG', 'Platforms']:
            for x, y, surface in tmx_map.get_layer_by_name(layer).tiles():
                groups = [self.all_sprites]
                if layer == 'Terrain': groups.append(self.collision_sprites)
                if layer == 'Platforms': groups.append(self.semi_collision_sprites)
                match layer:
                    case 'BG': z = Z_LAYERS['bg tiles']
                    case 'FG': z = Z_LAYERS['bg tiles']
                    case _: z = Z_LAYERS['main']
                
                Sprite((x * TILE_SIZE, y * TILE_SIZE), surface, groups, z)
        
        # background objects
        for obj in tmx_map.get_layer_by_name('BG details'):
            if obj.name == 'static':
                Sprite((obj.x, obj.y), obj.image, self.all_sprites, z = Z_LAYERS['bg tiles'])
            else:
                AnimatedSprite((obj.x, obj.y), level_frames[obj.name], self.all_sprites, Z_LAYERS['bg tiles'], ANIMATION_SPEED)
                if obj.name == 'candle':
                    AnimatedSprite((obj.x, obj.y) + vector(-20, -20), level_frames['candle_light'], self.all_sprites, Z_LAYERS['bg tiles'], ANIMATION_SPEED)

        # objects
        for obj in tmx_map.get_layer_by_name('Objects'):
            if obj.name == 'player':
                self.player = Player(
                    pos=(obj.x, obj.y), 
                    groups=self.all_sprites, 
                    collision_sprites=self.collision_sprites, 
                    semi_collision_sprites=self.semi_collision_sprites,
                    frames=level_frames['player']
                    )
            else:
                if obj.name in ('barrel', 'crate'):
                    Sprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites))
                else:
                    # frames
                    frames = level_frames[obj.name] if not 'palm' in obj.name else level_frames['palms'][obj.name]
                    if obj.name == 'floor_spike' and obj.properties['inverted']:
                        frames = [pygame.transform.flip(frame, False, True) for frame in frames]
                    
                    # groups
                    groups = [self.all_sprites]
                    if obj.name in ('palm_small', 'palm_large'): groups.append(self.semi_collision_sprites)
                    if obj.name in ('saw', 'floor_spike'): groups.append(self.damage_sprites)

                    # animation speed
                    animation_speed = ANIMATION_SPEED if not 'palm' in obj.name else ANIMATION_SPEED + uniform(-1, 1)

                    # z index
                    z = Z_LAYERS['main'] if not 'bg' in obj.name else Z_LAYERS['bg']
                    AnimatedSprite((obj.x, obj.y), frames, groups, z, animation_speed)
        
        # moving objects
        for move_obj in tmx_map.get_layer_by_name('Moving Objects'):
            if move_obj.name == 'spike':
                Spike(
                    position=(move_obj.x + move_obj.width//2, move_obj.y + move_obj.height//2),
                    surface=level_frames['spike'],
                    groups= (self.all_sprites, self.damage_sprites),
                    radius=move_obj.properties['radius'],
                    speed=move_obj.properties['speed'],
                    start_angle=move_obj.properties['start_angle'],
                    end_angle=move_obj.properties['end_angle']
                    )
                for radius in range(0, move_obj.properties['radius'], 15):
                    Spike(
                    position=(move_obj.x + move_obj.width//2, move_obj.y + move_obj.height//2),
                    surface=level_frames['spike_chain'],
                    groups=self.all_sprites,
                    radius=radius,
                    speed=move_obj.properties['speed'],
                    start_angle=move_obj.properties['start_angle'],
                    end_angle=move_obj.properties['end_angle'],
                    z=Z_LAYERS['bg details']
                    )
            else:
                frames = level_frames[move_obj.name]
                groups = (self.all_sprites, self.semi_collision_sprites) if move_obj.properties['platform'] else (self.all_sprites, self.damage_sprites)
                if move_obj.width > move_obj.height: # horizontal movement
                    move_direction = 'x'
                    start_pos = (move_obj.x, move_obj.y + move_obj.height / 2)
                    end_pos =  (move_obj.x + move_obj.width, move_obj.y + move_obj.height / 2)

                else: # vertical movement
                    move_direction = 'y'
                    start_pos = (move_obj.x + move_obj.width / 2, move_obj.y)
                    end_pos = (move_obj.x + move_obj.width / 2, move_obj.y + move_obj.height)
                speed = move_obj.properties['speed']
                MovingSprite(frames, groups, start_pos, end_pos, move_direction, speed, move_obj.properties['flip'])

                if move_obj.name == 'saw':
                    print(move_obj.name)
                    if move_direction == 'x':
                        y = start_pos[1] - level_frames['saw_chain'].get_height() / 2 
                        left, right = int(start_pos[0]), int(end_pos[0])
                        for x in range(left, right, 20):
                            Sprite((x, y), level_frames['saw_chain'], self.all_sprites, Z_LAYERS['bg details'])
                    if move_direction == 'y':
                        x = start_pos[0] - level_frames['saw_chain'].get_width() / 2
                        bottom, top = int(start_pos[1]), int(end_pos[1])
                        for y in range(bottom, top, 20):
                            Sprite((x, y), level_frames['saw_chain'], self.all_sprites, Z_LAYERS['bg details'])
                

    def run(self, delta_time):
        self.display_surface.fill("black")
        self.all_sprites.update(delta_time)
        self.all_sprites.draw(self.player.hitbox_rect.center)