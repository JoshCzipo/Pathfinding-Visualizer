from settings import *
from grid import Grid
from buttonclass import MenuButton, SideButton, ExitButton
from algorithms.AStar import AStar
from algorithms.DFS import DFS
from algorithms.BFS import BFS
from algorithms.greedyBFS import GreedyBFS
from algorithms.Dijkstra import Dijkstra
from algorithms.Bidirectional import Bidirectional
import sys



class App:
    def __init__(self):
        self.running = True
        self.algorithm = 'None'
        self.start = None
        self.end = None
        self.started = False
        self.completed = False
        self.win = pygame.display.set_mode((WIDTH + MENU, WIDTH + MENU))
        self.state = 'game'
        self.wincolor = LIGHTGREY

        self.title = pygame.display.set_caption("Algorithm Visualizer")

        self.icon = pygame.image.load("images/path.png")
        
        self.gridObj = Grid(ROWS, WIDTH, self.win) #initialize the grid.

        self.controlImg = pygame.image.load("images/controlScreen.png")

        #Bottom Buttons
        self.dfsBut = MenuButton(self.win, 0, 'Depth-First-Search', self.clickDFS)
        self.bfsBut = MenuButton(self.win, 1, 'Breadth-First-Search', self.clickBFS)
        self.DijkBut = MenuButton(self.win, 2, 'Dijkstra (weighted)', self.clickDijk)
        self.AStarBut = MenuButton(self.win, 3, 'A* (weighted)', self.clickAStar)
        self.convergeBut = MenuButton(self.win, 4, 'Bidirectional', self.clickConverge)
        self.greedyBut = MenuButton(self.win, 5, 'Greedy-BFS (weighted)', self.clickGreedy)
        
        #Side panel buttons
        self.StartBut = SideButton(self.win, 0, 'Start', self.clickStart)
        self.MazeBtn = SideButton(self.win, 1, 'Generate Maze', self.clickMaze)
        self.BarriBtn = SideButton(self.win, 2, 'Random Barriers', self.clickBarri)
        self.clearBtn = SideButton(self.win, 3, 'Clear Board', self.clearBoard)
        self.pathBtn = SideButton(self.win, 4, 'Clear Path', self.clearPath)
        self.controlBtn = SideButton(self.win, 5, 'Controls', self.controls)
        self.display = SideButton(self.win, 6, 'Selected:', None, True, f'{self.algorithm}')

        #exit button
        self.exitBtn = ExitButton(self.win, 'Close', self.exit)

    def get_clicked_pos(self, pos): #normalize click position to be a value within the grid.
        gap = WIDTH // ROWS
        y, x = pos

        row = y // gap
        col = x // gap

        return self.gridObj.validSpot(row, col)
    
    def run(self):
        
        self.win.fill(self.wincolor)
        self.render_buttons()
        pygame.display.set_icon(self.icon)

        while self.running:

            if self.started:
                continue

            if self.state == 'game':
                self.gridObj.draw()
                self.gameScreen()
            elif self.state == 'controls':
                self.controlScreen()

        pygame.quit()
        sys.exit()
            
    def controlScreen(self):

        image_size = self.controlImg.get_size()
        screen_size = self.win.get_size()

        x = (screen_size[0] - image_size[0]) // 2
        y = (screen_size[1] - image_size[1]) // 2

        self.win.blit(self.controlImg, (x, y))
        self.exitBtn.draw(GREY)

        pygame.display.update()


        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.exitBtn.contains(pos):
                    self.exitBtn.click()
    

    def gameScreen(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            pos = pygame.mouse.get_pos()
            self.buttonEvents(pos, event)

            if self.completed:
                continue

            if pygame.mouse.get_pressed()[0]:
                spot = self.get_clicked_pos(pos) #Create spot if clicked valid space within the grid

                if spot:
                    if not self.start and spot is not self.end:
                        self.start = spot
                        spot.make_start()
                    elif not self.end and spot is not self.start:
                        self.end = spot
                        spot.make_end()
                    elif spot is not self.start and spot is not self.end:
                        spot.make_barrier()

            elif pygame.mouse.get_pressed()[2]:
                spot = self.get_clicked_pos(pos) #right click to delete a valid spot on the grid

                if spot:
                    if not spot.isBorder():
                        if spot == self.start:
                            self.start = None
                        elif spot == self.end:
                            self.end = None

                        spot.remove_weight()
                        spot.reset()
            
            elif pygame.key.get_pressed()[pygame.K_e]:
                spot = self.get_clicked_pos(pos)

                if spot:
                    if spot is not self.start and spot is not self.end and not spot.is_barrier():
                        spot.add_weight()

    def buttonEvents(self, pos, event):
        buttons = [self.bfsBut, self.dfsBut, self.DijkBut, self.AStarBut, 
                   self.StartBut, self.MazeBtn, self.clearBtn, self.pathBtn, 
                   self.controlBtn, self.convergeBut, self.BarriBtn, self.greedyBut]

    
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for but in buttons:
                if but.contains(pos):
                    but.color = TURQOUISE
                    but.click()
                else:
                    but.color = BLACK
            
            self.display.text2 = f'{self.algorithm}'
            self.render_buttons()

    def runAlgo(self):
        
        if self.start and self.end and self.algorithm != 'None' and not self.completed:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            self.started = True
            grid = self.gridObj.grid
            
            for row in grid:
                for spot in row:
                    spot.update_neighbors(grid, 1)

            if self.algorithm == 'DFS':
                algo = DFS(self.gridObj, self.start, self.end)
            elif self.algorithm == 'BFS':
                algo = BFS(self.gridObj, self.start, self.end)
            elif self.algorithm == 'Dijkstra':
                algo = Dijkstra(self.gridObj, self.start, self.end)
            elif self.algorithm == 'AStar':
                algo = AStar(self.gridObj, self.start, self.end)
            elif self.algorithm == 'Bidirectional':
                algo = Bidirectional(self.gridObj, self.start, self.end)
            elif self.algorithm == 'Greedy':
                algo = GreedyBFS(self.gridObj, self.start, self.end)

            algo.execute()
            self.started = False
            self.completed = True

        
    def render_buttons(self):
        self.dfsBut.draw(GREY)
        self.bfsBut.draw(GREY)
        self.DijkBut.draw(GREY)
        self.AStarBut.draw(GREY)
        self.StartBut.draw(GREY)
        self.MazeBtn.draw(GREY)
        self.clearBtn.draw(GREY)
        self.pathBtn.draw(GREY)
        self.controlBtn.draw(GREY)
        self.convergeBut.draw(GREY)
        self.BarriBtn.draw(GREY)
        self.greedyBut.draw(GREY, 14)
        self.display.draw(GREY)

    def clickStart(self):
        self.runAlgo()

    def clickDFS(self):
        self.algorithm = 'DFS'
    
    def clickBFS(self):
        self.algorithm = 'BFS'
    
    def clickDijk(self):
        self.algorithm = 'Dijkstra'

    def clickAStar(self):
        self.algorithm = 'AStar'

    def clickConverge(self):
        self.algorithm = 'Bidirectional'
    
    def clickGreedy(self):
        self.algorithm = 'Greedy'

    def clickMaze(self):
        self.started = True
        self.start = None
        self.end = None

        self.gridObj.buildMaze()
        self.started = False

    def clearBoard(self):
        self.start = None
        self.end = None
        self.gridObj.clear_board()
        self.started = False
        self.completed = False

    def clearPath(self):
        self.completed = False
        self.gridObj.clear_path()

    def controls(self):
        self.state = 'controls'
    
    def exit(self):
        self.state = 'game'
        self.win.fill(self.wincolor)
        self.render_buttons()

    def clickBarri(self):
        self.gridObj.random_barriers()
    
    
    



        


   





