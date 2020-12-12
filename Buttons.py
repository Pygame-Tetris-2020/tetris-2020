# -*- coding: cp1252 -*-
# /usr/bin/env python
# Simon H. Larsen
# Buttons
# Project started: d. 26. august 2012

import pygame
from pygame.locals import *

import sett
from music import *

pygame.init()


class Button:

    def create_button(self, surface, color, x, y,
                      length, height, width,
                      text, text_color):
        """Responsible for creating the button.

        Accepts the following arguments:
        surface - defines the drawing surface
        color - defines the drawing color
        x - x-coord of left upper angle
        y - y-coord of left upper angle
        length - defines the length of button
        height - defines the height of button
        width - defines the width of button
        text - text in button
        text_color - color of the text on the button

        """
        surface = self.draw_button(surface, color,
                                   length, height, x, y, width)
        surface = self.write_text(surface, text,
                                  text_color, length, height, x, y)
        self.rect = pygame.Rect(x, y, length, height)
        return surface

    def write_text(self, surface, text, text_color, length, height, x, y):
        """Responsible for writing the text on the button.

        Accepts the following arguments:
        surface - defines the drawing surface
        text - text in button
        text_color - color of the text on the button
        x - x-coord of left upper angle
        y - y-coord of left upper angle
        length - defines the length of button
        height - defines the height of button

        """
        font_size = int(length // len(text))
        myFont = pygame.font.Font('tetris-font.ttf', font_size)
        myText = myFont.render(text, 1, text_color)
        surface.blit(myText, ((x + length / 2) - myText.get_width() / 2,
                              (y + height / 2) - myText.get_height() / 2))
        return surface

    def draw_button(self, surface, color, length, height, x, y, width):
        """Responsible for drawing the button.

        Accepts the following arguments:
        surface - defines the drawing surface
        color - defines the drawing color
        x - x-coord of left upper angle
        y - y-coord of left upper angle
        length - defines the length of button
        height - defines the height of button
        width - defines the width of button

        """
        for i in range(1, 10):
            s = pygame.Surface((length + (i * 2), height + (i * 2)))
            s.fill(color)
            alpha = (255 / (i + 2))
            if alpha <= 0:
                alpha = 1
            s.set_alpha(alpha)
            pygame.draw.rect(s, color, (x - i, y - i, length + i,
                                        height + i), width)
            surface.blit(s, (x - i, y - i))
        pygame.draw.rect(surface, color, (x, y, length, height), 0)
        pygame.draw.rect(surface, sett.BLACK, (x, y, length, height), 1)
        return surface

    def pressed(self, mouse):
        if mouse[0] > self.rect.topleft[0]:
            if mouse[1] > self.rect.topleft[1]:
                if mouse[0] < self.rect.bottomright[0]:
                    if mouse[1] < self.rect.bottomright[1]:
                        curr_sound.play('butt_click')
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False
        else:
            return False
