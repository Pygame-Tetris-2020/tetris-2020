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

    def special_draw(self, base_x=sett.glass_x, base_y=sett.glass_y):
        for i in Figure.make(self):
            i.draw(base_x, base_y)

    def draw(self, base_x=sett.glass_x, base_y=sett.glass_y):
        for cube in self.make():
            if 0 < cube.x < 17 and 0 < cube.y < 21:
                cube.draw(base_x, base_y)

    def draw_next(self, base_x=sett.glass_x, base_y=sett.glass_y):
        if self.type == 'J':
            self.x = 15
            self.y = 4
        elif self.type == 'O':
            self.x = 14
            self.y = 5
        for cube in self.make():
            cube.draw(base_x, base_y)

    def vert_move(self):
        self.y = self.y + 1
        Figure.make(self)

    def hor_move(self, direction, glass):
        if (Figure.make(self)[1].touch_check(glass)['left'] and direction == -1) or \
                (Figure.make(self)[2].touch_check(glass)['right'] and direction == 1):
            self.x = self.x + direction
            Figure.make(self)

    def turn(self, direction, glass):
        can_be_turned = True
        for i in range(4):
            for j in 'down', 'left', 'up', 'right':
                can_be_turned = bool(can_be_turned*Figure.make(self)[i].touch_check(glass)[j])
        if can_be_turned:
            self.orient = (self.orient + direction) % 360