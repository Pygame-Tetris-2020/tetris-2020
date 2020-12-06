from random import *

import pygame
from pygame import *

import Buttons

import sett

from main_menu import *
from pause import *
from box import *
from figure import *
from cube import *
from music import *
from settings import *
from game_over import *

def calc_x(x, base_x=sett.glass_x):
    """Принимает координату "x" кубика в клетках "стакана".

    Возвращает экранную координату "x" левого верхнего угла кубика.

    """
    return base_x + (x - 1) * sett.cube_edge


def calc_y(y, base_y=sett.glass_x):
    """Принимает координату "y" кубика в клетках "стакана".

    Возвращает экранную координату "y" левого верхнего угла кубика.

    """
    return base_y + (y - 1) * sett.cube_edge


class Cube:

    def __init__(self, surface, x, y, color):
        self.surface = surface
        self.x = x  # координата x, выраженная в клетках "стакана"
        self.y = y  # координата y, выраженная в клетках "стакана"
        self.color = color

    def draw(self, base_x=sett.glass_x, base_y=sett.glass_y):
        """Рисует кубик по координатам в клетках "стакана".

        """
        pygame.draw.rect(self.surface, self.color,
                                 (calc_x(self.x, base_x), calc_y(self.y, base_y), sett.cube_edge, sett.cube_edge))
        pygame.draw.rect(self.surface, (0, 0, 0),
                                 (calc_x(self.x, base_x), calc_y(self.y, base_y), sett.cube_edge, sett.cube_edge),
                                 1)

    def touch_check(self, glass):
        """Проверяет свободность соседних с данным кубиком клеток.

        Возвращает список логических значений, выражающих свободность клеток
        снизу, слева, сверху и справа от кубика.

        """
        return {'down': glass.cells[self.y + 1][self.x],
                'left': glass.cells[self.y][self.x - 1],
                'up': glass.cells[self.y - 1][self.x],
                'right': glass.cells[self.y][self.x + 1]
                }