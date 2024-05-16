import pygame
from math import sqrt

width = height = 1000
win = pygame.display.set_mode((width, height))

run = True

circle_pos = (500, 500)
velocity_x, velocity_y = 5, 3
velocity = pygame.math.Vector2(velocity_x, velocity_y)

circle_pos_2 = (200, 200)
velocity_x_2, velocity_y_2 = 4, -7
velocity_2 = pygame.math.Vector2(velocity_x_2, velocity_y_2)

play = True

def draw():
    win.fill("white")

    pygame.draw.circle(win, "blue", circle_pos, 50)
    pygame.draw.circle(win, "red", circle_pos_2, 50)

    pygame.display.update()

def circle_collision(pos_1, pos_2, vel_1, vel_2):
    dx = pos_1[0] - pos_2[0]
    dy = pos_1[1] - pos_2[1]
    distance = sqrt(dx * dx + dy * dy)

    vels = [vel_1, vel_2]

    if distance <= 100:
        if vel_1.y < 0 and vel_2.y > 0:
            vel_1.y = abs(vel_1.y)
            vel_2.y = -vel_2.y
            pos_1[1] += 1
            pos_2[1] -= 1
        elif vel_1.y > 0 and vel_2.y < 0:
            vel_1.y = -vel_1.y
            vel_2.y = abs(vel_2.y)
            pos_1[1] -= 1
            pos_2[1] += 1

        if vel_1.x < 0 and vel_2.x > 0:
            vel_1.x = abs(vel_1.x)
            vel_2.x = -vel_2.x
            pos_1[0] += 1
            pos_2[0] -= 1
        elif vel_1.x > 0 and vel_2.x < 0:
            vel_1.x = -vel_1.x
            vel_2.x = abs(vel_2.x)
            pos_1[0] -= 1
            pos_2[0] += 1

        if vel_1.y < 0 and vel_2.y < 0:
            if vel_1.x > 0 and vel_2.x > 0:
                if pos_1[0] < pos_2[0]:
                    vel_1.x = -vel_1.x
                else:
                    vel_2.x = -vel_2.x
            elif vel_1.x < 0 and vel_2.x < 0:
                if pos_1[0] < pos_2[0]:
                    vel_1.x = abs(vel_1.x)
                else:
                    vel_2.x = abs(vel_2.x)


def check_pos(pos, vel, radius):
    if pos[0] >= 1000 - radius:
        vel.x = -vel.x
    elif pos[0] <= radius:
        vel.x = abs(vel.x)
    
    if pos[1] >= 1000 - radius:
        vel.y = -vel.y
    elif pos[1] <= radius:
        vel.y = abs(vel.y)


while run:
    draw()

    if play:
        circle_pos += velocity
        circle_pos_2 += velocity_2

    check_pos(circle_pos, velocity, 50)
    check_pos(circle_pos_2, velocity_2, 50)
    circle_collision(circle_pos, circle_pos_2, velocity, velocity_2)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break
        elif event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_p]:
                play = not play

    pygame.time.Clock().tick(120)

pygame.quit()
