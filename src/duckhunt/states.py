import time
import pygame
from .registry import adjpos, adjrect, adjwidth, adjheight
from .gun import Gun
from .duck import Duck
from . import settings

DOG_POSITION = None
DOG_FRAME = None
DOG_REPORT_POSITION = None
DOG_LAUGH_RECT = None
DOG_ONE_DUCK_RECT = None
DOG_TWO_DUCKS_RECT = None
HIT_POSITION = None
HIT_RECT = None
HIT_DUCK_POSITION = None
HIT_DUCK_WHITE_RECT = None
HIT_DUCK_RED_RECT = None
SCORE_POSITION = None
SCORE_RECT = None
FONT = settings.FONT_FILE
FONT_STARTING_POSITION = None
FONT_GREEN = settings.COLOR_GREEN
FONT_BLACK = settings.COLOR_BLACK
FONT_WHITE = settings.COLOR_WHITE
ROUND_POSITION = None
SHOT_BG_POSITION = None
SHOT_POSITION = None
SHOT_RECT = None
BULLET_RECT = None
NOTICE_POSITION = None
NOTICE_RECT = None
NOTICE_WIDTH = None
NOTICE_LINE_1_HEIGHT = None
NOTICE_LINE_2_HEIGHT = None

def init():
    global DOG_POSITION, DOG_FRAME, DOG_REPORT_POSITION, DOG_LAUGH_RECT, DOG_ONE_DUCK_RECT, DOG_TWO_DUCKS_RECT
    global HIT_POSITION, HIT_RECT, HIT_DUCK_POSITION, HIT_DUCK_WHITE_RECT, HIT_DUCK_RED_RECT
    global SCORE_POSITION, SCORE_RECT, FONT_STARTING_POSITION, ROUND_POSITION
    global SHOT_BG_POSITION, SHOT_POSITION, SHOT_RECT, BULLET_RECT
    global NOTICE_POSITION, NOTICE_RECT, NOTICE_WIDTH, NOTICE_LINE_1_HEIGHT, NOTICE_LINE_2_HEIGHT

    # Standard World Objects scaling
    DOG_POSITION = adjpos (*settings.DOG_POS)
    DOG_FRAME = adjpos (*settings.DOG_FRAME_SIZE)
    DOG_REPORT_POSITION = adjpos (*settings.DOG_REPORT_POS)
    DOG_LAUGH_RECT = adjrect (*settings.DOG_LAUGH_RECT)
    DOG_ONE_DUCK_RECT = adjrect (*settings.DOG_ONE_DUCK_RECT)
    DOG_TWO_DUCKS_RECT = adjrect (*settings.DOG_TWO_DUCKS_RECT)

    # Rect definitions
    HIT_RECT = adjrect (*settings.HIT_RECT)
    HIT_DUCK_WHITE_RECT = adjrect (*settings.HIT_DUCK_WHITE_RECT)
    HIT_DUCK_RED_RECT = adjrect (*settings.HIT_DUCK_RED_RECT)
    SCORE_RECT = adjrect (*settings.SCORE_RECT)
    SHOT_RECT = adjrect (*settings.SHOT_RECT)
    BULLET_RECT = adjrect (*settings.BULLET_RECT)

    screen_width = adjwidth(settings.ORIG_W)

    # Calculate widths of HUD blocks
    shot_width = adjwidth(70)   # settings.SHOT_RECT width
    hit_width = adjwidth(287)   # settings.HIT_RECT width
    score_width = adjwidth(130) # settings.SCORE_RECT width

    # Calculate spacing to center elements
    total_block_width = shot_width + hit_width + score_width
    available_space = screen_width - total_block_width
    gap = available_space // 4

    # Base Y position (all aligned at bottom)
    base_y = adjheight(settings.HIT_POS[1])

    # 1. Shot Position
    shot_x = gap
    SHOT_POSITION = (shot_x, base_y)
    SHOT_BG_POSITION = (shot_x, base_y)

    # Round Position (relative to Shot, slightly above)
    round_y_offset = adjheight(settings.ROUND_POS[1] - settings.SHOT_POS[1])
    ROUND_POSITION = (shot_x, base_y + round_y_offset)

    # 2. Hit Position
    hit_x = shot_x + shot_width + gap
    HIT_POSITION = (hit_x, base_y)

    # Hit Ducks (relative to Hit bar)
    hit_duck_offset_x = adjwidth(settings.HIT_DUCK_POS[0] - settings.HIT_POS[0])
    hit_duck_offset_y = adjheight(settings.HIT_DUCK_POS[1] - settings.HIT_POS[1])
    HIT_DUCK_POSITION = (hit_x + hit_duck_offset_x, base_y + hit_duck_offset_y)

    # 3. Score Position
    score_x = hit_x + hit_width + gap
    SCORE_POSITION = (score_x, base_y)

    # Score Text
    score_text_offset_x = adjwidth(settings.FONT_START_POS[0] - settings.SCORE_POS[0])
    score_text_offset_y = adjheight(settings.FONT_START_POS[1] - settings.SCORE_POS[1])
    FONT_STARTING_POSITION = (score_x + score_text_offset_x, base_y + score_text_offset_y)

    # Notice Box Centering
    NOTICE_RECT = adjrect (*settings.NOTICE_RECT)
    NOTICE_WIDTH = adjwidth (settings.NOTICE_WIDTH)
    NOTICE_LINE_1_HEIGHT = adjheight (settings.NOTICE_LINE_1_HEIGHT)
    NOTICE_LINE_2_HEIGHT = adjheight (settings.NOTICE_LINE_2_HEIGHT)

    # Center notice box
    notice_x = (screen_width - NOTICE_WIDTH) // 2
    notice_y = adjheight(settings.NOTICE_POS[1])
    NOTICE_POSITION = (notice_x, notice_y)

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
        line1 = font.render(str(self.notices[0]), True, (255, 255, 255))
        line2 = font.render(str(self.notices[1]), True, (255, 255, 255))
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
        text = font.render(("R= %d" % round), True, FONT_GREEN, FONT_BLACK)
        surface.blit(text, ROUND_POSITION)

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
        text = font.render(str(self.registry.get('score')), True, FONT_WHITE)
        x, y = FONT_STARTING_POSITION
        x -= text.get_width()
        surface.blit(text, (x,y))

