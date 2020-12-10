import pygame
from pygame import MOUSEBUTTONDOWN

import Buttons
import sett
from music import *
from util import printer


def settings(surface):
    """Отображает окно пользовательских настроек и управляет им.

    Примает поверхность вывода.

    """
    finished = False
    while not finished:
        surface.fill(sett.WHITE)

        # Вывод надписей на экран
        printer(surface, 'Настройки', 40, (320, 160))
        printer(surface, 'Музыка', 32, (380, 260))
        printer(surface, 'Звуки', 32, (153, 260))
        printer(surface, 'Тема', 32, (645, 260))

        # Создание кнопок. Впоследствии будет переделано!
        music0_butt = Buttons.Button()
        music1_butt = Buttons.Button()
        music2_butt = Buttons.Button()

        sounds0_butt = Buttons.Button()
        sounds1_butt = Buttons.Button()

        theme0_butt = Buttons.Button()
        theme1_butt = Buttons.Button()

        back_butt = Buttons.Button()

        # Форматирование кнопок
        music0_butt.create_button(surface, sett.WHITE, 350, 330, 200,
                                  60, 3, "Без музыки", sett.BLACK)
        music1_butt.create_button(surface, sett.WHITE, 350, 430, 200,
                                  60, 3, "Оригинальная", sett.BLACK)
        music2_butt.create_button(surface, sett.WHITE, 350, 530, 200,
                                  60, 3, "Современная", sett.BLACK)

        sounds1_butt.create_button(surface, sett.WHITE, 135, 330, 150,
                                   60, 3, "Включить", sett.BLACK)
        sounds0_butt.create_button(surface, sett.WHITE, 135, 430, 150,
                                   60, 3, "Выключить", sett.BLACK)

        theme0_butt.create_button(surface, sett.WHITE, 615, 330, 150,
                                  60, 3, "Светлая", sett.BLACK)
        theme1_butt.create_button(surface, sett.WHITE, 615, 430, 150,
                                  60, 3, "Тёмная", sett.BLACK)

        back_butt.create_button(surface, sett.WHITE, 375, 650, 150,
                                60, 3, "Назад", sett.BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == MOUSEBUTTONDOWN:
                if back_butt.pressed(pygame.mouse.get_pos()):
                    finished = True

                elif music0_butt.pressed(pygame.mouse.get_pos()):
                    curr_music.stop()
                elif music1_butt.pressed(pygame.mouse.get_pos()):
                    curr_music.change('original')
                elif music2_butt.pressed(pygame.mouse.get_pos()):
                    curr_music.change('modern')

                elif theme0_butt.pressed(pygame.mouse.get_pos()):
                    sett.BLACK, sett.WHITE, sett.WHITE_HEX = (0, 0, 0), (255, 255, 255), '#ffffff'
                elif theme1_butt.pressed(pygame.mouse.get_pos()):
                    sett.BLACK, sett.WHITE, sett.WHITE_HEX = (255, 255, 255), (0, 0, 0), '#000000'

                elif sounds0_butt.pressed(pygame.mouse.get_pos()):
                    curr_sound.is_sound_on = False
                elif sounds1_butt.pressed(pygame.mouse.get_pos()):
                    curr_sound.is_sound_on = True

        pygame.display.flip()
