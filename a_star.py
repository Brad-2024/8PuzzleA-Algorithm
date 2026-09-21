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
    goal_state = [["_", 1, 2], # the goal state of the 8-puzzle
                  [3, 4, 5],
                  [6, 7, 8]]

    explored = set() # initialize the explored set to keep track of visited states

    tie_breaker = count() # create a counter to break ties in the priority queue

    frontier = [] # initialize the priority queue

    if heuristic == "misplaced": # calculate the heuristic value based on the chosen heuristic
        h = misplaced_heuristic(puzzle.configuration)
    else:
        h = manhattan_heuristic(puzzle.configuration)

    heapq.heappush(frontier, (h, next(tie_breaker), 0, puzzle)) # put the initial state into the priority queue

    num_nodes = 0

    while frontier:
        priority, _, g_cost, node = heapq.heappop(frontier) # pop the node with lowest priority

        state = board_key(node) # turn the board into a hashable representation

        if state in explored: # skip if the node has already been explored
            continue

        explored.add(state) # add the node to the explored set
        num_nodes += 1

        if node.configuration == goal_state: # check if the goal state has been reached
            print(
                f"Goal state reached! "
                f"Number of nodes explored: {num_nodes} "
                f"Depth of the solution: {g_cost + 1}"
            )
            return num_nodes, g_cost + 1

        children = possible_boards(node) # get all the children of the current node

        for child in children:
            child_state = board_key(child)

            if child_state not in explored:
                new_g = g_cost + 1 # calculate the new g cost for the child node

                if heuristic == "misplaced": # calculate the heuristic value for the child node
                    h = misplaced_heuristic(child.configuration)
                elif heuristic == "manhattan":
                    h = manhattan_heuristic(child.configuration)
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
    goal_state = [["_", 1, 2],
                  [3, 4, 5],
                  [6, 7, 8]]

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

            target_x = tile // 3
            target_y = tile % 3

            distance += abs(i - target_x) + abs(j - target_y)

    return distance


def possible_boards(board):
    """
    Generates all possible board configuration by moving available tiles into the empty space.
    :param board: the current board configuration
    :return: the list of possible board configurations
    """
    neighbors = []

    empty_tile = board.find_empty_tile()
    empty_neighbors = board.find_empty_neighbor()

    for neighbor in empty_neighbors:
        new_board = copy.deepcopy(board)
        new_board.move_tile(empty_tile, neighbor)
        neighbors.append(new_board)

    return neighbors


if __name__ == "__main__":
    initial_configuration = [
        ["_", 1, 2],
        [3, 4, 5],
        [6, 7, 8]
    ]

    for i in range(5):
        board = Board(initial_configuration)
        board.randomize()

        a_star(board, "misplaced")

    for i in range(5):
        board = Board(initial_configuration)
        board.randomize()

        a_star(board, "manhattan")