import pygame
from math import sin, cos, radians
pygame.font.init()

"""
Controls:
WASD - Move tank
Left, Right Arrow Keys - Move aim
Enter - Shoot rocket
I, O - Increase, Decrease speed
"""

clock = pygame.time.Clock()
turn = 0
speed = 12
winner = None

font = pygame.font.SysFont("ariel", 100)
font_2 = pygame.font.SysFont("ariel", 75)

ground_color = (141, 110, 99)
W, H = 1500, 800
win = pygame.display.set_mode((W, H))
pygame.display.set_caption("Tank Game")

ground_color = (141, 110, 99)
ground = [[0, 350], [200, 350], [399, 200], [575, 200], [750, 500], [1000, 500], [1100, 400], [1150, 400], [1225, 550], [1450, 550], [1500, 450], [1500, 800], [0, 800]]

divider = pygame.Rect(750, 0, 1, H)

tank_1 = pygame.Rect(0, 350 - 35, 35, 35)
tank_2 = pygame.Rect(1335, 550 - 35, 35, 35)

IMAGE_1 = pygame.Surface((75, 10), pygame.SRCALPHA)
pygame.draw.rect(IMAGE_1, "red", (0, 0, 75, 10))

IMAGE_2 = pygame.Surface((75, 10), pygame.SRCALPHA)
pygame.draw.rect(IMAGE_2, "blue", (0, 0, 75, 10))

tank_1_center_x, tank_1_center_y = tank_1.center
pivot = [tank_1_center_x, tank_1_center_y]
offset = pygame.math.Vector2(30, 0)
angle = 0

tank_2_center_x, tank_2_center_y = tank_2.center
pivot_2 = [tank_2_center_x, tank_2_center_y]
offset_2 = pygame.math.Vector2(-30, 0)
angle_2 = 0

rocket = pygame.Rect(1, 1, 20, 20)
rocket_shot = False
dx = dy = 0
start_ticks = pygame.time.get_ticks()


def rotate(surface, angle, pivot, offset):
    rotated_image = pygame.transform.rotozoom(surface, -angle, 1)
    rotated_offset = offset.rotate(angle)
    rect = rotated_image.get_rect(center=pivot+rotated_offset)
    return rotated_image, rect


def draw():
    global aim_rect, aim_rect_2
    rotated_image, aim_rect = rotate(IMAGE_1, angle, pivot, offset)
    rotated_image_2, aim_rect_2 = rotate(IMAGE_2, angle_2, pivot_2, offset_2)

    win.fill((129, 212, 250))
    win.blit(rotated_image, aim_rect)
    win.blit(rotated_image_2, aim_rect_2)

    pygame.draw.polygon(win, ground_color, ground)

    pygame.draw.rect(win, "red", tank_1)
    pygame.draw.rect(win, "blue", tank_2)
    pygame.draw.rect(win, "black", rocket)
    pygame.draw.rect(win, "black", divider)
    win.blit(speed_text, (250 - speed_text.get_width()/2, 750 - speed_text.get_height()))
    
    pygame.display.flip()


