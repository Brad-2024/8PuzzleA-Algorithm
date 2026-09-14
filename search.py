# from board import Board
import heapq
import random

def a_star(puzzles, heuristic):
    iterations = 0
    frontier = []
    heapq.heappush(frontier, (misplaced_heuristic(puzzles[0]), random.random() * 100, puzzles[0]))
    nodes_explored = 0
    explored = []

    goal = [["_","1","2"], ["3","4","5"], ["6","7","8"]]  
    while(True): 
        if frontier == []:
            return 
        
        h, r, node  = heapq.heappop(frontier)

        # print(f"Board after iteration {iterations}:")
        # node.print_board()

        if node.configuration == goal:
            print(f"Goal state reached for {heuristic} heuristic after {iterations} iterations and {nodes_explored} nodes explored.")
            return node

        explored.append(node)
        neighbors = node.get_puzzle_neighbors()

        for neighbor in neighbors:
            if neighbor not in frontier and neighbor not in explored:
                neighbor.depth = node.depth + 1
                if heuristic == "misplaced":
                    heapq.heappush(frontier, (neighbor.depth + misplaced_heuristic(neighbor), random.random() * 100, neighbor))
                elif heuristic == "manhattan":
                    heapq.heappush(frontier, (neighbor.depth + manhattan_heuristic(neighbor), random.random() * 100, neighbor))
                else: 
                    heapq.heappush(frontier, (45.8, random.random() * 100, neighbor))
        iterations += 1
        nodes_explored += len(neighbors)

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

