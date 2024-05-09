from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites):
        super().__init__(groups)
        self.image = pygame.Surface((48, 56))
        self.image.fill('red')

        # rects
        self.rect = self.image.get_frect(topleft=pos)
        self.old_rect = self.rect.copy()

        # movement
        self.direction = vector()
        self.speed = 200
        self.gravity = 1000

        # collision
        self.collision_sprites = collision_sprites
    
    def input(self):
        keys = pygame.key.get_pressed()

        input_vector = vector()
        if keys[pygame.K_RIGHT]:
            input_vector.x += 1

        if keys[pygame.K_LEFT]:
            input_vector.x -=1
        
        # using normilize() method to make sure the length of vector will be always one. And also we are checking
        # if length if our vector is not equal to zero, because we cannot use normalize() in this situation
        self.direction.x = input_vector.normalize().x if input_vector else input_vector.x

    def move(self, delta_time):
        # increasing position of the rect by speed in certain direction

        self.rect.x += self.direction.x * self.speed * delta_time 
        self.collision('horizontal')

        self.direction.y += self.gravity / 2 * delta_time
        self.rect.y += self.direction.y * delta_time
        self.direction.y += self.gravity / 2 * delta_time
        self.collision('vertical')



    def collision(self, axis):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.rect):
                if axis == 'horizontal':
                    # left side collision
                    if self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.old_rect.right:
                        self.rect.left = sprite.rect.right

                    # right side collision
                    if self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.old_rect.left:
                        self.rect.right = sprite.rect.left

                else: # if axis == 'vertical'
                    # bottom side collision
                    if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
                        self.rect.bottom = sprite.rect.top
                    
                    # top side collision
                    if self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
                        self.rect.top = sprite.rect.bottom

                    # if we have any vertical collisions, we are not apllying gravity
                    self.direction.y = 0

    def update(self, delta_time):
        self.old_rect = self.rect.copy()
        self.input()
        self.move(delta_time)