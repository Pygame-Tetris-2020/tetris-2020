from random import *

import pygame
from pygame import *

import tetris_settings as sett


# coding UTF-8


def calc_x(x):
    """Принимает координату "x" кубика в клетках "стакана".

    Возвращает экранную координату "x" левого верхнего угла кубика.

    """
    return sett.glass_x + (x - 1) * sett.cube_edge


def calc_y(y):
    """Принимает координату "y" кубика в клетках "стакана".

    Возвращает экранную координату "y" левого верхнего угла кубика.

    """
    return sett.glass_y + (y - 1) * sett.cube_edge


class Cube:

    def __init__(self, surface, x, y, color):
        self.surface = surface
        self.x = x  # координата x, выраженная в клетках "стакана"
        self.y = y  # координата y, выраженная в клетках "стакана"
        self.color = color

    def draw(self):
        """Рисует кубик по координатам в клетках "стакана".

        """
        if 0 < self.x < 17 and 0 < self.y < 21:
            pygame.draw.rect(self.surface, self.color,
                             (calc_x(self.x), calc_y(self.y), sett.cube_edge, sett.cube_edge))
            pygame.draw.rect(self.surface, sett.BLACK,
                             (calc_x(self.x), calc_y(self.y), sett.cube_edge, sett.cube_edge),
                             1)

    def touch_check(self):
        """Проверяет свободность соседних с данным кубиком клеток.

        Возвращает список логических значений, выражающих свободность клеток
        снизу, слева, сверху и справа от кубика.

        """
        return [glass.cells[self.y + 1][self.x],
                glass.cells[self.y][self.x - 1],
                glass.cells[self.y - 1][self.x],
                glass.cells[self.y][self.x + 1]
                ]


class Figure:

    def __init__(self, surface, x, y, color, type):
        self.surface = surface
        self.x = x  # координата x опорного кубика, выраженная в клетках "стакана"
        self.y = y  # координата y опорного кубика, выраженная в клетках "стакана"
        self.color = color
        self.type = type
        self.orient = 0  # ориентация фигуры

    def make(self):
        cube_list = []
        for i in sett.figure_dict[self.type][self.orient]:
            cube_list.append(Cube(self.surface, self.x + i[0],
                                  self.y + i[1], self.color))
        return cube_list

    def draw(self):
        for i in Figure.make(self):
            Cube.draw(i)

    def vert_move(self):
        self.y = self.y + 1
        Figure.make(self)

    def hor_move(self, direction):
        if (Cube.touch_check(Figure.make(self)[1])[1] and direction == -1) or \
                (Cube.touch_check(Figure.make(self)[2])[3] and direction == 1):
            self.x = self.x + direction
            Figure.make(self)

    def turn(self, direction):
        self.orient = (self.orient + direction) % 4


class Box:

    def __init__(self, surface, color, x_left_up, y_left_up, width, height):
        self.surface = surface
        self.color = color  # цвет границы поля
        self.x_left_up = x_left_up  # координата x левого верхнего угла поля
        self.y_left_up = y_left_up  # координата y левого верхнего угла поля
        self.width = width  # ширина поля в клетках
        self.height = height  # высота поля в клетках

        self.cells = [[True for j in range(self.width + 2)] for i in range(self.height + 2)] # список состояний клеток
        for i in [self.height + 1]:
            for j in range(self.width + 2):
                self.cells[i][j] = False
        for j in [0, self.width + 1]:
            for i in range(self.height + 2):
                self.cells[i][j] = False

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x_left_up + 1, self.y_left_up + 1,
                                              sett.cube_edge * self.width, sett.cube_edge * self.height), 1)

    def block_cell(self, x, y):
        self.cells[x][y] = False

    def free_cell(self, x, y):
        self.cells[x][y] = True


pygame.init()
screen = pygame.display.set_mode((sett.width, sett.height))

glass = Box(screen, sett.BLACK, sett.glass_x, sett.glass_y, 10, 20)
next_box = Box(screen, sett.BLACK, sett.next_box_x, sett.next_box_y, 5, 5)

curr_fig = Figure(screen, 5, 0, choice(sett.colors), choice(list(sett.figure_dict)))  # Первая фигура
next_fig = Figure(screen, 13, 3, choice(sett.colors), choice(list(sett.figure_dict)))  # Фигура, следующая за первой

# Список неподвижных кубиков, отображаемых на экране
dead_cubes = []

finished = False
clock = pygame.time.Clock()

control_tick = 0
moving_delay = 500

while not finished:
    clock.tick(sett.FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                curr_fig.hor_move(-1)
            elif event.key == pygame.K_RIGHT:
                curr_fig.hor_move(1)
            elif event.key == pygame.K_UP:
                curr_fig.turn(1)
            elif event.key == pygame.K_DOWN:
                curr_fig.turn(-1)
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            moving_delay = 25
        else:
            moving_delay = 500

    screen.fill(sett.WHITE)  # Фон

    glass.draw()
    next_box.draw()

    curr_fig.draw()
    next_fig.draw()

    for i in curr_fig.make():
        if i.touch_check()[0]:
            can_be_moved = True
        else:
            can_be_moved = False
            break

    # noinspection PyUnboundLocalVariable
    if can_be_moved:
        if pygame.time.get_ticks() - control_tick >= moving_delay:
            curr_fig.vert_move()
            control_tick = pygame.time.get_ticks()
    else:
        for j in curr_fig.make():
            glass.block_cell(j.y, j.x)
        dead_cubes += curr_fig.make()
        next_fig.x = 5
        next_fig.y = 0
        curr_fig = next_fig
        next_fig = Figure(screen, 13, 3, choice(sett.colors), choice(list(sett.figure_dict)))

    for dead_cube in dead_cubes:
        dead_cube.draw()

    pygame.display.update()

pygame.quit()