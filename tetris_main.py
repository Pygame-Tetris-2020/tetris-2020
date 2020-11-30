from random import *

import pygame
from pygame import *

import tetris_settings as sett


def calc_x(x):
    """Принимает координату "x" кубика в клетках 'стакана'.

    Возвращает экранную координату "x" левого верхнего угла кубика.

    """
    return sett.glass_x + (x - 1) * sett.cube_edge


def calc_y(y):
    """Принимает координату "y" кубика в клетках 'стакана'.

    Возвращает экранную координату "y" левого верхнего угла кубика.

    """
    return sett.glass_y + (y - 1) * sett.cube_edge


class Cube:
    """Создает кубик, являющийся частью полной фигуры."""

    def __init__(self, surface, x, y, color):
        """Инициализация кубика.

        Принимает следующие аргументы:
        surface -- поверхность, на которой изображается кубик
        x -- координата х, выраженная в клетках 'стакана'
        y -- координата у, выраженная в клетках 'стакана'
        color -- цвет кубика

        """
        self.surface = surface
        self.x = x
        self.y = y
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
    """Создает фигуру определенной формы, состоящую из четырёх кубиков.  """

    def __init__(self, surface, x, y, color, type):
        """Инициализация фигуры, состоящей из четырёх кубиков.

        Положение фигуры определяется её ориентацией и положением опорного кубика.

        Принимает следующие аргументы:
        surface -- поверхность, на которой изображается фигура
        x -- координата х опорного кубика, выраженная в клетках "стакана"
        y -- координата у опорного кубика, выраженная в клетках "стакана"
        color -- цвет кубика
        type -- тип фигуры
        orient -- ориентация фигуры

        """
        self.surface = surface
        self.x = x
        self.y = y
        self.color = color
        self.type = type
        self.orient = 0

    def make(self):
        """Возвращает список кубиков, из которых состоит фигура.  """
        cube_list = []
        for i in sett.figure_dict[self.type][self.orient]:
            cube_list.append(Cube(self.surface, self.x + i[0],
                                  self.y + i[1], self.color))
        return cube_list

    def draw(self):
        """Рисует фигуру.  """
        for i in Figure.make(self):
            Cube.draw(i)

    def draw_next(self):
        if self.type == 'J':
            self.x = 15
            self.y = 4
        elif self.type == 'O':
            self.x = 14
            self.y = 5
        for i in Figure.make(self):
            Cube.draw(i)

    def vert_move(self):
        """Отвечает за вертикальное движение(падение в ходе игры) фигуры.  """
        self.y = self.y + 1
        Figure.make(self)

    def hor_move(self, direction):
        """Отвечает за движение фигуры влево-вправо.

        Принимает аргумент direction -- направление движения

        """
        if (Cube.touch_check(Figure.make(self)[1])[1] and direction == -1) or \
                (Cube.touch_check(Figure.make(self)[2])[3] and direction == 1):
            self.x = self.x + direction
            Figure.make(self)

    def turn(self, direction):
        can_be_turned = True
        for i in range(4):
            for j in range(4):
                can_be_turned = bool(can_be_turned * Cube.touch_check(Figure.make(self)[i])[j])
        if can_be_turned:
            self.orient = (self.orient + direction) % 4


class Box:

    def __init__(self, surface, color, x_left_up, y_left_up, width, height):
        self.surface = surface
        self.color = color  # цвет границы поля
        self.x_left_up = x_left_up  # координата x левого верхнего угла поля
        self.y_left_up = y_left_up  # координата y левого верхнего угла поля
        self.width = width  # ширина поля в клетках
        self.height = height  # высота поля в клетках

        self.cells = [[True for j in range(self.width + 2)] for i in range(self.height + 2)]  # список состояний клеток
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

    def is_line_free(self, x):
        line = False
        for i in [x]:
            for j in range(self.width + 2):
                line = bool(line + self.cells[i][j])
        return line

    def destroy_line(self, num, dead_cubes):
        has_been_destroyed = False
        if not self.is_line_free(num):
            has_been_destroyed = True
            for dead_cube in dead_cubes:
                if dead_cube.y == num:
                    self.free_cell(dead_cube.y, dead_cube.x)
                    dead_cube.y = 0
                    dead_cube.x = 0
                elif dead_cube.y < num:
                    self.free_cell(dead_cube.y, dead_cube.x)
                    dead_cube.y += 1
                    self.block_cell(dead_cube.y, dead_cube.x)
        return dead_cubes, has_been_destroyed


def points_counter(curr_points, destroyed_lines):
    curr_points += destroyed_lines
    return curr_points


def points_table(curr_points):
    """
    Временно отвечает за отображение всех надписей.
    Нуждается в исправлении!
    """
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

""" Список неподвижных кубиков, отображаемых на экране """
dead_cubes = []

curr_points = 0  # Текущее количество очков игрока
destroyed_lines = 0  # После усовершенствования счетчика очков удалить!

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
            if event.key == pygame.K_UP:
                curr_fig.turn(1)
            elif event.key == pygame.K_DOWN:
                curr_fig.turn(-1)
    if pygame.key.get_pressed()[pygame.K_LEFT]:
        curr_fig.hor_move(-1)
    elif pygame.key.get_pressed()[pygame.K_RIGHT]:
        curr_fig.hor_move(1)
    if pygame.key.get_pressed()[pygame.K_SPACE]:
        moving_delay = 25
    else:
        moving_delay = 500

    screen.fill(sett.WHITE)  # Фон

    glass.draw()
    next_box.draw()

    curr_fig.draw()
    next_fig.draw_next()

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
        next_fig = Figure(screen, 14, 4, choice(sett.colors), choice(list(sett.figure_dict)))

        destroyed_lines = 0
        for i in range(1, glass.height + 1):
            dead_cubes, has_been_destroyed = glass.destroy_line(i, dead_cubes)
            destroyed_lines += int(has_been_destroyed)

    curr_points = points_counter(curr_points, destroyed_lines)
    destroyed_lines = 0
    points_table(curr_points)

    for dead_cube in dead_cubes:
        dead_cube.draw()
        if dead_cube.x == 0 and dead_cube.y == 0:
            dead_cubes.remove(dead_cube)

    pygame.display.update()

pygame.quit()
