from time import time
import random

from script_lib.tsp_utils import build_dist_matrix, tour_cost


def ox_crossover(p1, p2):
    """Order crossover for TSP permutations."""
    n = len(p1)
    a, b = sorted(random.sample(range(n), 2))
    child = [-1] * n
    child[a:b + 1] = p1[a:b + 1]
    fill = [city for city in p2 if city not in child]
    idx = 0

    for i in range(n):
        if child[i] == -1:
            child[i] = fill[idx]
            idx += 1

    return child


def mutate_swap(individual, rate=0.02):
    mutated = individual[:]
    for i in range(len(mutated)):
        if random.random() < rate:
            j = random.randint(0, len(mutated) - 1)
            mutated[i], mutated[j] = mutated[j], mutated[i]
    return mutated


def tournament_select(population, costs, k=5):
    candidates = random.sample(range(len(population)), min(k, len(population)))
    best = min(candidates, key=lambda i: costs[i])
    return population[best][:]


def tsp_genetic(cities, pop_size=150, max_gen=1000, mutation_rate=0.02):
    """Genetic Algorithm for TSP."""
    n = len(cities)
    dist = build_dist_matrix(cities)
    start_time = time()

    population = [list(range(n)) for _ in range(pop_size)]
    for individual in population:
        random.shuffle(individual)

    best_path = None
    best_cost = float("inf")

    for _ in range(max_gen):
        costs = [tour_cost(individual, dist) for individual in population]
        best_idx = costs.index(min(costs))
        if costs[best_idx] < best_cost:
            best_cost = costs[best_idx]
            best_path = population[best_idx][:]

        new_population = [best_path[:]]
        while len(new_population) < pop_size:
            p1 = tournament_select(population, costs)
            p2 = tournament_select(population, costs)
            child = ox_crossover(p1, p2)
            child = mutate_swap(child, mutation_rate)
            new_population.append(child)
        population = new_population

    elapsed = time() - start_time
    return best_path, best_cost, elapsed
