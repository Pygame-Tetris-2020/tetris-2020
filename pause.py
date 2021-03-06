import pygame
from pygame import MOUSEBUTTONDOWN

import Buttons
import sett
import main_menu
from util import printer


def pause(surface):
    """Отображает окно паузы.

    Примает поверхность вывода.

    """
    finished = False
    while not finished:
        surface.fill(sett.WHITE)
        printer(surface, 'Пауза', 50, (360, 330))

        cont_butt = Buttons.Button()
        cont_butt.create_button(surface, sett.WHITE, 325, 420, 250,
                                80, 3, "Продолжить", sett.BLACK)

        exit_butt = Buttons.Button()
        exit_butt.create_button(surface, sett.WHITE, 325, 520, 250,
                                80, 3, "Выйти из игры", sett.BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == MOUSEBUTTONDOWN:
                if cont_butt.pressed(pygame.mouse.get_pos()):
                    finished = True
                elif exit_butt.pressed(pygame.mouse.get_pos()):
                    main_menu.menu(surface)

        pygame.display.flip()
