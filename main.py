import pygame
from pygame import *

from random import *

import Buttons

import sett

from main_menu import *
from pause import *
from box import *
from figure import *
from cube import *
from music import *
from game_over import *

# coding UTF-8

pygame.init()

screen = pygame.display.set_mode((sett.width, sett.height))
pygame.display.set_caption('Тетрис')

curr_music.play() # Запуск выбранной музыки
menu(screen) # Отображение главного меню

pygame.quit()