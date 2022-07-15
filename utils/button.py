from typing import Text
from .object import Object
from .settings import *

class Button(Object):
    def __init__(self, win, x, y, width, height, color, toggle_func=None, text=None, text_color=BLACK):
        super(Button, self).__init__(win, x, y, width, height)
        self.color = color
        self.text = text
        self.text_color = text_color
        self.toggle_func = toggle_func

    def update(self):
        super().draw(self.color)
        if self.text:
            pygame.draw.rect(
                self.win, BLACK, ( self.x ,self.y, self.width, self.height),2)
            button_font = get_font(16)
            text_surface = button_font.render(self.text, 1, self.text_color)
            self.win.blit(text_surface, (
                self.x + self.width / 2 - text_surface.get_width() / 2,
                self.y + self.height / 2 - text_surface.get_height()/2))
            
    def toggle(self):
        if self.toggle_func:
            self.toggle_func()