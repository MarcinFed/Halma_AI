import copy

from BoardCheck import in_place
from Heuristics import select_current_goal, euclidean_distance, distance_to_goal


# Function to optimize the heuristic evaluation by squaring the distance
def optimize_minmax(distance):
    return distance ** 2


# Function to calculate the heuristic score of a given game state
def minmax_solution_score(player, game, blocked_pawns1, heuristics_player1, heuristics_player2):
    goal1 = select_current_goal(game.get_goal(player), player, game)
    goal2 = select_current_goal(game.get_goal(3 - player), 3 - player, game)
    divider = 100  # Default divisor for heuristic normalization
    if heuristics_player1 == euclidean_distance:
        divider = 10000  # Adjusting for Euclidean distance scaling

    board = game.board
    score = 0

    # Iterate through the board to compute the heuristic evaluation
    for i in range(16):
        for j in range(16):
            if board[i][j] == player:
                if (i, j) in blocked_pawns1:
                    score -= 1000  # Penalize blocked pawns

                # Compute heuristic value based on selected heuristics
                score += optimize_minmax(heuristics_player1((i, j), goal1, game)) - (
                        optimize_minmax(heuristics_player2((i, j), goal2, game)) / divider)
    return score


# Standard Minimax algorithm for game decision-making
def minimax(depth, isMaximizingPlayer, player, game, blocked_pawns1, blocked_pawns2, heuristics_player1,
            heuristics_player2):
    iteration_counter = 0

    # Base case: return heuristic evaluation if depth is 0 or game is over
    if depth == 0 or game.is_game_over():
        return minmax_solution_score(1, game, blocked_pawns1, heuristics_player1,
                                     heuristics_player2), None, iteration_counter

    if isMaximizingPlayer:
        maxEval = float('inf')  # Initialize max evaluation to a high value
        bestMove = None
        board_before = copy.deepcopy(game.board)  # Store the board state before making moves

        # Iterate through all possible moves for player 1 (maximizing player)
        for move in game.generate_all_possible_moves(1, blocked_pawns1):
            game.make_move(1, move)
            blocked_pawns1 = in_place(game.board, 1)
            eval, _, child_counter = minimax(depth - 1, False, player, game, blocked_pawns1, blocked_pawns2,
                                             heuristics_player1, heuristics_player2)
            iteration_counter += child_counter + 1

            if eval < maxEval:
                maxEval = eval
                bestMove = move

            game.undo_move(board_before)  # Restore previous board state
        return maxEval, bestMove, iteration_counter

    else:  # Minimizing player
        minEval = float('-inf')  # Initialize min evaluation to a low value
        bestMove = None
        board_before = copy.deepcopy(game.board)

        # Iterate through all possible moves for player 2 (minimizing player)
        for move in game.generate_all_possible_moves(2, blocked_pawns2):
            game.make_move(2, move)
            blocked_pawns2 = in_place(game.board, 2)
            eval, _, child_counter = minimax(depth - 1, True, player, game, blocked_pawns1, blocked_pawns2,
                                             heuristics_player1, heuristics_player2)
            iteration_counter += child_counter + 1

            if eval > minEval:
                minEval = eval
                bestMove = move

            game.undo_move(board_before)  # Restore previous board state
        return minEval, bestMove, iteration_counter


# Minimax algorithm with Alpha-Beta Pruning to optimize decision-making
def minimax_with_alpha_beta(depth, isMaximizingPlayer, player, game, alpha, beta, blocked_pawns1, blocked_pawns2,
                            heuristics_player1, heuristics_player2):
    iteration_counter = 0

    # Base case: return heuristic evaluation if depth is 0 or game is over
    if depth == 0 or game.is_game_over():
        return minmax_solution_score(1, game, blocked_pawns1, heuristics_player1,
                                     heuristics_player2), None, iteration_counter

    board_before = copy.deepcopy(game.board)  # Store board state before moves

    if isMaximizingPlayer:
        maxEval = float('inf')
        bestMove = None

        # Iterate through all possible moves for player 1 (maximizing player)
        for move in game.generate_all_possible_moves(1, blocked_pawns1):
            game.make_move(1, move)
            blocked_pawns1 = in_place(game.board, 1)
            eval, _, child_counter = minimax_with_alpha_beta(depth - 1, False, player, game, alpha, beta,
                                                             blocked_pawns1, blocked_pawns2, heuristics_player1,
                                                             heuristics_player2)
            iteration_counter += child_counter + 1
            game.undo_move(board_before)

            if eval < maxEval:
                maxEval = eval
                bestMove = move

            alpha = max(alpha, eval)  # Update alpha value
            if beta <= alpha:
                break  # Prune the remaining branches
        return maxEval, bestMove, iteration_counter
    else:
        minEval = float('-inf')
        bestMove = None

        # Iterate through all possible moves for player 2 (minimizing player)
        for move in game.generate_all_possible_moves(2, blocked_pawns2):
            game.make_move(2, move)
            blocked_pawns2 = in_place(game.board, 2)
            eval, _, child_counter = minimax_with_alpha_beta(depth - 1, True, player, game, alpha, beta, blocked_pawns1,
                                                             blocked_pawns2, heuristics_player1, heuristics_player2)
            iteration_counter += child_counter + 1
            game.undo_move(board_before)

            if eval > minEval:
                minEval = eval
                bestMove = move

            beta = min(beta, eval)  # Update beta value
            if beta <= alpha:
                break  # Prune the remaining branches
        return minEval, bestMove, iteration_counter
