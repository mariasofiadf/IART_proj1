from math import exp

from matplotlib import pyplot

from algorithms.genetic import genetic
from src.algorithms.simulated_annealing import simulated_annealing
from src.io.read import read_data_center
from src.neighbourhood.neighbourhood import Neighbourhood
from src.solution.data_center import DataCenter, Server
from src.solution.evaluation import evaluate_solution

# Pools example [1,0,0,2,1]
# This means servers 2 and 3 are assigned to pool 0,
# servers 0 and 4 are assigned to pool 1
# and server 3 is assigned to pool 2
# pools = []

# dataCenter example [[1,1,1,-2,-1,-1,3,5],
#                     [-1,2,2,4,4,4,-2,0 ]] 
# -1 means slot is available
# -2 means slot is unavailable
# other numbers mean server N is allocated there
dataCenter = [[]]

# config is an object of the class DataCenter defined in dataCenterCOnfig.py
# @dataclass
# class DataCenter:
#     rows: int # number of rows
#     slots: int # number of slots per row
#     unavailable: array[int] # coordinates of unavailable slots
#     pools: int # number of pools
#     servers: array[int] #array with server sizes. len(servers) = number of servers

unavailable = [(0, 0), (0, 4)]
servers = [Server(0, 3, 10), Server(1, 3, 10), Server(2, 2, 5), Server(3, 1, 5), Server(4, 1, 1)]
rows = 2
slots = 5
pools = 2
config = DataCenter(rows, slots, unavailable, pools, servers)

neighbourModes = [Neighbourhood.ADD_SV, Neighbourhood.RMV_SV, Neighbourhood.SWTCH_SV_POOL, Neighbourhood.MOV_SV_SLOT,
                  Neighbourhood.SWTCH_SV_ROW]

solution = genetic(config, neighbourModes, 4, 1)
# solution = hillClimbing(config,500,neighbourModes)
print("Pools: ", solution.pools)
print("DataCenter: ", solution.dataCenter)

print("Evaluation: ", evaluate_solution(solution, config))

unavailable = [(0, 0)]

evaluations = list()
it_list = list()

servers = [Server(0, 3, 10), Server(1, 3, 10), Server(2, 2, 5), Server(3, 1, 5), Server(4, 1, 1)]
rows = 2
slots = 5
pools = 2
config = read_data_center('../../data/problem.txt')

neighbourModes = [Neighbourhood.ADD_SV, Neighbourhood.RMV_SV, Neighbourhood.SWTCH_SV_POOL]

temp = 100
no_iterations = 150

sol = simulated_annealing(config, no_iterations, neighbourModes, temp, 'linear')
print(exp(1))
print(sol)

pyplot.plot(it_list, evaluations)
pyplot.ylabel('Evaluation')
pyplot.xlabel('Iteration')
pyplot.xlim(0, no_iterations)
pyplot.ylim(0, sol[1] + 2)
pyplot.show()

# for i in range (len(it_list)):
# print('%d -> eval: %.2f' % (it_list[i], evaluations[i]))
