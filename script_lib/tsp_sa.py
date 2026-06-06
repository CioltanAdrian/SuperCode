from time import time
import math
import random

from script_lib.tsp_utils import build_dist_matrix, tour_cost


def tsp_simulated_annealing(cities, temp=1000.0, cooling_rate=0.99, T_end=0.01, max_iter=200000):
    """Simulated Annealing metaheuristic for TSP adaptat pentru GUI."""
    # Mapăm argumentele din interfață către variabilele folosite deja în algoritmul tău
    T_start = temp
    cooling = cooling_rate

    n = len(cities)
    dist = build_dist_matrix(cities)
    start_time = time()

    path = list(range(n))
    random.shuffle(path)
    current_cost = tour_cost(path, dist)
    best_path = path[:]
    best_cost = current_cost

    temperature = T_start
    for _ in range(max_iter):
        if temperature < T_end:
            break

        i, j = sorted(random.sample(range(n), 2))
        new_path = path[:i] + path[i:j + 1][::-1] + path[j + 1:]
        new_cost = tour_cost(new_path, dist)
        delta = new_cost - current_cost

        if delta < 0 or random.random() < math.exp(-delta / temperature):
            path = new_path
            current_cost = new_cost
            if current_cost < best_cost:
                best_cost = current_cost
                best_path = path[:]

        temperature *= cooling

    elapsed = time() - start_time
    return best_path, best_cost, elapsed
