from settings import *
import calculations

class Bidirectional:
    def __init__(self, gridObj, start, end):
        self.q1 = [ start ]
        self.q2 = [ end ]
        self.visited1 = { start }
        self.visited2 = { end }
        self.came_from1 = {}
        self.came_from2 = {}
        self.end = end
        self.start = start
        self.gridObj = gridObj
    
    def mergeLists(self, came_from1, came_from2, cur):
        next = came_from2[cur]
        prev = cur
                
        while next in came_from2:
            came_from1[next] = prev
            prev = next
            next = came_from2[next]

        came_from1[next] = prev
        
        return came_from1

    def execute(self):
        while self.q1 and self.q2:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()


            cur1 = self.q1.pop(0)
            cur2 = self.q2.pop(0)

            if cur1 is not self.start:
                cur1.make_closed()

            if cur2 is not self.end:
                cur2.make_closed(True)

            if cur1 in self.visited2:
                self.came_from1 = self.mergeLists(self.came_from1, self.came_from2, cur1)
                calculations.reconstruct_path(self.came_from1, self.end, self.gridObj, self.start, self.end)
                return True
            
            elif cur2 in self.visited1:
                self.came_from2 = self.mergeLists(self.came_from2, self.came_from1, cur2)
                calculations.reconstruct_path(self.came_from2, self.start, self.gridObj, self.start, self.end)
                return True

            for neighbor in cur1.neighbors:
                if neighbor not in self.visited1:
                    if neighbor is not self.end:
                        neighbor.make_open()
                    self.visited1.add(neighbor)
                    self.came_from1[neighbor] = cur1
                    self.q1.append(neighbor)
            
            for neighbor in cur2.neighbors:
                if neighbor not in self.visited2:
                    if neighbor is not self.end:
                        neighbor.make_open(True)
                    self.visited2.add(neighbor)
                    self.came_from2[neighbor] = cur2
                    self.q2.append(neighbor)
            
            self.gridObj.draw()
        
        return False