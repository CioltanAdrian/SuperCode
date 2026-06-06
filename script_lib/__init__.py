from script_lib.tsp_bkt import tsp_bkt
from script_lib.tsp_nn import nearest_neighbor
from script_lib.tsp_hc import hill_climbing_2opt
from script_lib.tsp_sa import tsp_simulated_annealing
from script_lib.tsp_ga import tsp_genetic
from script_lib.tsp_plotting import plot_tsp_solutions, plot_tsp_comparison

LAB12_ALGORITHMS = {
    "BKT": "Backtracking exact pentru TSP",
    "NN": "Nearest Neighbor pentru TSP",
    "HC": "Hill Climbing 2-opt pentru TSP",
    "SA": "Simulated Annealing pentru TSP",
    "GA": "Algoritm Genetic pentru TSP",
    "NLP": "Clasificare text cu dataset-uri extinse in limba engleza",
}

__all__ = [
    "tsp_bkt",
    "nearest_neighbor",
    "hill_climbing_2opt",
    "tsp_simulated_annealing",
    "tsp_genetic",
    "plot_tsp_solutions",
    "plot_tsp_comparison",
    "LAB12_ALGORITHMS",
]
