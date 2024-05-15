from settings import *
from manual_timer import Timer 

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
        self.jump_height = 800
        self.jump = False

        # collision
        self.collision_sprites = collision_sprites
        self.on_surface = {
            'floor': False,
            'left': False,
            'right': False
        }

        self.platform = None

        # timer
        self.timers = {
            "wall jump": Timer(500),
            "wall slide block": Timer(250)
        }
    
    def input(self):
        keys = pygame.key.get_pressed()

        input_vector = vector()

        if not self.timers['wall jump'].active:  # not allowing to user change x direction while we have wall kind jumping
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                input_vector.x += 1

            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                input_vector.x -=1

            # using normilize() method to make sure the length of vector will be always one. And also we are checking
            # if length of our vector is not equal to zero, because we cannot use normalize() in this situation
            self.direction.x = input_vector.normalize().x if input_vector else input_vector.x

        if keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]:
            self.jump = True

    def move(self, delta_time):
        # increasing position of the rect by speed in certain direction

        # horizontal
        self.rect.x += self.direction.x * self.speed * delta_time 
        self.collision('horizontal')

        # vertical
        if not self.on_surface['floor'] and any((self.on_surface['left'], self.on_surface['right'])) and not self.timers['wall slide block'].active:
            self.direction.y = 0
            self.rect.y += self.gravity / 10 * delta_time

        else:
            self.direction.y += self.gravity / 2 * delta_time
            self.rect.y += self.direction.y * delta_time
            self.direction.y += self.gravity / 2 * delta_time

        
        # checking how to execute jump logic
        if self.jump:
            # checking if we are jumping while locating on the floor
            if self.on_surface['floor']:
                self.direction.y = -self.jump_height
                self.timers["wall slide block"].activate()
                self.rect.bottom -=1

            # check if we are jumping while can be colliding with some walls not on the floor
            elif any((self.on_surface['left'], self.on_surface['right'])) and not self.timers['wall slide block'].active:
                self.timers['wall jump'].activate() # activating wall jump timer to control jump frequency
                self.direction.y = -self.jump_height
                self.direction.x = 1 if self.on_surface['left'] else -1  # changing x coordinate of player to jump in opposite side

            self.jump = False
            
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
                    
                    # top side collision
                    if self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
                        self.rect.top = sprite.rect.bottom

                    # bottom side collision
                    if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
                        self.rect.bottom = sprite.rect.top

                    # if we have any vertical collisions, we are not apllying gravity
                    self.direction.y = 0

    def platform_move(self, delta_time):
        if self.platform:
            self.rect.topleft += self.platform.direction * self.platform.speed * delta_time 

    def check_contact(self):
        # creating rects that will surround our player to check side of needed collisions
        floor_rect = pygame.Rect(self.rect.bottomleft, (self.rect.width, 2)) # rect that will be on the bottom side player
        right_rect = pygame.Rect(self.rect.topright + vector(0, self.rect.height / 4), (2, self.rect.height / 2)) # player`s right side
        left_rect = pygame.Rect(self.rect.topleft + vector(-2, self.rect.height / 4), (2, self.rect.height / 2)) # players`s left side

        # generating all possibe rects that can be collided
        collide_rects = [sprite.rect for sprite in self.collision_sprites]

        # collisions
        self.on_surface['floor'] = True if floor_rect.collidelist(collide_rects) >= 0 else False
        self.on_surface['right'] = True if right_rect.collidelist(collide_rects) >= 0 else False
        self.on_surface['left']  = True if left_rect.collidelist(collide_rects)  >= 0 else False 

        self.platform = None
        for sprite in [sprite for sprite in self.collision_sprites.sprites() if hasattr(sprite, 'moving')]:
            if sprite.rect.colliderect(floor_rect):
                self.platform = sprite
    
    def update_timers(self):
        for timer in self.timers.values():
            timer.update()  # controlling every timer that we have automatically


    def update(self, delta_time):
        self.old_rect = self.rect.copy()
        self.update_timers()
        self.input()
        self.move(delta_time)
        self.platform_move(delta_time)
        self.check_contact()
