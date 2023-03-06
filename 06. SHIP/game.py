from logging.config import listen
from sqlite3 import Time
from time import time
import pygame
from battery import Battery
from config import *
from screen import Screen
from player import Player
from map import MapLoader
import json, os


class Game:
    hunter = 'Tripulant'
    player = 'Invader'
    death_count = 0
    def __init__(self) -> None:
        self.playing = True
        self.screen = Screen()
        self.score = 0
        with open(os.path.join("ps4.json"), 'r+') as file:
            button_keys = json.load(file)
        self.players = {}
        self.exit = []
        self.clock = pygame.time.Clock()
        self.map_loader = MapLoader()
        self.map = []
        self.map = self.map_loader.load("map/map.txt")
        self.goal = []
        for i in range(5):
            battery = Battery(self.map)
            self.goal.append(battery)
        self.wall = pygame.Rect(340, 110, 120, 20)
        self.door = pygame.Rect(340, 100, 120, 20)
        self.map.append(self.wall)

        self.tripulant = Player((355, 700), PLAYER_1_COLOR, pygame.K_LEFT,
                          pygame.K_UP, pygame.K_RIGHT, pygame.K_DOWN, self.hunter)
        self.player2 = Player((375, 220), PLAYER_2_COLOR, button_keys['left_arrow'],
                          button_keys['up_arrow'], button_keys['right_arrow'],button_keys['down_arrow'], self.player)
        self.player3 = Player((417, 220), PLAYER_3_COLOR, pygame.K_a,
                          pygame.K_w, pygame.K_d, pygame.K_s, self.player)
        self.players.update({1: self.player2})
        self.players.update({2: self.player3})

    def listen_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False

    def listen_keyboard(self):
        self.tripulant.move(
            self.map, self.player2.get_rect(), None)
        self.player2.move(
            self.map, self.tripulant.get_rect(), 0)
        self.player3.move(
            self.map, self.tripulant.get_rect(), 1)

        for player in self.players:
            if (self.tripulant.is_colliding_player(self.players[player].get_rect())):
                self.players[player].dead = True
                self.players[player].x = 900
                self.death_count += 1
                self.tripulant.speed += 0.5
                print(self.death_count)

        for player in self.players:
            if (self.players[player].is_colliding_door((340, 100, 120, 20))):
                self.exit.append(player)
                self.players[player].x = 900
                
        for i in range(len(self.goal)):
            if (self.goal[i-1].is_colliding_player(self.player2.get_rect())):
                self.goal.pop(i-1)
                self.score += 1
        for i in range(len(self.goal)):
            if (self.goal[i-1].is_colliding_player(self.player3.get_rect())):
                self.goal.pop(i-1)
                self.score += 1
        if self.score == 5:
            self.score = 0
            self.map.pop(290)
    
    def victory(self):
        total_seconds = self.screen.frame_count // self.screen.frame_rate
        minutes = total_seconds // 60
        index = None
        if minutes < 3:
            if self.death_count >= 2:
                self.screen.victory(self.hunter, None)
                for player in self.players:
                    self.players[player].speed = 0
                self.tripulant.speed = 0
            if len(self.exit) >= 1 and self.death_count == 1:
                index = self.exit[0]
                self.screen.victory(self.player, index)
                for player in self.players:
                    self.players[player].speed = 0
                self.tripulant.speed = 0
            if len(self.exit) == 2:
                self.screen.victory(self.player, None)
                for player in self.players:
                    self.players[player].speed = 0
                self.tripulant.speed = 0
            
        elif minutes >= 3:
            self.screen.victory(self.hunter, None)
            for player in self.players:
                self.players[player].speed = 0
            self.tripulant.speed = 0
              
    def loop(self):
        while self.playing:
            self.listen_keyboard()
            self.listen_events()
            self.screen.draw(self.map, self.score)
            pygame.draw.rect(self.screen.surface, (215, 56, 64), self.door, 0)
            for i in range(len(self.goal)):
                self.goal[i].draw(self.screen.surface)
            self.tripulant.draw(self.screen.surface)
            for player in self.players:
                self.players[player].draw(self.screen.surface)
            self.victory()
            pygame.display.flip()
            self.clock.tick(60)