import pygame

import sett
from main_menu import *
from cube import *


class Box:

    def __init__(self, surface, color, x_left_up, y_left_up, width, height):
        self.surface = surface
        self.color = color  # цвет границы поля
        self.x_left_up = x_left_up  # координата x левого верхнего угла поля
        self.y_left_up = y_left_up  # координата y левого верхнего угла поля
        self.width = width  # ширина поля в клетках
        self.height = height  # высота поля в клетках

        self.cells = []
        for i in range(self.height + 2):
            pass
        for i in [self.height + 1]:
            for j in range(self.width + 2):
                self.cells[i][j] = False
        for j in [0, self.width + 1]:
            for i in range(self.height + 2):
                self.cells[i][j] = False

    def draw(self):
        """Отвечает за отрисовку поля.

        """
        pygame.draw.rect(self.surface, self.color,
                         [self.x_left_up + 1, self.y_left_up + 1,
                          sett.cube_edge * self.width,
                          sett.cube_edge * self.height], 1)

    def block_cell(self, x, y):
        """Блокирует клетку.

        Принимает координаты блокируемой клетки.

        """
        self.cells[x][y] = False

    def free_cell(self, x, y):
        """Освобождает клетку.

        Принимает координаты освобождаемой клетки.

        """
        self.cells[x][y] = True

    def is_line_free(self, x):
        """Проверяет свободность линии.

        Принимает вертикальную координату анализируемой линии.
        Возвращает логическое значение.

        """
        line = False
        for i in [x]:
            for j in range(self.width + 2):
                line = bool(line + self.cells[i][j])
        return line

    def destroy_line(self, num, dead_cubes):
        """Уничтожает заполненную линию.

        Принимает вертикальную координату уничтожаемой линии
        и список неподвижных кубиков.
        Возвращает список неподвижных кубиков и флаг уничтожения линии.

        """
        has_been_destroyed = False
        if not self.is_line_free(num):
            has_been_destroyed = True
            for dead_cube in dead_cubes:
                if dead_cube.y == num:
                    self.free_cell(dead_cube.y, dead_cube.x)
                    dead_cube.y = sett.glass_y - 5
                    dead_cube.x = sett.glass_x - 5
                elif dead_cube.y < num:
                    self.free_cell(dead_cube.y, dead_cube.x)
                    dead_cube.y += 1
                    self.block_cell(dead_cube.y, dead_cube.x)
        return dead_cubes, has_been_destroyed
