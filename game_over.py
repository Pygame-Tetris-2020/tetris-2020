from random import *

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

def printer(surface, string, pt, cor):
    font = pygame.font.Font('tetris-font.ttf', pt)
    text = font.render(string, 1, sett.BLACK)
    surface.blit(text, cor)

def game_over(surface, points):
    finished = False
    game_ov.play()
    while not finished:
        surface.fill(sett.WHITE)
        printer(surface, 'Игра окончена', 45, (245, 330))
        printer(surface, 'Линий: ' + str(points), 30, (245, 450))
        printer(surface, 'Очков: ' + str(points), 30, (245, 500))
        printer(surface, 'Имя игрока:', 30, (245, 400))


        original.stop()
        modern.stop()

        ex_butt = Buttons.Button()
        ex_butt.create_button(surface, sett.WHITE, 350, 580, 200, 60, 3, "В меню", sett.BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == MOUSEBUTTONDOWN:
                if ex_butt.pressed(pygame.mouse.get_pos()):
                    original.play()
                    main_menu.menu(surface)

        pygame.display.flip()