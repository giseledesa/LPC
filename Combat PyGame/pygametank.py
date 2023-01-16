import pygame
import math
import settings
from pygame import Vector2

pygame.init()

screen = pygame.display.set_mode((settings.screen_width,
                                  settings.screen_height))
pygame.display.set_caption("Tank-Pong")


# draw function
def draw_objects(obj, x, y, w, h, data, ang):
    obj.image = pygame.image.load(data)
    obj.image.set_colorkey((0, 0, 0))
    obj.image = pygame.transform.scale(obj.image, [w, h])
    obj.image = pygame.transform.rotozoom(obj.image, ang, 1)
    obj.rect = obj.image.get_rect(center=(x, y))
        #(x - int(obj.image.get_width()/2),
                           #y - int(obj.image.get_height()/2),
                           #obj.image.get_width(), obj.image.get_height())
    obj.angle = ang


def move_tank(obj, speed, angle_in_radians):
    new_x = obj.x + (speed * math.cos(math.radians(angle_in_radians)))
    new_y = obj.y - (speed * math.sin(math.radians(angle_in_radians)))

    for wall in wall_list:
        wall_collision = obj.rect.colliderect(wall.rect)
        if wall_collision:
            if abs(obj.rect.top - wall.rect.bottom) < 10 and obj.y > 0:
                return obj.x, obj.y+1
            if abs(obj.rect.bottom - wall.rect.top) < 10 and obj.y > 0:
                return obj.x, obj.y-1
            if abs(obj.rect.right - wall.rect.left) < 10 and obj.x > 0:
                return obj.x-1, obj.y
            if abs(obj.rect.left - wall.rect.right) < 10 and obj.x > 0:
                return obj.x+1, obj.y

    for tank in tank_list:
        tank_collision = obj.rect.colliderect(tank.rect)
        if tank_collision:
            if abs(obj.rect.top - tank.rect.bottom) < 10 and obj.y > 0:
                return obj.x, obj.y+1
            if abs(obj.rect.bottom - tank.rect.top) < 10 and obj.y > 0:
                return obj.x, obj.y-1
            if abs(obj.rect.right - tank.rect.left) < 10 and obj.x > 0:
                return obj.x-1, obj.y
            if abs(obj.rect.left - tank.rect.right) < 10 and obj.x > 0:
                return obj.x+1, obj.y

    return new_x, new_y


def shoot(obj, bullets):
    global l_bullet_ready
    global r_bullet_ready
    global game_over
    bounce = 0
    dx = math.cos(math.radians(obj.angle))
    dy = math.sin(math.radians(obj.angle))

    # create bullet
    if obj == l_tank:
        if l_bullet_ready:
            if obj.angle == 0:
                bullets.append(pygame.Rect(obj.rect.midright[0], obj.rect.midright[1] + 5, 10, 10))
            if 0 < obj.angle < 90:
                bullets.append(pygame.Rect(obj.rect.topright[0] + 5, obj.rect.topright[1] - 5, 10, 10))
            if obj.angle == 90:
                bullets.append(pygame.Rect(obj.rect.midtop[0] - 5, obj.rect.midtop[1], 10, 10))
            if 90 < obj.angle < 180:
                bullets.append(pygame.Rect(obj.rect.topleft[0] - 5, obj.rect.topleft[1] + 5, 10, 10))
            if obj.angle == 180:
                bullets.append(pygame.Rect(obj.rect.midleft[0], obj.rect.midleft[1] - 5, 10, 10))
            if 180 < obj.angle < 270:
                bullets.append(pygame.Rect(obj.rect.bottomleft[0] - 5, obj.rect.bottomleft[1] + 5, 10, 10))
            if obj.angle == 270:
                bullets.append(pygame.Rect(obj.rect.midbottom[0] + 5, obj.rect.midbottom[1], 10, 10))

            print(obj.angle)
            print(dx)
            print(dy)
            l_bullet_ready = False

        # move bullet
        for bullet in bullets:
            # bullet[0].x += math.cos(math.radians(bullet[1]))
            # bullet[0].y += math.sin(math.radians(bullet[1]))
            bullet.x += 1
            bullet.y += 1
            pygame.draw.rect(screen, (255, 0, 0), bullet)

        # destroy bullet
        for tank in tank_list:
            for index, bullet in enumerate(bullets):
                if bullet.colliderect(r_tank):
                    del bullets[index]
                    tank.kill()
                    game_over = True

    if obj == r_tank:
        if r_bullet_ready and len(bullets) < 1:
            bullets.append(pygame.Rect(obj.rect.midtop[0], obj.rect.midtop[1], 10, 10))
            r_bullet_ready = False

        # move bullet
        for bullet in bullets:
            bullet.x += (1 * math.cos(math.radians(obj.angle)))
            bullet.y -= (1 * math.sin(math.radians(obj.angle)))
            pygame.draw.rect(screen, (255, 0, 0), bullet)


        # destroy bullet
        for tank in tank_list:
            for index, bullet in enumerate(bullets):
                if bullet.colliderect(l_tank):
                    del bullets[index]
                    tank.kill()
                    game_over = True

    #wall bounce
    for wall in wall_list:
        for index, bullet in enumerate(bullets):
            if bullet.colliderect(wall):
                bounce += 1

                if abs(bullet.top - wall.rect.bottom) < 1 and bullet.y > 0:
                    dx *= 1
                    dy *= -1
                    if bounce == 3:
                        del bullets[index]
                    print("shot the wall")
                if abs(bullet.bottom - wall.rect.top) < 1 and bullet.y > 0:
                    dx *= 1
                    dy *= -1
                    if bounce == 3:
                        del bullets[index]
                    print("shot the wall")
                if abs(bullet.right - wall.rect.left) < 1 and bullet.x < 0:
                    dx *= -1
                    dy *= 1
                    if bounce == 3:
                        del bullets[index]
                    print("shot the wall")
                if abs(bullet.left - wall.rect.right) < 1 and bullet.x > 0:
                    dx *= -1
                    dy *= 1
                    if bounce == 3:
                        del bullets[index]
                    print("shot the wall")


    # return bullet list
    return bullets


