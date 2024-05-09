from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.Surface((48, 56))
        self.image.fill('red')
        self.rect = self.image.get_frect(topleft=pos)

        # movement
        self.direction = vector()
        self.speed = 200
    
    def input(self):
        keys = pygame.key.get_pressed()

        input_vector = vector()
        if keys[pygame.K_RIGHT]:
            input_vector.x += 1

        if keys[pygame.K_LEFT]:
            input_vector.x -=1
        
        # using normilize() method to make sure the length of vector will be always one. And also we are checking
        # if length if our vector is not equal to zero, because we cannot use normalize() in this situation
        self.direction = input_vector.normalize() if input_vector else input_vector

    def move(self, delta_time):
        self.rect.topleft += self.direction * self.speed * delta_time # increasing position of the rect by speed in certain direction

    def update(self, delta_time):
        self.input()
        self.move(delta_time)