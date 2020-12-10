import pygame
from pygame import MOUSEBUTTONDOWN

import Buttons
import sett
from music import *
from util import printer
import stat_hist


def stat(surface):
    
    """Отображает окно статистики

    """
    image = pygame.image.load(stat_hist.histogramm())
    
    finished = False
    while not finished:
        surface.fill(sett.WHITE)
        back_butt = Buttons.Button()
        surface.blit(image, (10, 150))
        printer(surface, 'Статистика', 40, (300, 50))

        rec_x = 378 - 8*(len(str(stat_hist.record())) - 1) # Центрирование строки с рекордным результатом
        printer(surface, 'Рекорд: ' + str(stat_hist.record()), 25, (rec_x, 600))
        

        back_butt.create_button(surface, sett.WHITE, 375, 660,
                                150, 60, 3, "Назад", sett.BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == MOUSEBUTTONDOWN:
                if back_butt.pressed(pygame.mouse.get_pos()):
                    finished = True
        pygame.display.flip()