# sprite setup
drawGroup = pygame.sprite.Group()

# tank setup
l_tank = pygame.sprite.Sprite(drawGroup)
l_tank_angle = settings.p1_angle
l_tank.x = settings.p1_x
l_tank.y = settings.p1_y

r_tank = pygame.sprite.Sprite(drawGroup)
r_tank_angle = settings.p2_angle
r_tank.x = settings.p2_x
r_tank.y = settings.p2_y

tank_list = [l_tank, r_tank]

# bullet setup
l_bullet_ready = False
r_bullet_ready = False
l_bullet_group = []
r_bullet_group = []

# draw battlefield
wall_list = []
for i in range(len(settings.brick_positions)):
    wall = pygame.sprite.Sprite(drawGroup)
    draw_objects(wall, settings.brick_positions[i][0],
                 settings.brick_positions[i][1],
                 settings.brick_positions[i][2],
                 settings.brick_positions[i][3],
                 "Sprites/obstacle.png", 0)
    wall_list.append(wall)

# main loop
game_loop = True
game_over = False
game_clock = pygame.time.Clock()

while game_loop:

    for event in pygame.event.get():
        # Command to close the game
        if event.type == pygame.QUIT:
            game_loop = False

    # get keys
    keys = pygame.key.get_pressed()

    # left tank controls
    if keys[pygame.K_d]:
        l_tank_angle -= 1
        l_tank_angle %= 360

    if keys[pygame.K_a]:
        l_tank_angle += 1
        l_tank_angle %= 360

    if keys[pygame.K_w]:
        l_tank.x, l_tank.y = move_tank(l_tank, settings.tank_speed,
                                       l_tank_angle)

    if keys[pygame.K_s]:
        l_bullet_ready = True

    # right tank controls
    if keys[pygame.K_LEFT]:
        r_tank_angle += 1
        r_tank_angle %= 360

    if keys[pygame.K_RIGHT]:
        r_tank_angle -= 1
        r_tank_angle %= 360

    if keys[pygame.K_UP]:
        r_tank.x, r_tank.y = move_tank(r_tank, settings.tank_speed,
                                       r_tank_angle)

    if keys[pygame.K_DOWN]:
        r_bullet_ready = True

    draw_objects(l_tank, l_tank.x, l_tank.y, 40, 40,
                 "Sprites/l_tank.png", l_tank_angle)
    draw_objects(r_tank, r_tank.x, r_tank.y, 40, 40,
                 "Sprites/r_tank.png", r_tank_angle)

    # end game
    if game_over:
        font = pygame.font.Font("Font/Press Start 2P.ttf", 70)
        text = font.render("GAME OVER!", True, (0, 0, 0))
        screen.blit(text, (screen.get_width() // 2 - 140, screen.get_height() // 2))
        pygame.display.update()
        pygame.time.wait(2500)
        game_loop = False

    # update screen
    screen.fill(settings.screen_color)
    drawGroup.draw(screen)
    font = pygame.font.Font("Font/Press Start 2P.ttf", 50)
    text = font.render("TANK PONG", True, (200, 200, 0))
    screen.blit(text, (300, 5))
    l_bullet_group = shoot(l_tank, l_bullet_group)
    r_bullet_group = shoot(r_tank, r_bullet_group)
    game_clock.tick(60)
    pygame.display.update()

pygame.quit()
