from dataCenter import DataCenter, Server, Solution
from random import randint

from utils import assignServer

MAX_ALLOC_TRIES = 100

def randomSolution(config: DataCenter):
    pools = []

    # Randomly assign pools to servers
    for i in range(len(config.servers)):
        pools.append(randint(0,config.pools-1))

    # Initialize data center with -1
    dataCenter =[[-1 for r in range(config.slots)] for s in range(config.rows)]

    solution = Solution(pools, dataCenter)

    # Set unavailable slots accordingly (-2)
    for coords in config.unavailable:
        r,s = coords
        dataCenter[r][s] = -2 # -2 means unavailable

    # Try to assign servers
    for index, server in enumerate(config.servers):
        assigned = False
        solution = assignServer(solution,config,server)
    
    return Solution(pools, dataCenter)
