from .object import Object
from .settings import BG_COLOR, pygame

class Canvas(Object):
    def __init__(self, win, x, y, width, height):
        super(Canvas, self).__init__(win, x, y, width, height)

    def brush(self, x, y, color, radius):
        pygame.draw.circle(self.win, color, (x, y), radius)

    def clear(self):
        self.win.fill((BG_COLOR))

    def draw(self):
        pygame.draw.rect(
            self.win, (128, 128, 128), (self.x ,self.y, self.width, self.height))
