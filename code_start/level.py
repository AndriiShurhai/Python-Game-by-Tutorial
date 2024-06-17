from settings import *
from sprites import Sprite, MovingSprite, AnimatedSprite, Spike, Item, ParticleEffect
from player import Player
from groups import AllSprites
from random import uniform
from enemies import Tooth, Shell, Pearl

class Level:
    def __init__(self, tmx_map, level_frames, data):
        self.display_surface = pygame.display.get_surface()

        # level_data
        self.level_width = tmx_map.width * TILE_SIZE
        self.level_bottom = tmx_map.height * TILE_SIZE
        
        tmx_level_properties = tmx_map.get_layer_by_name('Data')[0].properties
        if tmx_level_properties['bg']:
            bg_tile = level_frames['bg_tiles'][tmx_level_properties['bg']]
        else:
            bg_tile = None
        
        # groups
        self.all_sprites = AllSprites(
            width=tmx_map.width, 
            height=tmx_map.height, 
            bg_tile=bg_tile, 
            top_limit=tmx_level_properties['top_limit'], 
            clouds={'large': level_frames['cloud_large'], 'small': level_frames['cloud_small']},
            horizon_line=tmx_level_properties['horizon_line']
            )
        
        self.collision_sprites = pygame.sprite.Group()
        self.semi_collision_sprites = pygame.sprite.Group()
        self.damage_sprites = pygame.sprite.Group()
        self.tooth_sprites = pygame.sprite.Group()
        self.pearl_sprites = pygame.sprite.Group()
        self.items_sprites = pygame.sprite.Group()

        self.pearl_surface = level_frames['pearl']
        self.particle_frames = level_frames['particle']

        self.data = data

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
            print(obj)
            if obj.name == 'player':
                self.player = Player(
                    pos=(obj.x, obj.y), 
                    groups=self.all_sprites, 
                    collision_sprites=self.collision_sprites, 
                    semi_collision_sprites=self.semi_collision_sprites,
                    frames=level_frames['player'],
                    data=self.data
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

            if obj.name == 'flag':
                self.level_finish_rect = pygame.FRect((obj.x, obj.y), (obj.width, obj.height))
        
        # moving objects
        for move_obj in tmx_map.get_layer_by_name('Moving Objects'):
            print(move_obj)
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

        # enemies
        for obj in tmx_map.get_layer_by_name('Enemies'):
            if obj.name == 'tooth':
                Tooth((obj.x, obj.y), level_frames['tooth'], (self.all_sprites, self.damage_sprites, self.tooth_sprites), self.collision_sprites)
            if obj.name == 'shell':
                self.shell = Shell(
                    position=(obj.x, obj.y), 
                    frames=level_frames['shell'], 
                    groups=(self.all_sprites, self.collision_sprites), 
                    player=self.player, 
                    create_pearl=self.create_pearl)
        
        # items
        for obj in tmx_map.get_layer_by_name('Items'):
            Item(obj.name, (obj.x + TILE_SIZE / 2, obj.y + TILE_SIZE / 2), level_frames['items'][obj.name], (self.all_sprites, self.items_sprites), self.data)
        
        # water
        for obj in tmx_map.get_layer_by_name('Water'):
            rows, columns = int(obj.height / TILE_SIZE), int(obj.width / TILE_SIZE)
            for row in range(rows):
                for column in range(columns):
                    x = obj.x + column * TILE_SIZE
                    y = obj.y + row * TILE_SIZE
                    
                    if row == 0:
                        AnimatedSprite((x,y), level_frames['water_top'], self.all_sprites, Z_LAYERS['water'])
                    else:
                        Sprite((x, y), level_frames['water_body'], self.all_sprites, Z_LAYERS['water'])

    def create_pearl(self, position, angle):
        Pearl(position, (self.all_sprites, self.damage_sprites, self.pearl_sprites), self.pearl_surface, 200, angle)

    def pearl_collision(self):
        for sprite in self.collision_sprites:
            if type(sprite) != Shell:
                sprite = pygame.sprite.spritecollide(sprite, self.pearl_sprites, True)
                if sprite:
                    ParticleEffect((sprite[0].rect.center), self.particle_frames, self.all_sprites)


    def hit_collision(self):
        for sprite in self.damage_sprites:
            if sprite.rect.colliderect(self.player.hitbox_rect):
                self.player.get_damage()
                if type(sprite) == Pearl:
                    ParticleEffect((sprite.rect.center), self.particle_frames, self.all_sprites)
                    sprite.kill()

    def item_collision(self):
        if self.items_sprites:
            item_sprites = pygame.sprite.spritecollide(self.player, self.items_sprites, True)
            if item_sprites:
                item_sprites[0].activate()
                ParticleEffect((item_sprites[0].rect.center), self.particle_frames, self.all_sprites)


    def attack_collision(self):
        for target in self.pearl_sprites.sprites() + self.tooth_sprites.sprites():
            facing_target = self.player.rect.centerx < target.rect.centerx and self.player.facing_right or \
                            self.player.rect.centerx > target.rect.centerx and not self.player.facing_right 
            if target.rect.colliderect(self.player.rect) and self.player.attacking and facing_target:
                target.reverse()
    
    def check_constraint(self):
        # left and right
        if self.player.hitbox_rect.left <= 0:
            self.player.hitbox_rect.left = 0
        if self.player.hitbox_rect.right >= self.level_width:
            self.player.hitbox_rect.right = self.level_width

        # bottom
        if self.player.hitbox_rect.bottom >= self.level_bottom:
            print('sad')
        
        if self.player.hitbox_rect.colliderect(self.level_finish_rect):
            print('yesss')
        

    def run(self, delta_time):
        self.display_surface.fill("black")
        self.all_sprites.update(delta_time)
        self.pearl_collision() 
        self.hit_collision()
        self.item_collision()
        self.attack_collision()
        self.check_constraint()
        self.all_sprites.draw(self.player.hitbox_rect.center, delta_time)