import pygame
from duckhunt.core import settings
from duckhunt.utils.registry import adjpos


class Gun(object):
    def __init__(self, registry):
        self.registry = registry
        self.rounds = settings.GUN_ROUNDS
        self.mousePos = (0,0)
        self.mouseImg = pygame.image.load(settings.CROSSHAIRS_IMG)
        self.mouseImg = pygame.transform.scale(self.mouseImg, adjpos(*self.mouseImg.get_size()))

    def render(self):
        surface = self.registry.get('surface')
        surface.blit(self.mouseImg, self.mousePos)

    def reloadIt(self):
        self.rounds = settings.GUN_ROUNDS

    def moveCrossHairs(self, pos):
        xOffset = self.mouseImg.get_width() // 2
        yOffset = self.mouseImg.get_height() // 2
        x, y = pos
        self.mousePos = (x - xOffset), (y - yOffset)

    def shoot(self):
        if self.rounds <= 0:
            return False

        self.registry.get('soundHandler').enqueue('blast')
        self.rounds = self.rounds - 1
        return True
