from .settings import pygame

class Object:
    def __init__(self, win: pygame.Surface, x: int, y, width: int, height: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.win = win

    def clicked(self, pos):
        x, y = pos
        if not (x >= self.x and x <= self.x + self.width):
            return False
        if not (y >= self.y and y <= self.y + self.height):
            return False
        
        return True