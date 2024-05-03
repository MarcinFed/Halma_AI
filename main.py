from HalmaGame import start_game
from Heuristics import euclidean_distance, manhattan_distance, chebyshev_distance, distance_and_jumps

if __name__ == '__main__':
    start_game(euclidean_distance, distance_and_jumps, True, 2)