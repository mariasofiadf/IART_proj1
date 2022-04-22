import sys
from dataCenter import DataCenter, Server, Solution
import numpy as np


def evaluate(solution: Solution, dataCenter: DataCenter):
    pools = solution.pools
    servers = dataCenter.servers

    nPools = len(set(pools))
    garanteedCapacities = [ sys.maxsize for i in range(nPools)] # [1,0]

    for i, row in enumerate(solution.dataCenter):
        serversInRow = [x for x in set(row) if x >= 0] # Gets servers in row. Filters to remove values -1 and -2 which are not servers!
        currCapacities = [ 0 for i in range(nPools)] 

        # Iterate servers in row
        for server in serversInRow:
            # pools[server] is server's pool
            currCapacities[pools[server]] += servers[server].capacity
        
        # If the current garanteed capacity is lower than the previous minimum, update it
        if(min(currCapacities)<min(garanteedCapacities)):
            garanteedCapacities = currCapacities.copy()

    return min(garanteedCapacities)




