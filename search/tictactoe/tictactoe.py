"""
Tic Tac Toe Player
"""

import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """

    # initial starting point of the game
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """

    # X is returned in the initial state
    if board == initial_state():
        return 'X'

    x_counter = 0
    o_counter = 0

    # play has commenced, return current player
    for i in board:
        for j in i:
            if j == 'X':
                x_counter += 1
            if j == 'O':
                o_counter += 1

    # X goes first so if O less moves than X it is O's turn
    if x_counter > o_counter:
        return 'O'

    # if even plays, X
    return 'X'


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    # can only take an action once so set
    actions = set()

    # enumerate actions so as to carry index of action
    # add available moves to set
    for i_idx, i in enumerate(board):
        for j_idx, j in enumerate(i):
            if j == EMPTY:
                actions.add((i_idx, j_idx))

    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    # make a copy of the board so as to not mess with the actual play board
    board_analysis = copy.deepcopy(board)

    # return an exception if the move indexes an element (play square) outside the list
    if action[0] > 2 or action[1] > 2 or action[0] < 0 or action[1] < 0:
        raise Exception('Out of bounds move!')

    # if the move places a player on an already occupies play square, raise exception
    if board_analysis[action[0]][action[1]] != EMPTY:
        raise Exception('Illegal move!')
    # otherwise play move
    else:
        board_analysis[action[0]][action[1]] = player(board)

    # return the result of the move
    return board_analysis


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    # there is no winner if the board is in the original game state
    if board == initial_state():
        return None

    # find winning horizontal
    for row in board:
        if row[0] != EMPTY:
            if row[0] == row[1] and row[1] == row[2]:
                return row[0]

    # find winning vertical
    for column in range(0, 3):
        if board[0][column] != EMPTY:
            if board[0][column] == board[1][column] and board[1][column] == board[2][column]:
                return board[0][column]

    # find winning diagonally
    # top left to bottom right
    if board[0][0] != EMPTY:
        if board[0][0] == board[1][1] and board[1][1] == board[2][2]:
            return board[0][0]

    # top right to bottom left
    if board[0][2] != EMPTY:
        if board[0][2] == board[1][1] and board[1][1] == board[2][0]:
            return board[0][2]

    # no winner found
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    # game is not over if the game is in the original state
    if board == initial_state():
        return False

    # game is over if the winner function returns true - i.e. there is a winner
    if winner(board) != None:
        return True

    # if there is no winner, check that there is not a tie
    if not winner(board):
        for i in board:
            # if there are EMPTY play squares left, the game is still in play
            if EMPTY in i:
                return False
        # no play squares left, game is tied
        return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    # returns the utility of the game
    # as this is an adversarial game of two players, -1, 0 and 1 are used to represent the
    # 3 possible outcomes
    result = winner(board)
    # maximising player is X (1)
    if result == 'X':
        return 1
    # minimising player is O (-1)
    if result == 'O':
        return -1
    # tie (0)
    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    # if the game is terminal, return None as per specs
    if terminal(board):
        return None

    # maximising players max-value function of the minimax algo
    def __max_value(state):

        # if the board is terminal, return the utility
        if terminal(state):
            response = (utility(state), None)
            return response

        # minimax algo
        v = -float('inf')
        best_action = None
        # iterate actions and apply minimax
        for action in actions(state):
            _v = __min_value(result(state, action))[0]
            if _v > v:
                best_action = action
                v = _v
        # returns the optimum move for the maximising player
        response = (v, best_action)
        return response

    # minimising players min-value function of the minimax algo
    def __min_value(state):

        # if the board is terminal, return the utility
        if terminal(state):
            response = (utility(state), None)
            return response

        # minimax algo
        v = float('inf')
        best_action = None
        # iterate actions and apply minimax
        for action in actions(state):
            _v = __max_value(result(state, action))[0]
            if _v < v:
                best_action = action
                v = _v
        # returns the optimum move for the maximising player
        response = (v, best_action)
        return response

    # making a copy of the board - appears to not be required, but doing as best practice
    board_copy = copy.deepcopy(board)

    # determines whether or not to apply minimax in favour of the maximising or minimising player
    if player(board) == 'X':
        return __max_value(board_copy)[1]

    elif player(board) == 'O':
        return __min_value(board_copy)[1]
