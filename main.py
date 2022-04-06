from random import randint
from dataCenter import DataCenter, Server, Solution
from solution import randomSolution
from evaluation import evaluate


# Pools example [1,0,0,2,1] 
# This means servers 2 and 3 are assigned to pool 0,
# servers 0 and 4 are assigned to pool 1
# and server 3 is assigned to pool 2
pools = []

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

unavailable = [(0,0)]
servers = [Server(3,10), Server(3,10), Server(2,5), Server(1,5), Server(1,1)]
rows = 2
slots = 5
pools = 2
config = DataCenter(rows,slots,unavailable,pools,servers)


solution = randomSolution(config)

print("Pools: ", solution.pools)
print("DataCenter: ", solution.dataCenter)

print(evaluate(solution, config))

