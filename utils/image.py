from .object import Object
from .settings import BG_COLOR, pygame

class Image(Object):
    def __init__(self, win, x, y, width, height, image_path):
        super(Image, self).__init__(win, x, y, width, height)
        # load image
        img = pygame.image.load(image_path)
        self.img = img
        self.img_width = img.get_width()
        self.img_height = img.get_height()

    def update(self):
        tmp_img = pygame.transform.scale(self.img, (self.width, self.height))
        self.win.blit(tmp_img, (self.x, self.y))
