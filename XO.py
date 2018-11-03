from random import shuffle

# size of board
N = 3

# Utility functions


def print_board(board):

    print()
    print('Board:')
    for line_ in board:
        for item in line_:
            print(item, end='')
        print()
    print()


def check_input_validity(input_type, curr_player):
    not_valid = True
    while not_valid:
        print('{}, please insert the {} number'.format(curr_player, input_type))
        try:
            input_value = int(input())
        except:
            print('{}, please insert a valid {} number'.format(curr_player, input_type))
            continue
        if input_value < 0 or input_value >= N:
            print('{}, please insert a valid {} number'.format(curr_player, input_type))
            continue
        not_valid = False
    return input_value


def check_line(board, line, curr_player, curr_player_symbol, is_win):
    for sym in board[line]:
        if sym != curr_player_symbol:
            is_win = False
            break
    if is_win:
        return declare_win(curr_player)


def check_col(board, col, curr_player, curr_player_symbol, is_win):
    for line in board:
        if line[col] != curr_player_symbol:
            is_win = False
            break
    if is_win:
        return declare_win(curr_player)


def check_main_diagonal(board, line, col, curr_player, curr_player_symbol, is_win):
    if line == col:
        for i in range(N):
            if board[i][i] != curr_player_symbol:
                is_win = False
                break
    else:
        is_win = False

    if is_win:
        return declare_win(curr_player)


def check_opposite_diagonal(board, line, col, curr_player, curr_player_symbol, is_win):
    if line + col == N - 1:
        j = 2
        for i in range(N):
            if j < 0:
                is_win = False
                break
            if board[i][j] != curr_player_symbol:
                is_win = False
                break
            j-=1
    else:
        is_win = False

    if is_win:
        return declare_win(curr_player)


def declare_win(curr_player):
    print('The winner is {}!!!'.format(curr_player))
    print_board(board)
    return(True)


def switch_users(curr_player_, x_player, o_player):
    if curr_player_ == x_player:
        curr_player_ = o_player
        curr_player_sym = 'o'
    else:
        curr_player_ = x_player
        curr_player_sym = 'x'
    return curr_player_, curr_player_sym


# initiate board
board = [['-' for x in range(N)] for y in range(N)]
number_of_moves_left = N * N  # number of moves equals to the number of squares on the board

# initiate players
player_1 = input('Hello! Please enter the first player name\n')
player_2 = input('Please enter the second player name\n')

while player_1 == player_2:
    player_2 = input('Both names are the same. Please choose a different name for second player\n')

# choose 1st player randomly
players = [player_1, player_2]
shuffle(players)
x_player = players[0]
o_player = players[1]
curr_player = x_player
curr_player_symbol = 'x'

print('The X player is {}. You start!'.format(x_player))
print('The O player is {}'.format(o_player))


# main loop of the game

while True:
    # print a fancy board
    print_board(board)

    # get input for next move
    line = check_input_validity('line', curr_player)
    col = check_input_validity('column', curr_player)

    if board[line][col] != '-':
        print('{}, you entered a taken spot on the board'.format(curr_player))
        continue
    else:
        board[line][col] = curr_player_symbol

    # check if win
    if check_line(board, line, curr_player, curr_player_symbol, True):
        break
    if check_col(board, col, curr_player, curr_player_symbol, True):
        break
    if check_main_diagonal(board, line, col, curr_player, curr_player_symbol, True):
        break
    if check_opposite_diagonal(board, line, col, curr_player, curr_player_symbol, True):
        break

    # check if tie
    number_of_moves_left-=1
    if number_of_moves_left == 0:
        print('Result is a tie!')
        print_board(board)
        break

    # switch users
    curr_player, curr_player_symbol = switch_users(curr_player, x_player, o_player)