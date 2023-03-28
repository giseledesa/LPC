import random
import pygame
import math
import json, os
from config import SPEED, TOP_BAR_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT


def check_destination(pos, x, y):     
    if pos[0] - x < 5 and pos[1] - y < 5:         
        return True


class Family:
    collided_player = False
    size = 30
    speed = 5
    elapsed = 0
    vector = None
    
    def __init__(self, rect, sprite):
        if sprite == 0:
            self.family_sprite = self.family_sprite = pygame.image.load(
                    "img/mother.png").convert_alpha()
        elif sprite == 1:
            self.family_sprite = self.family_sprite = pygame.image.load(
                    "img/father.png").convert_alpha()
        elif sprite == 2:
            self.family_sprite = self.family_sprite = pygame.image.load(
                    "img/child.png").convert_alpha()
        self.family_angle = 0
        self.random_pos(rect)
        self.start_time = 0
        self.rect = self.get_rect()
        self.end = 0
        self.prog = False
        self.dead = False
        self.rand_coord = (random.randint(100, SCREEN_WIDTH - 200),                            
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
            self.rand_coord = (random.randint(100, SCREEN_WIDTH - 150),
                               random.randint(100, SCREEN_HEIGHT - TOP_BAR_HEIGHT - 50))

    def move_toward_player(self, player_coords):
        self.speed = 6
        self.start_time += 1
        x = 1 if player_coords[0] > self.x else -1
        y = 1 if player_coords[1] > self.y else -1
        if random.random() < 0.25:
            x = -x
        if random.random() < 0.25:
            y = -y
        if self.start_time == 3:
            self.vector = pygame.Vector2(x, y)
            self.x += self.vector[0] * self.speed
            self.y += self.vector[1] * self.speed
            self.x += x
            self.y += y
        if self.start_time > 3:
            self.start_time = 0
        

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
        if self.dead:
            self.family_angle = 13
        if not self.dead:
            self.elapsed += 1
            if self.elapsed == 10:
                self.family_angle += 1
            if self.elapsed > 10:
                self.elapsed = 0
            if self.family_angle > 11:
                self.family_angle = 0
        
    def prog_animation(self):
        rand = random.randint(25, 200)
        color = (0, 0, 0)
        self.family_angle = 12
        colorImage = pygame.Surface(self.family_sprite.get_size(), pygame.SRCALPHA).convert_alpha()
        colorImage.fill(color)
        self.family_sprite.blit(colorImage, (0,0), None, pygame.BLEND_MAX)
            
    def get_image(self) -> pygame.Surface:
        sub = self.family_sprite.subsurface(
            (self.family_angle * self.size, 0, self.size, self.size))

        vertical = 0
        horizontal = 0
        return pygame.transform.flip(sub, horizontal, vertical)

    def get_rect(self):
        return (self.x, self.y, self.size, self.size)
    
    def get_coord(self):
        return (self.x, self.y)

    def draw(self, surface: pygame.Surface):
        if not self.prog:
            self.animate_idle()
        if self.prog:
            self.prog_animation()
        surface.blit(self.get_image(), self.get_coord())

    def is_colliding_player(self, player_rect):
        self.collided_player = pygame.Rect(
            self.x, self.y, self.size, self.size).colliderect(player_rect)
        return self.collided_player