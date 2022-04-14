from dataCenter import DataCenter, Solution, Server
from evaluation import evaluate_solution
from neighbourhood import Neighbourhood, neighbourhood
from solution import randomSolution
from read import readDataCenter
from math import exp
from numpy.random import rand

def simulatedAnnealing(config: DataCenter, iterations: int, neighbourModes, init_temp):
    #initial point
    best = randomSolution(config)
    best_eval = evaluate_solution(best, config)
    curr, curr_eval = best, best_eval
    temp = init_temp
    for i in range (iterations):
        temp -=  init_temp/iterations
        #new solution
        new_sol = neighbourhood(curr,neighbourModes,config)
        new_sol_eval = evaluate_solution(new_sol, config)

        diff = new_sol_eval - curr_eval
        probabilty = exp((-diff / temp))

        if(diff > 0 or rand() < probabilty):
            curr, curr_eval = new_sol, new_sol_eval
        print('>%d f(%s) = %.5f, prob: %.3f' % (i, curr, curr_eval, probabilty))
    return [curr, curr_eval]


unavailable = [(0,0)]
servers = [Server(0,3,10), Server(1,3,10), Server(2,2,5), Server(3,1,5), Server(4,1,1)]
rows = 2
slots = 5
pools = 2
config = readDataCenter('problem.txt')


neighbourModes = [Neighbourhood.ADD_SV,Neighbourhood.RMV_SV,Neighbourhood.SWTCH_SV_POOL]

temp = 100
iter = 4500


sol = simulatedAnnealing(config, iter, neighbourModes, temp)
print(exp(1))
print(sol)
    
