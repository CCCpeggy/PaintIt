import pygame
pygame.init()
pygame.font.init()

WHITE = (225, 225, 225)
BLACK = (0, 0, 0)
RED = (225, 0, 0)
GREEN = (0, 225, 0)
BLUE = (0, 0, 225)

FPS = 60

WIDTH, HEIGHT = 700, 700

TOOLBAR_HEIGHT = HEIGHT - WIDTH

BRUSH_WIDTH = 10

BG_COLOR = WHITE

DRAW_GRID_LINES = False

def get_font(size):
    return pygame.font.SysFont("comicsans",size)