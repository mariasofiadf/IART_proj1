from math import exp

from matplotlib import pyplot
from numpy.random import rand

from src.io.read import readDataCenter
from src.neighbourhood.neighbourhood import Neighbourhood, neighbourhood
from src.solution.data_center import DataCenter, Server
from src.solution.evaluation import evaluate_solution
from src.solution.solution import randomSolution


def simulatedAnnealing(config: DataCenter, iterations: int, neighbourModes, init_temp, temp_mode):
    # initial point
    best = randomSolution(config)
    best_eval = evaluate_solution(best, config)
    curr, curr_eval = best, best_eval

    temp = init_temp
    for i in range(iterations - 1):
        if (temp_mode == 'linear'):
            temp -= init_temp / iterations
        else:
            temp /= 1.05
        # new solution
        new_sol = neighbourhood(curr, neighbourModes, config)
        new_sol_eval = evaluate_solution(new_sol, config)
        if (new_sol_eval > best_eval):
            best = new_sol
            best_eval = new_sol_eval

        diff = new_sol_eval - curr_eval
        probabilty = exp((-diff / temp))

        if (diff > 0):
            print('>%d  = %.5f, prob: %.3f, temp: %.3f' % (i, best_eval, probabilty, temp))
        if (diff > 0 or rand() < probabilty):
            curr, curr_eval = new_sol, new_sol_eval

        evaluations.append(curr_eval)
        it_list.append(i)
    return [best, best_eval]


unavailable = [(0, 0)]

evaluations = list()
it_list = list()

servers = [Server(0, 3, 10), Server(1, 3, 10), Server(2, 2, 5), Server(3, 1, 5), Server(4, 1, 1)]
rows = 2
slots = 5
pools = 2
config = readDataCenter('../../data/problem.txt')

neighbourModes = [Neighbourhood.ADD_SV, Neighbourhood.RMV_SV, Neighbourhood.SWTCH_SV_POOL]

temp = 100
iter = 150

sol = simulatedAnnealing(config, iter, neighbourModes, temp, 'linear')
print(exp(1))
print(sol)

pyplot.plot(it_list, evaluations)
pyplot.ylabel('Evaluation')
pyplot.xlabel('Iteration')
pyplot.xlim(0, iter)
pyplot.ylim(0, sol[1] + 2)
pyplot.show()

# for i in range (len(it_list)):
# print('%d -> eval: %.2f' % (it_list[i], evaluations[i]))
