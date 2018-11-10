from random import randint
from collections import namedtuple

# Size of board.
N = 3

Player = namedtuple('Player', 'name symbol')


class Model:
    """
    Handle all operations involving the board of the game.
    """

    def __init__(self):
        self.board = [[None for x in range(N)] for y in range(N)]

    def update_board(self, line, col, curr_player):
        if self.board[line][col] is not None:
            return False
        else:
            self.board[line][col] = curr_player
            return True

    def line_won(self, curr_player):
        for line in self.board:
            if all(x == curr_player for x in line):
                return True
        return False

    def col_won(self, curr_player):
        for col in range(N):
            if all(line[col] == curr_player for line in self.board):
                return True
        return False

    def diagonal_won(self, curr_player):
        # Main diagonal.
        if all(self.board[index][index] == curr_player for index in range(N)):
            return True
        # Opposite diagonal.
        if all(self.board[index][N-1-index] == curr_player for index in range(N)):
            return True
        return False


class View:
    """
    Present output to user.
    """

    def print_board(self, players, board):
        print()
        print('Board:')
        for line in board:
            for spot in line:
                if spot is None:
                    print('-', end='')
                else:
                    print(players[spot].symbol, end='')
            print()
        print()

    def declare_winner(self, players, curr_player):
        print()
        print('***')
        print(f'The winner is {players[curr_player].name}!!!')
        print('***')

    def declare_tie(self):
        print()
        print('***')
        print('The result is a tie!!!')
        print('***')


class Controller:
    """
    Initiate and operate the game to its end, including interaction with the user.
    """

    def __init__(self):
        self.model = Model()
        self.view = View()
        self.players, self.curr_player = self._initiate_players()
        self.number_of_moves_left = N * N  # Equals to number of squares on board.

    def _initiate_players(self):
        x_player_name = input('Enter X player name\n')
        o_player_name = input('Enter O player name\n')
        while x_player_name == o_player_name:
            o_player_name = input('Both names are the same. Choose a different name for O player\n')
        players = [Player(name=x_player_name, symbol='x'), Player(name=o_player_name, symbol='o')]
        curr_player = randint(0, 1)
        return players, curr_player

    def show_board(self):
        self.view.print_board(self.players, self.model.board)

    def next_move(self):
        while True:
            line = self.get_valid_input('line')
            col = self.get_valid_input('column')
            next_move_finished = self.model.update_board(line, col, self.curr_player)
            if next_move_finished:
                break
            else:
                print(f'{self.players[self.curr_player].name}, try again (spot is taken)')

    def get_valid_input(self, input_type):
        while True:
            print(f'{self.players[self.curr_player].name}, please insert the {input_type} number')
            try:
                input_value = int(input())
            except ValueError:
                print(f'{self.players[self.curr_player].name}, input not valid')
                continue
            if input_value < 0 or input_value >= N:
                print(f'{self.players[self.curr_player].name}, insert a {input_type} num between 0 to {N-1}, including')
            else:
                break
        return input_value

    def switch_player(self):
        self.curr_player = 1 - self.curr_player  # Flip bit (0/1).

    def game_done(self):
        # Check if game is won and declare it.
        if self.model.line_won(self.curr_player) \
                or self.model.col_won(self.curr_player) \
                or self.model.diagonal_won(self.curr_player):
            self.view.declare_winner(self.players, self.curr_player)
            self.show_board()
            return True
        # Check if game is tie and declare it.
        self.number_of_moves_left -= 1
        if self.number_of_moves_left == 0:
            self.view.declare_tie()
            self.show_board()
            return True
        return False

    def main(self):
        game_done = False
        while not game_done:
            # Print current board status.
            self.show_board()
            # Get input for next move.
            self.next_move()
            # Check if player won or if game is tie and declare it.
            game_done = self.game_done()
            # Switch player.
            self.switch_player()


if __name__ == '__main__':
    controller = Controller()
    controller.main()
