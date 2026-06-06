from time import time

from script_lib.tsp_utils import build_dist_matrix

def tsp_bkt(cities, time_limit=10.0):
    """TSP Backtracking — finds optimal tour (feasible only for small n)."""
    n = len(cities)
    dist = build_dist_matrix(cities)
    best = {'cost': float('inf'), 'path': None}
    start_time = time()

    def backtrack(path, visited, current_cost):
        if time() - start_time > time_limit:
            return
        if len(path) == n:
            total = current_cost + dist[path[-1]][path[0]]
            if total < best['cost']:
                best['cost'] = total
                best['path'] = path[:]
            return

        for city in range(n):
            if not visited[city]:
                # Branch and bound pruning
                if current_cost + dist[path[-1]][city] < best['cost']:
                    visited[city] = True
                    path.append(city)
                    backtrack(path, visited, current_cost + dist[path[-2]][city])
                    path.pop()
                    visited[city] = False

    visited = [False] * n
    visited[0] = True
    backtrack([0], visited, 0.0)
    elapsed = time() - start_time
    return best['path'], best['cost'], elapsed
