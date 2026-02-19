"""
Глобальні налаштування та константи гри DuckHunt.
Містить шляхи до файлів, кольори, розміри об'єктів та параметри складності.
"""

import os

# Screen
ORIG_W = 800
ORIG_H = 500

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
IMAGES_DIR = os.path.join(ASSETS_DIR, 'images')
AUDIO_DIR = os.path.join(ASSETS_DIR, 'audio')
FONTS_DIR = os.path.join(ASSETS_DIR, 'fonts')

# Images
CONTROLS_IMG = os.path.join(IMAGES_DIR, 'controls.png')
SPRITES_IMG = os.path.join(IMAGES_DIR, 'sprites.png')
CROSSHAIRS_IMG = os.path.join(IMAGES_DIR, 'crosshairs.png')

# Fonts
FONT_FILE = os.path.join(FONTS_DIR, 'arcadeclassic.ttf')

# Audio Volumes
GLOBAL_VOLUME = 1.0
VOL_BARK = 0.7
VOL_BLAST = 0.7
VOL_DROP = 0.2
VOL_FLYAWAY = 1.0
VOL_GAMEOVER = 0.7
VOL_HIT = 1.0
VOL_NEXTROUND = 1.0
VOL_POINT = 1.0
VOL_QUACK = 0.7

# Difficulty
DUCK_SPEED_MIN = 4
DUCK_SPEED_MAX = 6

# Colors
COLOR_GREEN = (154, 233, 0)
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)

# Game Settings
GUN_ROUNDS = 3
DUCK_ANIMATION_DELAY = 8
FRAMES_PER_SEC = 60

# Object Properties (Raw values)
DUCK_FRAME_W = 81
DUCK_FRAME_H = 75
DUCK_X_OFFSET = 250
DUCK_Y_OFFSET = 225
DUCK_FLYOFF_Y_OFFSET = 155
DUCK_FALL_Y_OFFSET = 235

DOG_POS = (250, 350)
DOG_FRAME_SIZE = (122, 110)
DOG_REPORT_POS = (450, 325)
DOG_LAUGH_RECT = (385, 120, 80, 85)
DOG_ONE_DUCK_RECT = (650, 0, 100, 100)
DOG_TWO_DUCKS_RECT = (630, 115, 120, 100)

HIT_POS = (245, 440)
HIT_RECT = (0, 0, 287, 43)
HIT_DUCK_POS = (329, 445)
HIT_DUCK_WHITE_RECT = (218, 44, 18, 15)
HIT_DUCK_RED_RECT = (200, 44, 18, 15)

SCORE_POS = (620, 440)
SCORE_RECT = (69, 43, 130, 43)

FONT_START_POS = (730, 442)
ROUND_POS = (60, 410)
SHOT_BG_POS = (60, 440)
SHOT_POS = (60, 440)
SHOT_RECT = (0, 43, 70, 43)
BULLET_RECT = (200, 59, 13, 17)

NOTICE_POS = (370, 120)
NOTICE_RECT = (0, 86, 128, 63)
NOTICE_WIDTH = 128
NOTICE_LINE_1_HEIGHT = 128
NOTICE_LINE_2_HEIGHT = 150
