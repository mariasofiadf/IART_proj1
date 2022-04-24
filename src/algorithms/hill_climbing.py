from src.neighbourhood.neighbourhood import get_random_neighbour
from src.solution.data_center import DataCenter
from src.solution.evaluation import evaluate_solution
from src.solution.solution import random_solution


def hill_climbing(config: DataCenter, iterations: int, neighbour_modes):
    solution = random_solution(config)
    for i in range(iterations):
        newSolution = get_random_neighbour(solution, neighbour_modes, config)
        print(newSolution)
        if evaluate_solution(newSolution, config) >= evaluate_solution(solution, config):
            print('>%d f(%s) => %.5f' % (i, newSolution, evaluate_solution(solution, config)))
            solution = newSolution
    return solution
