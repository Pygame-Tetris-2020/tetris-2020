import pygame
from pygame import *

import main_menu

class Music:
    def __init__(self, song):
        self.song = song

    def play(self):
        pygame.mixer.music.load(self.song)
        pygame.mixer.music.play(-1)

    def stop(self):
        pygame.mixer.music.stop()


class Sound:
    def __init__(self, sound):
        self.sound = sound

    def play(self):
        if is_sounds_on:
            self.play()

original = Music('sounds/TR1.mp3')
modern = Music('sounds/TR2.mp3')
curr_music = original

figure_stopping = pygame.mixer.Sound('sounds/figure_stopping.mp3')
destroying_line = pygame.mixer.Sound('sounds/destroying_line.mp3')
game_ov = pygame.mixer.Sound('sounds/game_over.mp3')