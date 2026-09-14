import copy
import heapq
from itertools import count

from board import Board


def board_key(board):
    return tuple(tuple(row) for row in board.configuration)


def a_star(puzzle, heuristic):
    goal_state = [["_", 1, 2],
                  [3, 4, 5],
                  [6, 7, 8]]

    explored = set()

    tie_breaker = count()

    frontier = []

    if heuristic == "misplaced":
        h = misplaced_heuristic(puzzle.configuration)
    else:
        h = manhattan_heuristic(puzzle.configuration)

    heapq.heappush(frontier, (h, next(tie_breaker), 0, puzzle))

    num_nodes = 0

    while frontier:
        priority, _, g_cost, node = heapq.heappop(frontier)

        state = board_key(node)

        if state in explored:
            continue

        explored.add(state)
        num_nodes += 1

        if node.configuration == goal_state:
            print(
                f"Goal state reached! "
                f"Number of nodes explored: {num_nodes}"
            )
            return

        children = possible_boards(node)

        for child in children:
            child_state = board_key(child)

            if child_state not in explored:
                new_g = g_cost + 1

                if heuristic == "misplaced":
                    h = misplaced_heuristic(child.configuration)
                elif heuristic == "manhattan":
                    h = manhattan_heuristic(child.configuration)
                else:
                    raise ValueError("Unknown heuristic")

                f = new_g + h

                heapq.heappush(
                    frontier,
                    (f, next(tie_breaker), new_g, child)
                )


def misplaced_heuristic(configuration):
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

    board = Board(initial_configuration)
    board.randomize()

    a_star(board, "misplaced")