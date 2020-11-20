import pygame

from pygame.draw import *
from random import *


# Цвета тетрамино
CYAN = (0, 240, 240)
BLUE = (0, 0, 240)
MUSTARD = (240, 160, 0)
YELLOW = (240, 240, 0)
GREEN = (0, 240, 0)
VIOLET = (160, 0, 240)
RED = (240, 0, 0)
colors = [ CYAN, BLUE, MUSTARD, YELLOW,
           GREEN, VIOLET, RED
           ]
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Настроечные константы (впоследствии перенесем в отдельный файл)
FPS = 1
width = 800 # ширина экрана
height = 800 # высота экрана
cube_edge = 35 # ребро одного кубика
glass_x = 200 # экранная координата x левого верхнего угла "стакана"
glass_y = 50 # экранная координата y левого верхнего угла "стакана"


def calc_x(x):
    '''
    Принимает координату x кубика в клетках "стакана". Возвращает экранную координату x левого верхнего угла кубика.
    '''
    return glass_x + (x - 1)*cube_edge


def calc_y(y):
    '''
    Принимает координату y кубика в клетках "стакана". Возвращает экранную координату y левого верхнего угла кубика.
    '''
    return glass_y + (y - 1)*cube_edge


class Cube:
    def __init__(self, surface, x, y, color):
        self.surface = surface
        self.x = x # координата x, выраженная в клетках "стакана"
        self.y = y  # координата y, выраженная в клетках "стакана"
        self.color = color

    def draw(self):
        '''
        Рисует кубик по координатам в клетках "стакана"
        '''
        if 0 < self.x < 11 and 0 < self.y < 21:
            rect(self.surface, self.color, (calc_x(self.x), calc_y(self.y), cube_edge, cube_edge))
            rect(self.surface, BLACK, (calc_x(self.x), calc_y(self.y), cube_edge, cube_edge), 1)

    def touch_check(self):
        '''
        Проверяет свободность соседних с данным кубиком клеток.
        Возвращает список логических значений, выражающих свободность клеток снизу, слева, сверху и справа от кубика
        '''
        return [ glass_list[self.x][self.y + 1],
                 glass_list[self.x - 1][self.y],
                 glass_list[self.x][self.y - 1],
                 glass_list[self.x + 1][self.y]
                 ]


class Figure:
    def __init__(self, surface, x, y, color, type):
        self.surface = surface
        self.x = x # координата x опорного кубика, выраженная в клетках "стакана"
        self.y = y  # координата y опорного кубика, выраженная в клетках "стакана"
        self.color = color
        self.type = type # тип фигуры

    def make(self):
        cube_list = []
        for i in figure_list[self.type]:
            cube_list.append( Cube(self.surface, self.x + i[0], self.y + i[1], self.color) )
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


pygame.init()
screen = pygame.display.set_mode((width, height))

# Присваивание логических значений клеткам "стакана"
glass_list = [ [True for j in range(22)] for i in range(12) ]
for i in [0, 11]:
    for j in range(22):
        glass_list[i][j] = False
for i in range(12):
    glass_list[i][21] = False

# Словарь фигур (впоследствии перенести в файл с настройками!)
# Порядок следования кубиков в словаре: самый нижний, самый левый, самый правый, оставшийся
figure_list = { 'I': [(0, 0), (-1, 0), (2, 0), (1, 0)],
                'J': [(0, 0), (-1, 0), (1, 0), (-1, -1)],
                'L': [(0, 0), (-1, 0), (1, 0), (1, -1)],
                'O': [(0, 0), (0, -1), (1, 0), (1, -1)],
                'S': [(0, 0), (-1, 0), (1, -1), (0, -1)],
                'T': [(0, 0), (-1, 0), (1, 0), (0, -1)],
                'Z': [(0, 0), (-1, -1), (1, 0), (0, -1)]
                }

# Список ключей (вероятно, следует оставить здесь, а не переносить в файл с настройками)
key_list = ['I', 'J', 'L', 'O', 'S', 'T', 'Z']

curr_fig = Figure(screen, 5, 0, choice(colors), choice(key_list)) # Первая фигура
next_fig = Figure(screen, 5, 0, choice(colors), choice(key_list)) # Фигура, следующая за первой

# Список неподвижных кубиков, отображаемых на экране
dead_cubes = []

finished = False
clock = pygame.time.Clock()

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEWHEEL:
            pass
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                Figure.hor_move(curr_fig, -1)
            elif event.key == pygame.K_RIGHT:
                Figure.hor_move(curr_fig, 1)

    screen.fill(WHITE) # Фон
    rect(screen, BLACK, (glass_x, glass_y, cube_edge * 10, cube_edge * 20), 1) # Границы стакана

    Figure.draw(curr_fig)

    for i in Figure.make(curr_fig):
        if Cube.touch_check(i)[0]:
            can_be_moved = True
        else:
            can_be_moved = False
            break

    if can_be_moved:
        Figure.vert_move(curr_fig)
    else:
        for j in Figure.make(curr_fig):
            glass_list[j.x][j.y] = False
            dead_cubes += Figure.make(curr_fig)
            curr_fig = next_fig
            next_fig = Figure(screen, 5, 0, choice(colors), choice(key_list))

    for i in dead_cubes:
        Cube.draw(i)

    pygame.display.update()

pygame.quit