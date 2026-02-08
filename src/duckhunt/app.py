import os
import sys
import pygame

from duckhunt.core import settings
from duckhunt.core import driver

class Game(object):
    def __init__(self, width, height, fullscreen=False):
        self.running = True
        self.surface = None
        self.game_surface = None
        self.clock = pygame.time.Clock()
        self.size = width, height
        self.fullscreen = fullscreen

        bg_path = os.path.join(settings.IMAGES_DIR, 'background.jpg')
        bg = pygame.image.load(bg_path)
        self.background = pygame.transform.smoothscale(bg, self.size)
        self.driver = None

        self.window_size = self.size
        self.scale = 1.0
        self.scale_pos = (0, 0)

        self.accumulator = 0.0
        self.logic_update_rate = 50.0
        self.dt = 1.0 / self.logic_update_rate

    def init(self):
        if not self.fullscreen:
            os.environ['SDL_VIDEO_CENTERED'] = '1'

        flags = pygame.FULLSCREEN if self.fullscreen else 0
        if self.fullscreen:
            self.surface = pygame.display.set_mode((0, 0), flags)
        else:
            self.surface = pygame.display.set_mode(self.size, flags)

        self.window_size = self.surface.get_size()

        self.game_surface = pygame.Surface(self.size).convert_alpha()
        self.driver = driver.Driver(self.game_surface)

        self._recompute_scale()

    def _recompute_scale(self):
        window_w, window_h = self.window_size
        game_w, game_h = self.size
        scale = min(window_w / game_w, window_h / game_h)
        self.scale = scale
        scaled_w = int(game_w * scale)
        scaled_h = int(game_h * scale)
        pos_x = (window_w - scaled_w) // 2
        pos_y = (window_h - scaled_h) // 2
        self.scale_pos = (pos_x, pos_y)
        self.scaled_size = (scaled_w, scaled_h)

    def handleEvent(self, event):
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            self.running = False
        else:
            self.driver.handleEvent(event)
            if event.type == pygame.VIDEORESIZE:
                self.window_size = event.size
                self._recompute_scale()

    def loop(self):
        frame_time = self.clock.tick(settings.FRAMES_PER_SEC) / 1000.0

        if frame_time > 0.25:
            frame_time = 0.25

        self.accumulator += frame_time

        while self.accumulator >= self.dt:
            self.driver.update(self.dt)
            self.accumulator -= self.dt

    def render(self):
        self.game_surface.blit(self.background, (0, 0))
        self.driver.render()

        if self.scaled_size != self.size:
            scaled = pygame.transform.smoothscale(self.game_surface, self.scaled_size)
        else:
            scaled = self.game_surface

        self.surface.fill((0, 0, 0))
        self.surface.blit(scaled, self.scale_pos)
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