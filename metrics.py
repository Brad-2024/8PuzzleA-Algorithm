from board import *
from a_star import *
from datetime import datetime
from scipy.optimize import brentq


    def f(b):
        return sum(b**i for i in range(depth+1)) - (nodes_generated+1)
    return brentq(f, 0, nodes_generated+1)

def search_metrics(f):
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
    filename = f"data/{datetime.now().strftime("%Y-%m-%d %H-%M-%S")}_metrics.txt"
    with open(filename, "w") as f:
        data = search_metrics(f)
        avg_data = avg_metrics(f, data)

    return data, avg_data

if __name__ == "__main__":
    data, avg_data = run_metrics()



