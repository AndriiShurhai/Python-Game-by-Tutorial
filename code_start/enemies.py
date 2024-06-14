from settings import *
import random
import math
from manual_timer import Timer

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
        (floor_rect_left.collidelist(self.collision_rects) < 0 and self.direction < 0):
             self.direction *= -1
        

class Shell(pygame.sprite.Sprite):
    def __init__(self, position, frames, groups, player, create_pearl):
        super().__init__(groups)


        self.frame_index = 0
        self.frames = frames
        self.state = 'idle'
        self.original_image = self.frames[self.state][self.frame_index]
        self.image = self.original_image

        self.rect = self.image.get_rect(topleft=position)
        self.old_rect = self.rect.copy()
        self.z = Z_LAYERS['main']

        self.start_angle = 0
        self.end_angle = 180

        self.shoot_timer = Timer(4000)

        self.player = player

        self.flipped = False
        
        self.has_fired = False

        self.create_pearl = create_pearl

        self.angle_degrees = 0

        self.angle_radians = None

    
    def state_management(self):
        player_position = pygame.math.Vector2(self.player.hitbox_rect.center)
        shell_position = pygame.math.Vector2(self.rect.center)
        player_near = shell_position.distance_to(player_position) < 400

        if player_near and not self.shoot_timer.active and self.start_angle <= -self.angle_degrees <= self.end_angle:
            self.state = 'fire'
            self.frame_index = 0
            self.shoot_timer.activate()
    
    def angle_management(self, delta_time):
        vector_to_player = pygame.math.Vector2(self.player.hitbox_rect.center) - pygame.math.Vector2(self.rect.center)
        self.angle_radians = math.atan2(vector_to_player.y, vector_to_player.x)
        self.angle_degrees = math.degrees(self.angle_radians)

        # Determine if the player is to the left or right of the shell
        player_is_left = self.player.hitbox_rect.centerx < self.rect.centerx
        # Check if the angle is within the specified range
        if self.start_angle <= -self.angle_degrees <= self.end_angle:

            # Flip the image if the player is on the other side
            if player_is_left and not self.flipped:
                self.flipped = True
                self.original_image = pygame.transform.flip(self.original_image, False, True)
                
            elif not player_is_left and self.flipped:
                self.flipped = False
                self.original_image = pygame.transform.flip(self.original_image, False, True)

        self.frame_index += ANIMATION_SPEED * delta_time
        if self.frame_index < len(self.frames[self.state]):
            self.original_image = self.frames[self.state][int(self.frame_index)] if not player_is_left else pygame.transform.flip(self.frames[self.state][int(self.frame_index)], False, True)
            if self.state == 'fire' and int(self.frame_index) == 3 and self.has_fired:
                self.create_pearl(self.rect.center, self.angle_radians)
                self.has_fired = False
        else:
            self.frame_index = 0
            if self.state == 'fire':
                self.state = 'idle'
                self.has_fired = True

        # Rotate the original image
        self.image = pygame.transform.rotate(self.original_image, -self.angle_degrees)

        # Update rect to match the new image
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self, delta_time):
        self.shoot_timer.update()
        self.state_management()
        self.angle_management(delta_time)

class Pearl(pygame.sprite.Sprite):
    def __init__(self, position, groups, surface, speed, angle):
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_frect(center=position)
        self.speed = speed
        self.z = Z_LAYERS['main']

        self.velocity = pygame.math.Vector2(math.cos(angle), math.sin(angle)) * self.speed

    
    def update(self, delta_time):
        self.rect.x += self.velocity.x * delta_time
        self.rect.y += self.velocity.y * delta_time

        if not pygame.display.get_surface().get_rect().contains(self.rect):
            self.kill()



