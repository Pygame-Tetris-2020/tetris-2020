import pygame

import sett

def printer(surface, string, pt, cor):
    """Выводит текст на экран.

    Примает поверхность вывода, выводимую строку, размер шрифта и координату левого верхнего угла поля с текстом.

    """
    font = pygame.font.Font('tetris-font.ttf', pt)
    text = font.render(string, 1, sett.BLACK)
    surface.blit(text, cor)