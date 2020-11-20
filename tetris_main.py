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
        if 0 < self.x < 11 and 0 < self.y < 21:
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
        return [glass_list[self.x][self.y + 1],
                glass_list[self.x - 1][self.y],
                glass_list[self.x][self.y - 1],
                glass_list[self.x + 1][self.y]
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


pygame.init()
screen = pygame.display.set_mode((sett.width, sett.height))

# Присваивание логических значений клеткам "стакана"
glass_list = [[True for j in range(22)] for i in range(12)]
for i in [0, 11]:
    for j in range(22):
        glass_list[i][j] = False
for i in range(12):
    glass_list[i][21] = False

# Список ключей фигур
key_list = ['I', 'J', 'L', 'O', 'S', 'T', 'Z']

curr_fig = Figure(screen, 5, 0, choice(sett.colors), choice(key_list))  # Первая фигура
next_fig = Figure(screen, 5, 0, choice(sett.colors), choice(key_list))  # Фигура, следующая за первой

# Список неподвижных кубиков, отображаемых на экране
dead_cubes = []

finished = False
clock = pygame.time.Clock()

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

    screen.fill(sett.WHITE)  # Фон
    # Границы стакана
    pygame.draw.rect(screen, sett.BLACK, (sett.glass_x, sett.glass_y,
                                          sett.cube_edge * 10, sett.cube_edge * 20), 1)

    curr_fig.draw()

    for i in curr_fig.make():
        if i.touch_check()[0]:
            can_be_moved = True
        else:
            can_be_moved = False
            break

    # noinspection PyUnboundLocalVariable
    if can_be_moved:
        curr_fig.vert_move()
    else:
        for j in curr_fig.make():
            glass_list[j.x][j.y] = False
            dead_cubes += curr_fig.make()
            curr_fig = next_fig
            next_fig = Figure(screen, 5, 0,
                              choice(sett.colors), choice(key_list))

    for i in dead_cubes:
        i.draw()

    pygame.display.update()

pygame.quit()
