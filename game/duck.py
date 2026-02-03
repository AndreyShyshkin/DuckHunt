import  random
from .registry import adjpos, adjheight

FRAME_SIZE = adjpos (81, 75)
XOFFSET, YOFFSET = adjpos (250, 225)
FLYOFF_YOFFSET = YOFFSET + adjheight (155)

class Duck(object):

    def __init__(self, registry):
        self.registry = registry
        self.imageReversed = False
        self.isDead = False
        self.flyOff = False
        self.sprites = registry.get('sprites')
        self.rsprites = registry.get('rsprites')

        # Animation
        self.animationDelay = 8
        self.frame = 0
        self.animationFrame = 0
        
        # Find a starting position
        surface = registry.get('surface')
        x = random.choice([0, surface.get_width()])
        y = random.randint(0, surface.get_height() // 2)
        self.position = x, y
        
        # Simple start direction
        self.dx, self.dy = adjpos(3, 1)

    def update(self):
        surface = self.registry.get('surface')
        self.frame = (self.frame + 1) % self.animationDelay
        x, y = self.position

        
        self.position = (x + self.dx), (y + self.dy)
        
        
        if x > surface.get_width() or x < 0:
            self.dx = -self.dx
            self.imageReversed = not self.imageReversed
            
    def render(self):
        surface = self.registry.get('surface')
        width, height = FRAME_SIZE
        x, y = self.position

        
        if self.frame == 0:
            self.animationFrame += 1
        animationFrame = 1 if (self.animationFrame % 4 == 3) else (self.animationFrame % 4)

        # Animate flying
        xOffset = XOFFSET
        rect = ((width * animationFrame) + xOffset), YOFFSET, width, height
        surface.blit(self.rsprites if self.imageReversed else self.sprites, self.position, rect)