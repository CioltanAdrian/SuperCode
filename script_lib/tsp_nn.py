from time import time

from script_lib.tsp_utils import build_dist_matrix, tour_cost


def nearest_neighbor(cities, start=0):
    """Nearest Neighbor greedy heuristic for TSP."""
    n = len(cities)
    dist = build_dist_matrix(cities)
    start_time = time()

    visited = [False] * n
    path = [start]
    visited[start] = True

    for _ in range(n - 1):
        current = path[-1]
        nearest = min(
            (city for city in range(n) if not visited[city]),
            key=lambda city: dist[current][city],
        )
        path.append(nearest)
        visited[nearest] = True

    cost = tour_cost(path, dist)
    elapsed = time() - start_time
    return path, cost, elapsed
