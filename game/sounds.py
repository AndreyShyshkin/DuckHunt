import os
import pygame

SOUNDS_DIR = "media"

def getSound(name, volume):
    soundPath = os.path.join(SOUNDS_DIR, name)
    sound = pygame.mixer.Sound(soundPath)
    sound.set_volume(volume)
    return sound

class SoundHandler:


    def enqueue(self, sound):
        self.queue.add(self.sounds[sound])

    def flush(self):
        for sound in self.queue:
            if not self.mute:
                sound.play()
                def stop(self):
                    self.queue.remove(sound)
        self.queue.clear()

    def toggleSound(self):
        self.mute = not self.mute
        if self.mute:
            pygame.mixer.stop()
