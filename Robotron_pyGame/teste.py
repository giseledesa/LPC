import math
import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, img, pos, angle):
        super().__init__()
        img.set_colorkey((0, 0, 0, 0))
        self.angle = angle
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.pos = pos
        self.speed = 5
        self.angle_step = 5
        self._update_image() 

    def _update_image(self):
        x, y = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self._update_image()
        nx = 1 + self.pos[0]
        ny = -self.pos[1]
        self.pos = (nx, ny)
        self.rect.center = round(nx), round(ny)

pygame.init()
window = pygame.display.set_mode((300, 300))
clock = pygame.time.Clock()
background = pygame.Surface(window.get_size())
background.set_alpha(5)

all_sprites = pygame.sprite.Group()
ship_image = pygame.image.load('img/grunt.png').convert_alpha()
player = Player(ship_image, (window.get_width()//2-40, window.get_height()//2+40), 45)
all_sprites.add(player)

run = True
while run:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    all_sprites.update()

    window.blit(background, (0, 0))
    all_sprites.draw(window)
    pygame.display.update()

pygame.quit()
exit()