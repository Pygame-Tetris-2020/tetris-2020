from random import randint, choice

import pygame

import sett
import Buttons
from box import *
from figure import *
from cube import *
from pause import *
from music import *
from game_over import *
from util import printer

def auxiliary_counter(destroyed_lines):
    """Определяет величину прибавки очков в зависимости от числа уничтоженных линий

    Возвращает велчину прибавки очков.

    """
    increase = 0
    if destroyed_lines == 1:
        increase = 100
    elif destroyed_lines == 2:
        increase = 300
    elif destroyed_lines == 3:
        increase = 700
    elif destroyed_lines == 4:
        increase = 1500
    return increase


class Game:
    def __init__(self, surface):
        self.screen = surface
        self.glass = Box(self.screen, sett.BLACK, sett.glass_x,
                         sett.glass_y, 10, 20)
        self.next_box = Box(self.screen, sett.BLACK, sett.next_box_x,
                            sett.next_box_y, 6, 6)
        self.pause_butt = Buttons.Button()
        self.dead_cubes = []  # Создание списка неподвижных кубиков

        self.curr_fig = Figure(self.screen, 5, 0, choice(sett.colors),
                               choice(list(sett.figure_dict)))
        self.next_fig = Figure(self.screen, 14, 4, choice(sett.colors),
                               choice(list(sett.figure_dict)))

        self.curr_lines = 0  # Количество уничтоженных линий
        self.curr_points = 0 # Число очков, набранных игроком

        # Служебные параметры
        self.finished = False  # Флаг окончания игры
        self.vert_control_tick = 0
        self.vert_moving_delay = sett.normal_vert_moving_delay
        self.hor_control_tick = 0

    def points_counter(self, destroyed_lines):
        """Подсчитывает количество уничтоженных линий и число очков.

        Примает количество линий, уничтоженных в один приём.

        """
        self.curr_lines += destroyed_lines
        self.curr_points += auxiliary_counter(destroyed_lines)

    def draw(self):
        """Отрисовывает все объекты класса.

        """
        self.screen.fill(sett.WHITE)  # Фон
        self.glass.draw()
        self.next_box.draw()
        self.pause_butt.create_button(self.screen, sett.WHITE, 640, 420,
                                      100, 80, 3, "Пауза", sett.BLACK)
        self.curr_fig.draw()
        self.next_fig.draw_next()

        for dead_cube in self.dead_cubes:  # Отрисовка неподвижных кубиков
            dead_cube.draw()

        printer(self.screen, "Следующая:", 28, (585, 52))
        printer(self.screen, "Линии: " + str(self.curr_lines), 28, (585, 320))
        printer(self.screen, "Очки: " + str(self.curr_points), 28, (585, 365))

    def check_events(self):
        """Обрабатывает игровые события.

        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.finished = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.curr_fig.turn(90, self.glass)
                elif event.key == pygame.K_DOWN:
                    self.curr_fig.turn(-90, self.glass)
            elif event.type == MOUSEBUTTONDOWN:
                if self.pause_butt.pressed(pygame.mouse.get_pos()):
                    pause(self.screen)

        if pygame.key.get_pressed()[pygame.K_LEFT]:
            if pygame.time.get_ticks() - self.hor_control_tick >= \
                    sett.hor_moving_delay:
                self.curr_fig.hor_move(-1, self.glass)
                self.hor_control_tick = pygame.time.get_ticks()
        elif pygame.key.get_pressed()[pygame.K_RIGHT]:
            if pygame.time.get_ticks() - self.hor_control_tick >= \
                    sett.hor_moving_delay:
                self.curr_fig.hor_move(1, self.glass)
                self.hor_control_tick = pygame.time.get_ticks()

        if pygame.key.get_pressed()[pygame.K_SPACE]:
            self.vert_moving_delay = 25
        else:
            self.vert_moving_delay = sett.normal_vert_moving_delay

    def vert_moving(self):
        """Выполняет вертикальное перемещение фигуры.

        """
        global can_be_moved
        for cube in self.curr_fig.make():
            if cube.touch_check(self.glass)['down']:
                can_be_moved = True
            else:
                can_be_moved = False
                curr_sound.play('figure_stopping')
                break

        if can_be_moved:
            if pygame.time.get_ticks() - \
                    self.vert_control_tick >= self.vert_moving_delay:
                self.curr_fig.vert_move()
                self.vert_control_tick = pygame.time.get_ticks()
        else:
            for j in self.curr_fig.make():
                self.glass.block_cell(j.y, j.x)
            self.dead_cubes += self.curr_fig.make()
            self.next_fig.x = 5
            self.next_fig.y = 0
            self.curr_fig = self.next_fig
            self.next_fig = Figure(self.screen, 14, 4,
                                   choice(sett.colors),
                                   choice(list(sett.figure_dict)))

    def destroy_lines(self):
        """Проверяет свободность всех линий стакана.
        Удаляет заполненные линии.

        """
        destroyed_lines = 0
        for i in range(1, self.glass.height + 1):
            self.dead_cubes, has_been_destroyed = \
                self.glass.destroy_line(i, self.dead_cubes)
            destroyed_lines += int(has_been_destroyed)
            if has_been_destroyed:
                curr_sound.play('destroying_line')

        self.points_counter(destroyed_lines)

    def dead_cubes_operator(self):
        """Сортирует неподвижные кубики.
        Удаляет кубики из уничтоженных линий.

        """
        for dead_cube in self.dead_cubes:
            if dead_cube.y == 0:
                game_over(self.screen, self.curr_lines, self.curr_points)
            if not (0 < dead_cube.x < 17 and 0 < dead_cube.y < 21):
                self.dead_cubes.remove(dead_cube)

    def driver(self):
        """Управляет игровым процессом.

        """
        clock = pygame.time.Clock()

        while not self.finished:
            clock.tick(sett.FPS)
            self.check_events()
            self.vert_moving()
            self.destroy_lines()
            self.dead_cubes_operator()
            self.draw()
            pygame.display.update()
