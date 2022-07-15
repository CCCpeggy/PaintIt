from .object import Object
from .settings import BG_COLOR, pygame

class Canvas(Object):
    def __init__(self, win, x, y, width, height):
        super(Canvas, self).__init__(win, x, y, width, height)
        self.last_pos = None
        self.is_draw = False

    def update(self):
        if not self.is_draw:
            self.last_pos = None
        self.is_draw = False
        
    def brush(self, x, y, color, width):
        if self.last_pos:
            pygame.draw.line(self.win, color, self.last_pos, (x, y), int(width * 1.1))
        pygame.draw.circle(self.win, color, (x, y), width / 2)
        self.last_pos = x, y
        self.is_draw = True
    
    def clear(self):
        self.win.fill((BG_COLOR))

    