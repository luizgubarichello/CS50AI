"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    qty_X = 0
    qty_O = 0

    for row in board:
        for position in row:
            if position == X:
                qty_X += 1
            elif position == O:
                qty_O += 1

    if qty_X == qty_O:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions_list = []

    for row in range(len(board)):
        for collumn in range(len(board[row])):
            if board[row][collumn] == EMPTY:
                actions_list.append((row, collumn))

    return actions_list


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    new_board = copy.deepcopy(board)
    player_to_move = player(board=board)

    if player_to_move == X:
        if board[action[0]][action[1]] == EMPTY:
            new_board[action[0]][action[1]] = X
            return new_board
        raise Exception('Illegal move')
    else:
        if board[action[0]][action[1]] == EMPTY:
            new_board[action[0]][action[1]] = O
            return new_board
        raise Exception('Illegal move')


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Check rows
    for row in board:
        row_set = {i for i in row}
        if len(row_set) == 1:
            for value in row_set:
                return value
    
    # Check collumns
    for c in range(len(board)):
        column_set = {row[c] for row in board}
        if len(column_set) == 1:
            for value in column_set:
                return value
    
    # Check diagonals
    diagonal1_set = {board[p][p] for p in range(len(board))}
    if len(diagonal1_set) == 1:
        for value in diagonal1_set:
            return value
    diagonal2_set = {board[-p-1][p] for p in range(len(board))}
    if len(diagonal2_set) == 1:
        for value in diagonal2_set:
            return value
    
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board=board) != None:
        return True
    
    for row in board:
        if EMPTY in row:
            return False

    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    b_winner = winner(board=board)
    if b_winner == X:
        return 1
    elif b_winner == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board=board):
        return None
    
    player_to_move = player(board=board)

    if player_to_move == X:
        return max_value(board=board)[1]
    else:
        return min_value(board=board)[1]


def max_value(board):
    v = float('-inf')
    best_action = set()

    if terminal(board=board):
        return [utility(board=board), best_action]
    
    actions_list = actions(board=board)
    for action in actions_list:
        aux = max(v, min_value(result(board=board, action=action))[0])
        if aux > v:
            v = aux
            best_action = action
        
    return [v, best_action]


def min_value(board):
    v = float('inf')
    best_action = set()

    if terminal(board=board):
        return [utility(board=board), best_action]
    
    actions_list = actions(board=board)
    for action in actions_list:
        aux = min(v, max_value(result(board=board, action=action))[0])
        if aux < v:
            v = aux
            best_action = action

    return [v, best_action]