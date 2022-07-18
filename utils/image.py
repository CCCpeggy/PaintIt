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
        scale = min(self.width / self.img_width, self.height / self.img_height)
        self.width, self.height = int(self.img_width * scale), int(self.img_height * scale)

    def update(self):
        tmp_img = pygame.transform.scale(self.img, (self.width, self.height))
        self.win.blit(tmp_img, (self.x, self.y))
