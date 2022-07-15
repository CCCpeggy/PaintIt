from .object import Object
from .settings import BG_COLOR, pygame

class Canvas(Object):
    def __init__(self, win, x, y, width, height):
        super(Canvas, self).__init__(win, x, y, width, height)
        self.last_pos = None
        self.is_update = False
        
    def update(self):
        if self.is_update:
            self.last_pos = None
        self.is_update = True

    def brush(self, x, y, color, width):
        if self.last_pos:
            pygame.draw.line(self.win, color, self.last_pos, (x, y), width)
        pygame.draw.circle(self.win, color, (x, y), width / 2)
        self.last_pos = x, y
        self.is_update = False
    
    def clear(self):
        self.win.fill((BG_COLOR))

    