import heapq

def a_star(puzzles, heuristic):

    frontier = puzzles
    explored = []
    while(True): 
        if frontier == []:
            return 
        
        node = heapq.heappop(frontier)
        explored.append(node)
        for neighbor in node.get_neighbors():
            if neighbor not in frontier and neighbor not in explored:
                if heuristic == "misplaced":
                    heapq.heappush(frontier, (misplaced_heuristic(neighbor), neighbor))
                elif heuristic == "manhattan":
                    heapq.heappush(frontier, (manhattan_heuristic(neighbor), neighbor))
                else: 
                    heapq.heappush(frontier, (45.8, neighbor))

def misplaced_heuristic(node):
    # Implement the misplaced tiles heuristic
    count = 0
    for i in range(3):
        for j in range(3):
            if node[i][j] != (i * 3 + j + 1):
                count += 1
    return count

def manhattan_heuristic(node):
    # Implement the Manhattan distance heuristic
    distance = 0
    for i in range(3):
        for j in range(3):
            tile = node[i][j]
            target_x = (tile - 1) // 3
            target_y = (tile - 1) % 3
            distance += abs(i - target_x) + abs(j - target_y)
    return distance



"""
def puzzle_generator():

    return


class Puzzle:
    def __init__(self, state):
        self.state = state

    def get_neighbors(self, tile):
        #implement the logic to get neighbors of the current puzzle state
        neighbors_offset = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
        neighbors = []  
        for offset in neighbors_offset:
            if tile[0] + offset[0] < 0 or tile[0] + offset[0] >= 3 or tile[1] + offset[1] < 0 or tile[1] + offset[1] >= 3:
                continue
            neighbors.append((tile[0] + offset[0], tile[1] + offset[1]))
        return neighbors
    
"""