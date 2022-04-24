from src.neighbourhood.neighbourhood import get_random_neighbour, get_neighbours
from src.solution.data_center import DataCenter
from src.solution.evaluation import evaluate_solution
from src.solution.solution import random_solution


def hill_climbing_steepest_ascent(config: DataCenter, iterations: int):
    solution = random_solution(config)
    for i in range(iterations):
        neighbours = get_neighbours(solution, config)
        newSolution = max(neighbours, key=lambda x: evaluate_solution(x, config))
        if evaluate_solution(newSolution, config) >= evaluate_solution(solution, config):
            print('>%d f(%s) => %.5f' % (i, newSolution, evaluate_solution(solution, config)))
            solution = newSolution
        else:
            break
    return solution


def hill_climbing_basic(config: DataCenter, iterations: int):
    solution = random_solution(config)
    for i in range(iterations):
        better_neighbour = solution
        for _ in range(iterations):
            newSolution = get_random_neighbour(solution, config)
            if evaluate_solution(newSolution, config) > evaluate_solution(better_neighbour, config):
                better_neighbour = newSolution
                break
        print('>%d f(%s) => %.5f' % (i, better_neighbour, evaluate_solution(better_neighbour, config)))
        solution = better_neighbour
    return solution


def hill_climbing_basic_random(config: DataCenter, iterations: int):
    solution = random_solution(config)
    for i in range(iterations):
        newSolution = get_random_neighbour(solution, config)
        print(newSolution)
        if evaluate_solution(newSolution, config) >= evaluate_solution(solution, config):
            print('>%d f(%s) => %.5f' % (i, newSolution, evaluate_solution(solution, config)))
            solution = newSolution
    return solution
