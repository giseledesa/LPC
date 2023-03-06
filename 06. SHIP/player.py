import random
import pygame
import json, os
from config import SPEED, TOP_BAR_HEIGHT


class Player:
    collided_player = False
    collided_door = False
    size = 45
    pygame.mixer.init()
    elapsed = 0
    def __init__(self, initial_coord, color, key_left, key_up, key_right,
                 key_down, route):
        self.speed = SPEED
        if route == 'Tripulant':
            self.player_sprite = pygame.image.load(
                "img/killer_all.png")
            self.speed += 0.5
        elif route == 'Invader':
            self.player_sprite = pygame.image.load(
                "img/player_all.png")
            self.color = color
            #self.player_sprite.fill(color, None, pygame.BLEND_MAX)
        self.joysticks = []
        for i in range(pygame.joystick.get_count()):
            self.joysticks.append(pygame.joystick.Joystick(i))
        for joystick in self.joysticks:
            joystick.init()
        self.player_angle = 8
        self.x = initial_coord[0]
        self.y = initial_coord[1]
        self.direction = 1
        self.x_velocity = 0
        self.y_velocity = 0
        self.running = False
        self.angle = 0
        with open(os.path.join("ps4.json"), 'r+') as file:
            self.button_keys = json.load(file)
        self.LEFT, self.RIGHT, self.UP, self.DOWN = False, False, False, False
        self.analog_keys = {0:0, 1:0, 2:0, 3:0, 4:-1, 5: -1 }
        self.key_down = key_down
        self.key_left = key_left
        self.key_right = key_right
        self.key_up = key_up
        self.dead = False
        self.sound_shot = pygame.mixer.Sound("sound/shot.mp3")
        self.sound_move = pygame.mixer.Sound("sound/move.mp3")
        self.sound_explosion = pygame.mixer.Sound("sound/explosion.mp3")
        self.sound_move.set_volume(0.6)
    
    def listen_joystick(self):
        for event in pygame.event.get():
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == self.key_left:
                    self.LEFT = True
                    self.running = True
                if event.button == self.key_right:
                    self.RIGHT = True
                    self.running = True
                if event.button == self.key_down:
                    self.DOWN = True
                    self.running = True
                if event.button == self.key_up:
                    self.UP = True
                    self.running = True
            if event.type == pygame.JOYBUTTONUP:
                if event.button == self.key_left:
                    self.LEFT = False
                    self.running = False
                if event.button == self.key_right:
                    self.RIGHT = False
                    self.running = False
                if event.button == self.key_down:
                    self.DOWN = False
                    self.running = False
                if event.button == self.key_up:
                    self.UP = False
                    self.running = False
            if event.type == pygame.JOYAXISMOTION:
                self.analog_keys[event.axis] = event.value

                # Horizontal Analog
            if abs(self.analog_keys[0]) > .4:
                if self.analog_keys[0] < -.7:
                    self.LEFT = True
                    self.running = True
                else:
                    self.LEFT = False
                    self.running = False
                if self.analog_keys[0] > .7:
                    self.RIGHT = True
                    self.running = True
                else:
                    self.RIGHT = False
                    self.running = False
                # Vertical Analog
            if abs(self.analog_keys[1]) > .4:
                if self.analog_keys[1] < -.7:
                    self.UP = True
                    self.running = True
                else:
                    self.UP = False
                    self.running = False
                if self.analog_keys[1] > .7:
                    self.DOWN = True
                    self.running = True
                else:
                    self.DOWN = False
                    self.running = False
        if self.LEFT:
            self.animate_run()
            self.angle = 180
            self.direction = -1
        elif self.RIGHT:
            self.animate_run()
            self.angle = 0
            self.direction = -1
        elif self.UP:
            self.animate_run()
            self.angle = 90
            self.direction = -1
        elif self.DOWN:
            self.animate_run()
            self.angle = 270
            self.direction = -1
        else:
            if self.running == False and not self.dead:
                self.animate_idle()

    def listen_keyboard(self):
        key = pygame.key.get_pressed()
        if not self.dead:
            if key[self.key_left]:
                self.angle = 180
                self.animate_run()
                self.direction = -1
            elif key[self.key_down]:
                self.animate_run()
                self.angle = 270
                self.direction = -1
            elif key[self.key_right]:
                self.animate_run()
                self.angle = 0
                self.direction = -1
            elif key[self.key_up]:
                self.animate_run()
                self.angle = 90
                self.direction = -1
            else:
                self.animate_idle()

    def colliding_rects(self, rects):
        rect = pygame.Rect(self.x + (self.x_velocity * self.direction),
                           self.y + (self.y_velocity * self.direction),
                           self.size, self.size)
                           
        if rect.collidelist(rects) < 0:
            self.x += self.x_velocity * self.direction
            self.y += self.y_velocity * self.direction

    def animate_idle(self):
        self.elapsed += 1
        if self.elapsed == 5:
            self.player_angle += 1
        if self.elapsed > 5:
            self.elapsed = 0
        if self.player_angle > 1:
            self.player_angle = 0

    def animate_death(self):
        self.player_angle = 6
        self.elapsed += 1
        if self.elapsed == 7:
            self.player_angle += 1
        if self.elapsed > 7:
            self.elapsed = 0
        if self.player_angle > 13:
            self.player_angle = 13
        
    def animate_run(self):
        if self.x_velocity == 0 or self.y_velocity == 0:
            self.elapsed += 1
            if self.elapsed == 5:
                self.player_angle += 1
            if self.elapsed > 5:
                self.elapsed = 0
            if self.player_angle > 5:
                self.player_angle = 2

    def move(self, map, enemy_rect, joy_number):
        self.direction = 0
        if not self.dead:
            for i in self.joysticks:
                if i.get_instance_id() == joy_number:
                    self.listen_joystick()
                else:
                    self.listen_keyboard()
        if self.angle > 360:
            self.angle = 0
        elif self.angle < 0:
            self.angle = 360

        if self.angle == 0:
            self.x_velocity = self.speed
            self.y_velocity = 0
        elif self.angle == 180:
            self.x_velocity = self.speed
            self.y_velocity = 0
        elif self.angle == 90:
            self.x_velocity = 0
            self.y_velocity = self.speed
        else:
            self.x_velocity = 0
            self.y_velocity = self.speed

        if self.angle <= 90 or self.angle >= 270:
            self.x_velocity = -self.x_velocity

        if self.angle > 180:
            self.y_velocity = -self.y_velocity

        if self.dead:
            self.animate_death()
        self.colliding_rects(map + [enemy_rect])
        self.is_colliding_player(enemy_rect)

    def get_image(self) -> pygame.Surface:
        sub = self.player_sprite.subsurface(
            (self.player_angle * self.size, 0, self.size, self.size))

        vertical = 0
        horizontal = self.x_velocity > 0
        return pygame.transform.flip(sub, horizontal, vertical)

    def get_rect(self):
        return (self.x, self.y, self.size, self.size)
    
    def get_coord(self):
        return (self.x, self.y)

    def draw(self, surface: pygame.Surface):
        surface.blit(self.get_image(), self.get_coord())

    def is_colliding_player(self, player_rect):
        self.collided_player = pygame.Rect(self.x + (self.x_velocity * self.direction),
                           self.y + (self.y_velocity * self.direction),
                           self.size, self.size).colliderect(player_rect)
        return self.collided_player
    
    def is_colliding_door(self, door_rect):
        self.collided_door = pygame.Rect(self.x + (self.x_velocity * self.direction),
                           self.y + (self.y_velocity * self.direction),
                           self.size, self.size).colliderect(door_rect)
        return self.collided_door
    
    def has_touched_enemy(self):
        if self.collided_player:
            return True
        return False

