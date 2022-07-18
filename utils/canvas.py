import cv2
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

    def to_cv2_image(self):
        # https://stackoverflow.com/questions/53101698/how-to-convert-a-pygame-image-to-open-cv-image
        #  create a copy of the surface
        view = pygame.surfarray.array3d(self.surface)
        #  convert from (width, height, channel) to (height, width, channel)
        view = view.transpose([1, 0, 2])
        #  convert from rgb to bgr
        mask = cv2.cvtColor(view, cv2.COLOR_RGB2GRAY)
        mask[mask > 0] = 255
        return mask

    def set_by_numpy(self, img):
        h, w = img.shape[:2]
        self.surface = pygame.image.frombuffer(img.flatten(), (w, h), "RGB")
        self.surface.set_colorkey((0,0,0))
        self.surface.set_alpha(128)