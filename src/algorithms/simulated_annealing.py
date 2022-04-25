from math import exp

from numpy.random import rand

from src.neighbourhood.neighbourhood import get_random_neighbour
from src.solution.data_center import DataCenter
from src.solution.evaluation import evaluate_solution
from src.solution.solution import random_solution

from numpy.random import rand
from matplotlib import pyplot

def simulated_annealing(config: DataCenter, iterations: int, init_temp, schedule_function, evaluations=None,
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
        temp = schedule_function(init_temp, iterations, temp)
        # new solution
        new_sol = get_random_neighbour(curr, config)
        new_sol_eval = evaluate_solution(new_sol, config)
        if(new_sol_eval > best_eval):
            best = new_sol
            best_eval = new_sol_eval
            

        diff =  new_sol_eval - curr_eval
        probabilty = exp((-diff / temp))

        #if(diff > 0):
            #print('>%d  = %.5f, prob: %.3f, temp: %.3f' % (i, best_eval, probabilty, temp))
        if(diff > 0 or rand() < probabilty):
            curr, curr_eval = new_sol, new_sol_eval  

        evaluations.append(best_eval)
        it_list.append(i)
    return best, evaluations


def non_linear_schedule(init_temp, iterations, temp):
    return temp / 1.05


def linear_schedule(init_temp, iterations, temp):
    return temp - init_temp / iterations
