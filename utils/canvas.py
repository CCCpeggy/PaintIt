from .object import Object
from .settings import BLACK, pygame

class Canvas(Object):
    def __init__(self, win, x, y, width, height, surface_width, surface_height):
        super(Canvas, self).__init__(win, x, y, width, height)
        self.surface = pygame.Surface((surface_width, surface_height))
        self.surface.set_colorkey((0,0,0))
        self.surface.set_alpha(128)
        self.surface_width = surface_width
        self.surface_height = surface_height
        self.last_pos = None
        self.is_draw = False

    def update(self):
        if not self.is_draw:
            self.last_pos = None
        self.is_draw = False
        tmp_surface = pygame.transform.scale(self.surface, (self.width, self.height))
        self.win.blit(tmp_surface, (0, 0))
        
    def brush(self, x, y, color, width):
        x = x * self.surface_width  // self.width
        y = y * self.surface_height // self.height
        if self.last_pos:
            pygame.draw.line(self.surface, color, self.last_pos, (x, y), int(width * 1.1))
        pygame.draw.circle(self.surface, color, (x, y), width / 2)
        self.last_pos = x, y
        self.is_draw = True
    
    def clear(self):
        self.surface.fill(BLACK)

    