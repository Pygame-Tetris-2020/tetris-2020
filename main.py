import pygame

from main_menu import *
from music import *

# coding UTF-8

pygame.init()

screen = pygame.display.set_mode((sett.width, sett.height))
pygame.display.set_caption('Тетрис')

curr_music.play()  # Запуск текущей музыки

menu(screen)  # Отображение главного меню

pygame.quit()
