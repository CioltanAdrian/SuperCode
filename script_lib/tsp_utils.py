import math


def euclidean(c1, c2):
    return math.sqrt((c1[0] - c2[0]) ** 2 + (c1[1] - c2[1]) ** 2)


def build_dist_matrix(cities):
    n = len(cities)
    dist = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            dist[i][j] = euclidean(cities[i], cities[j])
    return dist


def tour_cost(path, dist):
    n = len(path)
    return sum(dist[path[i]][path[(i + 1) % n]] for i in range(n))
