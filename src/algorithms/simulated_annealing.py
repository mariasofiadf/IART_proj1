from math import exp

from numpy.random import rand

from src.neighbourhood.neighbourhood import neighbourhood
from src.solution.data_center import DataCenter
from src.solution.evaluation import evaluate_solution
from src.solution.solution import random_solution


def simulated_annealing(config: DataCenter, iterations: int, neighbour_modes, init_temp, temp_mode, evaluations=None,
                        it_list=None):
    if evaluations is None:
        evaluations = []
    if it_list is None:
        it_list = []

    # initial point
    best = random_solution(config)
    best_eval = evaluate_solution(best, config)
    curr, curr_eval = best, best_eval

    temp = init_temp
    for i in range(iterations - 1):
        if temp_mode == 'linear':
            temp -= init_temp / iterations
        else:
            temp /= 1.05
        # new solution
        new_sol = neighbourhood(curr, neighbour_modes, config)
        new_sol_eval = evaluate_solution(new_sol, config)
        if new_sol_eval > best_eval:
            best = new_sol
            best_eval = new_sol_eval

        diff = new_sol_eval - curr_eval
        probabilty = exp((-diff / temp))

        if diff > 0:
            print('>%d  = %.5f, prob: %.3f, temp: %.3f' % (i, best_eval, probabilty, temp))
        if diff > 0 or rand() < probabilty:
            curr, curr_eval = new_sol, new_sol_eval

        evaluations.append(curr_eval)
        it_list.append(i)
    return [best, best_eval]
