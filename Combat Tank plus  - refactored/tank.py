import random
import pygame
from bullet import Bullet
import json, os
from config import SPEED, TOP_BAR_HEIGHT


class Tank:
    size = 45
    pygame.mixer.init()

    def __init__(self, initial_coord, color, key_left, key_up, key_right,
                 key_down, key_shoot):
        self.tank_sprite = pygame.image.load(
            "img/tank.png")
        self.tank_sprite.fill(color, None, pygame.BLEND_MAX)
        self.color = color
        self.joysticks = []
        for i in range(pygame.joystick.get_count()):
            self.joysticks.append(pygame.joystick.Joystick(i))
        for joystick in self.joysticks:
            joystick.init()
        self.tank_angle = 0
        self.x = initial_coord[0]
        self.y = initial_coord[1]
        self.direction = 1
        self.x_velocity = 0
        self.y_velocity = 0
        self.angle = 0
        with open(os.path.join("ps4.json"), 'r+') as file:
            self.button_keys = json.load(file)
        self.LEFT, self.RIGHT, self.UP, self.DOWN, self.SHOOT = False, False, False, False, False
        self.analog_keys = {0:0, 1:0, 2:0, 3:0, 4:-1, 5: -1 }
        self.j_right, self.j_left,self.j_up,self.j_down,self.j_shoot = 0,0,0,0,0

        for i in self.button_keys.keys():
            button = self.button_keys[i]
            if button == key_down:
                self.j_down = key_down
                self.key_down = None
            else:
                self.key_down = key_down
                self.j_down = None
            if button == key_up:
                self.j_up = key_up
                self.key_up = None
            else:
                self.key_up = key_up
                self.j_up = None
            if button == key_right:
                self.j_right = key_right
                self.key_right = None
            else:
                self.key_right = key_right
                self.j_right = None
            if button == key_left:
                self.j_left = key_left
                self.key_left = None
            else:
                self.j_left = None
                self.key_left = key_left
            if button == key_shoot:
                self.j_shoot = key_shoot
                self.key_shoot = None
            else:
                self.j_shoot = None
                self.key_shoot = key_shoot
        
        self.bullet = None
        self.shooted = False
        self.spin = False
        self.start_spin = 0

        self.sound_shot = pygame.mixer.Sound("sound/shot.mp3")
        self.sound_move = pygame.mixer.Sound("sound/move.mp3")
        self.sound_explosion = pygame.mixer.Sound("sound/explosion.mp3")
        self.sound_move.set_volume(0.6)
    
    def listen_joystick(self):
        for event in pygame.event.get():
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == self.key_left:
                    self.LEFT = True
                if event.button == self.key_right:
                    self.RIGHT = True
                if event.button == self.key_down:
                    self.DOWN = True
                if event.button == self.key_up:
                    self.UP = True
                if event.button == self.key_shoot:
                    self.SHOOT = True
            if event.type == pygame.JOYBUTTONUP:
                if event.button == self.key_left:
                    self.LEFT = False
                if event.button == self.key_right:
                    self.RIGHT = False
                if event.button == self.key_down:
                    self.DOWN = False
                if event.button == self.key_up:
                    self.UP = False
                if event.button == self.key_shoot:
                    self.SHOOT = False

            if event.type == pygame.JOYAXISMOTION:
                self.analog_keys[event.axis] = event.value
                # print(analog_keys)
                # Horizontal Analog
            if abs(self.analog_keys[0]) > .4:
                if self.analog_keys[0] < -.7:
                    self.LEFT = True
                else:
                    self.LEFT = False
                if self.analog_keys[0] > .7:
                    self.RIGHT = True
                else:
                    self.RIGHT = False
                # Vertical Analog
            if abs(self.analog_keys[1]) > .4:
                if self.analog_keys[1] < -.7:
                    self.UP = True
                else:
                    self.UP = False
                if self.analog_keys[1] > .7:
                    self.DOWN = True
                else:
                    self.DOWN = False
        if self.LEFT:
            self.angle += 4
        if self.RIGHT:
            self.angle -= 4
        if self.UP:
            self.direction = -1
        if self.DOWN:
            self.direction = 1
        if self.SHOOT:
            if not self.shooted and self.bullet is None:
                pygame.mixer.Channel(3).play(self.sound_shot)
                self.bullet = Bullet(self.x + self.size / 2,
                                     self.y + self.size /
                                     2, -self.x_velocity / SPEED,
                                     -self.y_velocity / SPEED)
            self.shooted = True
        else:
            self.shooted = False

    def listen_keyboard(self):
        key = pygame.key.get_pressed()
        if key[self.key_left]:
            self.angle += 4
        if key[self.key_down]:
            self.direction = 1
        if key[self.key_right]:
            self.angle -= 4
        if key[self.key_up]:
            self.direction = -1
        if key[self.key_shoot]:
            if not self.shooted and self.bullet is None:
                pygame.mixer.Channel(3).play(self.sound_shot)
                self.bullet = Bullet(self.x + self.size / 2,
                                     self.y + self.size /
                                     2, -self.x_velocity / SPEED,
                                     -self.y_velocity / SPEED)
            self.shooted = True
        else:
            self.shooted = False

        if key[self.key_left] or key[self.key_right] or key[self.key_up] or \
                key[self.key_down]:
            pygame.mixer.Channel(2).play(self.sound_move)

    def colliding_rects(self, rects):
        rect = pygame.Rect(self.x + (self.x_velocity * self.direction),
                           self.y + (self.y_velocity * self.direction),
                           self.size, self.size)

        if rect.collidelist(rects) < 0:
            self.x += self.x_velocity * self.direction
            self.y += self.y_velocity * self.direction

    def bullet_move(self, map, enemy_rect):
        if self.bullet is not None:
            self.bullet.move(map, enemy_rect)
            if self.bullet.end_life:
                self.bullet = None

    def move(self, map, enemy_rect):
        self.direction = 0
        if not self.spin:
            for i in self.joysticks:
                if i.get_button(0) == self.key_shoot:
                    self.listen_joystick()
                else:
                    self.listen_keyboard()
        if self.angle > 360:
            self.angle = 0
        elif self.angle < 0:
            self.angle = 360

        quad = self.angle / 90
        deg = quad % 1
        quad -= quad % 1

        if quad == 1 or quad == 3:
            deg = 1 - deg

        middle = 0.125
        if deg < 0.25 - middle:
            self.tank_angle = 0
            self.x_velocity = SPEED
            self.y_velocity = 0
        elif deg < 0.5 - middle:
            self.tank_angle = 1
            self.x_velocity = SPEED
            self.y_velocity = SPEED / 2
        elif deg < 0.75 - middle:
            self.tank_angle = 2
            self.x_velocity = SPEED
            self.y_velocity = SPEED
        elif deg < 1 - middle:
            self.tank_angle = 3
            self.x_velocity = SPEED / 2
            self.y_velocity = SPEED
        else:
            self.tank_angle = 4
            self.x_velocity = 0
            self.y_velocity = SPEED

        if self.angle <= 90 or self.angle >= 270:
            self.x_velocity = -self.x_velocity

        if self.angle > 180:
            self.y_velocity = -self.y_velocity

        self.colliding_rects(map + [enemy_rect])
        self.bullet_move(map, enemy_rect)

        if self.start_spin > 200:
            self.spin = False
            self.random_pos(map)
            self.start_spin = 0
        if self.spin:
            self.start_spin += 1
            self.angle += 22.5

    def get_image(self) -> pygame.Surface:

        sub = self.tank_sprite.subsurface(
            (self.tank_angle * self.size, 0, self.size, self.size))

        vertical = self.y_velocity < 0
        horizontal = self.x_velocity < 0
        return pygame.transform.flip(sub, horizontal, vertical)

    def get_rect(self):
        return (self.x, self.y, self.size, self.size)

    def get_coord(self):
        return (self.x, self.y)

    def draw(self, surface: pygame.Surface):
        surface.blit(self.get_image(), self.get_coord())
        if self.bullet is not None:
            pygame.draw.rect(surface, self.color, self.bullet.get_rect())

    def random_pos(self, rects):
        while True:
            x = random.randint(0, 800)
            y = random.randint(0, 600 - TOP_BAR_HEIGHT)

            rect = pygame.Rect(x, y, self.size, self.size)
            if rect.collidelist(rects) < 0:
                self.x = x
                self.y = y

                break

    def has_shooted_enemy(self):
        if self.bullet is not None and self.bullet.collided_tank:
            self.bullet = None
            pygame.mixer.Channel(1).play(self.sound_explosion)
            return True
        return False