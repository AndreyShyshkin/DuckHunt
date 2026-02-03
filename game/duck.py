import  random
from .registry import adjpos, adjheight

FRAME_SIZE = adjpos (81, 75)
XOFFSET, YOFFSET = adjpos (250, 225)

class Duck(object):

    def __init__(self, registry):
        self.registry = registry
        self.sprites = registry.get('sprites')
        self.rsprites = registry.get('rsprites')
        
        self.imageReversed = False
        self.animationDelay = 8
        self.frame = 0
        self.animationFrame = 0

       
        surface = registry.get('surface')
        x = random.choice([0, surface.get_width()])
        y = random.randint(0, surface.get_height() // 2)
        self.position = x, y
        
        
        self.dx, self.dy = adjpos(3, 0)

    def update(self):
        self.frame = (self.frame + 1) % self.animationDelay
        x, y = self.position
        
        
        new_x = x + self.dx
        new_y = y + self.dy
        
        

    def render(self):
        surface = self.registry.get('surface')
        width, height = FRAME_SIZE
        
       
        rect = XOFFSET, YOFFSET, width, height
        surface.blit(self.sprites, self.position, rect)