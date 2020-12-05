import pygame
from pygame import *

import Buttons

import tetris_settings as sett

from tetris_menu import *
from tetris_pause import *
from box import *
from figure import *
from cube import *

class Music:
    def __init__(self, song):
        self.song = song

    def play(self):
        pygame.mixer.music.load(self.song)
        pygame.mixer.music.play(-1)

    def stop(self):
        pygame.mixer.music.stop()


def play_sound(sound, option):
    if option:
        sound.play()


original = Music('tetris_sounds/TR1.mp3')
modern = Music('tetris_sounds/TR2.mp3')

figure_stopping = [pygame.mixer.Sound('tetris_sounds/figure_stopping.mp3'), True]
destroying_line = [pygame.mixer.Sound('tetris_sounds/destroying_line.mp3'), True]
game_ov = [pygame.mixer.Sound('tetris_sounds/game_over.mp3'), True]