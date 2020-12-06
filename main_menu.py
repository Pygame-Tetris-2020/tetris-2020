from random import *

import pygame
from pygame import *

import Buttons

import sett

from box import *
from figure import *
from cube import *
from music import *
from settings import *
from game_over import *
from game import *

def printer(surface, string, pt, cor):
    font = pygame.font.Font('tetris-font.ttf', pt)
    text = font.render(string, 1, sett.BLACK)
    surface.blit(text, cor)

def menu(surface):
    vert_control_tick = 0
    vert_moving_delay = 50
    demo_fig = []
    finished = False
    while not finished:
        surface.fill(sett.WHITE)
        printer(surface, 'Тетрис', 50, (340, 330))

        play_butt = Buttons.Button()
        play_butt.create_button(surface, sett.WHITE, 350, 420, 200, 80, 3, "Играть", sett.BLACK)

        settings_butt = Buttons.Button()
        settings_butt.create_button(surface, sett.WHITE, 350, 520, 200, 80, 3, "Настройки", sett.BLACK)

        stat_butt = Buttons.Button()
        stat_butt.create_button(surface, sett.WHITE, 350, 620, 200, 80, 3, "Статистика", sett.BLACK)

        if len(demo_fig) < 5:
            for i in range(5 - len(demo_fig)):
                demo_fig.append(Figure(surface, randint(2, 24), randint(-10, -2), choice(sett.colors),
                              choice(list(sett.figure_dict))))

        for i in demo_fig:
            i.special_draw(0, 0)

        if pygame.time.get_ticks() - vert_control_tick >= vert_moving_delay:
            for i in demo_fig:
                i.vert_move()
            vert_control_tick = pygame.time.get_ticks()

        for i in demo_fig:
            if i.y >=25:
                demo_fig.remove(i)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == MOUSEBUTTONDOWN:
                if play_butt.pressed(pygame.mouse.get_pos()):
                    new_game = Game(surface)
                    new_game.drive()
                elif settings_butt.pressed(pygame.mouse.get_pos()):
                    settings(surface)
                elif stat_butt.pressed(pygame.mouse.get_pos()):
                    print("Statistics!")

        pygame.display.flip()