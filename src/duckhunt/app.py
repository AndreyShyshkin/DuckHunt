import os
import sys
import pygame

from duckhunt.core import settings
from duckhunt.core import driver

class Game(object):
    def __init__(self, width, height):
        self.running = True
        self.surface = None
        self.clock = pygame.time.Clock()
        self.size = width, height

        bg_path = os.path.join(settings.IMAGES_DIR, 'background.jpg')
        bg = pygame.image.load(bg_path)
        self.background = pygame.transform.smoothscale(bg, self.size)
        self.driver = None

        self.accumulator = 0.0
        self.logic_update_rate = 60.0
        self.dt = 1.0 / self.logic_update_rate

    def init(self):
        self.surface = pygame.display.set_mode(self.size)
        self.driver = driver.Driver(self.surface)

    def handleEvent(self, event):
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            self.running = False
        else:
            self.driver.handleEvent(event)

    def loop(self):
        frame_time = self.clock.tick(settings.FRAMES_PER_SEC) / 1000.0

        if frame_time > 0.25:
            frame_time = 0.25

        self.accumulator += frame_time

        while self.accumulator >= self.dt:
            self.driver.update()
            self.accumulator -= self.dt

    def render(self):
        self.surface.blit(self.background, (0,0))
        self.driver.render()
        pygame.display.flip()

    def cleanup(self):
        pygame.quit()
        sys.exit(0)

    def execute(self):
        self.init()

        while (self.running):
            for event in pygame.event.get():
                self.handleEvent(event)
            self.loop()
            self.render()

        self.cleanup()