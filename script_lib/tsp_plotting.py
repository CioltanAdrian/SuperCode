import matplotlib.pyplot as plt
import random
from time import time

from script_lib.tsp_bkt import tsp_bkt
from script_lib.tsp_nn import nearest_neighbor
from script_lib.tsp_hc import hill_climbing_2opt
from script_lib.tsp_sa import tsp_simulated_annealing
from script_lib.tsp_ga import ox_crossover, mutate_swap, tournament_select, tsp_genetic
from script_lib.tsp_utils import build_dist_matrix, tour_cost


def generate_random_cities(n, seed=42):
    random.seed(seed)
    return [(random.uniform(0, 100), random.uniform(0, 100)) for _ in range(n)]


def draw_tour(ax, cities, path, title="", color='#3498db'):
    n = len(cities)
    xs = [cities[i][0] for i in path] + [cities[path[0]][0]]
    ys = [cities[i][1] for i in path] + [cities[path[0]][1]]
    ax.plot(xs, ys, '-o', color=color, markersize=6, linewidth=1.5, alpha=0.85)
    ax.scatter([c[0] for c in cities], [c[1] for c in cities],
               color='#e74c3c', s=40, zorder=5)
    for idx, city in enumerate(cities):
        ax.annotate(str(idx), city, textcoords="offset points",
                    xytext=(4, 4), fontsize=7, color='#2c3e50')
    ax.set_title(title, fontsize=10, fontweight='bold')
    ax.set_xlim(-5, 105)
    ax.set_ylim(-5, 105)
    ax.axis('off')


def plot_tsp_solutions(n_cities=12, seed=42):
    cities = generate_random_cities(n_cities, seed)

    algorithms = []

    if n_cities <= 12:
        path, cost, t = tsp_bkt(cities, time_limit=15.0)
        algorithms.append(('BKT (Optimal)', path, cost, t, '#8e44ad'))

    path, cost, t = nearest_neighbor(cities)
    algorithms.append(('Nearest Neighbor', path, cost, t, '#e67e22'))

    path, cost, t = hill_climbing_2opt(cities)
    algorithms.append(('Hill Climbing (2-opt)', path, cost, t, '#3498db'))

    path, cost, t = tsp_simulated_annealing(cities)
    algorithms.append(('Simulated Annealing', path, cost, t, '#2ecc71'))

    path, cost, t = tsp_genetic(cities)
    algorithms.append(('Genetic Algorithm', path, cost, t, '#e74c3c'))

    ncols = len(algorithms)
    fig, axes = plt.subplots(1, ncols, figsize=(4 * ncols, 5))
    if ncols == 1:
        axes = [axes]
    fig.suptitle(f'TSP Solutions Comparison ({n_cities} cities)', fontsize=14, fontweight='bold')

    for ax, (name, path, cost, t, color) in zip(axes, algorithms):
        draw_tour(ax, cities, path,
                  title=f'{name}\nCost: {cost:.1f} | Time: {t:.3f}s',
                  color=color)

    plt.tight_layout()
    plt.show()


def _simulated_annealing_history(cities, T_start=1000.0, T_end=0.01,
                                 cooling=0.9995, max_iter=10000,
                                 record_every=250):
    n = len(cities)
    dist = build_dist_matrix(cities)
    path = list(range(n))
    random.shuffle(path)
    current_cost = tour_cost(path, dist)
    best_cost = current_cost
    temperature = T_start
    history = []

    for iteration in range(max_iter):
        if temperature < T_end:
            break

        i, j = sorted(random.sample(range(n), 2))
        new_path = path[:i] + path[i:j + 1][::-1] + path[j + 1:]
        new_cost = tour_cost(new_path, dist)
        delta = new_cost - current_cost

        if delta < 0 or random.random() < pow(2.718281828459045, -delta / temperature):
            path = new_path
            current_cost = new_cost
            best_cost = min(best_cost, current_cost)

        if iteration % record_every == 0:
            history.append((iteration, best_cost))

        temperature *= cooling

    history.append((max_iter, best_cost))
    return history


