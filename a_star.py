def a_star(puzzle, heuristic):
    frontier = puzzle 
    explored = []
    while(True): 
        if frontier == []:
            return 
        node = frontier.pop()
        

        if heuristic == "manhattan": 
            return
