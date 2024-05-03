import copy

from BoardCheck import in_place
from Heuristics import select_current_goal, euclidean_distance, distance_to_goal


def optimize_minmax(distance):
    return distance ** 2


def minmax_solution_score(player, game, blocked_pawns1, heuristics):
    goal1 = select_current_goal(game.get_goal(player), player, game)
    goal2 = select_current_goal(game.get_goal(3 - player), 3 - player, game)
    divider = 100
    if heuristics == euclidean_distance:
        divider = 10000
    board = game.board
    score = 0
    for i in range(16):
        for j in range(16):
            if board[i][j] == player:
                if (i, j) in blocked_pawns1:
                    score -= 1000
                score += optimize_minmax(heuristics((i, j), goal1, game)) - (optimize_minmax(heuristics((i, j), goal2, game))/divider)
    return score


def minimax(depth, isMaximizingPlayer, player, game, blocked_pawns1, blocked_pawns2, heuristics):
    if depth == 0 or game.is_game_over():
        return minmax_solution_score(1, game, blocked_pawns1, heuristics), None

    if isMaximizingPlayer:
        maxEval = float('inf')
        bestMove = None
        board_before = copy.deepcopy(game.board)
        for move in game.generate_all_possible_moves(1, blocked_pawns1):  # Assuming player 1 is maximizing
            game.make_move(1, move)
            blocked_pawns1 = in_place(game.board, 1)
            eval, _ = minimax(depth - 1, False, player, game, blocked_pawns1, blocked_pawns2, heuristics)
            if eval < maxEval:
                maxEval = eval
                bestMove = move
            game.undo_move(board_before)
        return maxEval, bestMove

    else:  # Minimizing player
        minEval = float('-inf')
        bestMove = None
        board_before = copy.deepcopy(game.board)
        for move in game.generate_all_possible_moves(2, blocked_pawns2):  # Assuming player 2 is minimizing
            game.make_move(2, move)
            blocked_pawns2 = in_place(game.board, 2)
            eval, _ = minimax(depth - 1, True, player, game, blocked_pawns1, blocked_pawns2, heuristics)
            if eval > minEval:
                minEval = eval
                bestMove = move
            game.undo_move(board_before)
        return minEval, bestMove




def minimax_with_alpha_beta(depth, isMaximizingPlayer, player, game, alpha, beta, blocked_pawns1, blocked_pawns2, heuristics):
    if depth == 0 or game.is_game_over():
        return minmax_solution_score(1, game, blocked_pawns1, heuristics), None

    board_before = copy.deepcopy(game.board)
    if isMaximizingPlayer:
        maxEval = float('inf')
        bestMove = None
        for move in game.generate_all_possible_moves(1, blocked_pawns1):
            game.make_move(1, move)
            blocked_pawns1 = in_place(game.board, 1)
            eval, _ = minimax_with_alpha_beta(depth - 1, False, player, game, alpha, beta, blocked_pawns1, blocked_pawns2, heuristics)
            game.undo_move(board_before)
            if eval < maxEval:
                maxEval = eval
                bestMove = move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return maxEval, bestMove
    else:
        minEval = float('-inf')
        bestMove = None
        for move in game.generate_all_possible_moves(2, blocked_pawns2):
            game.make_move(2, move)
            blocked_pawns2 = in_place(game.board, 2)
            eval, _ = minimax_with_alpha_beta(depth - 1, True, player, game, alpha, beta, blocked_pawns1, blocked_pawns2, heuristics)
            game.undo_move(board_before)
            if eval > minEval:
                minEval = eval
                bestMove = move
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return minEval, bestMove