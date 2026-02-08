import os, sys
import pygame
import pygame.transform
import argparse
from src.duckhunt.registry import init_screen_params

# Game parameters
TITLE = "Duck Hunt"
FRAMES_PER_SEC = 50
BG_COLOR = 255, 255, 255

# Initialize pygame before importing modules
pygame.mixer.pre_init(44100, -16, 2, 1024)
pygame.init()
pygame.display.set_caption(TITLE)
pygame.mouse.set_visible(False)

import src.duckhunt.driver
import src.duckhunt.duck

class Game(object):
    def __init__(self, width, height):
        self.running = True
        self.surface = None
        self.clock = pygame.time.Clock()
        self.size = width, height
        background = os.path.join('assets/images', 'background.jpg')
        bg = pygame.image.load(background)
        self.background = pygame.transform.smoothscale (bg, self.size)
        self.driver = None

    def init(self):
        self.surface = pygame.display.set_mode(self.size)
        self.driver = src.game.driver.Driver(self.surface)

    def handleEvent(self, event):
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == 27):
            self.running = False
        else:
            self.driver.handleEvent(event)

    def loop(self):
        self.clock.tick(FRAMES_PER_SEC)
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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Duck Hunt Game")
    parser.add_argument('--width', type=int, default=800, help='Screen width (default: 800)')
    parser.add_argument('--height', type=int, default=500, help='Screen height (default: 500)')
    parser.add_argument('--volume', type=float, default=1.0, help='Master volume (0.0 to 1.0, default: 1.0)')
    parser.add_argument('--difficulty', type=int, default=1, help='Difficulty level (1: Normal, 2: Fast, 3: Hard, default: 1)')

    args = parser.parse_args()

    # Update global settings
    init_screen_params(args.width, args.height)
    # Recalculate coordinates based on new screen params
    src.game.states.init()
    src.game.duck.init()

    src.game.settings.GLOBAL_VOLUME = max(0.0, min(1.0, args.volume))

    # Adjust difficulty (speed multiplier)
    # Level 1: 4-6
    # Level 2: 6-8
    # Level 3: 8-10
    speed_boost = (args.difficulty - 1) * 2
    src.game.settings.DUCK_SPEED_MIN += speed_boost
    src.game.settings.DUCK_SPEED_MAX += speed_boost

    theGame = Game(args.width, args.height)
    theGame.execute()