from math import exp
from typing import ByteString
from numpy import tri

from numpy.random import rand

from src.neighbourhood.neighbourhood import get_random_neighbour
from src.solution.data_center import DataCenter
from src.solution.evaluation import evaluate_solution
from src.solution.solution import random_solution

from numpy.random import rand
from matplotlib import pyplot

TRIES = 100

def simulated_annealing(config: DataCenter, iterations: int, init_temp, schedule_function, curr_evals=None,
                        best_evals=None):
    if curr_evals is None:
        curr_evals = []
    if best_evals is None:
        best_evals = []

    # initial point
    best = random_solution(config)
    best_eval = evaluate_solution(best, config)
    curr, curr_eval = best, best_eval
    
    temp = init_temp
    for i in range(iterations - 1):
        temp = schedule_function(init_temp, iterations, i, temp)
        # new solution
        new_sol = get_random_neighbour(curr, config)
        tries = 0
        while(evaluate_solution(new_sol, config)==0 and tries < TRIES):
            new_sol = get_random_neighbour(curr, config)
            tries += 1

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
        curr_evals.append(curr_eval)
        best_evals.append(best_eval)
    return best, curr_evals, best_evals


def non_linear_schedule(init_temp, iterations,i, temp):
    return init_temp * (0.96**i) 

def linear_schedule(init_temp, iterations,i, temp):
    return temp - init_temp / iterations
