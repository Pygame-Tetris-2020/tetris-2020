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

original = Music('tetris_sounds/TR1.mp3')
modern = Music('tetris_sounds/TR2.mp3')