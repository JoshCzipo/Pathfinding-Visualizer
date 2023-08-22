from settings import *
from queue import PriorityQueue
import calculations

class AStar:
    def __init__(self, gridObj, start, end):
        self.gridObj = gridObj
        self.grid = gridObj.grid
        self.start = start
        self.end = end
        self.count = 0
        self.came_from = {}
        self.open_set = PriorityQueue()
        self.g_score = []
        self.f_score = []
        self.visited = {self.start}

    def execute(self):
        
        self.open_set.put((0, self.count, self.start))

        self.g_score = {spot: float("inf") for row in self.grid for spot in row}
        self.g_score[self.start] = 0

        self.f_score = {spot: float("inf") for row in self.grid for spot in row}
        self.f_score[self.start] = calculations.h(self.start.get_pos(), self.end.get_pos())


        while not self.open_set.empty():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            current = self.open_set.get()[2]
            self.visited.remove(current)

            if current is self.end:
                calculations.reconstruct_path(self.came_from, self.end, self.gridObj, self.start, self.end)
                return True
            
            for neighbor in current.neighbors:
                temp_g_score = self.g_score[current] + neighbor.weight

                if temp_g_score < self.g_score[neighbor]:
                    self.came_from[neighbor] = current
                    self.g_score[neighbor] = temp_g_score
                    self.f_score[neighbor] = temp_g_score + calculations.h(neighbor.get_pos(), self.end.get_pos())
                    
                    if neighbor not in self.visited:
                        if neighbor is not self.end:
                            neighbor.make_open()
                        self.count += 1
                        self.open_set.put((self.f_score[neighbor], self.count, neighbor))
                        self.visited.add(neighbor)
                                
            self.gridObj.draw()

            if current is not self.start and current is not self.end:
                current.make_closed()

        return False