class StartState(BaseState):
    def __init__(self, reg):
        super(StartState, self).__init__() # Add super init call
        global registry
        registry = reg

    def start(self):
        return RoundStartState()

class RoundStartState(BaseState):
    def __init__(self):
        super(RoundStartState, self).__init__()
        self.frame = 1
        self.animationFrame = 0
        self.animationDelay = 10
        self.dogPosition = DOG_POSITION
        self.barkCount = 0

    def execute(self, event):
        pass

    def update(self):
        timer = int(time.time())

        if (timer - self.timer) > 2:
            self.showNotice = False
            return PlayState()

        self.notices = ("ROUND", self.registry.get('round'))
        self.frame += 1

    def render(self):
        timer = int(time.time())
        surface = self.registry.get('surface')
        sprites = self.registry.get('sprites')
        x, y = self.dogPosition
        width, height = DOG_FRAME

        self.renderNotices()
        self.renderControls()

        if (self.frame % 15) == 0:
            self.animationFrame += 1

        if self.animationFrame < 5:
            x += 1
            self.dogPosition = (x, y)
            rect = ((width * self.animationFrame), 0, width, height)

        else:
            self.animationDelay = 16
            animationFrame = self.animationFrame % 5
            rect = ((width * animationFrame), height, width, height)

            if (self.barkCount < 2) and not pygame.mixer.get_busy():
                self.registry.get('soundHandler').enqueue('bark')
                self.barkCount += 1

            if (animationFrame == 1):
                self.dogPosition = (x + adjwidth (5)), (y - adjheight (10))

            elif (animationFrame == 2):
                self.dogPosition = (x + adjwidth (5)), (y + adjheight (5))

            elif (animationFrame > 2):
                return 

        surface.blit(sprites, self.dogPosition, rect)

