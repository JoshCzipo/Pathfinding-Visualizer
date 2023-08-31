from settings import *
import calculations
import heapq

class GreedyBFS:
    def __init__(self, gridObj, start, end):
        self.open_list = [(0, start)]
        self.visited = {start}
        self.came_from = {}
        self.end = end
        self.start = start
        self.gridObj = gridObj
        self.running = True


    def execute(self):
        while self.open_list:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()

            _, cur = heapq.heappop(self.open_list)  # Get the spot with the lowest heuristic value

            if cur is self.end:
                calculations.reconstruct_path(self.came_from, self.end, self.gridObj, self.start, self.end)
                return True

            if cur is not self.start:
                cur.make_closed()
            
            for neighbor in cur.neighbors:
                    if neighbor not in self.visited:
                        self.visited.add(neighbor)     
                        
                        if neighbor is not self.end:
                            neighbor.make_open()
                            
                        self.came_from[neighbor] = cur
                        heapq.heappush(self.open_list, (calculations.heuristic(neighbor, self.end), neighbor))
            

            self.gridObj.draw()
        return False
