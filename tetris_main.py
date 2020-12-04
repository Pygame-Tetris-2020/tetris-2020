import pygame
from pygame import *

import tetris_settings as sett

from tetris_menu import *
from box import *
from figure import *
from cube import *

# coding UTF-8


def points_counter(curr_points, destroyed_lines):
    curr_points += destroyed_lines
    return curr_points


def points_table(curr_points):
    '''
    Временно отвечает за отображение всех надписей.
    Нуждается в исправлении!
    '''
    my_font = pygame.font.Font('tetris-font.ttf', 28)

    string = "Следующая:"
    text = my_font.render(string, 1, sett.BLACK)
    screen.blit(text, (585, 52))

    string = "Линии: " + str(curr_points)
    text = my_font.render(string, 1, sett.BLACK)
    screen.blit(text, (585, 320))

    string = "Очки: 0"
    text = my_font.render(string, 1, sett.BLACK)
    screen.blit(text, (585, 365))


pygame.init()
screen = pygame.display.set_mode((sett.width, sett.height))
pygame.display.set_caption('Тетрис')

glass = Box(screen, sett.BLACK, sett.glass_x, sett.glass_y, 10, 20)
next_box = Box(screen, sett.BLACK, sett.next_box_x, sett.next_box_y, 6, 6)

curr_fig = Figure(screen, 5, 0, choice(sett.colors), choice(list(sett.figure_dict)))  # Первая фигура
next_fig = Figure(screen, 14, 4, choice(sett.colors), choice(list(sett.figure_dict)))  # Фигура, следующая за первой

# Список неподвижных кубиков, отображаемых на экране
dead_cubes = []

curr_points = 0 # Текущее количество очков игрока
destroyed_lines = 0 # После усовершенствования счетчика очков удалить!

finished = False
clock = pygame.time.Clock()

vert_control_tick = 0
vert_moving_delay = 500

hor_control_tick = 0
hor_moving_delay = 100

pygame.mixer.music.load('tetris_sounds/TR1.mp3')
pygame.mixer.music.play(-1)

figure_stopping = pygame.mixer.Sound('tetris_sounds/figure_stopping.mp3')
destroying_line = pygame.mixer.Sound('tetris_sounds/destroying_line.mp3')

while not finished:
    while not finished:
        menu(screen)
    clock.tick(sett.FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                curr_fig.turn(90, glass)
            elif event.key == pygame.K_DOWN:
                curr_fig.turn(-90, glass)
    if pygame.key.get_pressed()[pygame.K_LEFT]:
        if pygame.time.get_ticks() - hor_control_tick >= hor_moving_delay:
            curr_fig.hor_move(-1, glass)
            hor_control_tick = pygame.time.get_ticks()
    elif pygame.key.get_pressed()[pygame.K_RIGHT]:
        if pygame.time.get_ticks() - hor_control_tick >= hor_moving_delay:
            curr_fig.hor_move(1, glass)
            hor_control_tick = pygame.time.get_ticks()
    if pygame.key.get_pressed()[pygame.K_SPACE]:
        vert_moving_delay = 25
    else:
        vert_moving_delay = 500

    screen.fill(sett.WHITE)  # Фон

    glass.draw()
    next_box.draw()

    curr_fig.draw()
    next_fig.draw_next()

    for i in curr_fig.make():
        if i.touch_check(glass)['down']:
            can_be_moved = True
        else:
            can_be_moved = False
            figure_stopping.play()
            break

    # noinspection PyUnboundLocalVariable
    if can_be_moved:
        if pygame.time.get_ticks() - vert_control_tick >= vert_moving_delay:
            curr_fig.vert_move()
            vert_control_tick = pygame.time.get_ticks()
    else:
        for j in curr_fig.make():
            glass.block_cell(j.y, j.x)
        dead_cubes += curr_fig.make()
        next_fig.x = 5
        next_fig.y = 0
        curr_fig = next_fig
        next_fig = Figure(screen, 14, 4, choice(sett.colors), choice(list(sett.figure_dict)))

        destroyed_lines = 0
        for i in range(1, glass.height + 1):
            dead_cubes, has_been_destroyed = glass.destroy_line(i, dead_cubes)
            destroyed_lines += int(has_been_destroyed)
            if has_been_destroyed:
                destroying_line.play()

    curr_points = points_counter(curr_points, destroyed_lines)
    destroyed_lines = 0
    points_table(curr_points)


    for dead_cube in dead_cubes:
        dead_cube.draw()
        if dead_cube.x == 0 and dead_cube.y == 0:
            dead_cubes.remove(dead_cube)

    pygame.display.update()

pygame.quit()