class PlayState(BaseState):
    def __init__(self):
        super(PlayState, self).__init__()
        self.ducks = [Duck(self.registry), Duck(self.registry)]
        self.roundTime = 10 
        self.frame = 0
        self.dogCanComeOut = False
        self.dogPosition = DOG_REPORT_POSITION
        self.dogdy = 5
        self.dogRectToDraw = None 

    def execute(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.gun.moveCrossHairs(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            hasFired = self.gun.shoot()
            for duck in self.ducks:
                if hasFired and duck.isShot(event.pos):
                    self.registry.set('score', self.registry.get('score') + 10)
                    self.hitDucks[self.hitDuckIndex] = True
                    self.hitDuckIndex += 1
                elif not duck.isDead and self.gun.rounds <= 0:
                     duck.flyOff = True

    def update(self):
        timer = int(time.time())

        if self.dogCanComeOut:
            self.frame += 3
            ducksShot = 0
            for duck in self.ducks:
                if duck.isDead:
                    ducksShot += 1

            rectSource = None
            if ducksShot == 1:
                rectSource = DOG_ONE_DUCK_RECT
                if self.frame == 3:
                    self.registry.get('soundHandler').enqueue('hit')
            elif ducksShot == 2:
                rectSource = DOG_TWO_DUCKS_RECT
                if self.frame == 3:
                    self.registry.get('soundHandler').enqueue('hit')
            else:
                rectSource = DOG_LAUGH_RECT
                if self.frame == 3:
                    self.registry.get('soundHandler').enqueue('flyaway')

            x1, y1 = self.dogPosition
            x_src, y_src, w_src, h_max = rectSource

            current_visible_height = h_max

            if self.frame < h_max:
                self.dogPosition = x1, (y1 - 3)
                current_visible_height = self.frame
            else:
                self.dogPosition = x1, (y1 + 3)
                current_visible_height -= (self.frame - h_max)

            if current_visible_height <= 0:
                self.dogPosition = DOG_REPORT_POSITION
                self.frame = 0
                self.dogCanComeOut = False
                self.ducks = [Duck(self.registry), Duck(self.registry)]
                self.timer = timer
                self.gun.reloadIt()
                self.dogRectToDraw = None
            else:
                self.dogRectToDraw = (x_src, y_src, w_src, current_visible_height)
            
            return 

        for duck in self.ducks:
            duck.update()

        timesUp = (timer - self.timer) > self.roundTime
        if not (timesUp or (self.ducks[0].isFinished and self.ducks[1].isFinished)):
            return None

        for duck in self.ducks:
            if not duck.isFinished and not duck.isDead:
                duck.flyOff = True
                return None

        for duck in self.ducks:
            if not duck.isDead:
                self.hitDuckIndex += 1

        if self.hitDuckIndex >= 9:
            return RoundEndState(self.hitDucks)

        self.dogCanComeOut = True

    def render(self):
        timer = int(time.time())
        surface = self.registry.get('surface')
        sprites = self.registry.get('sprites')

        self.renderControls()

        for duck in self.ducks:
            duck.render()

        if self.dogCanComeOut and self.dogRectToDraw:
            surface.blit(sprites, self.dogPosition, self.dogRectToDraw)

        self.gun.render()

class RoundEndState(BaseState):
    def __init__(self, hitDucks):
        super(RoundEndState, self).__init__()
        self.isGameOver = False
        self.hitDucks = hitDucks

        missedCount = 0
        for i in self.hitDucks:
            if i == False:
                missedCount += 1
        if missedCount >= 4:
            self.isGameOver = True
            self.notices = ("GAMEOVER", "")
            self.registry.get('soundHandler').enqueue('gameover')
        else:
            self.registry.get('soundHandler').enqueue('nextround')

    def execute(self, event):
        pass

    def update(self):
        if pygame.mixer.get_busy():
            return None 

        if self.isGameOver:
            return GameOverState()
        else:
            self.registry.set('round', self.registry.get('round') + 1)
            return RoundStartState()

    def render(self):
        self.renderNotices()
        self.renderControls()

class GameOverState(BaseState):
    def __init__(self):
        super(GameOverState, self).__init__()
        self.state = None

    def execute(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.registry.set('score', 0)
            self.registry.set('round', 1)
            self.state = RoundStartState()

    def update(self):
        self.notices = ("GAMEOVER", "")
        if self.state:
            return self.state

    def render(self):
        self.renderNotices()
        self.renderControls()