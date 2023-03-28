import random
import pygame
import math
import json, os
from config import SPEED, TOP_BAR_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT


class Grunt:
    collided_player = False
    size = 30
    speed = 5
    elapsed = 0
    
    def __init__(self, rect):
        self.grunt_sprite = pygame.image.load(
                "img/grunt.png").convert_alpha()
        self.grunt_angle = 0
        self.random_pos(rect)
        self.start_time = 0
        self.end = 0
    
    def random_pos(self, rects):
        while True:
            x = random.randint(100, SCREEN_WIDTH - 200)
            y = random.randint(100, SCREEN_HEIGHT - TOP_BAR_HEIGHT - 100)

            rect = pygame.Rect(x, y, self.size, self.size)
            if rect.collidelist(rects) < 0:
                self.x = x
                self.y = y
                break

    def animate_idle(self):
        self.elapsed += 1
        if self.elapsed == 10:
            self.grunt_angle += 1
        if self.elapsed > 10:
            self.elapsed = 0
        if self.grunt_angle > 2:
            self.grunt_angle = 0

    def get_image(self) -> pygame.Surface:
        sub = self.grunt_sprite.subsurface(
            (self.grunt_angle * self.size, 0, self.size, self.size))

        vertical = 0
        horizontal = 0
        return pygame.transform.flip(sub, horizontal, vertical)

    def get_rect(self):
        return (self.x, self.y, self.size, self.size)
    
    def get_coord(self):
        return (self.x, self.y)

    def move_toward_player(self, player_coords):
        dx = player_coords[0] - self.x
        dy = player_coords[1] - self.y
        angle = math.atan2(dy, dx)
        self.start_time += 1
        if self.start_time == 5: 
            self.x += self.speed * math.cos(angle)
            self.y += self.speed * math.sin(angle)
        if self.start_time > 5:
            self.start_time = 0

    def draw(self, surface: pygame.Surface):
        self.animate_idle()
        surface.blit(self.get_image(), self.get_coord())

    def is_colliding_player(self, player_rect):
        self.collided_player = pygame.Rect(
            self.x, self.y, self.size, self.size).colliderect(player_rect)
        return self.collided_player
    

