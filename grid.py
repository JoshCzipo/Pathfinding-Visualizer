from spotclass import Spot
from settings import *
import random

class Grid():

    def __init__(self, rows, width, win):
        self.grid = []
        self.gap = width // rows
        self.rows = rows
        self.width = width
        self.win = win
        self.textfont = pygame.font.SysFont("monospace", 18)
        self.textfont.set_bold(True)

        for i in range(rows):
            self.grid.append([])
            for j in range(rows):
                spot = Spot(i, j, self.gap, rows)
                if spot.isBorder():
                    spot.make_barrier()
                self.grid[i].append(spot)

    def draw_grid(self):

        for i in range(self.rows):
            pygame.draw.line(self.win, BLACK, (0, i * self.gap), (self.width, i * self.gap))

            for j in range(self.rows):
                pygame.draw.line(self.win, BLACK, (j * self.gap, 0), (j * self.gap, self.width))
    
    def clear_board(self):
    
        for row in self.grid:
            for spot in row:
                if not spot.isBorder():
                    spot.remove_weight()
                    spot.visited = False
                    spot.reset()

    def clear_path(self):

        for row in self.grid:
            for spot in row:
                if not spot.isBorder():
                    spot.visited = False
                    if spot.is_open() or spot.is_closed() or spot.is_path():
                        spot.reset()

    def random_barriers(self):

        for row in self.grid:
            for spot in row:
                if not spot.isBorder():
                   if not spot.is_start() and not spot.is_end():
                       num = random.randint(1, 4)
                       if num == 1:
                           spot.make_barrier()


    def validSpot(self, r, c):
        if r < self.rows - 1 and c < self.rows - 1 and r > 0 and c > 0: return self.grid[r][c]
        return False
    

    def draw(self):
        for row in self.grid:
            for spot in row:
                spot.draw(self.win, self.textfont)
        
        self.draw_grid()
        pygame.display.update()

    
    def buildMaze(self):

        start = self.grid[1][2]

        for row in self.grid:
            for spot in row:

                if not spot.isBorder():
                    spot.visited = False
                    spot.reset()

                spot.color = BLACK
                
                if spot.col % 2 != 0 or spot.row % 2 == 0:
                    spot.make_barrier()

                spot.update_neighbors(self.grid, 2)

        self.generate_maze_dfs(start)


    def generate_maze_dfs(self, spot):
        spot.visited = True
        spot.reset()

        random.shuffle(spot.neighbors)

        for neighbor in spot.neighbors:

            if not neighbor.visited:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()

                neighbor_row = (spot.row + neighbor.row) // 2
                neighbor_col = (spot.col + neighbor.col) // 2

                
                self.grid[neighbor_row][neighbor_col].reset()
                neighbor.make_open()
                
                self.draw()

                self.generate_maze_dfs(neighbor)
    
        self.draw()
