import random
import pygame
from bullet import Bullet
import json, os
from config import SPEED, TOP_BAR_HEIGHT


class Player:
    size = 30
    elapsed = 0

    def __init__(self, initial_coord, color, key_left, key_up, key_right,
                 key_down):
        self.player_sprite = pygame.image.load(
            "img/player.png")
        self.joysticks = []
        for i in range(pygame.joystick.get_count()):
            self.joysticks.append(pygame.joystick.Joystick(i))
        for joystick in self.joysticks:
            joystick.init()
        self.player_angle = 3
        self.bullet_angle = 2
        self.running = False
        self.x = initial_coord[0]
        self.y = initial_coord[1]
        self.direction = 1
        self.shoot_delay = 15
        self.bullets = 0
        self.side = 0
        self.x_velocity = 0
        self.y_velocity = 0
        self.angle = 0
        with open(os.path.join("ps4.json"), 'r+') as file:
            self.button_keys = json.load(file)
        self.LEFT, self.RIGHT, self.UP, self.DOWN, self.SHOOT = False, False, False, False, False
        self.analog_keys = {0:0, 1:0, 2:0, 3:0, 4:-1, 5: -1 }
        self.key_down = key_down
        self.key_left = key_left
        self.key_right = key_right
        self.key_up = key_up
        
        self.dead = False
        self.bullet = []
        
    
    def listen_joystick(self):
        for event in pygame.event.get():
            if event.type == pygame.JOYBUTTONDOWN:
                self.running = True
                if event.button == self.key_left:
                    self.LEFT = True
                if event.button == self.key_right:
                    self.RIGHT = True
                if event.button == self.key_down:
                    self.DOWN = True
                if event.button == self.key_up:
                    self.UP = True
            if event.type == pygame.JOYBUTTONUP:
                self.running = False
                if event.button == self.key_left:
                    self.LEFT = False
                if event.button == self.key_right:
                    self.RIGHT = False
                if event.button == self.key_down:
                    self.DOWN = False
                if event.button == self.key_up:
                    self.UP = False

            if event.type == pygame.JOYAXISMOTION:
                self.analog_keys[event.axis] = event.value
                # Horizontal Analog
            
            if abs(self.analog_keys[0]) > .4:
                if self.analog_keys[0] < -.6:
                    self.LEFT = True
                    self.running = True
                else:
                    self.LEFT = False
                    self.running = False
                if self.analog_keys[0] > .6:
                    self.RIGHT = True
                    self.running = True
                else:
                    self.RIGHT = False  
                # Vertical Analog
            if abs(self.analog_keys[1]) > .4:
                if self.analog_keys[1] < -.6:
                    self.UP = True
                    self.running = True
                else:
                    self.UP = False
                    self.running = False
                if self.analog_keys[1] > .6:
                    self.DOWN = True
                    self.running = True
                else:
                    self.DOWN = False
        if self.LEFT:
            if self.UP:
                self.angle = 'UP_LEFT'
            elif self.DOWN:
                self.angle = 'DOWN_LEFT'
            else:
                self.angle = 'LEFT'
            self.direction = -1
        elif self.RIGHT:
            if self.UP:
                self.angle = 'UP_RIGHT'
            elif self.DOWN:
                self.angle = 'DOWN_RIGHT'
            else:
                self.angle = 'RIGHT'
            self.direction = -1
        elif self.UP:
            self.angle = 'UP'
            self.direction = -1
        elif self.DOWN:
            self.angle = 'DOWN'
            self.direction = -1
        self.animate_run(self.angle)
            
    
    def shooting_bullets(self):
        BULLET_ANGLE = 0
        SHOOT_X = 0
        SHOOT_Y = 0
        SHOOT_DOWN = False
        SHOOT_UP = False
        SHOOT_LEFT = False
        SHOOT_RIGHT = False

        if self.joysticks[0].get_button(0):
            SHOOT_DOWN = True
        if self.joysticks[0].get_button(1):
            SHOOT_RIGHT = True
        if self.joysticks[0].get_button(2):
            SHOOT_LEFT = True
        if self.joysticks[0].get_button(3):
            SHOOT_UP = True
            
        if self.bullets <= 0:
            if SHOOT_LEFT:
                if SHOOT_UP:
                    SHOOT_X = -1
                    SHOOT_Y = -1
                    BULLET_ANGLE = 2
                elif SHOOT_DOWN:
                    SHOOT_X = -1
                    SHOOT_Y = 1
                    BULLET_ANGLE = 3
                else:
                    SHOOT_X = -1
                    SHOOT_Y = 0
                    BULLET_ANGLE = 0
                b = Bullet(self.x - self.size / 2, self.y, SHOOT_X, SHOOT_Y, BULLET_ANGLE)
                self.bullet.append(b)
            elif SHOOT_RIGHT:
                if SHOOT_UP:
                    SHOOT_X = 1
                    SHOOT_Y = -1
                    BULLET_ANGLE = 3
                elif SHOOT_DOWN:
                    SHOOT_X = 1
                    SHOOT_Y = 1
                    BULLET_ANGLE = 2
                else:
                    SHOOT_X = 1
                    SHOOT_Y = 0
                    BULLET_ANGLE = 0
                b = Bullet(self.x + self.size / 2, self.y, SHOOT_X, SHOOT_Y, BULLET_ANGLE)
                self.bullet.append(b)
            elif SHOOT_DOWN:
                SHOOT_X = 0
                SHOOT_Y = 1
                BULLET_ANGLE = 1
                b = Bullet(self.x, self.y + self.size / 2, SHOOT_X, SHOOT_Y, BULLET_ANGLE)
                self.bullet.append(b)
            elif SHOOT_UP:
                SHOOT_X = 0
                SHOOT_Y = -1
                BULLET_ANGLE = 1
                b = Bullet(self.x, self.y - self.size / 2, SHOOT_X, SHOOT_Y, BULLET_ANGLE)
                self.bullet.append(b)
            self.bullets = self.shoot_delay
        self.bullets -= 1
    '''
    def listen_keyboard(self):
        key = pygame.key.get_pressed()
        if key[self.key_left]:
            if key[self.key_up]:
                self.angle = 'UP_LEFT'
            elif key[self.key_down]:
                self.angle = 'DOWN_LEFT'
            else:
                self.angle = 'LEFT'
            self.direction = -1
            self.running = True
        elif key[self.key_right]:
            if key[self.key_up]:
                self.angle = 'UP_RIGHT'
            elif key[self.key_down]:
                self.angle = 'DOWN_RIGHT'
            else:
                self.angle = 'RIGHT'
            self.direction = -1
            self.running = True
        elif key[self.key_down]:
            self.angle = 'DOWN'
            self.direction = -1
            self.running = True
        elif key[self.key_up]:
            self.angle = 'UP'
            self.running = True
            self.direction = -1
        else: 
            self.running = False

        self.animate_run(self.angle)
    '''
    def animate_run(self, direction):
        if self.running:
            self.elapsed += 1
            if self.elapsed == 2:
                self.player_angle += 1
            elif self.elapsed > 2:
                self.elapsed = 0
            if direction == 'DOWN':
                if self.player_angle > 5:
                    self.player_angle = 3
            elif direction == 'LEFT' or direction == 'RIGHT':
                if self.player_angle > 2:
                    self.player_angle = 0
            elif direction == 'UP':
                if self.player_angle > 8:
                    self.player_angle = 6
            else:
                if self.player_angle > 2:
                    self.player_angle = 0

    def colliding_rects(self, rects):
        rect = pygame.Rect(self.x + (self.x_velocity * self.direction),
                           self.y + (self.y_velocity * self.direction),
                           self.size, self.size)
        
        if rect.collidelist(rects) < 0:
            self.x += self.x_velocity * self.direction
            self.y += self.y_velocity * self.direction

    def bullet_move(self, map):
        if self.bullet:
            for b in self.bullet:
                b.move(map)
                if b.end_life:
                    index = self.bullet.index(b)
                    self.bullet.pop(index)

    def move(self, map):
        self.direction = 0
        if not self.dead:
            self.listen_joystick()
            #self.listen_keyboard()
            self.shooting_bullets()
        if self.angle == 'LEFT':
            self.y_velocity = 0
            self.x_velocity = SPEED
            self.side = 1
        elif self.angle == 'RIGHT':
            self.y_velocity = 0
            self.x_velocity = -SPEED
            self.side = 0
        elif self.angle == 'UP':
            self.y_velocity = SPEED
            self.x_velocity = 0
            self.side = 0
        elif self.angle == 'DOWN':
            self.y_velocity = -SPEED
            self.x_velocity = 0
            self.side = 0
        elif self.angle == 'UP_LEFT':
            self.y_velocity = SPEED
            self.x_velocity = SPEED
            self.side = 1
        elif self.angle == 'UP_RIGHT':
            self.y_velocity = SPEED
            self.x_velocity = -SPEED
            self.side = 0
        elif self.angle == 'DOWN_RIGHT':
            self.y_velocity = -SPEED
            self.x_velocity = -SPEED
            self.side = 0
        else:
            self.y_velocity = -SPEED
            self.x_velocity = SPEED
            self.side = 1

        self.colliding_rects(map)
        self.bullet_move(map)

    def get_image(self) -> pygame.Surface:

        sub = self.player_sprite.subsurface(
            (self.player_angle * self.size, 0, self.size, self.size))

        vertical = 0
        horizontal = self.side > 0
        return pygame.transform.flip(sub, horizontal, vertical)

    def get_rect(self):
        return (self.x, self.y, self.size, self.size)

    def get_coord(self):
        return (self.x, self.y)

    def draw(self, surface: pygame.Surface):
        surface.blit(self.get_image(), self.get_coord())
        if self.bullet:
            for i in range(len(self.bullet)):
                surface.blit(self.bullet[i].get_image(), self.bullet[i].get_coord())

    def random_pos(self, rects):
        while True:
            x = random.randint(0, 800)
            y = random.randint(0, 600 - TOP_BAR_HEIGHT)

            rect = pygame.Rect(x, y, self.size, self.size)
            if rect.collidelist(rects) < 0:
                self.x = x
                self.y = y

                break

    def has_shooted_enemy(self, enemy_rect):
        for b in self.bullet:
            b.is_colliding_enemy(enemy_rect)
            if self.bullet and b.collided_enemy:
                index = self.bullet.index(b)
                self.bullet.pop(index)
                return True
        return False