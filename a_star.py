import copy
import heapq
from itertools import count

from board import Board


def board_key(board):
    """
    Convert the 2D board into a hashable representation for the set.
    :param board: The Board
    :return: the hashable representation of the board
    """
    return tuple(tuple(row) for row in board.configuration)


def a_star(puzzle, heuristic):
    """
    A* search algorithm to solve the 8-puzzle problem.
    :param puzzle: the Board to be solved
    :param heuristic: the heuristic to be used ("misplaced" or "manhattan")
    :return: the number of nodes explored to reach the goal state
    """
    goal_state = [["_", "1", "2"], # the goal state of the 8-puzzle
                  ["3", "4", "5"],
                  ["6", "7", "8"]]

    explored = set() # initialize the explored set to keep track of visited states

    tie_breaker = count() # create a counter to break ties in the priority queue

    frontier = [] # initialize the priority queue

    if heuristic == "misplaced": # calculate the heuristic value based on the chosen heuristic
        h = misplaced_heuristic(puzzle.configuration)
    elif heuristic == "manhattan":
        h = manhattan_heuristic(puzzle.configuration)
    elif heuristic == "relaxed":
        h = relaxed_adjacency_heuristic(puzzle.configuration)

    heapq.heappush(frontier, (h, next(tie_breaker), 0, puzzle)) # put the initial state into the priority queue

    num_nodes = 1

    best_g = {board_key(puzzle): 0}

    while frontier:
        priority, _, g_cost, node = heapq.heappop(frontier) # pop the node with lowest priority

        state = board_key(node) # turn the board into a hashable representation

        if g_cost != best_g[state]:
            continue

        if state in explored: # skip if the node has already been explored
            continue

        explored.add(state) # add the node to the explored set

        if node.configuration == goal_state: # check if the goal state has been reached
            # print(
            #     f"Goal state reached! "
            #     f"Number of nodes explored: {num_nodes} "
            #     f"Depth of the solution: {g_cost + 1}"
            # )
            return num_nodes, g_cost

        children = node.get_puzzle_neighbors() # get all the children of the current node

        num_nodes += len(children)

        for child in children:
            child_state = board_key(child)

            if child_state in explored:
                continue

            new_g = g_cost + 1 # calculate the new g cost for the child node

            if new_g >= best_g.get(child_state, float("inf")):
                continue

            best_g[child_state] = new_g

            if heuristic == "misplaced": # calculate the heuristic value for the child node
                h = misplaced_heuristic(child.configuration)
            elif heuristic == "manhattan":
                h = manhattan_heuristic(child.configuration)
            elif heuristic == "relaxed":
                h = relaxed_adjacency_heuristic(child.configuration)
            else:
                raise ValueError("Unknown heuristic")

            f = new_g + h # calculate the f value for the child node

            heapq.heappush( # put the child node into the priority queue
                frontier,
                (f, next(tie_breaker), new_g, child)
            )


def misplaced_heuristic(configuration):
    """
    Calculate the number of misplaced tiles in the given configuration.
    :param configuration: the current configuration of the board
    :return: the number of misplaced tiles
    """
    goal_state = [["_", "1", "2"],
                  ["3", "4", "5"],
                  ["6", "7", "8"]]

    count_misplaced = 0

    for i in range(3):
        for j in range(3):
            if configuration[i][j] != "_":
                if configuration[i][j] != goal_state[i][j]:
                    count_misplaced += 1

    return count_misplaced


def manhattan_heuristic(configuration):
    """
    Calculate the Manhattan distance for the given configuration.
    :param configuration: the current configuration of the board
    :return: the Manhattan distance
    """
    distance = 0

    for i in range(3):
        for j in range(3):
            tile = configuration[i][j]

            if tile == "_":
                continue

            target_x = int(tile) // 3
            target_y = int(tile) % 3

            distance += abs(i - target_x) + abs(j - target_y)

    return distance

def find_tile_coordinates(configuration, tile):
    """
    Find the coordinates of a specific tile in the given configuration.
    :param configuration: the current configuration of the board
    :param tile: the tile to find
    :return: the coordinates of the tile (row, column) or None if the tile is not found
    """
    for i in range(3):
        for j in range(3):
            if configuration[i][j] == tile:
                return (i, j)
    return None

def out_of_place_tiles(configuration):
    """
    Get a list of the tiles that are out-of-place in the given configuration.
    :param configuration: the current configuration of the board
    :return: a list of the out-of-place tiles
    """
    goal_state = [["_", "1", "2"],
                  ["3", "4", "5"],
                  ["6", "7", "8"]]

    out_of_place = []

    for i in range(3):
        for j in range(3):
            if configuration[i][j] != "_" and configuration[i][j] != goal_state[i][j]:
                out_of_place.append((i, j))

    return out_of_place

def swap_tiles(configuration, tile1_coords, tile2_coords):
    """
    Swap two tiles.
    :param configuration: the current configuration of the board
    :param tile1_coords: the coordinates of the first tile to swap
    :param tile2_coords: the coordinates of the second tile to swap
    :return: the new configuration after swapping the tiles
    """

    x1, y1 = tile1_coords
    x2, y2 = tile2_coords
    configuration[x1][y1], configuration[x2][y2] = configuration[x2][y2], configuration[x1][y1]
    return configuration

def relaxed_adjacency_heuristic(configuration):
    """
    Calculate the relaxed adjacency heuristic for the given configuration.
    :param configuration: the current configuration of the board
    :return: the relaxed adjacency heuristic value
    """
    num_swaps = 0

    goal_state = [["_", "1", "2"],["3", "4", "5"],["6", "7", "8"]] # the goal state of the 8-puzzle

    temp_config = [row[:] for row in configuration] # Create a copy of the configuration

    empty_tile = None

    true_coords = {"_": (0, 0), "1": (0, 1), "2": (0, 2), "3": (1, 0), "4": (1, 1), "5": (1, 2), "6": (2, 0), "7": (2, 1), "8": (2, 2)}
    true_values = {(0,0): "_", (0,1): "1", (0,2): "2", (1,0): "3", (1,1): "4", (1,2): "5", (2,0): "6", (2,1): "7", (2,2): "8"}

    empty_tile = find_tile_coordinates(temp_config, "_")

    while temp_config != goal_state:
        if empty_tile == true_coords["_"]:
            out_of_place = out_of_place_tiles(temp_config)
            temp_config = swap_tiles(temp_config, empty_tile, out_of_place[0])
            empty_tile = out_of_place[0]
        else:
            true_tile = true_values[empty_tile]
            true_tile_coords = find_tile_coordinates(temp_config, true_tile)
            temp_config = swap_tiles(temp_config, empty_tile, true_tile_coords)
            empty_tile = true_tile_coords
        num_swaps += 1

    return num_swaps

if __name__ == "__main__":
    initial_configuration = [
        ["_", "1", "2"],
        ["3", "4", "5"],
        ["6", "7", "8"]
    ]

    # for i in range(5):
    #     board = Board(initial_configuration)
    #     board.randomize()
    #
    #     a_star(board, "misplaced")
    #
    # for i in range(5):
    #     board = Board(initial_configuration)
    #     board.randomize()
    #
    #     a_star(board, "manhattan")

    example_configuration = [
        ["_", "2", "1"],
        ["3", "4", "5"],
        ["6", "7", "8"]
    ]

    num_swaps = relaxed_adjacency_heuristic(example_configuration)
    print(f"Relaxed adjacency heuristic value: {num_swaps}")