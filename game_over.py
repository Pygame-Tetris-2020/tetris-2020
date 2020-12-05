from random import *

import pygame
from pygame import *

import Buttons

import tetris_settings as sett

from box import *
from figure import *
from cube import *
from tetris_gamesett import *
from music import *
from tetris_menu import *

def printer(surface, string, pt, cor):
    font = pygame.font.Font('tetris-font.ttf', pt)
    text = font.render(string, 1, sett.BLACK)
    surface.blit(text, cor)

def game_over(surface, points):
    finished = False
    if game_ov[1]:
        game_ov[0].play()
    while not finished:
        surface.fill(sett.WHITE)
        printer(surface, 'Игра окончена', 45, (245, 330))
        printer(surface, 'Линий: ' + str(points), 30, (245, 450))
        printer(surface, 'Очков: ' + str(points), 30, (245, 500))
        printer(surface, 'Имя игрока:', 30, (245, 400))


        original.stop()
        modern.stop()

        restart_butt = Buttons.Button()
        restart_butt.create_button(surface, sett.WHITE, 350, 560, 250, 60, 3, "Новая игра", sett.BLACK)

        ex_butt = Buttons.Button()
        ex_butt.create_button(surface, sett.WHITE, 350, 640, 250, 60, 3, "Выйти из игры", sett.BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == MOUSEBUTTONDOWN:
                if restart_butt.pressed(pygame.mouse.get_pos()):
                    pass
                elif ex_butt.pressed(pygame.mouse.get_pos()):
                    original.play()
                    tetris_menu.menu(surface)

        pygame.display.flip()