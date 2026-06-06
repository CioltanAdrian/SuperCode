from time import time

from script_lib.tsp_nn import nearest_neighbor
from script_lib.tsp_utils import build_dist_matrix, tour_cost


def two_opt_swap(path, i, k):
    return path[:i] + path[i:k + 1][::-1] + path[k + 1:]


def hill_climbing_2opt(cities, max_iter=5000):
    """Hill Climbing using 2-opt moves for TSP."""
    n = len(cities)
    dist = build_dist_matrix(cities)
    start_time = time()

    path, cost, _ = nearest_neighbor(cities)
    improved = True
    iterations = 0

    while improved and iterations < max_iter:
        improved = False
        for i in range(1, n - 1):
            for k in range(i + 1, n):
                new_path = two_opt_swap(path, i, k)
                new_cost = tour_cost(new_path, dist)
                if new_cost < cost - 1e-10:
                    path = new_path
                    cost = new_cost
                    improved = True
        iterations += 1

    elapsed = time() - start_time
    return path, cost, elapsed
