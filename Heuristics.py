import random


def euclidean_distance(move, goal, game):
    return ((move[0] - goal[0])**2 + (move[1] - goal[1])**2)**0.5


def manhattan_distance(move, goal, game):
    return abs(move[0] - goal[0]) + abs(move[1] - goal[1])


def chebyshev_distance(move, goal, game):
    return max(abs(move[0] - goal[0]), abs(move[1] - goal[1]))


def distance_and_jumps(move, goal, game):
    manhattan = manhattan_distance(move, goal, game)
    jumps_potential = 0

    jump_directions = [(2, 0), (0, 2), (-2, 0), (0, -2)]

    for dx, dy in jump_directions:
        inter_x, inter_y = move[0] + dx // 2, move[1] + dy // 2
        jump_x, jump_y = move[0] + dx, move[1] + dy
        if 0 <= jump_x < 16 and 0 <= jump_y < 16 and 0 <= inter_x < 16 and 0 <= inter_y < 16:
            if game.board[inter_x][inter_y] != 0 and game.board[jump_x][jump_y] == 0:
                jumps_potential += 1

    effective_distance = optimize(manhattan) - jumps_potential
    return effective_distance


def optimize(distance):
    return distance ** 2


def is_blocked(field, board):
    return board[field[0]][field[1]] != 0


def select_current_goal(goals, player, game):
    goal = ()
    distance = 0
    for field in goals:
        if player == 1:
            curr_distance = euclidean_distance(field, (0, 0), game)
            if curr_distance > distance:
                distance = curr_distance
                goal = field
        else:
            curr_distance = euclidean_distance(field, (15, 15), game)
            if curr_distance > distance:
                distance = curr_distance
                goal = field
    return goal


def distance_to_goal(move, player, game, current_field, heuristics):
    goal = select_current_goal(game.get_goal(player), player, game)
    board = game.board
    distance_sum = 0
    for i in range(16):
        for j in range(16):
            if board[i][j] == player and (i, j) != current_field:
                distance_sum += optimize(heuristics((i, j), goal, game))
    distance_sum += (optimize(heuristics(move, goal, game))
                      + random.randint(0, 20)
                     )
    return distance_sum