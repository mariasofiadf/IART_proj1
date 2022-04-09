import random
from dataCenter import Solution, DataCenter, Server
from enum import Enum
from typing import List
import numpy as np

class Neighbourhood(Enum):
    RMV_SV = 0
    ADD_SV = 1
    MOV_SV_SLOT = 2
    SWTCH_SV_ROW = 3
    SWTCH_SV_POOL = 4



def neighbourhood(solution: Solution, modes: List[Neighbourhood], config: DataCenter):
    index = random.randint(0, len(modes)-1)
    mode = modes[index]

    servers = [x for x in set(np.array(solution.dataCenter).flatten()) if x >=0]
    nonAllocatedServers = [i for i,x in enumerate(config.servers) if i not in servers]

    print(servers)
    print(nonAllocatedServers)
    if(mode == Neighbourhood.RMV_SV):
        toRmv = random.randint(0, len(servers)-1)
        for row in solution.dataCenter:
            for i, slot in enumerate(row):
                if(slot == servers[toRmv]):
                    row[i] = -1

    if(mode == Neighbourhood.ADD_SV):
        toAdd = random.randint(0, len(nonAllocatedServers)-1)
        tries = 0
        assigned = False
        while not assigned and tries < MAX_ALLOC_TRIES:
            tries += 1
            # Get random row and slot
            r = random.randint(0, config.rows-1)
            s = random.randint(0, config.slots-1)
            valid = True

            # Check if server fits at slot s in row r
            for i in range(server.slots):
                if(s+i >= config.slots):
                    valid = False
                    break
                if solution.dataCenter[r][s+i] != -1: # -1 means available
                    valid = False

            # If server doesn't fit it won't be valid
            if not valid:
                continue
            
            # If it's valid, assign it
            for i in range(server.slots):
                dataCenter[r][s+i] = index

            assigned = True
    
    
    # if(mode == Neighbourhood.MOV_SV_SLOT):

    
    # if(mode == Neighbourhood.SWTCH_SV_ROW):

    
    # if(mode == Neighbourhood.SWTCH_SV_POOL):

    return solution

unavailable = [(0,0)]
servers = [Server(3,10), Server(3,10), Server(2,5), Server(1,5), Server(1,1)]
rows = 2
slots = 5
pools = 2
config = DataCenter(rows,slots,unavailable,pools,servers)

arr = [Neighbourhood.ADD_SV]
sol = Solution([1,2],[[-1,-1,-1],[1,2,3]])

print("Initial Solution: ", sol)
new_sol = neighbourhood(sol, arr, config)


print("Neighbour Solution: ", new_sol)