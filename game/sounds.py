import os
import pygame
from . import settings

def getSound(name, volume):
    soundPath = os.path.join(settings.AUDIO_DIR, name)
    sound = pygame.mixer.Sound(soundPath)
    sound.set_volume(volume)
    return sound

class SoundHandler:
    def __init__(self):
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
        self.queue.add(self.sounds[sound])

    def flush(self):
        for sound in self.queue:
            if not self.mute:
                sound.play()
        self.queue.clear()

    def toggleSound(self):
        self.mute = not self.mute
        if self.mute:
            pygame.mixer.stop()
