# from board import Board
import heapq
import itertools
import random

def a_star(puzzles, heuristic):
    iterations = 0
    frontier = []
    frontier_keys = set()
    counter = itertools.count()
    key0 = puzzles[0].state_key()
    
    heapq.heappush(frontier, (0 + misplaced_heuristic(puzzles[0]), next(counter), puzzles[0]))
    nodes_explored = 0
    frontier_keys.add(key0)
    explored = set()

    GOAL = [["_","1","2"], ["3","4","5"], ["6","7","8"]] 

    while(True): 
        if frontier == []:
            return 
        
        f, t, node  = heapq.heappop(frontier)
        node_key = node.state_key()
        frontier_keys.remove(node_key)

        # print(f"Board after iteration {iterations}:")
        # node.print_board()

        if node.configuration == GOAL:
            print(f"Goal state reached for {heuristic} heuristic after {iterations} iterations and {nodes_explored} nodes explored.")
            node.print_board()
            return node

        explored.add(node_key)

        neighbors = node.get_puzzle_neighbors()
        nodes_explored += len(neighbors)

        for neighbor in neighbors:
            neighbor_key = neighbor.state_key()
            if neighbor_key not in frontier_keys and neighbor_key not in explored:
                neighbor.depth = node.depth + 1
                if heuristic == "misplaced":
                    f = neighbor.depth + misplaced_heuristic(neighbor)
                elif heuristic == "manhattan":
                    f = neighbor.depth + manhattan_heuristic(neighbor)
                else: 
                    f = neighbor.depth

                heapq.heappush(frontier, (f, next(counter), neighbor))
                frontier_keys.add(neighbor_key)
        iterations += 1

def misplaced_heuristic(node):
    # Implement the misplaced tiles heuristic
    goal = ["_", "1", "2", "3", "4", "5", "6", "7", "8"]
    count = 0
    for i in range(3):
        for j in range(3):
            if node.configuration[i][j] != "_" and node.configuration[i][j] != goal[i * 3 + j]:
                count += 1
    return count

def manhattan_heuristic(node):
    # Implement the Manhattan distance heuristic
    distance = 0
    for i in range(3):
        for j in range(3):
            tile = node.configuration[i][j]
            if tile == "_":
                continue
            t = int(tile)
            target_y = (t) // 3 
            target_x = (t) % 3 
            distance += abs(i - target_y) + abs(j - target_x)
    return distance

