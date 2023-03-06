import pygame
from config import *
from map import MapLoader

color = 0
class Screen:
    frame_count = 0
    frame_rate = 60
    start_time = 90
    
    def __init__(self) -> None:
        self.surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.font = pygame.font.Font("font/pixel_lcd_7.ttf", 30)
        self.victory_font = pygame.font.Font("font/Megafont.ttf", 30)
        self.vignette = pygame.image.load("img/vignette.png")
        self.vignette = pygame.transform.scale(self.vignette, (800,780))
        self.timer = pygame.image.load("img/timer.png")
        self.timer = pygame.transform.scale(self.timer, (150,125))
        self.battery_count = pygame.image.load("img/battery.png")
        self.battery_count = pygame.transform.scale(self.battery_count, (65, 60))
        self.output_string = ""
        self.map_loader = MapLoader()
        self.shader_loader = MapLoader()
        self.tiles = MapLoader()
        self.shader = []
        self.tiles = []
        self.map = []
        self.map = self.map_loader.load("map/map.txt")
        self.shader = self.shader_loader.load("map/shader.txt")
        self.floor = pygame.Rect(40, 150, 720, 600)
        
    def countdown_timer(self):
        total_seconds = self.frame_count // self.frame_rate
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        output_string = "{0:02}:{1:02}".format(minutes, seconds)
        if total_seconds < 0:
            total_seconds = 0
        self.frame_count += 1
        return output_string
    
    def victory(self, route, index):
        if route == 'Tripulant':
            vic_string = "{} Won!".format(route)
            hunter_victory = self.victory_font.render(vic_string, True, WHITE_COLOR)
            self.surface.blit(hunter_victory, (250,400))
            self.frame_count = 0
        if route == 'Invader' and index is None:
            vic_string = "{}s Won!".format(route)
            hunter_victory = self.victory_font.render(vic_string, True, WHITE_COLOR)
            self.surface.blit(hunter_victory, (250,400))
            self.frame_count = 0
        if route == 'Invader' and index is not None:
            vic_string = "{} {} Won!".format(route, index)
            hunter_victory = self.victory_font.render(vic_string, True, WHITE_COLOR)
            self.surface.blit(hunter_victory, (250,400))
            self.frame_count = 0

    def draw(self, map, score):
        self.surface.fill(BLACK_COLOR)
        pygame.draw.rect(self.surface, BG_COLOR, self.floor, 0)
        for x in range(20, 741, BLOCK_SIZE):
            for y in range(150, 750, BLOCK_SIZE):
                grid_shader = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
                pygame.draw.rect(self.surface, GRID_SHADER, grid_shader, 4)
                grid_back = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
                pygame.draw.rect(self.surface, GRID_COLOR, grid_back, 2)
                grid_light = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
                pygame.draw.rect(self.surface, GRID_LIGHT, grid_light, 1)
        #for border in map:
        #   pygame.draw.rect(self.surface, RECTS_COLOR, border)
        for i in self.shader:
            pygame.draw.rect(self.surface, SHADER_COLOR, i, 10)
        for rect in map:
            pygame.draw.rect(self.surface, MAP_COLOR, rect, 10)
            
        top_bar = pygame.Rect(0, 0, SCREEN_WIDTH, 90)
        pygame.draw.rect(self.surface, BLACK_COLOR, top_bar, 100)
        self.output_string = self.countdown_timer()
        count_timer = self.font.render(self.output_string, True, TIMER_COLOR)
        self.surface.blit(self.vignette, (0, 40))
        self.surface.blit(self.timer, (332, 0))
        self.surface.blit(self.battery_count, (605, 27))
        self.surface.blit(count_timer, (355,40))
        
        score_players = self.font.render(
            str(score), True, WHITE_COLOR)
        self.surface.blit(score_players, (660, 40))
    


    
