from settings import *

class Spot:

    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows
        self.weight = 1
        self.visited = False
        self.barrier = False

    def get_pos(self):
        return self.row, self.col
    
    def is_empty(self):
        return self.color == WHITE

    def is_closed(self):
        return self.color == TURQOUISE or self.color == LIGHTGREEN
    
    def is_open(self):
        return self.color == BLUE or self.color == GREEN
    
    def is_barrier(self):
        return self.barrier
    
    def is_start(self):
        return self.color == ORANGE
    
    def is_end(self):
        return self.color == RED
    
    def is_weight(self):
        return self.color == PURPLE
    
    def is_path(self):
        return self.color == YELLOW

    def reset(self):
        self.barrier = False
        self.color = WHITE

    def make_open(self, green=False):
        if green:
            self.color = GREEN
        else:
            self.color = BLUE

    def make_closed(self, green=False):
        if green:
            self.color = LIGHTGREEN
        else:
            self.color = TURQOUISE
    
    def make_barrier(self):
        self.barrier = True
        self.color = BLACK

    def make_start(self):
        self.color = ORANGE
    
    def make_end(self):
        self.color = RED
    
    def make_path(self):
        self.color = YELLOW

    def add_weight(self):
        if self.weight < 9:
            self.weight += 1

    def remove_weight(self):
        self.weight = 1

    def draw(self, win, textfont):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))
        
        textTBD = textfont.render(str(self.weight), True, BLACK)
        
        if self.weight > 1:
            win.blit(textTBD, (self.x, self.y))
        elif self.is_start():
            win.blit(textfont.render('1', True, WHITE), (self.x, self.y))
        elif self.is_end():
            win.blit(textfont.render('2', True, WHITE), (self.x, self.y))


    def update_neighbors(self, grid, dist):
        self.neighbors = []

        if self.row < self.total_rows - dist and not grid[self.row + dist][self.col].barrier: #Check if it can move DOWN (dist) blocks away
            self.neighbors.append(grid[self.row + dist][self.col])

        if self.row > (dist - 1) and not grid[self.row - dist][self.col].barrier: #Check if it can move UP (dist) blocks away
            self.neighbors.append(grid[self.row - dist][self.col])

        if self.col < self.total_rows - dist and not grid[self.row][self.col + dist].barrier: #Check if it can move RIGHT (dist) blocks away
            self.neighbors.append(grid[self.row][self.col + dist])

        if self.col > (dist - 1) and not grid[self.row][self.col - dist].barrier: #Check if it can move LEFT (dist) blocks away
            self.neighbors.append(grid[self.row][self.col - dist])

    def isBorder(self):
        if self.row == 0 or self.col == 0 or self.row == self.total_rows - 1 or self.col == self.total_rows - 1:
            return True
        return False


    def __lt__(self, other):
        return False