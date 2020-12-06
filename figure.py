import pygame

import sett
from cube import *

class Figure:
    def __init__(self, surface, x, y, color, type):
        self.surface = surface
        self.x = x  # координата x опорного кубика, выраженная в клетках "стакана"
        self.y = y  # координата y опорного кубика, выраженная в клетках "стакана"
        self.color = color
        self.type = type  # вид фигуры
        self.orient = 0  # ориентация фигуры

    def make(self):
        """Производит сборку фигуры из кубиков в соответсвии со словарем фигур.

        Возвращает список кубиков, из которых состоит фигура.

        """
        cube_list = []
        for cube in sett.figure_dict[self.type][self.orient]:
            cube_list.append(Cube(self.surface, self.x + cube[0], self.y + cube[1], self.color))
        return cube_list

    def special_draw(self, base_x, base_y):
        """Отвечает за рисование фигур в произвольном месте экрана.

        Принимает экранные координаты точки начала отсчета положения фигуры.

        """
        for cube in self.make():
            cube.draw(base_x, base_y)

    def draw(self):
        """Отвечает за рисование фигур в "стакане".

        """
        for cube in self.make():
            if 0 < cube.x < 17 and 0 < cube.y < 21:
                cube.draw()

    def draw_next(self):
        """Отвечает за рисование фигуры в поле для следующей фигуры.

        """
        if self.type == 'J':
            self.x = 15
            self.y = 4
        elif self.type == 'O':
            self.x = 14
            self.y = 5
        for cube in self.make():
            cube.draw()

    def vert_move(self):
        """Осуществляет перемещение фигуры по вертикали.

        """
        self.y = self.y + 1
        Figure.make(self)

    def hor_move(self, direction, glass):
        """Осуществляет перемещение фигуры по горизонтали.

        Принимает направление перемещения (1 - впрвво, -1 - влево) и "стакан", в котором находится фигура.

        """
        if (self.make()[1].touch_check(glass)['left'] and direction == -1) or \
                (self.make()[2].touch_check(glass)['right'] and direction == 1):
            self.x = self.x + direction
            Figure.make(self)

    def turn(self, angle, glass):
        """Отвечает за поворот фигуры.

        Принимает угол поворота и "стакан", в котором перемещается фигура.

        """
        can_be_turned = True
        for i in range(4):
            for j in 'down', 'left', 'up', 'right':
                can_be_turned = bool(can_be_turned * self.make()[i].touch_check(glass)[j])
        if can_be_turned:
            self.orient = (self.orient + angle) % 360