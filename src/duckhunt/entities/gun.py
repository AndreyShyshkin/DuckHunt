"""
Модуль, що описує зброю гравця.
Керує прицілом, обробкою пострілів та кількістю патронів.
"""

import pygame
from duckhunt.core import settings
from duckhunt.utils.registry import adjpos


class Gun(object):
    """
    Клас, що представляє рушницю гравця.
    Відповідає за відображення прицілу та логіку стрільби.
    """

    def __init__(self, registry):
        """Ініціалізує зброю, завантажує зображення прицілу та встановлює базову кількість патронів."""

        self.registry = registry
        self.rounds = settings.GUN_ROUNDS
        self.mousePos = (0,0)
        self.mouseImg = pygame.image.load(settings.CROSSHAIRS_IMG)
        self.mouseImg = pygame.transform.scale(self.mouseImg, adjpos(*self.mouseImg.get_size()))

    def render(self):
        """Відмальовує приціл на поточній позиції курсору миші."""

        surface = self.registry.get('surface')
        surface.blit(self.mouseImg, self.mousePos)

    def reloadIt(self):
        """Перезаряджає зброю (відновлює максимальну кількість патронів для нового раунду)."""

        self.rounds = settings.GUN_ROUNDS

    def moveCrossHairs(self, pos):
        """
        Оновлює координати прицілу.
        Зсуває картинку так, щоб реальний курсор миші знаходився чітко по центру графічного прицілу.
        """

        xOffset = self.mouseImg.get_width() // 2
        yOffset = self.mouseImg.get_height() // 2
        x, y = pos
        self.mousePos = (x - xOffset), (y - yOffset)

    def shoot(self):
        """
        Здійснює постріл, віднімає патрон та відтворює звук.
        Повертає True, якщо постріл успішний (були патрони).
        """

        if self.rounds <= 0:
            return False

        self.registry.get('soundHandler').enqueue('blast')
        self.rounds = self.rounds - 1
        return True
