from settings import *
import math
import random

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surface=pygame.Surface((TILE_SIZE, TILE_SIZE)), groups=None, z = Z_LAYERS['main']):
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_frect(topleft=pos)
        self.old_rect = self.rect.copy()
        self.z = z

class AnimatedSprite(Sprite):
    def __init__(self, pos, frames, groups, z = Z_LAYERS['main'], animation_speed = ANIMATION_SPEED):
        self.frames, self.frame_index = frames, 0
        super().__init__(pos, self.frames[self.frame_index], groups, z)
        self.animation_speed = animation_speed
    
    def animate(self, delta_time):
        self.frame_index += self.animation_speed * delta_time 
        self.image = self.frames[int(self.frame_index % len(self.frames))]

    def update(self, delta_time):
        self.animate(delta_time)

class Heart(AnimatedSprite):
    def __init__(self, position, frames, groups):
        super().__init__(position, frames, groups)
        self.active = False

    def animate(self, delta_time):
        self.frame_index += ANIMATION_SPEED * delta_time
        if self.frame_index < len(self.frames):
            self.image = self.frames[int(self.frame_index)]
        else:
            self.active = False
            self.frame_index = 0

    def update(self, delta_time):
        if self.active:
            self.animate(delta_time)
        else:
            if random.randint(0, 2000) == 1:
                self.active = True

class Item(AnimatedSprite):
    def __init__(self, item_type, position, frames, groups, data):
        super().__init__(position, frames, groups)
        self.rect.center = position
        self.item_type = item_type
        self.data = data

    def activate(self):
        if self.item_type == 'gold':
            self.data.coins += 5
        if self.item_type == 'silver':
            self.data.coins += 1
        if self.item_type == 'diamond':
            self.data.coins += 15
        if self.item_type == 'skull':
            self.data.coins += random.randint(1, 50)
        
        if self.item_type == 'potion':
            self.data.health += 1 

class ParticleEffect(AnimatedSprite):
    def __init__(self, position, frames, groups):
        super().__init__(position, frames, groups)
        self.rect.center = position
        self.z = Z_LAYERS['fg']
    def animate(self, delta_time):
        self.frame_index += self.animation_speed * delta_time
        if self.frame_index < len(self.frames):
            self.image = self.frames[int(self.frame_index)]
        else:
            self.kill()

class MovingSprite(AnimatedSprite):
    def __init__(self, frames, groups, start_pos, end_pos, move_direction, speed, flip=False):
        super().__init__(start_pos, frames, groups)

        if move_direction == 'x':
            self.rect.midleft = start_pos
        else:
            self.rect.midtop = start_pos

        self.start_pos = start_pos
        self.end_pos = end_pos
        
        # movement
        self.moving = True
        self.speed = speed
        self.direction = vector(1, 0) if move_direction == 'x' else vector(0, 1)
        self.move_direction = move_direction

        self.flip = flip
        self.reverse = {'x': False, 'y':False}

    def check_border(self):
        # horizontal bounces
        if self.move_direction == 'x':
            if self.rect.right >= self.end_pos[0] and self.direction.x == 1: # if going right and reach bounce
                self.direction.x = -1
                self.rect.right = self.end_pos[0]

            if self.rect.left <= self.start_pos[0] and self.direction.x == -1: # if going left and reach bounce
                self.direction.x = 1
                self.rect.left = self.start_pos[0]
            self.reverse['x'] = True if self.direction.x < 0 else False

        # vertical bounces
        if self.move_direction == 'y':
            if self.rect.bottom >= self.end_pos[1] and self.direction.y == 1: # if going down and reach bounce
                self.direction.y = -1
                self.rect.bottom = self.end_pos[1]
            
            if self.rect.top <= self.start_pos[1] and self.direction.y == -1: # if going up and reach bounce
                self.direction.y = 1
                self.rect.top = self.start_pos[1]
            self.reverse['y'] = True if self.direction.y > 0 else False
    
    def update(self, delta_time):
        self.old_rect = self.rect.copy()
        self.rect.topleft += self.direction * self.speed * delta_time
        self.check_border()

        self.animate(delta_time)

        if self.flip:
            self.image = pygame.transform.flip(self.image, self.reverse['x'], self.reverse['y'])

