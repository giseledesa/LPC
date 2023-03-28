import random
import pygame
import json, os
from config import SPEED, TOP_BAR_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT


class Electrodes:
    collided_player = False
    size = 30
    elapsed = 0

    def __init__(self, rect, sprite):
        if sprite == 0:
            self.electrodes_sprite = pygame.image.load("img/electrode1.png").convert_alpha()
        if sprite == 1:
            self.electrodes_sprite = pygame.image.load("img/electrode2.png").convert_alpha()
        if sprite == 2:
            self.electrodes_sprite = pygame.image.load("img/electrode3.png").convert_alpha()
        if sprite == 3:
            self.electrodes_sprite = pygame.image.load("img/electrode4.png").convert_alpha()
        self.electrodes_angle = 0
        self.random_pos(rect)
    
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
        if self.elapsed == 15:
            self.electrodes_angle += 1
        if self.elapsed > 15:
            self.elapsed = 0
        if self.electrodes_angle > 1:
            self.electrodes_angle = 0

    def get_image(self) -> pygame.Surface:
        sub = self.electrodes_sprite.subsurface(
            (self.electrodes_angle * self.size, 0, self.size, self.size))

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
