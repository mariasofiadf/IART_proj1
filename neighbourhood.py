from pydoc import doc
import random
from dataCenter import Solution, DataCenter, Server
from enum import Enum
from typing import List
import numpy as np
from random import randint

from utils import assignServer

class Neighbourhood(Enum):
    RMV_SV = 0
    ADD_SV = 1
    MOV_SV_SLOT = 2
    SWTCH_SV_ROW = 3
    SWTCH_SV_POOL = 4

def moveServer(solution: Solution, server: Server):
    return solution

def neighbourhood(solution: Solution, modes: List[Neighbourhood], config: DataCenter):
    index = random.randint(0, len(modes)-1)
    mode = modes[index]

    servers = [x for x in set(np.array(solution.dataCenter).flatten()) if x >=0]
    nonAllocatedServers = [i for i,x in enumerate(config.servers) if i not in servers]

    if(mode == Neighbourhood.RMV_SV):
        toRmv = random.randint(0, len(servers)-1)
        for row in solution.dataCenter:
            for i, slot in enumerate(row):
                if(slot == servers[toRmv]):
                    row[i] = -1

    if(mode == Neighbourhood.ADD_SV):
        toAdd = random.choice(nonAllocatedServers)
        assignServer(solution, config, config.servers[toAdd])
    
    # if(mode == Neighbourhood.MOV_SV_SLOT):
    #     toMove = random.choice(servers)
    #     moveServer(solution,config.servers[toMove])

    
    # if(mode == Neighbourhood.SWTCH_SV_ROW):
    #     toSwitch = random.choice(servers)
    #     assignServer(solution, config, config.servers[toAdd])

    
    if(mode == Neighbourhood.SWTCH_SV_POOL):
        toSwitch = random.choice(servers)
        r = solution.pools[toSwitch]
        while (r==solution.pools[toSwitch]):
            r = randint(0, config.pools-1)
        solution.pools[toSwitch] = r

    return solution

unavailable = [(0,0)]
servers = [Server(0,3,10), Server(1,3,10), Server(2,2,5), Server(3,1,5), Server(4,1,1)]
rows = 2
slots = 3
pools = 2
config = DataCenter(rows,slots,unavailable,pools,servers)

arr = [Neighbourhood.SWTCH_SV_ROW]
sol = Solution([1,2,2,1,2],[[-1,-1,-1],[1,2,3]])

print("Initial Solution: ", sol)
new_sol = neighbourhood(sol, arr, config)

print("Neighbour Solution: ", new_sol)