def move_tanks(direction):
    global pivot, pivot_2
    if turn == 0:
        if (direction == "left") and (tank_1.x != 0):
            tank_1.x -= 5
            if tank_1.x < 400 and tank_1.x > 200:
                tank_1.y += 4
            elif tank_1.x < 750 and tank_1.x >= 575:
                tank_1.y -= 9
        elif (direction == "right") and tank_1.x + tank_1.width < divider.x:
            tank_1.x += 5
            if tank_1.x + 35 >= 200 and tank_1.x < 400:
                tank_1.y -= 4
            elif tank_1.x >= 575 and tank_1.x < 750:
                tank_1.y += 9
        if tank_1.x >= 400 and tank_1.x + 35 < 575:
            tank_1.y = 200 - 35
        elif tank_1.x < 200:
            tank_1.y = 350 - 35
        pivot = tank_1.center

    elif turn == 1:
        if (direction == "left") and tank_2.x > divider.x:
            tank_2.x -= 5
            if tank_2.x < 1225 and tank_2.x > 1150:
                tank_2.y -= 18
            elif tank_2.x < 1100 and tank_2.x > 1000:
                tank_2.y += 5
            elif tank_2.x + tank_2.width <= 1500 and tank_2.x + tank_2.width > 1450:
                tank_2.y += 7
            
        elif (direction == "right") and (tank_2.x + 35 != 1500):
            tank_2.x += 5
            if tank_2.x + 35 > 1000 and tank_2.x < 1100:
                tank_2.y -= 5
            elif tank_2.x + 35 > 1150 and tank_2.x < 1225:
                tank_2.y += 8
            elif tank_2.x + tank_2.width >= 1450:
                tank_2.y -= 7
        
        if tank_2.x + 35 < 1150 and tank_2.x > 1100:
            tank_2.y = 400 - 35
        elif tank_2.x > 750 and tank_2.x < 1000:
            tank_2.y = 500 - 35
        elif tank_2.x + 35 > 1225 and tank_2.x + 35 < 1450:
            tank_2.y = 550 - 35
        pivot_2 = tank_2.center


def shoot_rocket():
    global turn, rocket_shot, dx, dy, start_ticks
    if turn == 0:
        rocket.x = aim_rect.x + aim_rect.width
        if angle <= 0:
            rocket.y = aim_rect.topright[1]
        elif angle > 0:
            rocket.y = aim_rect.bottomright[1]
        angle_rad = radians(angle)
        dx = speed * cos(angle_rad)
        dy = speed * sin(angle_rad)
        turn = 1
    elif turn == 1:
        rocket.x = aim_rect_2.x - rocket.width/2
        if angle_2 <= 0:
            rocket.y = aim_rect_2.bottomleft[1]
        elif angle_2 > 0:
            rocket.y = aim_rect_2.topleft[1]
        angle_rad = radians(angle_2)
        dx = -speed * cos(angle_rad)
        dy = -speed * sin(angle_rad)
        turn = 0
    start_ticks = pygame.time.get_ticks()
    rocket_shot = True


def you_won():
    global run
    win_text = font.render(f"{winner.title()} won!!", 1, winner)
    win.blit(win_text, (W/2 - win_text.get_width()/2, H/2 - win_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(3000)
    run = False


run = True

while run:
    
    clock.tick(60)

    speed_text = font_2.render(f"Rocket speed: {speed}", 1, "black")
    draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and rocket_shot == False:
                shoot_rocket()
            elif event.key == pygame.K_i:
                speed += 1
            elif event.key == pygame.K_o:
                speed -= 1
            
            pygame.display.flip()

    keys = pygame.key.get_pressed()
    if rocket_shot == False:
        if keys[pygame.K_a]:
            move_tanks("left")
        elif keys[pygame.K_d]:
            move_tanks("right")

        if keys[pygame.K_LEFT]:
            if turn == 0 and angle >= -90:
                angle -= 3
            elif turn == 1 and angle_2 >= -90:
                angle_2 -= 3
        elif keys[pygame.K_RIGHT]:
            if turn == 0 and angle <= 90:
                angle += 3
            elif turn == 1 and angle_2 <= 90:
                angle_2 += 3
    
    if rocket_shot:
        rocket.move_ip(dx, dy)
        next_pos = rocket.move(dx, dy)
        seconds = (pygame.time.get_ticks() - start_ticks) / 1000
        if seconds > 0.25:
            dy += 0.3
        if (rocket.x >= W) or (rocket.x < -20 or rocket.y > H):
            rocket_shot = False

        if turn == 0 and rocket.colliderect(tank_1):
            winner = "blue" # Blue because shoot_rocket() switches turns or smth
            you_won()
            break
        elif turn == 1 and rocket.colliderect(tank_2):
            winner = "red"
            you_won()
            break
        

pygame.quit()