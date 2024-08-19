from settings import *
import random
import math
from manual_timer import Timer

class HealthBar(pygame.sprite.Sprite):
    def __init__(self, group, enemy):
        super().__init__(group)
        self.enemy = enemy
        self.z = Z_LAYERS['main']
        self.bar_width = 50
        self.bar_height = 5
        self.image = pygame.Surface((self.bar_width, self.bar_height))

        # Positioning the health bar above the enemy
        self.rect = pygame.rect.FRect(
            enemy.rect.centerx - self.bar_width / 2, 
            enemy.rect.top - self.bar_height - 5, 
            self.bar_width, 
            self.bar_height
        )

    def update(self, *args):
        # Update the position based on the enemy's position
        self.rect.topleft = (
            self.enemy.rect.centerx - self.bar_width / 2, 
            self.enemy.rect.top - self.bar_height - 5
        )

        # Update the health bar based on the enemy's health
        health_ratio = self.enemy.health / 100  # Assuming max health is 100
        self.image.fill((0, 0, 0))  # Background color
        pygame.draw.rect(self.image, (255, 0, 0), (0, 0, self.bar_width * health_ratio, self.bar_height)) 


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

        self.hit_timer = Timer(250)
        self.take_damage_timer = Timer(700)

        self.health = 100

    def reverse(self):
        if not self.hit_timer.active:
            self.direction *=-1
            self.hit_timer.activate()
    
    def take_damage(self, amount):
        if not self.take_damage_timer.active:
            self.health -= amount
            self.take_damage_timer.activate()
        if self.health <= 0:
            self.kill()

    def update(self, delta_time):
        self.take_damage_timer.update()
        self.hit_timer.update()
        # animate
        self.frame_index += ANIMATION_SPEED * delta_time
        self.image = self.frames[int(self.frame_index % len(self.frames))]
        self.image = pygame.transform.flip(self.image, True, False) if self.direction < 0 else self.image

        # movement
        self.rect.x += self.direction * self.speed * delta_time

        floor_rect_right = pygame.FRect(self.rect.bottomright, (1, 1))
        floor_rect_left = pygame.FRect(self.rect.bottomleft, (-1, 1))
        wall_rect = pygame.FRect(self.rect.topleft + vector(-1, 0), (self.rect.width + 2, 1))

        if (floor_rect_right.collidelist(self.collision_rects) < 0 and self.direction > 0) or\
        (floor_rect_left.collidelist(self.collision_rects) < 0 and self.direction < 0) or\
            wall_rect.collidelist(self.collision_rects) != -1:
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
        self.take_damage_timer = Timer(900)

        self.player = player

        self.flipped = False
        
        self.has_fired = False

        self.create_pearl = create_pearl

        self.angle_degrees = 0

        self.angle_radians = None

        self.health = 75
    
    def state_management(self):
        player_position = pygame.math.Vector2(self.player.hitbox_rect.center)
        shell_position = pygame.math.Vector2(self.rect.center)
        player_near = shell_position.distance_to(player_position) < 400

        if player_near and not self.shoot_timer.active and self.start_angle <= -self.angle_degrees <= self.end_angle:
            self.state = 'fire'
            self.frame_index = 0
            self.shoot_timer.activate()
    
    def angle_management(self):
        vector_to_player = pygame.math.Vector2(self.player.hitbox_rect.center) - pygame.math.Vector2(self.rect.center)
        self.angle_radians = math.atan2(vector_to_player.y, vector_to_player.x)
        self.angle_degrees = math.degrees(self.angle_radians)

        # Determine if the player is to the left or right of the shell
        self.player_is_left = self.player.hitbox_rect.centerx < self.rect.centerx
        # Check if the angle is within the specified range
        if self.start_angle <= -self.angle_degrees <= self.end_angle:

            # Flip the image if the player is on the other side
            if self.player_is_left and not self.flipped:
                self.flipped = True
                self.original_image = pygame.transform.flip(self.original_image, False, True)
                
            elif not self.player_is_left and self.flipped:
                self.flipped = False
                self.original_image = pygame.transform.flip(self.original_image, False, True)

        # Rotate the original image
        self.image = pygame.transform.rotate(self.original_image, -self.angle_degrees)

        # Update rect to match the new image
        self.rect = self.image.get_rect(center=self.rect.center)

    def take_damage(self, amount):
        if not self.take_damage_timer.active:
            self.health -= amount
            self.take_damage_timer.activate()
        if self.health <= 0:
            self.kill()

    def update(self, delta_time):
        self.take_damage_timer.update()
        self.shoot_timer.update()
        self.angle_management()
        self.state_management()

        self.frame_index += ANIMATION_SPEED * delta_time
        if self.frame_index < len(self.frames[self.state]):
            self.original_image = self.frames[self.state][int(self.frame_index)] if not self.player_is_left else pygame.transform.flip(self.frames[self.state][int(self.frame_index)], False, True)
            if self.state == 'fire' and int(self.frame_index) == 3 and not self.has_fired:
                self.create_pearl(self.rect.center, angle=self.angle_radians)
                self.has_fired = True
        else:
            self.frame_index = 0
            if self.state == 'fire':
                self.state = 'idle'
                self.has_fired = False

    def draw(self, surface):
        super().draw(surface)
        self.health_bar.draw(surface, self.rect.topleft)

class Pearl(pygame.sprite.Sprite):
    def __init__(self, position, groups, surface, speed, angle):
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_frect(center=position)
        self.speed = speed
        self.z = Z_LAYERS['main']

        self.hit_timer = Timer(250)

        self.velocity = pygame.math.Vector2(math.cos(angle), math.sin(angle)) * self.speed

    
    def reverse(self):
        if not self.hit_timer.active:
            self.velocity.x *= random.uniform(-10, -1)
            self.velocity.y *= random.uniform(-10, -1)
            self.hit_timer.activate()
    
    def update(self, delta_time):
        self.hit_timer.update()

        self.rect.x += self.velocity.x * delta_time
        self.rect.y += self.velocity.y * delta_time
        
