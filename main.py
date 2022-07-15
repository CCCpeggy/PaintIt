from utils.settings import *
from utils.canvas import Canvas
from utils.button import Button

class PaintAPP:
    def __init__(self):
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Paint It")
        self.init_gui()

        self.clock = pygame.time.Clock()
        self.drawing_color = BLACK
        
        while self.run():
            self.clock.tick(FPS)
        pygame.quit()
            
    def init_gui(self):
        # init canvas
        self.canvas = Canvas(self.window, 0, 0, WIDTH, (HEIGHT - TOOLBAR_HEIGHT))
        self.canvas.clear();
        
        # init button
        button_size = 50
        button_gap = 60
        button_y = HEIGHT - button_gap
        self.buttons = [
            Button(self.window, 10 + button_gap * 0, button_y, button_size, button_size, BLACK),
            Button(self.window, 10 + button_gap * 1, button_y, button_size, button_size, RED),
            Button(self.window, 10 + button_gap * 2, button_y, button_size, button_size, GREEN),
            Button(self.window, 10 + button_gap * 3, button_y, button_size, button_size, BLUE),
            Button(self.window, 10 + button_gap * 4, button_y, button_size, button_size, WHITE, "Erase", BLACK),
            Button(self.window, 10 + button_gap * 5, button_y, button_size, button_size, WHITE , "Clear", BLACK)
        ]
        self.update_gui()
            
    def update_gui(self):
        for button in self.buttons:
            button.draw()
        
    def run(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                if self.canvas.clicked(pos):
                    self.canvas.brush(pos[0], pos[1], self.drawing_color, BRUSH_WIDTH)
                    break
                for button in self.buttons:
                    if button.clicked(pos):
                        self.drawing_color = button.color
                        if button.text == "Clear":
                            self.canvas.clear();
                        break
        self.update_gui()
        pygame.display.update()
        return True


if __name__ == "__main__":
    app = PaintAPP()