class Spike(Sprite):
    def __init__(self, position, surface, groups, radius, speed, start_angle, end_angle, z=Z_LAYERS['main']):
        self.center = position
        self.radius = radius
        self.speed = speed
        self.start_angle = start_angle
        self.end_angle = end_angle
        self.angle = self.start_angle
        self.direction = 1
        self.full_circle = True if self.end_angle == -1 else False

        y = self.center[1] + math.sin(math.radians(self.angle)) * self.radius
        x = self.center[0] + math.cos(math.radians(self.angle)) * self.radius

        super().__init__((x, y), surface, groups, z)

    def update(self, delta_time):
        self.angle += self.direction * self.speed * delta_time 

        if not self.full_circle:
            if self.angle >= self.end_angle:
                self.direction = -1
            if self.angle < self.start_angle:
                self.direction = 1

        y = self.center[1] + math.sin(math.radians(self.angle)) * self.radius
        x = self.center[0] + math.cos(math.radians(self.angle)) * self.radius

        self.rect.center = (x,y)

class Cloud(Sprite):
    def __init__(self, position, surface, groups, z=Z_LAYERS['clouds']):
        super().__init__(position, surface, groups, z)
        self.speed = random.randint(50, 120)
        self.direction = -1
        self.rect.midbottom = position

    def update(self, delta_time):
        self.rect.x += self.direction * self.speed * delta_time

        if self.rect.right <= 0:
            self.kill()

class Node(pygame.sprite.Sprite):
    def __init__(self, position, surface, groups, level, data, paths):
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_frect(center=(position[0] + TILE_SIZE / 2, position[1] + TILE_SIZE / 2))
        self.z = Z_LAYERS['path']
        self.level = level
        self.data = data
        self.paths = paths
    
    def can_move(self, direction):
        if direction in list(self.paths.keys()) and int(self.paths[direction][0][0]) <= self.data.unclocked_level:
            return True

class Icon(pygame.sprite.Sprite):
    def __init__(self, position, groups, frames):
        super().__init__(groups)
        self.icon = True

        # image
        self.frames, self.frame_index = frames, 0
        self.state = 'idle'
        self.image = self.frames[self.state][self.frame_index]
        self.z = Z_LAYERS['main']

        # rect
        self.rect = self.image.get_frect(center=position)

        self.path = None

        self.direction = vector()

        self.speed = 400

        self.animation_speed = 20

    def start_move(self, path):
        self.rect.center = path[0]
        self.path = path[1:]
        self.find_path()

    def find_path(self):
        if self.path:
            if self.rect.centerx == self.path[0][0]: # vertical
                self.direction = vector(0, 1 if self.path[0][1] > self.rect.centery else -1)
            else: # horizontal
                self.direction = vector(1 if self.rect.centerx < self.path[0][0] else -1, 0)
        else:
            self.direction = vector()

    def point_collision(self):
        if self.direction.y == 1 and self.rect.centery >= self.path[0][1] or self.direction.y == -1 and self.rect.centery <= self.path[0][1]:
            self.rect.centery = self.path[0][1]
            del self.path[0]
            self.find_path()

        if self.direction.x == 1 and self.rect.centerx >= self.path[0][0] or self.direction.x == -1 and self.rect.centerx <= self.path[0][0]:
            self.rect.centerx = self.path[0][0]
            del self.path[0]
            self.find_path()
    
    def get_state(self):
        self.state = 'idle'
        if self.direction == vector(1, 0):
            self.state = 'right'
        if self.direction == vector(-1, 0):
            self.state = 'left'
        if self.direction == vector(0, 1):
            self.state = 'down'
        if self.direction == vector(0, -1):
            self.state = 'up'
    
    def animate(self, delta_time):
        self.frame_index += ANIMATION_SPEED * delta_time 
        self.image = self.frames[self.state][int(self.frame_index % len(self.frames[self.state]))]

    def update(self, delta_time):
        if self.path:
            self.point_collision()
            self.rect.center += self.direction * self.speed * delta_time
        self.get_state()
        self.animate(delta_time)