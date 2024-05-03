import copy
import sys

from BoardCheck import in_place
from Heuristics import distance_to_goal, euclidean_distance, manhattan_distance, chebyshev_distance, distance_and_jumps
from Minimax import minimax, minimax_with_alpha_beta

BOARD = 'board.txt'


class HalmaGame:

    player_1_goal = [(15, 15), (15, 14), (15, 13), (15, 12), (15, 11),
                     (14, 15), (14, 14), (14, 13), (14, 12), (14, 11),
                     (13, 15), (13, 14), (13, 13), (13, 12),
                     (12, 15), (12, 14), (12, 13),
                     (11, 15), (11, 14)]
    player_2_goal = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4),
                     (1, 0), (1, 1), (1, 2), (1, 3), (1, 4),
                     (2, 0), (2, 1), (2, 2), (2, 3),
                     (3, 0), (3, 1), (3, 2),
                     (4, 0), (4, 1)]

    def __init__(self, board=None):
        if board is None:
            self.board = [[0] * 16 for _ in range(16)]
            with open(BOARD, 'r') as file:
                lines = file.readlines()
                row = -1
                for line in lines:
                    row += 1
                    line = line.strip()
                    column = -1
                    for char in line:
                        column += 1
                        self.board[row][column] = int(char)
        else:
            self.board = board
        self.board_history = []
        self.board_history.append(self.board)


    def get_board(self):
        return self.board

    def get_player_goal_fields(self, player):
        if player == 1:
            return self.player_1_goal
        else:
            return self.player_2_goal

    def undo_move(self, board):
        self.board = copy.deepcopy(board)


    def print_board(self, blocked_pawns1, blocked_pawns2):
        print("\t", end="  ")
        for col in range(16):
            if col < 9:
                print(col, end="  ")
            else:
                print(col, end=" ")
        print('\t')
        for col in range(16):
            if col == 0:
                print("\t", end=" ")
            print(" _ ", end="")
        print()
        # Print row and board cells
        for row in range(16):
            print(row, "\t|", sep="", end=" ")  # Add row number with pipe separator
            for col in range(16):
                cell = self.board[row][col]
                pos = (row, col)
                if pos in blocked_pawns1 or pos in blocked_pawns2:
                    print(f"\033[93m{cell}\033[0m", end='  ')  # Yellow or another neutral color for blocked pawns
                elif cell == 1:
                    print(f"\033[92m{cell}\033[0m", end='  ')  # Green for player 1
                elif cell == 2:
                    print(f"\033[91m{cell}\033[0m", end='  ')  # Red for player 2
                else:
                    print(cell, end='  ')
            print()
        print()

    def generate_all_possible_moves(self, player, blocked_pawns):
        no_jump_directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        jump_directions = [(2, 0), (0, 2), (-2, 0), (0, -2)]
        moves = []

        def add_jump_moves(start_i, start_j, end_i, end_j, visited):
            jumps = [(start_i, start_j, end_i, end_j)]
            for dx, dy in jump_directions:
                ni, nj = end_i + dx, end_j + dy
                pi, pj = end_i + dx // 2, end_j + dy // 2
                if 0 <= ni < 16 and 0 <= nj < 16 and (ni, nj) not in visited:
                    if self.board[ni][nj] == 0 and self.board[pi][pj] != 0:
                        visited.add((ni, nj))
                        jumps.extend(add_jump_moves(start_i, start_j, ni, nj, visited))
            return jumps

        for i in range(16):
            for j in range(16):
                if self.board[i][j] == player and (i, j) not in blocked_pawns:
                    # Direct moves
                    for dx, dy in no_jump_directions:
                        ni, nj = i + dx, j + dy
                        if 0 <= ni < 16 and 0 <= nj < 16 and self.board[ni][nj] == 0:
                            moves.append(((i, j), (ni, nj)))
                    # Jump moves
                    visited = set([(i, j)])
                    jump_moves = add_jump_moves(i, j, i, j, visited)
                    final_moves = set()
                    for start_i, start_j, end_i, end_j in jump_moves:
                        if (start_i, start_j) != (end_i, end_j):
                            final_moves.add(((start_i, start_j), (end_i, end_j)))
                    moves.extend(final_moves)
        return list(moves)

    def make_move(self, player, move):
        start, end = move
        self.board[end[0]][end[1]] = player
        self.board[start[0]][start[1]] = 0
        self.board_history.append(self.board)
        return self.board

    def get_goal(self, player):
        goals = []
        if player == 1:
            for field in self.player_1_goal:
                if self.board[field[0]][field[1]] == 0:
                    goals.append(field)
            if not goals:
                return [(15, 15)]
            return goals
        else:
            for field in self.player_2_goal:
                if self.board[field[0]][field[1]] == 0:
                    goals.append(field)
            if not goals:
                return [(0, 0)]
            return goals

    def checkPlayer1(self):
        for field in self.player_1_goal:
            if self.board[field[0]][field[1]] != 1:
                return False
        return True

    def checkPlayer2(self):
        for field in self.player_2_goal:
            if self.board[field[0]][field[1]] != 2:
                return False
        return True

    def is_game_over(self):
        return self.checkPlayer1() or self.checkPlayer2()


def player1_turn(game, blocked_pawns1, blocked_pawns2, heuristics, depth, alphabeta):
    print('Player 1')
    board_before = copy.deepcopy(game.board)
    if alphabeta:
        _, best_move = minimax_with_alpha_beta(depth, True, 1, game, float('-inf'), float('inf'), copy.deepcopy(blocked_pawns1), copy.deepcopy(blocked_pawns2), heuristics)
    else:
        _, best_move = minimax(depth, True, 1, game, copy.deepcopy(blocked_pawns1), copy.deepcopy(blocked_pawns2), heuristics)
    game.undo_move(board_before)
    if best_move:
        print(f"Player 1 moves from {best_move[0]} to {best_move[1]}")
        game.make_move(1, best_move)
    blocked_pawns1 = in_place(game.board, 1)
    game.print_board(blocked_pawns1, blocked_pawns2)
    if game.is_game_over():
        print("Player 1 wins!")
        return sys.exit(0)
    return blocked_pawns1


def player2_turn(game, blocked_pawns1, blocked_pawns2, heuristics):
    moves_player2 = game.generate_all_possible_moves(2, blocked_pawns2)
    options = []
    for move in moves_player2:
        options.append((move, distance_to_goal(move[1], 2, game, move[0], heuristics)))
    options = sorted(options, key=lambda x: x[1])
    print("Player 2")
    print(options[0][1])
    print('chosen move: ', options[0][0])
    game.make_move(2, options[0][0])
    blocked_pawns2 = in_place(game.board, 2)
    game.print_board(blocked_pawns1, blocked_pawns2)
    if game.is_game_over():
        print("Player 2 wins!")
        return sys.exit(0)
    return blocked_pawns2


def start_game(heuristics, alphabeta=False, depth=2):
    game = HalmaGame()
    blocked_pawns1 = []
    blocked_pawns2 = []
    while not game.is_game_over():
        blocked_pawns1 = player1_turn(game, blocked_pawns1, blocked_pawns2, heuristics, depth, alphabeta)
        blocked_pawns2 = player2_turn(game, blocked_pawns1, blocked_pawns2, heuristics)