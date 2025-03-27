import time

from HalmaGame import start_game
from Heuristics import euclidean_distance, manhattan_distance, chebyshev_distance, distance_and_jumps

if __name__ == '__main__':
    # Define the list of heuristic functions to be used
    heuristics = [euclidean_distance, manhattan_distance, chebyshev_distance, distance_and_jumps]
    # Define the list of depths to be used in the game
    depths = [1, 2]
    # Define the list of alpha-beta pruning options
    alpha_beta_values = [True, False]

    # Initialize an empty list to store the results
    results = []

    # Iterate over all combinations of heuristic functions, depths, and alpha-beta pruning options
    for heuristics_player1 in heuristics:
        for heuristics_player2 in heuristics:
            for depth in depths:
                for alpha_beta in alpha_beta_values:
                    # Record the start time of the game
                    start_time = time.time()
                    # Start the game with the current combination of parameters
                    rounds, visited_nodes = start_game(heuristics_player1, heuristics_player2, alpha_beta, depth)
                    # Record the end time of the game
                    end_time = time.time()
                    # Append the results of the game to the results list
                    results.append({
                        "heuristics_player1": heuristics_player1.__name__,
                        "heuristics_player2": heuristics_player2.__name__,
                        "depth": depth,
                        "alpha_beta": alpha_beta,
                        "time": end_time - start_time,
                        "rounds": rounds,
                        "visited_nodes": visited_nodes
                    })

    # Print the results of all games
    for result in results:
        print(f"Heurystyka gracza 1: {result['heuristics_player1']}, Heurystyka gracza 2: {result['heuristics_player2']}, Głębokość: {result['depth']}, Alphabeta: {result['alpha_beta']}")
        print(f"Czas działania gry: {result['time']} sekund")
        print(f"Rundy: {result['rounds']}")
        print(f"Odwiedzone węzły: {result['visited_nodes']}")
        print("______________________________________________________________________________________________________________________")
        print("\n")