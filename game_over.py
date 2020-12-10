import pygame
from pygame import MOUSEBUTTONDOWN
import datetime

import Buttons
import sett
import main_menu
from music import *
from stat_hist import *
from util import printer


def game_over(surface, lines, points):
    """Оперирует окном окончания игры.
    Записывает в txt-файлы дату, время игры и количество очков.
    Примает поверхность вывода и число набранных очков.
    Впоследствии будет добавлен третий аргумент -
    число уничтоженных линий (пока очки и линии совпадают).

    """
    finished = False
    curr_sound.play('game_ov')
    file = open("tetris_datetime.txt", "a")
    t = datetime.datetime.now()
    file.write(str(t)[0:16] + '\n')
    file.close()
    file = open("tetris_score.txt", "a")
    file.write(str(points) + '\n')
    file.close()
    histogramm()

    while not finished:
        surface.fill(sett.WHITE)

        printer(surface, 'Игра окончена', 45, (245, 330))

        lines_x = 365 - (len(str(lines)) - 1) * 8  # Центрирование строки с числом линий
        printer(surface, 'Линий: ' + str(lines), 30, (lines_x, 410))

        points_x = 365 - (len(str(points)) - 1)*8 # Центрирование строки с числом очков
        printer(surface, 'Очков: ' + str(points), 30, (points_x, 460))

        curr_music.stop()

        ex_butt = Buttons.Button()
        ex_butt.create_button(surface, sett.WHITE, 350, 530, 200,
                              60, 3, "В меню", sett.BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == MOUSEBUTTONDOWN:
                if ex_butt.pressed(pygame.mouse.get_pos()):
                    curr_music.play()
                    main_menu.menu(surface)

        pygame.display.flip()
