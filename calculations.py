def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def reconstruct_path(came_from, current, gridObj, start, end):
    while current in came_from:
        current = came_from[current]
        if current is not start and current is not end:
            current.make_path()
        gridObj.draw()

def heuristic(spot, end):
     return spot.weight * (abs(spot.row - end.row) + abs(spot.col - end.col))