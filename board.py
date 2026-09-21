import random


class Board:
    """
    A class representing the 8-puzzle board.
    """
    def __init__(self, initial_configuration):
        """
        :param initial_configuration: ex. {{"_", "1", "2"}, {"3", "4", "5"}, {"6", "7", "8"}}
        """
        self.configuration = initial_configuration

    def move_tile(self, start_tile, move_tile):
        """
        Moves a tile from the start_tile position to the move_tile position if the move is valid.
        :param start_tile: the coordinates of the tile to be moved (row, column)
        :param move_tile: the coordinates of the target position (row, column)
        :return: return True if the move was successful, False otherwise
        """
        x = start_tile[0]
        y = start_tile[1]
        new_x = move_tile[0]
        new_y = move_tile[1]
        if self.is_valid_tile(new_x, new_y):
            self.configuration[x][y], self.configuration[new_x][new_y] = self.configuration[new_x][new_y], self.configuration[x][y]
            return True
        else:
            return False

    def is_valid_tile(self, x, y):
        """
        Checks if the given tile coordinates are valid (within the bounds of the board).
        :param x: the row index of the tile
        :param y: the column index of the tile
        :return: True if the tile is valid, False otherwise
        """
        if x < 0 or x > 2 or y < 0 or y > 2:
            return False
        else:
            return True

    def find_empty_neighbor(self):
        """
        Find the coordinates of the tiles that are non-diagonal neighbors to the empty tile.
        :return: a list of coordinates of the neighboring tiles
        """
        for i in range(3):
            for j in range(3):
                if self.configuration[i][j] == "_":
                    empty_tile = (i, j)
                    break
        empty_x = empty_tile[0]
        empty_y = empty_tile[1]
        list_of_neighbors = [(empty_x+1, empty_y), (empty_x-1,empty_y), (empty_x, empty_y+1), (empty_x, empty_y-1)]
        for i in list_of_neighbors:
            if self.is_valid_tile(i[0], i[1]):
                pass
            else:
                list_of_neighbors.remove(i)
        return list_of_neighbors

    def find_empty_tile(self):
        """
        Finds the coordinates of the empty tile.
        :return: the coordinates of the empty tile (row, column)
        """
        for i in range(3):
            for j in range(3):
                if self.configuration[i][j] == "_":
                    return (i, j)

    def randomize(self):
        """
        Randomly shuffles the board configuration by making a series of valid moves.
        """
        random_num_moves = random.randint(100, 10000)


        i = 0

        while i < random_num_moves:
            empty_tile = self.find_empty_tile()
            empty_neighbors = self.find_empty_neighbor()
            random_neighbor = random.choice(empty_neighbors)
            success = self.move_tile(empty_tile, random_neighbor)
            if success:
                i += 1
            # print(f"Board after {i} moves:")
            # self.print_board()


    def print_board(self):
        """
        Prints the current configuration of the board.
        """
        for row in self.configuration:
            print(row)

    def get_puzzle_neighbors(self):
        empty_tile = self.find_empty_tile()
        empty_neighbors = self.find_empty_neighbor()
        boards = []
        for neighbor in empty_neighbors:
            new_board = self.configuration.copy()  # Create a copy of the current configuration
            new_board[empty_tile[0]][empty_tile[1]] = new_board[neighbor[0]][neighbor[1]]
            new_board[neighbor[0]][neighbor[1]] = "_"
            boards.append(Board(new_board))
        return boards

# main function
if __name__ == "__main__":
    initial_configuration = [["_", "1", "2"], ["3", "4", "5"], ["6", "7", "8"]]
    board = Board(initial_configuration)
    board.randomize()
