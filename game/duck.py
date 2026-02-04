import  random
from .registry import adjpos, adjheight
from . import settings

FRAME_SIZE = None
XOFFSET, YOFFSET = None, None
FLYOFF_YOFFSET = None
FALL_YOFFSET = None

def init():
    global FRAME_SIZE, XOFFSET, YOFFSET, FLYOFF_YOFFSET, FALL_YOFFSET
    FRAME_SIZE = adjpos (settings.DUCK_FRAME_W, settings.DUCK_FRAME_H)
    XOFFSET, YOFFSET = adjpos (settings.DUCK_X_OFFSET, settings.DUCK_Y_OFFSET)
    FLYOFF_YOFFSET = YOFFSET + adjheight (settings.DUCK_FLYOFF_Y_OFFSET)
    FALL_YOFFSET = YOFFSET + adjheight (settings.DUCK_FALL_Y_OFFSET)

class Duck(object):

    def __init__(self, registry):
        self.registry = registry
        self.imageReversed = False
        self.isDead = False
        self.isFinished = False
        self.flyOff = False
        self.sprites = registry.get('sprites')
        self.rsprites = registry.get('rsprites')

        # Animation
        self.animationDelay = settings.DUCK_ANIMATION_DELAY
        self.frame = 0
        self.animationFrame = 0
        self.justShot = False

        # Find a starting position
        surface = registry.get('surface')
        x = random.choice([0, surface.get_width()])
        y = random.randint(0, surface.get_height() // 2)
        self.position = x, y

        
        self.changeDirection()

    def update(self):
        surface = self.registry.get('surface')
        self.frame = (self.frame + 1) % self.animationDelay
        x, y = self.position

        # Update position
        self.position = (x + self.dx), (y + self.dy)
        if not self.isDead or not self.isFinished:
            self.changeDirection()

        frameWidth, frameHeight = FRAME_SIZE
        pastLeft = (x + frameWidth) < 0
        pastTop = (y + frameHeight) < 0
        pastRight = x > surface.get_width()
        if self.flyOff and (pastLeft or pastTop or pastRight):
            self.isFinished = True

    def render(self):
        surface = self.registry.get('surface')
        width, height = FRAME_SIZE
        x, y = self.position

        
        if self.isFinished:
            return

        # Set offsets
        xOffset = XOFFSET
        yOffset = FLYOFF_YOFFSET if self.flyOff else YOFFSET

        # Only update animation on key frames
        if self.frame == 0:
            self.animationFrame += 1
        animationFrame = 1 if (self.animationFrame % 4 == 3) else (self.animationFrame % 4)

        # Animate flying
        if not self.isDead:
            rect = ((width * animationFrame) + xOffset), yOffset, width, height
            surface.blit(self.rsprites if self.imageReversed else self.sprites, self.position, rect)

        # Animate the duck drop
        else:
            # First frame is special
            if self.justShot:
                if self.frame == 0:
                    self.justShot = False
                y -= self.dy
                self.position = (x, y)
                rect = XOFFSET, FALL_YOFFSET, width, height
                return surface.blit(self.sprites, self.position, rect)

            # Animate falling
            if y < (surface.get_height() // 2):
                rect = (XOFFSET + width), FALL_YOFFSET, width, height
                return surface.blit(self.sprites, self.position, rect)
            else:
                self.isFinished = True
                self.registry.get('soundHandler').enqueue('drop')

    def isShot(self, pos):
        x1, y1 = self.position
        x2, y2 = pos
        frameX, frameY = FRAME_SIZE

        # If the duck is already dead or flying off, they can't be shot
        if self.flyOff or self.isDead:
            return False

        # If shot was outside the duck image
        if x2 < x1 or x2 > (x1 + frameX):
            return False
        if y2 < y1 or y2 > (y1 + frameY):
            return False

        # Prepare for the fall
        self.isDead = True
        self.justShot = True
        self.frame = 1
        self.dx, self.dy = adjpos (0, 4)
        return True

    # Helper method to avoid code duplication
    def _get_random_velocity(self, speed_range, x_dir_mult, min_y, max_y):
        while True:
            dx = random.choice(speed_range) * x_dir_mult
            dy = random.randint(min_y, max_y)
            dx, dy = adjpos(dx, dy)
            # Ensure we have movement, prefer X movement check
            if dy != 0: 
                # Additional check to ensure we don't get stuck with 0 dx if that logic existed
                if dx != 0:
                    return dx, dy

    def changeDirection(self):
        surface = self.registry.get('surface')
        round = self.registry.get('round')
        frameWidth, frameHeight = FRAME_SIZE

        # Calculate speed range
        min_speed = settings.DUCK_SPEED_MIN + round
        max_speed = settings.DUCK_SPEED_MAX + round
        speedRange = range(min_speed, max_speed)

        x, y = self.position
        coinToss = 1 if random.randint(0, 1) else -1

        # Only update on key frames
        if not self.frame == 0:
            return

        # Set flyoff
        if self.flyOff:
            self.dx, self.dy = adjpos (0, -4)
            return

        # Die!
        if self.isDead:
            self.dx, self.dy = adjpos (0, 4)
            return

        
        
        # At the left side of the screen
        if x <= 0:
            self.dx, self.dy = self._get_random_velocity(speedRange, 1, -4, 4)

        # At the right side of the screen
        elif (x + frameWidth) > surface.get_width():
            self.dx, self.dy = self._get_random_velocity(speedRange, -1, -4, 4)

        # At the top of the screen
        elif y <= 0:
             self.dx, self.dy = self._get_random_velocity(speedRange, coinToss, 2, 4)

        # At the bottom of the screen
        elif y > (surface.get_height() // 2):
             self.dx, self.dy = self._get_random_velocity(speedRange, coinToss, -4, -2)

        # Reverse image if duck is flying opposite direction
        if self.dx < 0 and not self.imageReversed:
            self.imageReversed = True
        elif self.dx > 0 and self.imageReversed:
            self.imageReversed = False