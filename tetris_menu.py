from random import *

import pygame
from pygame import *

import tetris_settings as sett

from box import *
from figure import *
from cube import *

def printer(surface, string, pt, cor):
    font = pygame.font.Font('tetris-font.ttf', pt)
    text = font.render(string, 1, sett.BLACK)
    surface.blit(text, cor)

def menu(surface):
    vert_control_tick = 0
    vert_moving_delay = 50
    demo_fig = []
    while True:
        surface.fill(sett.WHITE)
        printer(surface, 'Тетрис', 50, (340, 330))

        pygame.draw.line(surface, sett.BLACK, (450, 0), (450, 800), 1)
        pygame.draw.line(surface, sett.BLACK, (0, 400), (900, 400), 1)

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

        pygame.display.update()