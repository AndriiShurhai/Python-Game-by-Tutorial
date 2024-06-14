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
        
        if self.item_type == 'portion':
            self.health += 1 

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
        self.full_circle = True if self.angle == -1 else False

        x = self.center[0] + self.radius * math.cos(math.radians(self.angle))
        y = self.center[1] + self.radius * math.sin(math.radians(self.angle))

        super().__init__((x, y), surface, groups, z)

    def update(self, delta_time):
        self.angle += self.direction * self.speed * delta_time 

        if not self.full_circle:
            if self.angle >= self.end_angle:
                self.direction = -1
            if self.angle < self.start_angle:
                self.direction = 1

        x = self.center[0] + self.radius * math.cos(math.radians(self.angle))
        y = self.center[1] + self.radius * math.sin(math.radians(self.angle))

        self.rect.center = (x,y)

