import random
import pygame
import json, os
from config import SPEED, TOP_BAR_HEIGHT


class Battery:
    collided_player = False
    size = 45
    pygame.mixer.init()
    elapsed = 0
    def __init__(self,rect):
        self.Battery_sprite = pygame.image.load(
                "img/battery_all.png")
        self.Battery_angle = 0
        self.random_pos(rect)
    
    def random_pos(self, rects):
        while True:
            x = random.randint(100, 760 - TOP_BAR_HEIGHT)
            y = random.randint(100, 800 - TOP_BAR_HEIGHT)

            rect = pygame.Rect(x, y, self.size, self.size)
            if rect.collidelist(rects) < 0:
                self.x = x
                self.y = y
                break

    def animate_idle(self):
        self.elapsed += 1
        if self.elapsed == 15:
            self.Battery_angle += 1
        if self.elapsed > 15:
            self.elapsed = 0
        if self.Battery_angle > 1:
            self.Battery_angle = 0

    def get_image(self) -> pygame.Surface:
        sub = self.Battery_sprite.subsurface(
            (self.Battery_angle * self.size, 0, self.size, self.size))

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
    