def _genetic_history(cities, pop_size=150, max_gen=100,
                     mutation_rate=0.02, scale=100):
    n = len(cities)
    dist = build_dist_matrix(cities)
    population = [list(range(n)) for _ in range(pop_size)]
    for individual in population:
        random.shuffle(individual)

    best_path = None
    best_cost = float("inf")
    history = []

    for gen in range(max_gen):
        costs = [tour_cost(individual, dist) for individual in population]
        best_idx = costs.index(min(costs))
        if costs[best_idx] < best_cost:
            best_cost = costs[best_idx]
            best_path = population[best_idx][:]

        history.append((gen * scale, best_cost))

        new_population = [best_path[:]]
        while len(new_population) < pop_size:
            p1 = tournament_select(population, costs)
            p2 = tournament_select(population, costs)
            child = ox_crossover(p1, p2)
            child = mutate_swap(child, mutation_rate)
            new_population.append(child)
        population = new_population

    return history


def plot_tsp_comparison(sizes=None, seed=42):
    if sizes is None:
        sizes = [50, 75, 100]

    algorithms = ['NN', 'HC 2-opt', 'SA', 'GA']
    colors = {
        'NN': '#1f77b4',
        'HC 2-opt': '#ff7f0e',
        'SA': '#2ca02c',
        'GA': '#d62728',
    }
    times = {a: [] for a in algorithms}
    costs = {a: [] for a in algorithms}

    print("Rulez benchmark-uri TSP...")
    for n in sizes:
        print(f"  n={n}...")
        cities = generate_random_cities(n, seed + n)

        random.seed(seed + n)
        _, cost, elapsed = nearest_neighbor(cities)
        times['NN'].append(elapsed)
        costs['NN'].append(cost)

        random.seed(seed + n)
        _, cost, elapsed = hill_climbing_2opt(cities)
        times['HC 2-opt'].append(elapsed)
        costs['HC 2-opt'].append(cost)

        random.seed(seed + n)
        _, cost, elapsed = tsp_simulated_annealing(cities)
        times['SA'].append(elapsed)
        costs['SA'].append(cost)

        random.seed(seed + n)
        _, cost, elapsed = tsp_genetic(cities)
        times['GA'].append(elapsed)
        costs['GA'].append(cost)

    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    (ax_cost, ax_scatter), (ax_time, ax_convergence) = axes

    for alg in algorithms:
        ax_cost.plot(sizes, costs[alg], '-o', label=alg,
                     color=colors[alg], linewidth=1.4, markersize=5)
    ax_cost.set_title('Costul solutiilor TSP')
    ax_cost.set_xlabel('Numar orase (N)')
    ax_cost.set_ylabel('Cost tur TSP')
    ax_cost.legend()
    ax_cost.grid(True, alpha=0.25)

    for alg in algorithms:
        ax_time.plot(sizes, times[alg], '-o', label=alg,
                     color=colors[alg], linewidth=1.4, markersize=5)
    ax_time.set_title('Timp de executie pe marimi mari ale problemei')
    ax_time.set_xlabel('Numar orase (N)')
    ax_time.set_ylabel('Timp executie (s)')
    ax_time.legend()
    ax_time.grid(True, alpha=0.25)

    for alg in algorithms:
        ax_scatter.scatter(times[alg], costs[alg], label=alg,
                           color=colors[alg], s=36)
        for x_val, y_val, n in zip(times[alg], costs[alg], sizes):
            ax_scatter.annotate(f'N={n}', (x_val, y_val),
                                textcoords='offset points',
                                xytext=(4, 3), fontsize=7)
    ax_scatter.set_title('Performanta: cost versus timp')
    ax_scatter.set_xlabel('Timp executie (s)')
    ax_scatter.set_ylabel('Cost tur')
    ax_scatter.legend()
    ax_scatter.grid(True, alpha=0.25)

    convergence_n = 75 if 75 in sizes else sizes[len(sizes) // 2]
    convergence_cities = generate_random_cities(convergence_n, seed + convergence_n)

    random.seed(seed + 1000)
    start_time = time()
    sa_history = _simulated_annealing_history(convergence_cities)
    _ = time() - start_time

    random.seed(seed + 2000)
    ga_history = _genetic_history(convergence_cities)

    ax_convergence.plot([x for x, _ in sa_history],
                        [y for _, y in sa_history],
                        label='SA - best cost',
                        color=colors['SA'], linewidth=1.6)
    ax_convergence.plot([x for x, _ in ga_history],
                        [y for _, y in ga_history],
                        label='GA - best cost (generatii scalate)',
                        color=colors['GA'], linewidth=1.6)
    ax_convergence.set_title(f'Convergenta exemplificativa pentru N={convergence_n}')
    ax_convergence.set_xlabel('Iteratii / generatii scalate')
    ax_convergence.set_ylabel('Cel mai bun cost')
    ax_convergence.legend()
    ax_convergence.grid(True, alpha=0.25)

    plt.tight_layout()
    plt.show()
