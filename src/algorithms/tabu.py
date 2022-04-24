from django.urls import conf
from src.neighbourhood.neighbourhood import get_random_neighbour
from src.solution.evaluation import evaluate_solution
from src.solution.solution import random_solution


def tabu_search(config, max_iter, modes, max_tenure):
    tabu_memory = {}
    solution = random_solution(config)
    best_neighbor = solution
    best_neighbor_f = evaluate_solution(solution, config)
    evaluations = list()
    for i in range(max_iter):
        for solution in tabu_memory:
            tabu_memory[solution] += 1
        neighbor = get_random_neighbour(solution, config)
        if neighbor in tabu_memory:
            continue
        neighbor_f = evaluate_solution(neighbor, config)
        if best_neighbor is None or neighbor_f > best_neighbor_f:
            best_neighbor = neighbor
            best_neighbor_f = neighbor_f
        tabu_memory[solution] = 0
        for solution, tenure in list(tabu_memory.items()):
            if tenure > max_tenure:
                del tabu_memory[solution]
        solution = best_neighbor
        evaluations.append(evaluate_solution(solution,config))
    return solution, evaluations
