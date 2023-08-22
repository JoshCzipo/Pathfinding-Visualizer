from settings import *
import calculations

class BFS:
    def __init__(self, gridObj, start, end):
        self.queue = [ start ]
        self.visited = { start }
        self.came_from = {}
        self.gridObj = gridObj
        self.start = start
        self.end = end
    
    def execute(self):
        while self.queue:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            cur = self.queue.pop(0)

            if cur is self.end:
                calculations.reconstruct_path(self.came_from, self.end, self.gridObj, self.start, self.end)
                return True

            if cur is not self.start:
                cur.make_closed()

            for neighbor in cur.neighbors:
                if neighbor not in self.visited:
                    if neighbor is not self.end:
                        neighbor.make_open()
                    self.came_from[neighbor] = cur
                    self.queue.append(neighbor)
                    self.visited.add(neighbor)
                
            self.gridObj.draw()
        
        return False