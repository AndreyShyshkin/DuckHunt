import os, sys
import pygame
import pygame.transform
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

    def init(self):
        self.surface = pygame.display.set_mode(self.size)
        self.driver = driver.Driver(self.surface)

    def handleEvent(self, event):
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == 27):
            self.running = False
        else:
            self.driver.handleEvent(event)

    def loop(self):
        self.clock.tick(settings.FRAMES_PER_SEC)
        self.driver.update()

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