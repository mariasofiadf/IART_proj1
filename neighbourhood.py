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
    solutionCopy = solution.deepcopy()
    index = random.randint(0, len(modes) - 1)
    mode = modes[index]

    servers = [x for x in set(np.array(solutionCopy.dataCenter).flatten()) if x >= 0]
    nonAllocatedServers = [i for i, x in enumerate(config.servers) if i not in servers]

    if mode == Neighbourhood.RMV_SV and len(servers) > 0:
        toRmv = random.randint(0, len(servers) - 1)
        for row in solutionCopy.dataCenter:
            for i, slot in enumerate(row):
                if slot == servers[toRmv]:
                    row[i] = -1

    if mode == Neighbourhood.ADD_SV:
        toAdd = random.choice(nonAllocatedServers)
        assignServer(solutionCopy, config, config.servers[toAdd])

    # if(mode == Neighbourhood.MOV_SV_SLOT):
    #     toMove = random.choice(servers)
    #     moveServer(solution,config.servers[toMove])

    # if(mode == Neighbourhood.SWTCH_SV_ROW):
    #     toSwitch = random.choice(servers)
    #     assignServer(solution, config, config.servers[toSwitch])

    if mode == Neighbourhood.SWTCH_SV_POOL and len(servers) > 0:
        toSwitch = random.choice(servers)
        r = solutionCopy.pools[toSwitch]
        while r == solutionCopy.pools[toSwitch]:
            r = randint(0, config.pools - 1)
        solutionCopy.pools[toSwitch] = r

    return solutionCopy
