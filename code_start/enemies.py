from settings import *
import random

class Tooth(pygame.sprite.Sprite):
    def __init__(self, position, frames, groups, collision_sprites):
        super().__init__(groups)
        self.frames, self.frame_index = frames, 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_frect(topleft=position)
        self.z = Z_LAYERS['main']

        self.direction = random.choice((-1,1))
        self.collision_rects = [sprite.rect for sprite in collision_sprites]

        self.speed = 200

    def update(self, delta_time):

        # animate
        self.frame_index += ANIMATION_SPEED * delta_time
        self.image = self.frames[int(self.frame_index % len(self.frames))]
        self.image = pygame.transform.flip(self.image, True, False) if self.direction < 0 else self.image

        # movement
        self.rect.x += self.direction * self.speed * delta_time

        floor_rect_right = pygame.FRect(self.rect.bottomright, (1, 1))
        floor_rect_left = pygame.FRect(self.rect.bottomleft, (-1, 1))

        if (floor_rect_right.collidelist(self.collision_rects) < 0 and self.direction > 0) or\
        floor_rect_left.collidelist(self.collision_rects) < 0 and self.direction < 0:
             self.direction *= -1
        
class Shell(pygame.sprite.Sprite):
    def __init__(self, position, frames, groups, reverse):
        super().__init__(groups)

        if reverse:
            self.frames = {}
            for key, surfaces in frames.items():
                self.frames[key] = [pygame.transform.flip(surface, True, False) for surface in surfaces]
            self.bullet_direction = -1  
        else:
            self.frames = frames
            self.bullet_direction = 1

        self.frame_index = 0
        self.state = 'idle'
        self.image = self.frames[self.state][self.frame_index]

        self.rect = self.image.get_rect(topleft=position)
        self.old_rect = self.rect.copy()
        self.z = Z_LAYERS['main']

