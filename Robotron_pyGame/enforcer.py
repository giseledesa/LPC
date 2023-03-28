import random
import pygame
import math
import json, os
from config import SPEED, TOP_BAR_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT


def check_destination(pos, x, y):
    if abs(pos[0] - x) < 10 and abs(pos[1] - y) < 10:
        return True


class Sphereoids:
    collided_player = False
    size = 30
    speed = 15
    elapsed = 0

    def __init__(self, rect):
        self.sphereoids_sprite = pygame.image.load(
            "img/sphereoid.png").convert_alpha()
        self.sphereoids_angle = 0
        self.random_pos(rect)
        self.start_time = 0
        self.end = 0
        self.timer = 0
        self.clock = random.randint(100, 500)
        self.enforcer_count = 0
        self.enforcer_limit = random.randint(2, 4)
        self.corners = [(120, 70),
                        (120, SCREEN_HEIGHT - TOP_BAR_HEIGHT - 70),
                        (SCREEN_WIDTH - 200, SCREEN_HEIGHT - TOP_BAR_HEIGHT - 70),
                        (SCREEN_WIDTH - 200, 70)]
        self.rand_coord = random.choice(self.corners)

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
            self.sphereoids_angle += 1
        if self.elapsed > 10:
            self.elapsed = 0
        if self.sphereoids_angle > 5:
            self.sphereoids_angle = 0

    def get_image(self) -> pygame.Surface:
        sub = self.sphereoids_sprite.subsurface(
            (self.sphereoids_angle * self.size, 0, self.size, self.size))

        vertical = 0
        horizontal = 0
        return pygame.transform.flip(sub, horizontal, vertical)

    def get_rect(self):
        return (self.x, self.y, self.size, self.size)

    def get_coord(self):
        return (self.x, self.y)

    def get_spawn(self, rect):
        return Enforcer(rect)

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
            self.rand_coord = random.choice(self.corners)

    def spawn_enforcer(self):
        self.timer += 1

        if self.timer >= self.clock:
            self.enforcer_count += 1
            self.timer = 0
            self.clock = random.randint(100, 500)
            return True

    def draw(self, surface: pygame.Surface):
        self.animate_idle()
        surface.blit(self.get_image(), self.get_coord())

    def is_colliding_player(self, player_rect):
        self.collided_player = pygame.Rect(
            self.x, self.y, self.size, self.size).colliderect(player_rect)
        return self.collided_player

    def kill(self):
        if self.enforcer_count == self.enforcer_limit:
            return True


class Enforcer:
    collided_player = False
    size = 30
    speed = 10
    elapsed = 0
    
    def __init__(self, pos):
        self.enforcer_sprite = pygame.image.load(
                "img/enforcer.png").convert_alpha()
        self.enforcer_angle = 0
        self.x = pos[0]
        self.y = pos[1]
        self.start_time = 0
        self.end = 0
        self.timer = 0
        self.clock = random.randint(100, 500)
        self.bullet = []

    def animate_idle(self):
        self.elapsed += 1
        if self.elapsed == 10:
            self.enforcer_angle += 1
        if self.elapsed > 10:
            self.elapsed = 0
        if self.enforcer_angle > 5:
            self.enforcer_angle = 0

    def get_image(self) -> pygame.Surface:
        sub = self.enforcer_sprite.subsurface(
            (self.enforcer_angle * self.size, 0, self.size, self.size))

        vertical = 0
        horizontal = 0
        return pygame.transform.flip(sub, horizontal, vertical)

    def get_rect(self):
        return (self.x, self.y, self.size, self.size)
    
    def get_coord(self):
        return (self.x, self.y)

    def move(self, player_coords):
        dx = player_coords[0] - self.x
        dy = player_coords[1] - self.y
        angle = math.atan2(dy, dx)
        self.start_time += 1
        if self.start_time == 5: 
            self.x += self.speed * math.cos(angle)
            self.y += self.speed * math.sin(angle)
        if self.start_time > 5:
            self.start_time = 0

    def shoot(self):
        self.timer += 1

        if self.timer >= self.clock:
            self.timer = 0
            self.clock = random.randint(100, 500)
            return True

    def draw(self, surface: pygame.Surface):
        self.animate_idle()
        surface.blit(self.get_image(), self.get_coord())

    def is_colliding_player(self, player_rect):
        self.collided_player = pygame.Rect(
            self.x, self.y, self.size, self.size).colliderect(player_rect)
        return self.collided_player


class EnforcerBullet:
    collided_player = False
    size = 30
    speed = 15
    elapsed = 0

    def __init__(self, pos, player_coords):
        self.enforcer_bullet_sprite = pygame.image.load(
            "img/enf_bullet.png").convert_alpha()
        self.enforcer_bullet_angle = 0
        self.x = pos[0]
        self.y = pos[1]
        self.target = player_coords
        self.start_time = 0
        self.timer = 0
        self.limit = 1000
        self.bullet = []
        self.dx = self.target[0] - self.x
        self.dy = self.target[1] - self.y
        self.angle = math.atan2(self.dy, self.dx)

    def animate_idle(self):
        self.elapsed += 1
        if self.elapsed == 10:
            self.enforcer_bullet_angle += 1
        if self.elapsed > 10:
            self.elapsed = 0
        if self.enforcer_bullet_angle > 5:
            self.enforcer_bullet_angle = 0

    def get_image(self) -> pygame.Surface:
        sub = self.enforcer_bullet_sprite.subsurface(
            (self.enforcer_bullet_angle * self.size, 0, self.size, self.size))

        vertical = 0
        horizontal = 0
        return pygame.transform.flip(sub, horizontal, vertical)

    def get_rect(self):
        return (self.x, self.y, self.size, self.size)

    def get_coord(self):
        return (self.x, self.y)

    def move(self):
        if not check_destination(self.target, self.x, self.y):
            self.dx = self.target[0] - self.x
            self.dy = self.target[1] - self.y
            #self.angle = math.atan2(self.dy, self.dx)
        self.start_time += 1
        if self.start_time == 5:
            self.x += self.speed * math.cos(self.angle)
            self.y += self.speed * math.sin(self.angle)
        if self.start_time > 5:
            self.start_time = 0

    def draw(self, surface: pygame.Surface):
        self.timer += 1
        self.animate_idle()
        surface.blit(self.get_image(), self.get_coord())

    def is_colliding_player(self, player_rect):
        self.collided_player = pygame.Rect(
            self.x, self.y, self.size, self.size).colliderect(player_rect)
        return self.collided_player

    def kill(self):
        if self.timer > self.limit:
            return True
