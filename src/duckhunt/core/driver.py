"""Головний контролер гри DuckHunt. Відповідає за ініціалізацію та ігровий цикл."""

import pygame
from duckhunt.utils import sounds, registry
from duckhunt.core import states, settings


class Driver(object):
    """
    Керує глобальним станом гри, ресурсами та перемиканням між екранами.
    Реалізує патерн State Machine (Машина станів) для управління грою.
    """

    def __init__(self, surface):
        """Ініціалізує драйвер, завантажує базові ресурси та запускає стартовий стан."""
        # Set a global registry
        self.registry = registry.Registry()
        self.registry.set('surface', surface)
        self.registry.set('soundHandler', sounds.SoundHandler())

        controls = pygame.image.load(settings.CONTROLS_IMG).convert_alpha()
        self.registry.set('controlImgs', pygame.transform.smoothscale(controls, states.adjpos(*controls.get_size())))

        sprites = pygame.image.load(settings.SPRITES_IMG).convert_alpha()
        sprites = pygame.transform.scale(sprites, states.adjpos(*sprites.get_size()))
        self.registry.set('sprites', sprites)

        rsprites = pygame.transform.flip(sprites, True, False)
        self.registry.set('rsprites', rsprites)

        self.registry.set('score', 0)
        self.registry.set('round', 1)

        # Start the duckhunt
        self.state = states.StartState(self.registry)
        self.state = self.state.start()

    def handleEvent(self, event):
        """Обробляє події вводу (натискання клавіш, миші) та передає їх поточному стану."""
        # Toggle sound
        if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
            self.registry.get('soundHandler').toggleSound()

        self.state.execute(event)

    def update(self, dt):
        """Оновлює логіку поточного стану та виконує перехід до нового стану, якщо потрібно."""
        newState = self.state.update(dt)

        if newState:
            self.state = newState

    def render(self):
        """Відмальовує графіку поточного стану та відтворює накопичені звуки."""
        self.state.render()
        self.registry.get('soundHandler').flush()
