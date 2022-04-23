from math import exp

from numpy.random import rand

from src.neighbourhood.neighbourhood import neighbourhood
from src.solution.data_center import DataCenter, Solution
from src.solution.evaluation import evaluate_solution
from src.solution.solution import random_solution

from numpy.random import rand
from matplotlib import pyplot

def simulated_annealing(config: DataCenter, iterations: int, neighbourModes, init_temp, temp_mode, solution: Solution):
    evaluations = list()
    #initial point
    best = solution
    best_eval = evaluate_solution(best, config)
    curr, curr_eval = best, best_eval
    
    temp = init_temp
    for i in range (iterations - 1):
        if(temp_mode == 'linear'):
            temp -=  init_temp/iterations
        else:
            temp/= 1.05
        #new solution
        new_sol = neighbourhood(curr,neighbourModes,config)
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

        evaluations.append(curr_eval)

    return [best, evaluations]



