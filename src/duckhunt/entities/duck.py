"""
Модуль, що описує поведінку качки в грі.
Містить логіку руху, анімації, відскоку від стін та реакції на влучання.
"""

import random
from duckhunt.utils.registry import adjpos, adjheight
from duckhunt.core import settings

FRAME_SIZE = None
XOFFSET, YOFFSET = None, None
FLYOFF_YOFFSET = None
FALL_YOFFSET = None

def init():
    """Ініціалізує глобальні константи розмірів та зсувів для спрайтів качки відповідно до розміру екрану."""

    global FRAME_SIZE, XOFFSET, YOFFSET, FLYOFF_YOFFSET, FALL_YOFFSET
    FRAME_SIZE = adjpos(settings.DUCK_FRAME_W, settings.DUCK_FRAME_H)
    XOFFSET, YOFFSET = adjpos(settings.DUCK_X_OFFSET, settings.DUCK_Y_OFFSET)
    FLYOFF_YOFFSET = YOFFSET + adjheight(settings.DUCK_FLYOFF_Y_OFFSET)
    FALL_YOFFSET = YOFFSET + adjheight(settings.DUCK_FALL_Y_OFFSET)

class Duck(object):
    """
    Клас, що представляє ігрову сутність качки.
    Керує її координатами, станом (жива/мертва/відлітає) та анімацією.
    """

    def __init__(self, registry):
        """Ініціалізує качку, задає початкові випадкові координати та параметри анімації."""

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

        self.dx = 0
        self.dy = 0

        surface = registry.get('surface')
        x = random.choice([0, surface.get_width()])
        y = random.randint(0, surface.get_height() // 2)
        self.position = x, y

        self.changeDirection()

    def update(self, dt):
        """Оновлює стан качки (координати, таймери анімації, перевірка вильоту за екран) кожен кадр."""

        surface = self.registry.get('surface')

        self.frame = (self.frame + 1) % self.animationDelay
        if self.frame == 0:
            self.animationFrame += 1

        x, y = self.position

        if not self.isDead:
            self.position = (x + self.dx), (y + self.dy)
            if not self.isFinished:
                self.changeDirection()
        else:
            if self.justShot:
                if self.frame == 0:
                    self.justShot = False

                y -= self.dy
                self.position = (x, y)

            elif y < (surface.get_height() // 2):
                self.position = (x + self.dx), (y + self.dy)
            else:
                self.isFinished = True
                self.registry.get('soundHandler').enqueue('drop')

        frameWidth, frameHeight = FRAME_SIZE
        x, y = self.position
        pastLeft = (x + frameWidth) < 0
        pastTop = (y + frameHeight) < 0
        pastRight = x > surface.get_width()

        if self.flyOff and (pastLeft or pastTop or pastRight):
            self.isFinished = True

    def render(self):
        """Відмальовує спрайт качки на екрані залежно від її поточного стану (політ або падіння)."""

        surface = self.registry.get('surface')
        width, height = FRAME_SIZE
        x, y = self.position

        if self.isFinished:
            return

        # Set offsets
        xOffset = XOFFSET
        yOffset = FLYOFF_YOFFSET if self.flyOff else YOFFSET

        animationFrameIdx = 1 if (self.animationFrame % 4 == 3) else (self.animationFrame % 4)

        # Animate flying
        if not self.isDead:
            rect = ((width * animationFrameIdx) + xOffset), yOffset, width, height
            surface.blit(self.rsprites if self.imageReversed else self.sprites, self.position, rect)

        # Animate the duck drop
        else:
            # First frame is special
            if self.justShot:
                rect = XOFFSET, FALL_YOFFSET, width, height
                return surface.blit(self.sprites, self.position, rect)

            # Animate falling
            if y < (surface.get_height() // 2):
                rect = (XOFFSET + width), FALL_YOFFSET, width, height
                return surface.blit(self.sprites, self.position, rect)
            else:
                pass

    def isShot(self, pos):
        """
        Перевіряє, чи потрапив постріл у площу (hitbox) качки.
        Повертає True, якщо влучання успішне, і змінює стан качки на 'мертва'.
        """

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
        self.dx, self.dy = adjpos(0, 4)
        return True

    # Helper method to avoid code duplication
    def _get_random_velocity(self, speed_range, x_dir_mult, min_y, max_y):
        """Допоміжний метод для генерації випадкового вектора швидкості (dx, dy), уникаючи нульових значень."""

        while True:
            dx = random.choice(speed_range) * x_dir_mult
            dy = random.randint(min_y, max_y)
            dx, dy = adjpos(dx, dy)
            if dy != 0 and dx != 0:
                return dx, dy

    def changeDirection(self):
        """Змінює напрямок руху качки та її швидкість при зіткненні з краями екрану."""
        
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
            self.dx, self.dy = adjpos(0, -4)
            return

        # Die!
        if self.isDead:
            self.dx, self.dy = adjpos(0, 4)
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