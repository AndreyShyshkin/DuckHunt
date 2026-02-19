"""
Модуль для завантаження та управління звуковими ефектами гри.
"""

import os
import pygame
from duckhunt.core import settings


def getSound(name, volume):
    """
    Завантажує звуковий файл з папки ресурсів, встановлює його гучність
    та повертає об'єкт pygame.mixer.Sound.
    """

    soundPath = os.path.join(settings.AUDIO_DIR, name)
    sound = pygame.mixer.Sound(soundPath)
    sound.set_volume(volume * settings.GLOBAL_VOLUME)
    return sound

class SoundHandler:
    """
    Клас для управління відтворенням звуків.
    Використовує чергу (set), щоб уникнути одночасного дублювання однакових звуків в одному кадрі.
    """

    def __init__(self):
        """Ініціалізує чергу звуків та завантажує всі аудіофайли гри у пам'ять."""

        self.mute = False
        self.queue = set()
        self.sounds = {
            'bark':      getSound("bark.ogg", settings.VOL_BARK),
            'blast':     getSound("blast.ogg", settings.VOL_BLAST),
            'drop':      getSound("drop.ogg", settings.VOL_DROP),
            'flyaway':   getSound("flyaway.ogg", settings.VOL_FLYAWAY),
            'gameover':  getSound("gameover.ogg", settings.VOL_GAMEOVER),
            'hit':       getSound("hit.ogg", settings.VOL_HIT),
            'nextround': getSound("next-round.ogg", settings.VOL_NEXTROUND),
            'point':     getSound("point.ogg", settings.VOL_POINT),
            'quack':     getSound("quack.ogg", settings.VOL_QUACK)
        }

    def enqueue(self, sound):
        """Додає звуковий ефект до черги на відтворення."""

        self.queue.add(self.sounds[sound])

    def flush(self):
        """Відтворює всі звуки з черги та очищує її. Викликається в кінці кожного кадру гри."""

        for sound in self.queue:
            if not self.mute:
                sound.play()
        self.queue.clear()

    def toggleSound(self):
        """Перемикає стан звуку (увімкнено/вимкнено). Якщо звук вимкнено, зупиняє всі поточні звуки."""

        self.mute = not self.mute
        if self.mute:
            pygame.mixer.stop()
