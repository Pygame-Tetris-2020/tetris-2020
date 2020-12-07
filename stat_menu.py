import pygame
from pygame import MOUSEBUTTONDOWN

import Buttons
import sett
from music import *


def printer(surface, string, pt, cor):
    """Выводит текст на экран.

    Примает поверхность вывода, выводимую строку, размер шрифта и координату левого верхнего угла поля с текстом.

    """
    font = pygame.font.Font('tetris-font.ttf', pt)
    text = font.render(string, 1, sett.BLACK)
    surface.blit(text, cor)


def stat(surface):
    
    """Отображает окно статистики

    """
    image = pygame.image.load('1.png')
    
    finished = False
    while not finished:
        surface.fill(sett.WHITE)
        back_butt = Buttons.Button()
        surface.blit(image, (30, 150))
        printer(surface, 'Статистика', 40, (300, 50))

        back_butt.create_button(surface, sett.WHITE, 375, 650,
                                150, 60, 3, "Назад", sett.BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == MOUSEBUTTONDOWN:
                if back_butt.pressed(pygame.mouse.get_pos()):
                    finished = True
        pygame.display.flip()