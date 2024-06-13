from settings import *
from manual_timer import Timer 
from os.path import join

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites, semi_collision_sprites, frames):
        # general setups
        super().__init__(groups)
        self.z = Z_LAYERS['main']

        # image
        self.frames, self.frame_index = frames, 0
        self.state, self.facing_right = 'idle', True
        self.image = self.frames[self.state][self.frame_index]

        # rects
        self.rect = self.image.get_frect(topleft=pos)
        self.hitbox_rect = self.rect.inflate(-76, -36)
        self.old_rect = self.hitbox_rect.copy()

        # movement
        self.direction = vector()
        self.speed = 200
        self.gravity = 1000
        self.jump_height = 800
        self.jump = False
        self.attacking = False

        # collision
        self.collision_sprites = collision_sprites
        self.semi_collision_sprites = semi_collision_sprites
        self.on_surface = {
            'floor': False,
            'left': False,
            'right': False
        }

        self.platform = None

        # timer
        self.timers = {
            "wall jump": Timer(500),
            "wall slide block": Timer(250),
            "platform skip": Timer(100),
            "jumping": Timer(500),
            "attack block": Timer(800)
        }
    
    def input(self):
        keys = pygame.key.get_pressed()

        input_vector = vector()

        if not self.timers['wall jump'].active:  # not allowing to user change x direction while we have wall kind jumping
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                input_vector.x += 1
                self.facing_right = True

            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                input_vector.x -=1
                self.facing_right = False
            
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.timers["platform skip"].activate()
            
            if keys[pygame.K_x]:
                self.attack()

            # using normilize() method to make sure the length of vector will be always one. And also we are checking
            # if length of our vector is not equal to zero, because we cannot use normalize() in this situation
            self.direction.x = input_vector.normalize().x if input_vector else input_vector.x

        if keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]:
            self.jump = True
            self.timers['jumping'].activate()
    
    def attack(self):
        if not self.timers['attack block'].active:
            self.attacking = True
            self.frame_index = 0
            self.timers["attack block"].activate()

    def move(self, delta_time):
        # increasing position of the rect by speed in certain direction

        # horizontal
        self.hitbox_rect.x += self.direction.x * self.speed * delta_time 
        self.collision('horizontal')

        # vertical
        if not self.on_surface['floor'] and any((self.on_surface['left'], self.on_surface['right'])) and not self.timers['wall slide block'].active:
            self.direction.y = 0
            self.hitbox_rect.y += self.gravity / 10 * delta_time

        else:
            self.direction.y += self.gravity / 2 * delta_time
            self.hitbox_rect.y += self.direction.y * delta_time
            self.direction.y += self.gravity / 2 * delta_time

        
        # checking how to execute jump logic
        if self.jump:
            # checking if we are jumping while locating on the floor
            if self.on_surface['floor']:
                self.direction.y = -self.jump_height
                self.timers["wall slide block"].activate()
                self.hitbox_rect.bottom -=1

            # check if we are jumping while can be colliding with some walls not on the floor
            elif any((self.on_surface['left'], self.on_surface['right'])) and not self.timers['wall slide block'].active:
                self.timers['wall jump'].activate() # activating wall jump timer to control jump frequency
                self.direction.y = -self.jump_height
                self.direction.x = 1 if self.on_surface['left'] else -1  # changing x coordinate of player to jump in opposite side

            self.jump = False
            
        self.collision('vertical')
        self.semi_collision()
        self.rect.center = self.hitbox_rect.center

    
    def collision(self, axis):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                if axis == 'horizontal':
                    # left side collision
                    if self.hitbox_rect.left <= sprite.rect.right and int(self.old_rect.left) >= int(sprite.old_rect.right):
                        self.hitbox_rect.left = sprite.rect.right

                    # right side collision
                    if self.hitbox_rect.right >= sprite.rect.left and int(self.old_rect.right) <= int(sprite.old_rect.left):
                        self.hitbox_rect.right = sprite.rect.left

                else: # if axis == 'vertical'
                    
                    # top side collision
                    if self.hitbox_rect.top <= sprite.rect.bottom and int(self.old_rect.top) >= int(sprite.old_rect.bottom):
                        self.hitbox_rect.top = sprite.rect.bottom
                        if hasattr(sprite, 'moving'):
                            self.hitbox_rect.top += 6

                    # bottom side collision
                    if self.hitbox_rect.bottom >= sprite.rect.top and int(self.old_rect.bottom) <= int(sprite.old_rect.top):
                        self.hitbox_rect.bottom = sprite.rect.top

                    # if we have any vertical collisions, we are not apllying gravity
                    self.direction.y = 0

    def semi_collision(self):
        if not self.timers["platform skip"].active:
            for sprite in self.semi_collision_sprites:
                if sprite.rect.colliderect(self.hitbox_rect):
                    # bottom side collision
                    if self.hitbox_rect.bottom >= sprite.rect.top and int(self.old_rect.bottom) <= sprite.old_rect.top:
                        self.hitbox_rect.bottom = sprite.rect.top
                        if self.direction.y > 0:
                            self.direction.y = 0

    def platform_move(self, delta_time):
        if self.platform and not self.timers['jumping'].active and not self.timers['platform skip'].active:
            self.hitbox_rect.topleft += self.platform.direction * self.platform.speed * delta_time

    def check_contact(self):
        # creating rects that will surround our player to check side of needed collisions
        floor_rect = pygame.Rect(self.hitbox_rect.bottomleft, (self.hitbox_rect.width, 2)) # rect that will be on the bottom side player
        right_rect = pygame.Rect(self.hitbox_rect.topright + vector(0, self.hitbox_rect.height / 4), (2, self.hitbox_rect.height / 2)) # player`s right side
        left_rect = pygame.Rect(self.hitbox_rect.topleft + vector(-2, self.hitbox_rect.height / 4), (2, self.hitbox_rect.height / 2)) # players`s left side

        # generating all possibe rects that can be collided
        collide_rects = [sprite.rect for sprite in self.collision_sprites]

        semi_collide_rects = [sprite.rect for sprite in self.semi_collision_sprites]

        # collisions
        self.on_surface['floor'] = True if floor_rect.collidelist(collide_rects) >= 0  or floor_rect.collidelist(semi_collide_rects) >= 0  and self.direction.y >= 0 else False
        self.on_surface['right'] = True if right_rect.collidelist(collide_rects) >= 0 else False
        self.on_surface['left']  = True if left_rect.collidelist(collide_rects)  >= 0 else False 

        self.platform = None
        sprites = self.collision_sprites.sprites() + self.semi_collision_sprites.sprites()
        for sprite in [sprite for sprite in sprites if hasattr(sprite, 'moving')]:
            if sprite.rect.colliderect(floor_rect):
                self.platform = sprite
    
    def update_timers(self):
        for timer in self.timers.values():
            timer.update()  # controlling every timer that we have automatically

    def animate(self, delta_time):
        self.frame_index += ANIMATION_SPEED * delta_time
        if self.state == 'attack' and self.frame_index >= len(self.frames[self.state]):
            self.state = 'idle'
        self.image = self.frames[self.state][int(self.frame_index % len(self.frames[self.state]))]
        self.image = self.image if self.facing_right else pygame.transform.flip(self.image, True, False)

        if self.attacking and self.frame_index >= len(self.frames[self.state]):
            self.attacking = False

    def get_state(self):
        if self.on_surface['floor']:
            if self.attacking:
                self.state = 'attack'
            else:
                self.state = 'idle' if self.direction.x == 0 else 'run'
        else:
            if self.attacking:
                self.state = 'air_attack'
            else:
                if any([self.on_surface['left'], self.on_surface['right']]):
                    self.state = 'wall'
                else:
                    self.state = 'jump' if self.direction.y < 0 else 'fall'

    def update(self, delta_time):
        self.old_rect = self.hitbox_rect.copy()
        self.update_timers()

        self.input()
        self.move(delta_time)
        self.platform_move(delta_time)
        self.check_contact()

        self.get_state()
        self.animate(delta_time)
