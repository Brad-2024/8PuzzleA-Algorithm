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

    depths = list(range(6, 29, 2))
    heuristics = ["misplaced", "manhattan", "relaxed"]

    data = [[[] for _ in depths] for _ in heuristics]

    all_boards = Board.generate_boards_from_depth(28)

    sampled_boards = {depth: random.choices(all_boards[depth], k=100) for depth in depths}

    for i, heuristic in enumerate(heuristics):
        for j, depth in enumerate(depths):
            for board in sampled_boards[depth]:
                nodes_expanded, solution_depth = a_star(board, heuristic)
                ebf = effective_branching_factor(nodes_expanded, solution_depth)
                data[i][j].append((nodes_expanded, ebf))
                print(f"Depth: {solution_depth}, Heuristic: {heuristic}, Nodes Expanded: {nodes_expanded}, Effective Branching Factor: {round(ebf, 2)}")
                f.write(f"Depth: {solution_depth}, Heuristic: {heuristic}, Nodes Expanded: {nodes_expanded}, Effective Branching Factor: {round(ebf, 2)}\n")

    return data

def avg_metrics(f, data):
    """
    Calculate the average metrics for each depth of each heuristic.
    :param f: the file to write the data to
    :param data: the data to calculate the averages of
    :return: a list of the average metrics for each depth of each heuristic
    """

    depths = list(range(6, 29, 2))
    heuristics = ["misplaced", "manhattan", "relaxed"]

    averages = [[[] for _ in depths] for _ in heuristics]

    for j, depth in enumerate(depths):
        for i, heuristic in enumerate(heuristics):
            cost_sum = sum(cost for cost, ebf in data[i][j])
            ebf_sum = sum(ebf for cost, ebf in data[i][j])

            avg_cost = int(cost_sum // len(data[i][j]))
            avg_ebf = ebf_sum / len(data[i][j])

            averages[i][j] = (avg_cost, avg_ebf)

            print(f"Depth: {depth}, Heuristic: {heuristic}, Avg. Nodes Expanded: {avg_cost}, Avg. Effective Branching Factor: {round(avg_ebf, 2)}")
            f.write(f"Depth: {depth}, Heuristic: {heuristic}, Avg. Nodes Expanded: {avg_cost}, Avg. Effective Branching Factor: {round(avg_ebf, 2)}\n")

    return averages

def run_metrics():
    """
    Run the search algorithm 100 times for each depth and each heuristic, also taking
    the average of the 100 iterations.
    :return: the data list and average data list
    """
    filename = f"data/{datetime.now().strftime('%Y-%m-%d %H-%M-%S')}_metrics.txt"
    with open(filename, "w") as f:
        data = search_metrics(f)
        avg_data = avg_metrics(f, data)

    return data, avg_data

if __name__ == "__main__":
    data, avg_data = run_metrics()



