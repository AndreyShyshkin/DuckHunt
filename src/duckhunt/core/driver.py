import pygame
from duckhunt.utils import sounds, registry
from duckhunt.core import states, settings


class Driver(object):
    def __init__(self, surface):
        # Set a global registry
        self.registry = registry.Registry()
        self.registry.set('surface', surface)
        self.registry.set('soundHandler', sounds.SoundHandler())

        
        controls = pygame.image.load(settings.CONTROLS_IMG).convert_alpha()
        self.registry.set('controlImgs', pygame.transform.smoothscale (controls, states.adjpos (*controls.get_size ())))

        
        sprites = pygame.image.load(settings.SPRITES_IMG).convert_alpha()
        sprites = pygame.transform.scale (sprites, states.adjpos (*sprites.get_size ()))
        self.registry.set('sprites', sprites)
        
        rsprites = pygame.transform.flip(sprites, True, False)
        self.registry.set('rsprites', rsprites)

        self.registry.set('score', 0)
        self.registry.set('round', 1)

        # Start the duckhunt
        self.state = states.StartState(self.registry)
        self.state = self.state.start()

    def handleEvent(self, event):
        # Toggle sound
        if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
            self.registry.get('soundHandler').toggleSound()

        self.state.execute(event)

    def update(self):
        newState = self.state.update()

        if newState:
            self.state = newState

    def render(self):
        self.state.render()
        self.registry.get('soundHandler').flush()