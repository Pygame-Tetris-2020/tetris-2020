import pygame

import sett


class Music:
    def __init__(self, music_bank):
        self.music_bank = music_bank
        self.curr_music = self.music_bank['original']

    def play(self):
        """Загружает и проигрывает фоновую музыку.

        """
        pygame.mixer.music.load(self.curr_music)
        pygame.mixer.music.play(-1)

    def stop(self):
        """Останавливает воспроизведение фоновой музыки.

        """
        pygame.mixer.music.stop()

    def change(self, song):
        """Заменяет текущую композицию на новую.

        Принимает ключ новой композиции в словаре композиций.

        """
        self.stop()
        self.curr_music = self.music_bank[song]
        self.play()


class Sounds:
    def __init__(self, sound_bank):
        self.sound_bank = sound_bank
        self.is_sound_on = True

    def play(self, sound):
        """Проигрывает игровой звук в случае, если эта опция не отключена пользователем.

        Принимает ключ звука в словаре звуков.

        """
        curr_sound = pygame.mixer.Sound(self.sound_bank[sound])
        if self.is_sound_on:
            curr_sound.play()


curr_music = Music(sett.music_bank)
curr_sound = Sounds(sett.sound_bank)