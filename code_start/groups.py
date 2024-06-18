from settings import *
from sprites import Sprite, Cloud
from manual_timer import Timer
import random

class WorldSprites(pygame.sprite.Group):
    def __init__(self, data):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.data = data
        self.offset = vector()

    def draw(self, target_position):
        self.offset.x = -(target_position[0] - WINDOW_WIDTH / 2)
        self.offset.y = -(target_position[1] - WINDOW_HEIGHT / 2)

        # background
        for sprite in sorted(self, key=lambda sprite: sprite.z):
            if sprite.z < Z_LAYERS['main']:
                if sprite.z == Z_LAYERS['path']:
                    if sprite.level <= self.data.unlocked_level:
                        self.display_surface.blit(sprite.image, sprite.rect.topleft + self.offset)
                else:
                    self.display_surface.blit(sprite.image, sprite.rect.topleft + self.offset)

        # main
        for sprite in sorted(self, key=lambda sprite: sprite.rect.centery):
            if sprite.z  == Z_LAYERS['main']:
                if hasattr(sprite, 'icon'):
                    self.display_surface.blit(sprite.image, sprite.rect.topleft + self.offset + vector(0,-28))
                else:
                    self.display_surface.blit(sprite.image, sprite.rect.topleft + self.offset)


class AllSprites(pygame.sprite.Group):
    def __init__(self, width, height, clouds, horizon_line, bg_tile=None, top_limit=None):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = vector()
        self.width = width * TILE_SIZE
        self.height = height * TILE_SIZE
        self.horizon_line = horizon_line

        self.borders = {
            'left': 0,
            'right': -self.width + WINDOW_WIDTH,
            'top': top_limit,
            'bottom': -self.height + WINDOW_HEIGHT,
        }

        self.sky = not bg_tile

        if bg_tile != None:
            for column in range(width):
                for row in range(-top_limit // TILE_SIZE - 1, height):
                    x=column*TILE_SIZE
                    y=row*TILE_SIZE
                    Sprite((x,y), bg_tile, self, -1)
        if self.sky and bg_tile == None:
            self.large_cloud = clouds['large']
            self.small_clouds = clouds['small']

            self.cloud_direction = -1

            # large cloud
            self.large_cloud_speed = 50
            self.large_cloud_x = 0
            self.large_cloud_tiles = int(self.width / self.large_cloud.get_width()) + 2
            self.large_cloud_width, self.large_cloud_height = self.large_cloud.get_size()

            # small clouds
            self.cloud_timer = Timer(2500, self.create_cloud, True)
            self.cloud_timer.activate()
            for _ in range(5):
                position = (random.randint(0, self.width), random.randint(self.borders['top'], self.horizon_line))
                surface = random.choice(self.small_clouds)
                Cloud(position, surface, self)

    def camera_constraint(self):
        self.offset.x = self.offset.x if self.offset.x < self.borders['left'] else self.borders['left']
        self.offset.x = self.offset.x if self.offset.x > self.borders['right'] else self.borders['right']

        self.offset.y = self.offset.y if self.offset.y > self.borders['bottom'] else self.borders['bottom']
        self.offset.y = self.offset.y if self.offset.y < self.borders['top'] else self.borders['top']
    
    def create_cloud(self):
        Cloud((random.randint(self.width+400, self.width+600), random.randint(self.borders['top'], self.horizon_line)), random.choice(self.small_clouds), self)

    def draw_sky(self):
        self.display_surface.fill('#ddc6a1')
        horizon_position = self.horizon_line + self.offset.y

        sea_rect = pygame.FRect(0, horizon_position, WINDOW_WIDTH, WINDOW_HEIGHT - horizon_position)
        pygame.draw.rect(self.display_surface, '#92a9ce', sea_rect)

        # accentuate horizone line
        pygame.draw.line(self.display_surface, '#f5f1de', (0, horizon_position), (WINDOW_WIDTH, horizon_position), 4)

    def draw_large_cloud(self, delta_time):
        self.large_cloud_x += self.cloud_direction * self.large_cloud_speed * delta_time
        if self.large_cloud_x <= -self.large_cloud_width:
            self.large_cloud_x = 0

        for cloud in range(self.large_cloud_tiles):
            left = self.large_cloud_x + self.large_cloud_width * cloud + self.offset.x
            top = self.horizon_line - self.large_cloud_height + self.offset.y
            self.display_surface.blit(self.large_cloud, (left, top))

    def draw(self, target_position, delta_time):

        self.offset.x = -(target_position[0] - WINDOW_WIDTH / 2)
        self.offset.y = -(target_position[1] - WINDOW_HEIGHT / 2)
        self.camera_constraint()

        if self.sky:
            self.cloud_timer.update()
            self.draw_sky()
            self.draw_large_cloud(delta_time)


        for sprite in sorted(self, key = lambda sprite: sprite.z):
            offset_pos = sprite.rect.topleft + self.offset
            self.display_surface.blit(sprite.image, offset_pos)