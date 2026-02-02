import os
import pygame
from . import registry, states


class Driver(object):
    def __init__(self, surface):
        
        self.registry = registry.Registry()
        self.registry.set('surface', surface)
        

        self.registry.set('score', 0)
        self.registry.set('round', 1)

        # Start the game
        self.state = states.StartState(self.registry)
        self.state = self.state.start()

    def handleEvent(self, event):
        self.state.execute(event)

    def update(self):
        newState = self.state.update()

        if newState:
            self.state = newState

    def render(self):
        self.state.render()
        self.registry.get('soundHandler').flush()
