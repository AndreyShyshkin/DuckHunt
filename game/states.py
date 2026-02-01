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