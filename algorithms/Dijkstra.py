from settings import *
import calculations
import heapq

class Dijkstra:
    def __init__(self, gridObj, start, end):
        self.distances = {}
        self.visited = {start}
        self.came_from = {}
        self.pq = [(0, start)]
        self.start = start
        self.end = end
        self.gridObj = gridObj
        self.grid = gridObj.grid


    def execute(self):
        self.distances = {spot : float("inf") for row in self.grid for spot in row}
        self.distances[self.start] = 0

        while self.pq:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            current_distance, current_node = heapq.heappop(self.pq)

            if current_node is self.end:
                calculations.reconstruct_path(self.came_from, self.end, self.gridObj, self.start, self.end)
                return True
            
            if current_node is not self.start and current_node is not self.end:
                current_node.make_closed()

            for neighbor in current_node.neighbors:
                if current_distance + neighbor.weight < self.distances[neighbor] and neighbor not in self.visited:
                    self.came_from[neighbor] = current_node
                    self.visited.add(neighbor)
                    
                    if neighbor is not self.end:
                        neighbor.make_open()
                    
                    self.distances[neighbor] = current_distance + neighbor.weight
                    heapq.heappush(self.pq, (current_distance + neighbor.weight, neighbor))
            
            self.gridObj.draw()

        return False