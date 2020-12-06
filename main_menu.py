from random import randint, choice

import pygame

import Buttons, sett
from figure import *
from settings import *
from game import *


def printer(surface, string, pt, cor):
    """Выводит текст на экран.

    Примает поверхность вывода, выводимую строку, размер шрифта и координату левого верхнего угла поля с текстом.

    """
    font = pygame.font.Font('tetris-font.ttf', pt)
    text = font.render(string, 1, sett.BLACK)
    surface.blit(text, cor)


def animation(surface, vert_control_tick, demo_fig):
    """Отвечает за анимацию фигур в главном меню.

    Примает поверхность вывода, временную метку последнего перемещения и словарь анимационных фигур.
    Возвращает временную метку последнего перемещения и словарь анимационных фигур.

    """
    # Редактирование списка анимационных фигур
    if len(demo_fig) < 5:
        for i in range(5 - len(demo_fig)):
            demo_fig.append(Figure(surface, randint(2, 24), randint(-10, -2), choice(sett.colors),
                                   choice(list(sett.figure_dict))))

    # Отрисовка анимационных фигур
    for figure in demo_fig:
        figure.special_draw(0, 0)

    # Перемещение анимационных фигур по вертикали
    if pygame.time.get_ticks() - vert_control_tick >= sett.animation_moving_delay:
        for figure in demo_fig:
            figure.vert_move()
        vert_control_tick = pygame.time.get_ticks()

    # Уничтожение фигур, вышедших за пределы экрана
    for figure in demo_fig:
        if figure.y >= 25:
            demo_fig.remove(figure)

    return vert_control_tick, demo_fig


def menu(surface):
    """Оперирует окном главного меню.

    Примает поверхность вывода.

    """
    finished = False

    vert_control_tick = 0
    demo_fig = []

    while not finished:
        surface.fill(sett.WHITE)

        printer(surface, 'Тетрис', 50, (340, 330))

        play_butt = Buttons.Button()
        settings_butt = Buttons.Button()
        stat_butt = Buttons.Button()

        play_butt.create_button(surface, sett.WHITE, 350, 420, 200, 80, 3, "Играть", sett.BLACK)
        settings_butt.create_button(surface, sett.WHITE, 350, 520, 200, 80, 3, "Настройки", sett.BLACK)
        stat_butt.create_button(surface, sett.WHITE, 350, 620, 200, 80, 3, "Статистика", sett.BLACK)

        vert_control_tick, demo_fig = animation(surface, vert_control_tick, demo_fig)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == MOUSEBUTTONDOWN:
                if play_butt.pressed(pygame.mouse.get_pos()):
                    new_game = Game(surface)
                    new_game.driver()
                elif settings_butt.pressed(pygame.mouse.get_pos()):
                    settings(surface)
                elif stat_butt.pressed(pygame.mouse.get_pos()):
                    print("Statistics!")

        pygame.display.flip()