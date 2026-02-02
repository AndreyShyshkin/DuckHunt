import os, time
import pygame
from .registry import adjpos, adjrect, adjwidth, adjheight
from .gun import Gun
from .duck import Duck

DOG_POSITION = adjpos (250, 350)
DOG_FRAME = adjpos (122, 110)
DOG_REPORT_POSITION = adjpos (450, 325)
DOG_LAUGH_RECT = adjrect (385, 120, 80, 85)
DOG_ONE_DUCK_RECT = adjrect (650, 0, 100, 100)
DOG_TWO_DUCKS_RECT = adjrect (630, 115, 120, 100)
HIT_POSITION = adjpos (245, 440)
HIT_RECT = adjrect (0, 0, 287, 43)
HIT_DUCK_POSITION = adjpos (329, 445)
HIT_DUCK_WHITE_RECT = adjrect (218, 44, 18, 15)
HIT_DUCK_RED_RECT = adjrect (200, 44, 18, 15)
SCORE_POSITION = adjpos (620, 440)
SCORE_RECT = adjrect (69, 43, 130, 43)
FONT = os.path.join('media', 'arcadeclassic.ttf')
FONT_STARTING_POSITION = adjpos (730, 442)
FONT_GREEN = 154, 233, 0
FONT_BLACK = 0, 0, 0
FONT_WHITE = 255, 255, 255
ROUND_POSITION = adjpos (60, 410)
SHOT_BG_POSITION = adjpos (60, 440)
SHOT_POSITION = adjpos (60, 440)
SHOT_RECT = adjrect (0, 43, 70, 43)
BULLET_RECT = adjrect (200, 59, 13, 17)
NOTICE_POSITION = adjpos (370, 120)
NOTICE_RECT = adjrect (0, 86, 128, 63)
NOTICE_WIDTH = adjwidth (128)
NOTICE_LINE_1_HEIGHT = adjheight (128)
NOTICE_LINE_2_HEIGHT = adjwidth (150)

registry = None

class BaseState(object):
    def __init__(self):
        global registry
        self.registry = registry
        self.timer = int(time.time())
        self.notices = set()
        self.gun = Gun(self.registry)
        self.hitDucks = [False for i in range(10)]
        self.hitDuckIndex = 0

    def renderNotices(self):
        if len(self.notices) == 0:
            return
        elif len(self.notices) == 1:
            self.notices.add("")

        surface = self.registry.get('surface')
        controlImgs = self.registry.get('controlImgs')
        font = pygame.font.Font(FONT, adjheight (20))
        notices_list = list(self.notices)
        line1 = font.render(str(notices_list[0]), True, (255, 255, 255))
        line2 = font.render(str(notices_list[1]), True, (255, 255, 255))
        x, y = NOTICE_POSITION
        x1 = x + (NOTICE_WIDTH - line1.get_width()) // 2
        x2 = x + (NOTICE_WIDTH - line2.get_width()) // 2
        surface.blit(controlImgs, NOTICE_POSITION, NOTICE_RECT)
        surface.blit(line1, (x1, NOTICE_LINE_1_HEIGHT))
        surface.blit(line2, (x2, NOTICE_LINE_2_HEIGHT))

    def renderControls(self):
        img = self.registry.get('controlImgs')
        surface = self.registry.get('surface')
        round = self.registry.get('round')
        controlImgs = self.registry.get('controlImgs')

        font = pygame.font.Font(FONT, adjheight (20))
        text = font.render(("R= %d" % round), True, FONT_GREEN, FONT_BLACK);
        surface.blit(text, ROUND_POSITION);

        startingX, startingY = SHOT_POSITION
        surface.blit(controlImgs, SHOT_POSITION, SHOT_RECT)
        for i in range(self.gun.rounds):
            x = startingX + adjwidth (10) + adjwidth (i * 18)
            y = startingY + adjheight (5)
            surface.blit(controlImgs, (x, y), BULLET_RECT)

        surface.blit(controlImgs, HIT_POSITION, HIT_RECT)
        startingX, startingY = HIT_DUCK_POSITION
        for i in range(10):
            x = startingX + adjwidth (i * 18)
            y = startingY
            if self.hitDucks[i]:
                surface.blit(img, (x, y), HIT_DUCK_RED_RECT)
            else:
                surface.blit(img, (x, y), HIT_DUCK_WHITE_RECT)

        surface.blit(img, SCORE_POSITION, SCORE_RECT)
        font = pygame.font.Font(FONT, adjheight (20))
        text = font.render(str(self.registry.get('score')), True, FONT_WHITE);
        x, y = FONT_STARTING_POSITION
        x -= text.get_width();
        surface.blit(text, (x,y));
