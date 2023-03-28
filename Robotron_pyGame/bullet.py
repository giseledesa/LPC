import pygame

from config import SPEED


class Bullet:
    size = 30
    speed = 5
    collided_enemy = False
    pygame.mixer.init()

    def __init__(self, x, y,  x_direction, y_direction, angle) -> None:
        self.bullet_sprite = pygame.image.load("img/bullet.png")
        self.x = x
        self.y = y
        self.x_velocity = x_direction * self.speed
        self.y_velocity = y_direction * self.speed
        self.x_direction = x_direction if x_direction >= 0 else -x_direction
        self.y_direction = y_direction if y_direction >= 0 else -y_direction
        self.angle = angle
        self.start_time = pygame.time.get_ticks()
        self.end_life = False

    def get_image(self) -> pygame.Surface:
        sub = self.bullet_sprite.subsurface(
            (self.angle * self.size + 2, 0, self.size, self.size))

        vertical = 0
        horizontal = 1
        return pygame.transform.flip(sub, horizontal, vertical)

    def get_coord(self):
        return (self.x, self.y)

    def is_colliding_walls(self, map):
        for rect in map:
            is_in_x = self.x >= rect[0] and self.x + \
                self.size <= rect[0] + rect[2]
            is_in_y = self.y >= rect[1] and self.y + \
                self.size <= rect[1] + rect[3]

            if is_in_x and self.y + self.size >= rect[1] and \
                    self.y + self.size <= rect[1] + rect[3]:
                self.end_life = True
               
            if is_in_x and self.y <= rect[1] + rect[3] and self.y >= rect[1]:
                self.end_life = True

            if is_in_y and self.x <= rect[0] + rect[2] and self.x >= rect[0]:
                self.end_life = True
               
            if is_in_y and self.x + self.size >= rect[0] and \
                    self.x + self.size <= rect[0] + rect[2]:
                self.end_life = True
              
    def is_colliding_enemy(self, enemy_rect):
        self.collided_enemy = pygame.Rect(
            self.x, self.y, self.size, self.size).colliderect(enemy_rect)

    def move(self, map):
        self.is_colliding_walls(map)

        self.x += self.x_velocity
        self.y += self.y_velocity

    def get_rect(self):
        return (self.x, self.y, self.size, self.size)
