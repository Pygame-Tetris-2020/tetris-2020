import pygame


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

# Настроечные константы (впоследствии перенесем в отдельный файл)
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
        rect(surface, color, (calc_x(x), calc_y(y), cube_edge, cube_edge))
        rect(surface, BLACK, (calc_x(x), calc_y(y), cube_edge, cube_edge), 1)

    def touch_check(self):
        '''
        Проверяет свободность соседних с данным кубиком клеток.
        Возвращает список логических значений, выражающих свободность клеток снизу, слева, сверху и справа от кубика
        '''
        return [ glass_list[self.x, self.y + 1],
                 glass_list[self.x - 1, self.y],
                 glass_list[self.x, self.y - 1],
                 glass_list[self.x + 1, self.y]
                 ]


class Figure:
    def __init__(self, surface, x, y, color):
        self.surface = surface
        self.x = x # координата x опорного кубика, выраженная в клетках "стакана"
        self.y = y  # координата y опорного кубика, выраженная в клетках "стакана"
        self.color = color


pygame.init()
screen = pygame.display.set_mode((width, height))

# Присваивание логических значений клеткам "стакана"
glass_list = [ [True for j in range(22)] for i in range(12) ]
for i in [0, 11]:
    for j in range(22):
        glass_list[i][j] = False
for j in [0, 21]:
    for i in range(12):
        glass_list[i][j] = False