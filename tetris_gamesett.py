from random import *

import pygame
from pygame import *

import Buttons

import tetris_settings as sett

from box import *
from figure import *
from cube import *
from music import *

def printer(surface, string, pt, cor):
    font = pygame.font.Font('tetris-font.ttf', pt)
    text = font.render(string, 1, sett.BLACK)
    surface.blit(text, cor)

def settings(surface):
    finished = False
    while not finished:
        surface.fill(sett.WHITE)
        printer(surface, 'Настройки', 40, (320, 30))

        printer(surface, 'Музыка', 32, (20, 110))

        music0_butt = Buttons.Button()
        music0_butt.create_button(surface, sett.WHITE, 50, 160, 200, 60, 3, "Без музыки", sett.BLACK)

        music1_butt = Buttons.Button()
        music1_butt.create_button(surface, sett.WHITE, 300, 160, 200, 60, 3, "Оригинальная", sett.BLACK)

        music2_butt = Buttons.Button()
        music2_butt.create_button(surface, sett.WHITE, 550, 160, 200, 60, 3, "Современная", sett.BLACK)

        printer(surface, 'Звуки в игре', 32, (20, 320))

        sounds0_butt = Buttons.Button()
        sounds0_butt.create_button(surface, sett.WHITE, 50, 370, 200, 60, 3, "Выключить", sett.BLACK)

        sounds1_butt = Buttons.Button()
        sounds1_butt.create_button(surface, sett.WHITE, 300, 370, 200, 60, 3, "Включить", sett.BLACK)

        printer(surface, 'Тема', 32, (20, 510))

        theme0_butt = Buttons.Button()
        theme0_butt.create_button(surface, sett.WHITE, 50, 570, 200, 60, 3, "Светлая", sett.BLACK)

        theme1_butt = Buttons.Button()
        theme1_butt.create_button(surface, sett.WHITE, 300, 570, 200, 60, 3, "Темная", sett.BLACK)

        back_butt = Buttons.Button()
        back_butt.create_button(surface, sett.WHITE, 375, 700, 150, 60, 3, "Назад", sett.BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == MOUSEBUTTONDOWN:
                if back_butt.pressed(pygame.mouse.get_pos()):
                    finished = True
                elif music0_butt.pressed(pygame.mouse.get_pos()):
                    modern.stop()
                    original.stop()
                elif music1_butt.pressed(pygame.mouse.get_pos()):
                    modern.stop()
                    original.play()
                elif music2_butt.pressed(pygame.mouse.get_pos()):
                    original.stop()
                    modern.play()
                elif stat_butt.pressed(pygame.mouse.get_pos()):
                    print("Statistics!")

        pygame.display.flip()