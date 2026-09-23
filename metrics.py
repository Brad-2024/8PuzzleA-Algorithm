from board import *
from a_star import *
from datetime import datetime
from scipy.optimize import brentq


def effective_branching_factor(nodes_generated, depth):
    """
    Calculate the effective branching factor based on the depth and number of nodes generated.
    :param nodes_generated: the number of nodes that were generated in the search
    :param depth: the depth of the goal state in the search
    :return: the effective branching factor of the search
    """
    def f(b):
        return sum(b**i for i in range(depth+1)) - (nodes_generated+1)
    return brentq(f, 0, nodes_generated+1)

def search_metrics(f):
    """
    Calculate the number of nodes generated and the effective branching factor for 100 iterations
    of each depth [6,8,10,12,14,16,18,20,22,24,26,28], and each heuristic [misplaced, manhattan, relaxed].
    :param f: the file to write the data to
    :return: a list of the # of nodes generated and effective branching factor
    for all depths and all heuristics

    """
    data = [[
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        []
    ], [
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        []
    ], [
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        []
    ]]

    index_to_depth = {0: 6, 1: 8, 2: 10, 3: 12, 4: 14, 5: 16, 6: 18, 7: 20, 8: 22, 9: 24, 10: 26, 11: 28}
    index_to_heuristic = {0: "misplaced", 1: "manhattan", 2: "relaxed"}


    for i in range(3):
        for j in range(12):
            for k in range(100):
                boards = Board.generate_boards_from_depth(28)[index_to_depth[j]]
                board = random.choice(boards)
                nodes_expanded, depth = a_star(board, index_to_heuristic[i])
                ebf = effective_branching_factor(nodes_expanded, depth)
                print(f"Depth: {depth}, Heuristic: {index_to_heuristic[i]}, Nodes Expanded: {nodes_expanded}, Effective Branching Factor: {round(ebf, 2)}")
                data[i][j].append((nodes_expanded, ebf))
                f.write(f"Depth: {depth}, Heuristic: {index_to_heuristic[i]}, Nodes Expanded: {nodes_expanded}, Effective Branching Factor: {round(ebf, 2)}\n")

    return data

def avg_metrics(f, data):
    """
    Calculate the average metrics for each depth of each heuristic.
    :param f: the file to write the data to
    :param data: the data to calculate the averages of
    :return: a list of the average metrics for each depth of each heuristic
    """
    averages = [[
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        []
    ], [
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        []
    ], [
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        []
    ]]

    index_to_depth = {0: 6, 1: 8, 2: 10, 3: 12, 4: 14, 5: 16, 6: 18, 7: 20, 8: 22, 9: 24, 10: 26, 11: 28}
    index_to_heuristic = {0: "misplaced", 1: "manhattan", 2: "relaxed"}

    for i in range(3):
        for j in range(12):
            cost_sum = sum(cost for cost, ebf in data[i][j])
            ebf_sum = sum(ebf for cost, ebf in data[i][j])

            avg_cost = int(cost_sum // len(data[i][j]))
            avg_ebf = ebf_sum / len(data[i][j])

            averages[i][j] = (avg_cost, avg_ebf)
            heuristic = index_to_heuristic[i]
            depth = index_to_depth[j]
            print(f"Depth: {depth}, Heuristic: {heuristic}, Avg. Nodes Expanded: {avg_cost}, Avg. Effective Branching Factor: {round(avg_ebf, 2)}")
            f.write(f"Depth: {depth}, Heuristic: {heuristic}, Avg. Nodes Expanded: {avg_cost}, Avg. Effective Branching Factor: {round(avg_ebf, 2)}\n")

    return averages

def run_metrics():
    """
    Run the search algorithm 100 times for each depth and each heuristic, also taking
    the average of the 100 iterations.
    :return: the data list and average data list
    """
    filename = f"data/{datetime.now().strftime("%Y-%m-%d %H-%M-%S")}_metrics.txt"
    with open(filename, "w") as f:
        data = search_metrics(f)
        avg_data = avg_metrics(f, data)

    return data, avg_data

if __name__ == "__main__":
    data, avg_data = run_metrics()



