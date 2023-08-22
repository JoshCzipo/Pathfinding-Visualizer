from settings import *

class Button(object):
    def __init__(self, win, color, x, y, width, height, text, callback, text2):
        self.win = win
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.text2 = text2
        self.callback = callback
        self.clicked = False


    def click(self):
        self.callback()

    def draw(self, outline=None, fontSize=buttonSize):
        if outline:
            pygame.draw.rect(self.win, outline, (self.x-2, self.y-2, self.width+4, self.height+4), 0)
        pygame.draw.rect(self.win, self.color, (self.x, self.y, self.width, self.height), 0)
        
        if self.text != '':
            font = pygame.font.SysFont(buttonFont, fontSize)
            text = font.render(self.text, 1, (255, 255, 255))
            text2 = font.render(self.text2, 1, TURQOUISE)
            text_x = self.x + (self.width / 2 - text.get_width() / 2)
            text_y = self.y + (self.height / 2 - text.get_height() / 2)
            self.win.blit(text, (text_x, text_y))
            if self.text2:
                self.win.blit(text2, (text_x, text_y + 20))


    def contains(self, pos):
        pos_x, pos_y = pos
        return self.x < pos_x < self.x + self.width and self.y < pos_y < self.y + self.height

class MenuButton(Button):

    def __init__(self, win, pos, text, callback, text2=None):

        self.yAdjust = 0

        if pos > 3:
            pos -= 4
            self.yAdjust = 65
        
        Button.__init__(self, win, BLACK, pos * 202 + 10, 810 + self.yAdjust, 185, 50, text, callback, text2)

    def highlight(self, highlight):
        self.color = GREY if highlight else BLACK

class SideButton(Button):

    def __init__(self, win, pos, text, callback, display=False, text2=None):
        height = 50
        width = 150
        color = BLACK

        if display:
            height = 100

        Button.__init__(self, win, color, 825, pos * 70 + 10, width, height, text, callback, text2)

    def highlight(self, highlight):
        self.color = GREY if highlight else BLACK

class ExitButton(Button):

    def __init__(self, win, text, callback, text2=None):
        
        Button.__init__(self, win, RED, 50, 50, 50, 50, text, callback, text2)

    def highlight(self, highlight):
        self.color = GREY if highlight else BLACK


