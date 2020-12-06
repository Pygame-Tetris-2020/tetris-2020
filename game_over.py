import pygame
from pygame import MOUSEBUTTONDOWN

import Buttons
import sett
import main_menu
from music import *


def printer(surface, string, pt, cor):
    """Выводит текст на экран.

    Примает поверхность вывода, выводимую строку, размер шрифта и координату левого верхнего угла поля с текстом.

    """
    font = pygame.font.Font('tetris-font.ttf', pt)
    text = font.render(string, 1, sett.BLACK)
    surface.blit(text, cor)


def game_over(surface, points):
    """Оперирует окном окончания игры.

    Примает поверхность вывода и число набранных очков.
    Впоследствии будет добавлен третий аргумент - число уничтоженных линий (пока очки и линии совпадают).

    """
    finished = False
    curr_sound.play('game_ov')

    while not finished:
        surface.fill(sett.WHITE)

        printer(surface, 'Игра окончена', 45, (245, 330))
        printer(surface, 'Линий: ' + str(points), 30, (245, 450))
        printer(surface, 'Очков: ' + str(points), 30, (245, 500))
        printer(surface, 'Имя игрока:', 30, (245, 400))

        curr_music.stop()

        ex_butt = Buttons.Button()
        ex_butt.create_button(surface, sett.WHITE, 350, 580, 200, 60, 3, "В меню", sett.BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == MOUSEBUTTONDOWN:
                if ex_butt.pressed(pygame.mouse.get_pos()):
                    curr_music.play()
                    main_menu.menu(surface)

        pygame.display.flip()