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
        currCapacities = []
        currCapacities = [ 0 for j in range(nPools)] 

        # Iterate servers in row
        for server in serversInRow:
            # pools[server] is server's pool
            currCapacities[0] += servers[server].capacity
        # If the current garanteed capacity is lower than the previous minimum, update it
        if(min(currCapacities)<min(garanteedCapacities)):
            garanteedCapacities = currCapacities.copy()
    
    return min(garanteedCapacities)





def evaluate_solution(solution: Solution, data_center: DataCenter):
    capacities_per_pool = [0] * data_center.pools
    for pool in range(data_center.pools):
        pool_servers = [server for server, server_pool in enumerate(solution.pools) if server_pool == pool]
        total_pool_capacity = sum(data_center.servers[server].capacity for server in pool_servers)
        capacities_per_row = [0] * data_center.rows
        for row in range(data_center.rows):
            servers_in_row_and_pool = set(server for server in solution.dataCenter[row] if server in pool_servers)
            total_lost_capacity = sum(data_center.servers[server].capacity for server in servers_in_row_and_pool)
            capacities_per_row[row] = total_pool_capacity - total_lost_capacity
        capacities_per_pool[pool] = min(capacities_per_row)
    return min(capacities_per_pool)