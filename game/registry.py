from .settings import ORIG_W, ORIG_H

RENDER_W, RENDER_H = ORIG_W, ORIG_H

def init_screen_params(width, height):
    global RENDER_W, RENDER_H
    RENDER_W = width
    RENDER_H = height

def adjwidth (x):
    return (RENDER_W * x) // ORIG_W

def adjheight (y):
    return (RENDER_H * y) // ORIG_H

def adjpos (x, y):
    return (adjwidth (x), adjheight (y))

def adjrect (a, b, c, d):
    return (adjwidth (a), adjheight (b), adjwidth (c), adjheight (d))

class Registry(object):
    def __init__(self):
        self.registry = {}

    def set(self, key, value):
        self.registry[key] = value
        return self

    def get(self, key):
        if key in self.registry:
            return self.registry[key]
        return None
