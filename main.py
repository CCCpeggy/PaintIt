from utils.settings import *
from utils.canvas import Canvas
from utils.button import *

class PaintAPP:
    def __init__(self):
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Paint It")
        self.init_gui()

        self.clock = pygame.time.Clock()
        self.drawing_color = BLACK
        self.is_last_left_pressed = False
        
        while self.run():
            self.clock.tick(FPS)
        pygame.quit()
        
    def set_rawing_color(self, color):
        self.drawing_color = color
            
    def init_gui(self):
        # init canvas
        self.canvas = Canvas(self.window, 0, 0, WIDTH, (HEIGHT - TOOLBAR_HEIGHT))
        self.canvas.clear();
        
        # init button
        button_y = HEIGHT - BUTTON_SIZE - BUTTON_GAP
        self.buttons = [
            Button(self.window, 10 + (BUTTON_SIZE + BUTTON_GAP) * 0, button_y, BUTTON_SIZE, BUTTON_SIZE, BLACK, lambda: self.set_rawing_color(BLACK)),
            Button(self.window, 10 + (BUTTON_SIZE + BUTTON_GAP) * 1, button_y, BUTTON_SIZE, BUTTON_SIZE, RED, lambda: self.set_rawing_color(RED)),
            Button(self.window, 10 + (BUTTON_SIZE + BUTTON_GAP) * 2, button_y, BUTTON_SIZE, BUTTON_SIZE, GREEN, lambda: self.set_rawing_color(GREEN)),
            Button(self.window, 10 + (BUTTON_SIZE + BUTTON_GAP) * 3, button_y, BUTTON_SIZE, BUTTON_SIZE, BLUE, lambda: self.set_rawing_color(BLUE)),
            Button(self.window, 10 + (BUTTON_SIZE + BUTTON_GAP) * 4, button_y, BUTTON_SIZE, BUTTON_SIZE, WHITE, lambda: self.set_rawing_color(BG_COLOR), "Erase", BLACK),
            Button(self.window, 10 + (BUTTON_SIZE + BUTTON_GAP) * 5, button_y, BUTTON_SIZE, BUTTON_SIZE, WHITE, lambda: self.canvas.clear(), "Clear", BLACK)
        ]
        self.update_gui()
            
    def update_gui(self):
        self.canvas.update()
        for button in self.buttons:
            button.update()
        
    def run(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            # click
            if not self.is_last_left_pressed:
                for button in self.buttons:
                    if button.clicked(pos):
                        button.toggle()
                        break
            # press
            if self.canvas.clicked(pos):
                self.canvas.brush(pos[0], pos[1], self.drawing_color, BRUSH_WIDTH)
            
            self.is_last_left_pressed = True
        else:
            self.is_last_left_pressed = False
        self.update_gui()
        pygame.display.update()
        return True


if __name__ == "__main__":
    app = PaintAPP()