import random
import pygame
import math
import json, os
from config import SPEED, TOP_BAR_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT


class Hulk:
    collided_family = False
    size = 30
    speed = 5
    elapsed = 0

    def __init__(self, rect):
        self.hulk_sprite = pygame.image.load(
                "img/hulk.png").convert_alpha()
        self.hulk_angle = 0
        self.random_pos(rect)
        self.start_time = 0
        self.end = 0
        self.hulk_direction = random.randint(0, 1)
        self.rand_coord = self.random_direction()
        print(self.rand_coord)
    
    def random_pos(self, rects):
        while True:
            x = random.randint(100, SCREEN_WIDTH - 200)
            y = random.randint(100, SCREEN_HEIGHT - TOP_BAR_HEIGHT - 100)

            rect = pygame.Rect(x, y, self.size, self.size)
            if rect.collidelist(rects) < 0:
                self.x = x
                self.y = y
                break

    def random_direction(self):
        if self.hulk_direction == 0:
            self.hulk_direction = 1
            return (random.randint(100, SCREEN_WIDTH - 200),
                    self.y)
        else:
            self.hulk_direction = 0
            return (self.x,
                    random.randint(100, SCREEN_HEIGHT - TOP_BAR_HEIGHT - 100))

    def move(self):
        dx = self.rand_coord[0] - self.x
        dy = self.rand_coord[1] - self.y
        angle = math.atan2(dy, dx)
        self.start_time += 1
        if self.start_time == 5:
            self.x += self.speed * math.cos(angle)
            self.y += self.speed * math.sin(angle)
        if self.start_time > 5:
            self.start_time = 0
        if check_destination(self.rand_coord, self.x, self.y):
            self.rand_coord = self.random_direction()

    def animate_idle(self):
        self.elapsed += 1
        if self.elapsed == 10:
            self.hulk_angle += 1
        if self.elapsed > 10:
            self.elapsed = 0
        if self.hulk_angle > 8:
            self.hulk_angle = 0

    def get_image(self) -> pygame.Surface:
        sub = self.hulk_sprite.subsurface(
            (self.hulk_angle * self.size, 0, self.size, self.size))

        vertical = 0
        horizontal = 0
        return pygame.transform.flip(sub, horizontal, vertical)

    def get_rect(self):
        return (self.x, self.y, self.size, self.size)
    
    def get_coord(self):
        return (self.x, self.y)

    def draw(self, surface: pygame.Surface):
        self.animate_idle()
        surface.blit(self.get_image(), self.get_coord())

    def is_colliding_player(self, player_rect):
        self.collided_player = pygame.Rect(
            self.x, self.y, self.size, self.size).colliderect(player_rect)
        return self.collided_player


def check_destination(pos, x, y):     
    if abs(pos[0] - x) < 10 and abs(pos[1] - y) < 10:
        return True