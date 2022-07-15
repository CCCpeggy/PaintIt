import pygame
pygame.init()
pygame.font.init()

WHITE = (225, 225, 225)
BLACK = (0, 0, 0)
RED = (225, 0, 0)
GREEN = (0, 225, 0)
BLUE = (0, 0, 225)

FPS = 120

WIDTH, HEIGHT = 600, 700

BUTTON_GAP = 10
BUTTON_SIZE = 50
TOOLBAR_HEIGHT = BUTTON_SIZE + BUTTON_GAP * 2

BRUSH_WIDTH = 20

BG_COLOR = WHITE

DRAW_GRID_LINES = False

def get_font(size):
    return pygame.font.SysFont("comicsans",size)