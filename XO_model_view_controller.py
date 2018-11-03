from random import randint
from collections import namedtuple

# Size of board.
N = 3


class Model:
    def __init__(self):
        self.board = [[None for x in range(N)] for y in range(N)]

    def get_board_status(self):
        return self.board

    def update_board(self, line, col, players, curr_player):
        if self.board[line][col] is not None:
            return False
        else:
            self.board[line][col] = players[curr_player].symbol
            return True

    def line_won(self, players, curr_player):
        for line in self.board:
            if all(x == players[curr_player].symbol for x in line):
                return True
        return False

    def col_won(self, players, curr_player):
        for col in range(N):
            if all(line[col] == players[curr_player].symbol for line in self.board):
                return True
        return False

    def diagonal_won(self, players, curr_player):
        # Main diagonal.
        if all(self.board[index][index] == players[curr_player].symbol for index in range(N)):
            return True
        # Opposite diagonal.
        if all(self.board[index][N-1-index] == players[curr_player].symbol for index in range(N)):
            return True
        return False


class View:
    def __init__(self):
        pass

    def print_board(self, board):
        print()
        print('Board:')
        for line in board:
            for item in line:
                if item is None:
                    print('-', end='')
                else:
                    print(item, end='')
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
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.players, self.curr_player = self.initiate_players()
        self.number_of_moves_left = N * N  # Equals to number of squares on board.

    def initiate_players(self):
        Player = namedtuple('Player', 'name symbol')
        x_player_name = input('Enter X player name\n')
        o_player_name = input('Enter O player name\n')
        while x_player_name == o_player_name:
            o_player_name = input('Both names are the same. Choose a different name for O player\n')
        players = [Player(name=x_player_name, symbol='x'), Player(name=o_player_name, symbol='o')]
        curr_player = randint(0, 1)
        return players, curr_player

    def show_board(self):
        board = self.model.get_board_status()
        self.view.print_board(board)

    def get_input(self):
        line = self.is_input_valid('line')
        col = self.is_input_valid('column')
        updated = self.model.update_board(line, col, self.players, self.curr_player)
        if not updated:
            print(f'{self.players[self.curr_player].name}, you entered a taken spot on the board, try again')
            return False
        return True

    def is_input_valid(self, input_type):
        valid_input = False
        while not valid_input:
            print(f'{self.players[self.curr_player].name}, please insert the {input_type} number')
            try:
                input_value = int(input())
            except ValueError:
                print(f'{self.players[self.curr_player].name}, input not valid')
                continue
            if input_value < 0 or input_value >= N:
                print(f'{self.players[self.curr_player].name}, insert a {input_type} num between 0 to {N-1}, including')
            else:
                valid_input = True
        return input_value

    def switch_player(self):
        self.curr_player = self.curr_player ^ 1

    def is_win(self):
        if self.model.line_won(self.players, self.curr_player) \
                or self.model.col_won(self.players, self.curr_player) \
                or self.model.diagonal_won(self.players, self.curr_player):
            self.view.declare_winner(self.players, self.curr_player)
            self.show_board()
            return True
        return False

    def is_tie(self):
        self.number_of_moves_left -= 1
        if self.number_of_moves_left == 0:
            self.view.declare_tie()
            self.show_board()
            return True
        return False

    def main(self):
        game_won = False
        game_tie = False
        while not (game_won or game_tie):
            # Print current board status.
            controller.show_board()
            # Get input for next move.
            got_input_successfully = controller.get_input()
            while not got_input_successfully:
                got_input_successfully = controller.get_input()
            # Check if player won.
            game_won = controller.is_win()
            # Check if tie.
            game_tie = controller.is_tie()
            # Switch player.
            controller.switch_player()


controller = Controller(Model(), View())
controller.main()
